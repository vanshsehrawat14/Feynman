/**
 * POST /api/generate
 * { topic: string }
 * → { videoUrl, explanation, topic }
 *
 * Strategy:
 *   1. Normalise topic → check known-topic map (always fast + reliable).
 *   2. For known topics: render pre-built scene, call Groq in parallel for
 *      a plain-English explanation to show alongside the video.
 *   3. For unknown topics: call Groq to generate a complete Manim script,
 *      validate it (no LaTeX calls), render it, fall back to closest known
 *      topic on any failure.
 */

import { Router }         from "express";
import { exec }           from "child_process";
import { writeFile, readFile, access } from "fs/promises";
import path               from "path";
import { fileURLToPath }  from "url";
import { promisify }      from "util";
import Groq               from "groq-sdk";
import { narrateVideo }   from "../narrate.js";

const execAsync = promisify(exec);
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Absolute path to newton/manim/
const MANIM_DIR = path.resolve(__dirname, "../../../manim");
const NARR_DIR  = path.join(MANIM_DIR, "output", "narrated");

export const generateRoute = Router();

// ── Groq client ────────────────────────────────────────────────────────────
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

// ── Known-topic registry ───────────────────────────────────────────────────
const KNOWN = new Map([
  // ── Calculus ──────────────────────────────────────────────────────────────
  ["derivative",            { file: "derivative.py",           cls: "DerivativeScene"       }],
  ["derivatives",           { file: "derivative.py",           cls: "DerivativeScene"       }],
  ["tangent line",          { file: "derivative.py",           cls: "DerivativeScene"       }],
  ["integral",              { file: "integral.py",             cls: "IntegralScene"         }],
  ["integrals",             { file: "integral.py",             cls: "IntegralScene"         }],
  ["riemann sum",           { file: "integral.py",             cls: "IntegralScene"         }],
  ["area under curve",      { file: "integral.py",             cls: "IntegralScene"         }],
  ["limit",                 { file: "limit.py",                cls: "LimitScene"            }],
  ["limits",                { file: "limit.py",                cls: "LimitScene"            }],
  ["chain rule",            { file: "chain_rule.py",           cls: "ChainRuleScene"        }],
  ["chain_rule",            { file: "chain_rule.py",           cls: "ChainRuleScene"        }],

  // ── Foundations ───────────────────────────────────────────────────────────
  ["vectors",               { file: "la_01_vectors.py",        cls: "VectorsScene"          }],
  ["vector",                { file: "la_01_vectors.py",        cls: "VectorsScene"          }],
  ["vector addition",       { file: "la_02_vector_add.py",     cls: "VectorAdditionScene"   }],
  ["add vectors",           { file: "la_02_vector_add.py",     cls: "VectorAdditionScene"   }],
  ["scalar multiplication", { file: "la_03_scalar_mult.py",    cls: "ScalarMultScene"       }],
  ["scalar mult",           { file: "la_03_scalar_mult.py",    cls: "ScalarMultScene"       }],
  ["dot product",           { file: "la_04_dot_product.py",    cls: "DotProductScene"       }],
  ["cross product",         { file: "la_05_cross_product.py",  cls: "CrossProductScene"     }],

  // ── Transformations ───────────────────────────────────────────────────────
  ["linear transformation", { file: "la_06_linear_transform.py", cls: "LinearTransformScene" }],
  ["linear transformations",{ file: "la_06_linear_transform.py", cls: "LinearTransformScene" }],
  ["matrix multiplication", { file: "la_07_matrix_mult.py",    cls: "MatrixMultScene"       }],
  ["matrix product",        { file: "la_07_matrix_mult.py",    cls: "MatrixMultScene"       }],
  ["rotation matrix",       { file: "la_08_rotation.py",       cls: "RotationScene"         }],
  ["rotation matrices",     { file: "la_08_rotation.py",       cls: "RotationScene"         }],
  ["rotation",              { file: "la_08_rotation.py",       cls: "RotationScene"         }],
  ["shear",                 { file: "la_09_shear.py",          cls: "ShearScene"            }],
  ["shear transformation",  { file: "la_09_shear.py",          cls: "ShearScene"            }],
  ["shear transformations", { file: "la_09_shear.py",          cls: "ShearScene"            }],
  ["projection",            { file: "la_10_projection.py",     cls: "ProjectionScene"       }],
  ["vector projection",     { file: "la_10_projection.py",     cls: "ProjectionScene"       }],

  // ── Core Concepts ─────────────────────────────────────────────────────────
  ["determinant",           { file: "la_11_determinant.py",    cls: "DeterminantScene"      }],
  ["determinants",          { file: "la_11_determinant.py",    cls: "DeterminantScene"      }],
  ["span",                  { file: "la_12_span.py",           cls: "SpanScene"             }],
  ["linear independence",   { file: "la_13_lin_indep.py",      cls: "LinearIndepScene"      }],
  ["linear dependent",      { file: "la_13_lin_indep.py",      cls: "LinearIndepScene"      }],
  ["basis",                 { file: "la_14_basis.py",          cls: "BasisScene"            }],
  ["basis vectors",         { file: "la_14_basis.py",          cls: "BasisScene"            }],
  ["change of basis",       { file: "la_15_change_of_basis.py",cls: "ChangeBasisScene"      }],

  // ── Advanced ──────────────────────────────────────────────────────────────
  ["eigenvalues",           { file: "la_16_eigen.py",          cls: "EigenScene"            }],
  ["eigenvectors",          { file: "la_16_eigen.py",          cls: "EigenScene"            }],
  ["eigenvalues and eigenvectors", { file: "la_16_eigen.py",   cls: "EigenScene"            }],
  ["svd",                   { file: "la_17_svd.py",            cls: "SVDScene"              }],
  ["singular value decomposition", { file: "la_17_svd.py",     cls: "SVDScene"              }],
  ["null space",            { file: "la_18_null_space.py",     cls: "NullSpaceScene"        }],
  ["nullspace",             { file: "la_18_null_space.py",     cls: "NullSpaceScene"        }],
  ["column space",          { file: "la_19_column_space.py",   cls: "ColumnSpaceScene"      }],
  ["col space",             { file: "la_19_column_space.py",   cls: "ColumnSpaceScene"      }],
  ["row reduction",         { file: "la_20_row_reduction.py",  cls: "RowReductionScene"     }],
  ["gaussian elimination",  { file: "la_20_row_reduction.py",  cls: "RowReductionScene"     }],

  // ── Intuition ─────────────────────────────────────────────────────────────
  ["what matrices do",             { file: "la_21_matrices_geom.py",  cls: "MatricesGeomScene"     }],
  ["matrices geometrically",       { file: "la_21_matrices_geom.py",  cls: "MatricesGeomScene"     }],
  ["what matrices do geometrically",{ file: "la_21_matrices_geom.py", cls: "MatricesGeomScene"     }],
  ["det zero",                     { file: "la_22_det_zero.py",       cls: "DetZeroScene"          }],
  ["why det zero",                 { file: "la_22_det_zero.py",       cls: "DetZeroScene"          }],
  ["zero determinant",             { file: "la_22_det_zero.py",       cls: "DetZeroScene"          }],
  ["why determinant zero means no inverse", { file: "la_22_det_zero.py", cls: "DetZeroScene"       }],
  ["why eigenvectors",             { file: "la_23_eigen_why.py",      cls: "EigenWhyScene"         }],
  ["eigenvectors matter",          { file: "la_23_eigen_why.py",      cls: "EigenWhyScene"         }],
  ["why eigenvectors matter",      { file: "la_23_eigen_why.py",      cls: "EigenWhyScene"         }],

  // ── Machine Learning ─────────────────────────────────────────────────────
  ["neural networks",       { file: "ml_01_neural_networks.py", cls: "NeuralNetworksScene"  }],
  ["neural network",        { file: "ml_01_neural_networks.py", cls: "NeuralNetworksScene"  }],
  ["gradient descent",      { file: "ml_02_gradient_descent.py", cls: "GradientDescentScene" }],
  ["backpropagation",       { file: "ml_03_backpropagation.py", cls: "BackpropagationScene" }],
  ["backprop",              { file: "ml_03_backpropagation.py", cls: "BackpropagationScene" }],
  ["loss function",         { file: "ml_04_loss_function.py",   cls: "LossFunctionScene"   }],
  ["loss functions",        { file: "ml_04_loss_function.py",   cls: "LossFunctionScene"   }],
  ["overfitting",           { file: "ml_05_overfitting.py",     cls: "OverfittingScene"    }],
  ["overfitting and underfitting", { file: "ml_05_overfitting.py", cls: "OverfittingScene" }],
  ["train test split",      { file: "ml_06_train_test.py",      cls: "TrainTestScene"      }],
  ["activation functions",  { file: "ml_07_activation.py",      cls: "ActivationScene"     }],
  ["activation function",   { file: "ml_07_activation.py",      cls: "ActivationScene"     }],
  ["learning rate",         { file: "ml_08_learning_rate.py",   cls: "LearningRateScene"   }],
  ["convolutional neural network", { file: "ml_09_cnn.py",      cls: "ConvolutionalScene"  }],
  ["cnn",                   { file: "ml_09_cnn.py",             cls: "ConvolutionalScene"  }],
  ["cnns",                  { file: "ml_09_cnn.py",             cls: "ConvolutionalScene"  }],
  ["attention",             { file: "ml_10_attention.py",       cls: "AttentionScene"      }],
  ["attention mechanism",   { file: "ml_10_attention.py",       cls: "AttentionScene"      }],
  ["embeddings",            { file: "ml_11_embeddings.py",      cls: "EmbeddingsScene"     }],
  ["pca",                   { file: "la_17_svd.py",             cls: "SVDScene"            }],

  // ── Algorithms ───────────────────────────────────────────────────────────
  ["bubble sort",           { file: "algo_01_bubble_sort.py",   cls: "BubbleSortScene"     }],
  ["quicksort",             { file: "algo_02_quicksort.py",     cls: "QuicksortScene"      }],
  ["quick sort",            { file: "algo_02_quicksort.py",     cls: "QuicksortScene"      }],
  ["merge sort",            { file: "algo_03_merge_sort.py",    cls: "MergeSortScene"      }],
  ["binary search",         { file: "algo_04_binary_search.py", cls: "BinarySearchScene"   }],
  ["dfs",                   { file: "algo_05_dfs.py",           cls: "DFSScene"            }],
  ["depth first search",    { file: "algo_05_dfs.py",           cls: "DFSScene"            }],
  ["bfs",                   { file: "algo_06_bfs.py",           cls: "BFSScene"            }],
  ["breadth first search",  { file: "algo_06_bfs.py",           cls: "BFSScene"            }],
  ["big o",                 { file: "algo_07_big_o.py",         cls: "BigOScene"           }],
  ["big o notation",        { file: "algo_07_big_o.py",         cls: "BigOScene"           }],
  ["recursion",             { file: "algo_08_recursion.py",     cls: "RecursionScene"      }],
  ["dynamic programming",   { file: "algo_09_dp.py",            cls: "DynamicProgrammingScene" }],
  ["hash tables",           { file: "algo_10_hash.py",          cls: "HashTableScene"      }],
  ["hash table",            { file: "algo_10_hash.py",          cls: "HashTableScene"      }],
  ["dijkstra",              { file: "algo_11_dijkstra.py",      cls: "DijkstraScene"       }],
  ["minimum spanning tree", { file: "algo_12_mst.py",           cls: "MSTScene"            }],
  ["mst",                   { file: "algo_12_mst.py",           cls: "MSTScene"            }],

  // ── Electrodynamics ───────────────────────────────────────────────────────
  ["electric fields",       { file: "phys_01_electric_field.py", cls: "ElectricFieldScene" }],
  ["electric field",        { file: "phys_01_electric_field.py", cls: "ElectricFieldScene" }],
  ["magnetic fields",       { file: "phys_02_magnetic_field.py", cls: "MagneticFieldScene" }],
  ["magnetic field",        { file: "phys_02_magnetic_field.py", cls: "MagneticFieldScene" }],
  ["electromagnetic induction", { file: "phys_03_induction.py", cls: "InductionScene"    }],
  ["maxwell equations",     { file: "phys_04_maxwell.py",       cls: "MaxwellScene"       }],
  ["maxwell's equations",   { file: "phys_04_maxwell.py",       cls: "MaxwellScene"       }],
  ["wave propagation",      { file: "phys_05_wave_propagation.py", cls: "WavePropagationScene" }],

  // ── Macroeconomics ────────────────────────────────────────────────────────
  ["supply and demand",     { file: "econ_01_supply_demand.py", cls: "SupplyDemandScene"  }],
  ["supply demand",         { file: "econ_01_supply_demand.py", cls: "SupplyDemandScene"  }],
  ["gdp",                   { file: "econ_02_gdp.py",           cls: "GDPScene"           }],
  ["gdp and growth",        { file: "econ_02_gdp.py",           cls: "GDPScene"           }],
  ["inflation",             { file: "econ_03_inflation.py",     cls: "InflationScene"     }],
  ["interest rates",        { file: "econ_04_interest_rates.py", cls: "InterestRatesScene" }],
  ["game theory",           { file: "econ_05_game_theory.py",   cls: "GameTheoryScene"    }],
]);

