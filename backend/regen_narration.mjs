/**
 * regen_narration.mjs — Standalone narration regenerator
 * Run from backend/ directory: node regen_narration.mjs [scene1 scene2 ...]
 * Example: node regen_narration.mjs eigen derivative gradient_descent
 */

import "dotenv/config";
import path    from "path";
import { fileURLToPath } from "url";
import { access, unlink } from "fs/promises";
import Groq    from "groq-sdk";
import { narrateVideo } from "./src/narrate.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MANIM_DIR = path.resolve(__dirname, "../manim");
const NARR_DIR  = path.join(MANIM_DIR, "output", "narrated");

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

// Map: short name → { videoRelPath, topic }
const SCENES = {
  eigen: {
    video: "la_16_eigen/480p15/EigenScene.mp4",
    topic: "Eigenvalues and Eigenvectors",
  },
  derivative: {
    video: "derivative/480p15/DerivativeScene.mp4",
    topic: "Derivatives",
  },
  gradient_descent: {
    video: "ml_02_gradient_descent/480p15/GradientDescentScene.mp4",
    topic: "Gradient Descent",
  },
  backpropagation: {
    video: "ml_03_backpropagation/480p15/BackpropagationScene.mp4",
    topic: "Backpropagation",
  },
  neural_networks: {
    video: "ml_01_neural_networks/480p15/NeuralNetworksScene.mp4",
    topic: "Neural Networks",
  },
  integral: {
    video: "integral/480p15/IntegralScene.mp4",
    topic: "Integrals",
  },
  limit: {
    video: "limit/480p15/LimitScene.mp4",
    topic: "Limits",
  },
  chain_rule: {
    video: "chain_rule/480p15/ChainRuleScene.mp4",
    topic: "Chain Rule",
  },
  determinant: {
    video: "la_11_determinant/480p15/DeterminantScene.mp4",
    topic: "Determinants",
  },
  linear_transform: {
    video: "la_06_linear_transform/480p15/LinearTransformScene.mp4",
    topic: "Linear Transformations",
  },
  vectors: {
    video: "la_01_vectors/480p15/VectorsScene.mp4",
    topic: "Vectors",
  },
  matrix_mult: {
    video: "la_07_matrix_mult/480p15/MatrixMultScene.mp4",
    topic: "Matrix Multiplication",
  },
  quicksort: {
    video: "algo_02_quicksort/480p15/QuicksortScene.mp4",
    topic: "Quicksort",
  },
  game_theory: {
    video: "econ_05_game_theory/480p15/GameTheoryScene.mp4",
    topic: "Game Theory",
  },
  induction: {
    video: "phys_03_induction/480p15/InductionScene.mp4",
    topic: "Electromagnetic Induction",
  },
  maxwell: {
    video: "phys_04_maxwell/480p15/MaxwellScene.mp4",
    topic: "Maxwell Equations",
  },
  dot_product: {
    video: "la_04_dot_product/480p15/DotProductScene.mp4",
    topic: "Dot Product",
  },
  cross_product: {
    video: "la_05_cross_product/480p15/CrossProductScene.mp4",
    topic: "Cross Product",
  },
  svd: {
    video: "la_17_svd/480p15/SVDScene.mp4",
    topic: "Singular Value Decomposition",
  },
  span: {
    video: "la_12_span/480p15/SpanScene.mp4",
    topic: "Span",
  },
  basis: {
    video: "la_14_basis/480p15/BasisScene.mp4",
    topic: "Basis Vectors",
  },
  det_zero: {
    video: "la_22_det_zero/480p15/DetZeroScene.mp4",
    topic: "Why Zero Determinant Means No Inverse",
  },
  bubble_sort: {
    video: "algo_01_bubble_sort/480p15/BubbleSortScene.mp4",
    topic: "Bubble Sort",
  },
};

async function deleteExisting(baseName) {
  const narrPath  = path.join(NARR_DIR, `${baseName}_narrated.mp4`);
  const audioPath = path.join(NARR_DIR, `${baseName}_audio.mp3`);
  for (const p of [narrPath, audioPath]) {
    try { await unlink(p); console.log(`  Deleted: ${path.basename(p)}`); } catch { /* not found */ }
  }
  // Also delete any segment files
  for (let i = 1; i <= 6; i++) {
    const segPath = path.join(NARR_DIR, `${baseName}_seg${i}.mp3`);
    try { await unlink(segPath); } catch { /* not found */ }
  }
}

async function processScene(name) {
  const scene = SCENES[name];
  if (!scene) {
    console.error(`\nUnknown scene: "${name}". Available: ${Object.keys(SCENES).join(", ")}`);
    return false;
  }

  const videoAbsPath = path.join(MANIM_DIR, "output", "videos", ...scene.video.split("/"));
  const baseName     = path.basename(videoAbsPath, ".mp4");

  try {
    await access(videoAbsPath);
  } catch {
    console.error(`\n[SKIP] Video not found: ${videoAbsPath}`);
    return false;
  }

  console.log(`\n${"=".repeat(60)}`);
  console.log(`Scene:  ${scene.topic}`);
  console.log(`Video:  ${scene.video}`);
  console.log(`Voice:  Adam (auq43ws1oslv0tO4BDa7)`);
  console.log(`${"=".repeat(60)}`);

  await deleteExisting(baseName);

  const start = Date.now();
  try {
    const narrPath = await narrateVideo(videoAbsPath, scene.topic, groq);
    const elapsed  = ((Date.now() - start) / 1000).toFixed(1);
    console.log(`\n  SUCCESS (${elapsed}s)`);
    console.log(`  Output: ${narrPath}`);
    return true;
  } catch (err) {
    console.error(`\n  FAILED: ${err.message}`);
    return false;
  }
}

// ── Main ──────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const toProcess = args.length > 0 ? args : ["eigen"];

console.log(`\nFeynman Narration Regenerator`);
console.log(`Voice ID: auq43ws1oslv0tO4BDa7 (Adam)`);
console.log(`Scenes: ${toProcess.join(", ")}`);
if (!process.env.ELEVENLABS_API_KEY) {
  console.error("\nFATAL: ELEVENLABS_API_KEY not set — aborting");
  process.exit(1);
}
if (!process.env.GROQ_API_KEY) {
  console.error("\nFATAL: GROQ_API_KEY not set — aborting");
  process.exit(1);
}
console.log(`ElevenLabs key: set`);
console.log(`Groq key: set`);

for (const name of toProcess) {
  const ok = await processScene(name);
  if (!ok && args.length > 0) {
    console.error(`\nStopping on failure of "${name}".`);
    process.exit(1);
  }
}

console.log(`\nAll done.`);