// ── Manim system prompt (full derivative.py included as working example) ───
async function buildSystemPrompt() {
  const example = await readFile(
    path.join(MANIM_DIR, "scenes/derivative.py"), "utf8"
  );
  return `\
You are an expert Manim animation programmer generating 3Blue1Brown-style educational videos.

HARD RULES — violating any one will crash the renderer:
1. NEVER use Tex(), MathTex(), or SingleStringMathTex(). LaTeX is NOT installed.
   Only use Text() for all text objects.
2. NEVER pass numbers_to_include to Axes — it uses MathTex internally.
   Instead, add tick labels manually using Text() as shown in the example.
3. NEVER create a Line, DashedLine, or Arrow where start == end (zero length crashes Cairo).
   Always guard: if abs(y_value) < 0.02: return VMobject()
4. For animated numbers use:
   DecimalNumber(value, mob_class=Text, num_decimal_places=2, include_sign=True, font_size=N, color=COLOR)
5. The class name MUST be exactly: GeneratedScene
6. Always set: self.camera.background_color = "#0F0E17"
7. Use numpy (imported as np by manim) for math functions: np.sin, np.cos, np.exp, etc.
8. Return ONLY valid Python code. No markdown fences. No prose. No comments outside the code.

COLOR PALETTE:
  Background : "#0F0E17"
  Curves     : "#58C4DD"   (3B1B blue)
  Tangent    : "#FFFF00"   (yellow)
  Accent     : "#FC6255"   (red)
  Axes       : "#888888"

MANDATORY TIMING RULES — the rendered video MUST be over 180 seconds total:
- Every self.play() call MUST have run_time=2 minimum
- Every Transform/ReplacementTransform MUST have run_time=3
- self.wait(1) between every animation
- self.wait(2) after every key insight
- self.wait(4) at the very end
- Use at least 6 separate self.play() calls in the geometry section
- Use at least 5 separate self.play() calls in the worked example section
- Total animation time must exceed 180 seconds

REQUIRED 6-SECTION STRUCTURE — the scene MUST cover ALL 6 sections about the SPECIFIC TOPIC requested:
Section 1 — Hook (40s): Opening question about the topic, one visual teaser
Section 2 — Geometric Intuition (90s): Build concept visually with NO algebra, at least 6 animations
Section 3 — Formal Notation (60s): Show the math notation, introduce each symbol separately
Section 4 — Worked Example (90s): Specific numbers, step by step, at least 5 animation steps
Section 5 — Deeper Insight (60s): Real-world application and why it matters
Section 6 — Summary (30s): Replay the single most important visual, self.wait(4) at the end

COMPLETE WORKING EXAMPLE (follow this pattern exactly):
${example}

Now write a GeneratedScene specifically about the topic the user requests. The animation must be entirely focused on that topic — not a generic math scene. Include real definitions, formulas, and examples relevant to that specific topic.`;
}

// ── Code validation ────────────────────────────────────────────────────────
const LATEX_PATTERNS = [/\bTex\s*\(/, /\bMathTex\s*\(/, /\bSingleStringMathTex\s*\(/];

function validateCode(code) {
  if (!code.includes("GeneratedScene")) return "missing GeneratedScene class";
  if (!code.includes("from manim import")) return "missing manim import";
  for (const pat of LATEX_PATTERNS) {
    if (pat.test(code)) return `forbidden LaTeX call detected`;
  }
  return null; // valid
}

// ── Auto-fix common code errors ───────────────────────────────────────────
function autoFixCode(code) {
  // Replace MathTex/Tex with Text
  let fixed = code
    .replace(/\bMathTex\s*\(/g, "Text(")
    .replace(/\bTex\s*\(/g, "Text(")
    .replace(/\bSingleStringMathTex\s*\(/g, "Text(");

  // Remove any backslash LaTeX commands (e.g. \frac, \int) that Text() can't handle
  // Replace common ones with unicode or plain text
  fixed = fixed
    .replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g, "($1)/($2)")
    .replace(/\\sqrt\{([^}]*)\}/g, "sqrt($1)")
    .replace(/\\infty/g, "inf")
    .replace(/\\sum/g, "sum")
    .replace(/\\int/g, "integral")
    .replace(/\\partial/g, "d")
    .replace(/\\cdot/g, "x")
    .replace(/\\times/g, "x")
    .replace(/\\leq/g, "<=")
    .replace(/\\geq/g, ">=")
    .replace(/\\neq/g, "!=")
    .replace(/\\approx/g, "~=")
    .replace(/\\pi/g, "pi")
    .replace(/\\alpha/g, "alpha")
    .replace(/\\beta/g, "beta")
    .replace(/\\lambda/g, "lambda")
    .replace(/\\sigma/g, "sigma");

  return fixed;
}

// ── Render helper ──────────────────────────────────────────────────────────
async function renderScene(sceneFile, className) {
  const cmd = [
    "python -m manim render",
    `"${path.join(MANIM_DIR, "scenes", sceneFile)}"`,
    className,
    "--format mp4 -qm --fps 30",
    `--media_dir "${path.join(MANIM_DIR, "output")}"`,
  ].join(" ");

  await execAsync(cmd, { timeout: 150_000 });

  // Manim output: output/videos/<scene_name_no_ext>/<quality>/<ClassName>.mp4
  const base = sceneFile.replace(/\.py$/, "");
  return `/${base}/720p30/${className}.mp4`;  // relative under /videos/
}

// ── Check for existing rendered video (720p30 first, then 480p15) ──────────
async function getExistingVideoPath(file, cls) {
  const base = file.replace(/\.py$/, "");
  for (const quality of ["720p30", "480p15"]) {
    const abs = path.join(MANIM_DIR, "output", "videos", base, quality, `${cls}.mp4`);
    try { await access(abs); return `/${base}/${quality}/${cls}.mp4`; } catch { /* try next */ }
  }
  return null; // not on disk — needs render
}

// ── Absolute video path (for narration) ────────────────────────────────────
function absVideoPath(relativePath) {
  // relativePath looks like /derivative/480p15/DerivativeScene.mp4
  return path.join(MANIM_DIR, "output", "videos", ...relativePath.split("/").filter(Boolean));
}

// ── Explanation via Groq ───────────────────────────────────────────────────
async function getExplanation(topic, angle = "") {
  const angleCtx = angle.trim()
    ? ` Emphasize this angle: "${angle}".`
    : "";
  const resp = await groq.chat.completions.create({
    model: "llama-3.3-70b-versatile",
    messages: [
      {
        role: "system",
        content:
          "You are a calculus tutor. Give a clear, engaging 2–3 sentence explanation of the topic for a student seeing it for the first time. Be concise and intuitive." +
          (angleCtx ? " Tailor the explanation to the requested focus." : ""),
      },
      { role: "user", content: `Explain: ${topic}${angleCtx}` },
    ],
    temperature: 0.5,
    max_tokens: 200,
  });
  return resp.choices[0].message.content.trim();
}

// ── Groq code generation ───────────────────────────────────────────────────
async function generateCode(topic, systemPrompt) {
  const resp = await groq.chat.completions.create({
    model: "llama-3.3-70b-versatile",
    messages: [
      { role: "system", content: systemPrompt },
      {
        role: "user",
        content: `Create a complete Manim animation specifically about: "${topic}".

The scene MUST be entirely about "${topic}" — not about a generic math concept.
Include the correct mathematical definitions, formulas, and visual intuitions specific to "${topic}".
Make it educational, visually rich, and mathematically accurate.
Follow the 6-section structure and timing rules exactly.
Class name must be GeneratedScene.
Total video duration must exceed 180 seconds — add enough self.wait() calls to ensure this.`,
      },
    ],
    temperature: 0.2,
    max_tokens: 4096,
  });

  let code = resp.choices[0].message.content;
  // Strip markdown fences if the model adds them
  code = code.replace(/^```python\s*/m, "").replace(/^```\s*/m, "").replace(/```\s*$/m, "").trim();
  return code;
}

// ── Route handler ──────────────────────────────────────────────────────────
generateRoute.post("/", async (req, res) => {
  const raw   = (req.body.topic ?? "").trim();
  const angle = (req.body.angle ?? "").trim();
  const topic = raw.toLowerCase();

  if (!topic) return res.status(400).json({ error: "topic is required" });

  const displayTitle = angle
    ? `${raw} — ${angle}`
    : raw;

  // ── 1. Known-topic fast path ─────────────────────────────────────────────
  if (KNOWN.has(topic)) {
    const { file, cls } = KNOWN.get(topic);
    try {
      // Check disk cache and fetch explanation in parallel — zero re-render if cached
      const [existingPath, explanation] = await Promise.all([
        getExistingVideoPath(file, cls),
        getExplanation(raw, angle),
      ]);

      // Use cached video; only render if somehow missing from disk
      const videoPath = existingPath ?? await renderScene(file, cls);
      const silentUrl = `/videos${videoPath}`;

      // Return narrated URL if already cached; otherwise start narration in background
      let narratedUrl = null;
      try {
        await access(path.join(NARR_DIR, `${cls}_narrated.mp4`));
        narratedUrl = `/narrated/${cls}_narrated.mp4`;
      } catch {
        narrateVideo(absVideoPath(videoPath), raw, groq)
          .then(p => console.log("[narrated]", path.basename(p)))
          .catch(e => console.warn("[narration skipped]", e.message));
      }

      return res.json({
        videoUrl:       silentUrl,
        narratedVideoUrl: narratedUrl,
        explanation,
        topic:          raw,
        displayTitle,
        angle:          angle || null,
      });
    } catch (err) {
      console.error("[known-topic render]", err.message);
      return res.status(500).json({ error: "Render failed", detail: err.message });
    }
  }

  // ── 2. Unknown topic: Groq generates Manim code ──────────────────────────
  let systemPrompt;
  try {
    systemPrompt = await buildSystemPrompt();
  } catch (err) {
    return res.status(500).json({ error: "Could not load system prompt", detail: err.message });
  }

  let code, explanation;
  try {
    [code, explanation] = await Promise.all([
      generateCode(raw, systemPrompt),
      getExplanation(raw, angle),
    ]);
  } catch (err) {
    return res.status(500).json({ error: "Groq API error", detail: err.message });
  }

  // Validate — attempt auto-fix if LaTeX calls are found
  let invalid = validateCode(code);
  if (invalid && invalid.includes("LaTeX")) {
    console.warn("[groq validation] LaTeX detected, attempting auto-fix...");
    code = autoFixCode(code);
    invalid = validateCode(code);
  }
  if (invalid) {
    console.warn("[groq validation fail]", invalid);
    return res.status(422).json({
      error: `Could not generate a video for "${raw}"`,
      detail: invalid,
      hint: `Try one of these pre-built topics: derivatives, integrals, eigenvalues, gradient descent, neural networks, limits, chain rule, determinants, linear transformations`,
    });
  }

  // Write generated scene to disk
  const slug       = topic.replace(/[^a-z0-9]/g, "_").slice(0, 40);
  const genFile    = `generated_${slug}.py`;
  const genPath    = path.join(MANIM_DIR, "scenes", genFile);
  await writeFile(genPath, code, "utf8");

  // Render
  try {
    const videoPath = await renderScene(genFile, "GeneratedScene");
    const silentUrl = `/videos${videoPath}`;

    // Start narration in background — don't block the response
    narrateVideo(absVideoPath(videoPath), raw, groq)
      .then(p => console.log("[narrated]", path.basename(p)))
      .catch(e => console.warn("[narration skipped]", e.message));

    return res.json({
      videoUrl:         silentUrl,
      narratedVideoUrl: null,
      explanation,
      topic:            raw,
      displayTitle,
      angle:            angle || null,
    });
  } catch (err) {
    console.error("[groq render fail]", err.message);
    return res.status(500).json({
      error: `Failed to generate video for "${raw}"`,
      detail: err.message,
      hint: `The topic "${raw}" could not be animated. Try a similar pre-built topic: derivatives, integrals, limits, chain rule, eigenvalues, gradient descent, neural networks`,
    });
  }
});
