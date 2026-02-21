/**
 * regen_narration.mjs — Standalone narration regenerator
 * Usage: node regen_narration.mjs [scene1 scene2 ...]
 * Example: node regen_narration.mjs eigen derivative gradient_descent
 *
 * Regenerates narrated MP4s for the specified scenes using the updated
 * narrate.js pipeline (Adam voice auq43ws1oslv0tO4BDa7, 6-segment, scene-aware).
 */

import dotenv from "dotenv";
import { resolve } from "path";
dotenv.config({ path: resolve(process.cwd(), "backend/.env") });
import path    from "path";
import { fileURLToPath } from "url";
import { access, unlink } from "fs/promises";
import Groq    from "groq-sdk";
import { narrateVideo } from "./backend/src/narrate.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MANIM_DIR = path.join(__dirname, "manim");
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
};

async function deleteExisting(baseName) {
  const narrPath = path.join(NARR_DIR, `${baseName}_narrated.mp4`);
  const audioPath = path.join(NARR_DIR, `${baseName}_audio.mp3`);
  for (const p of [narrPath, audioPath]) {
    try { await unlink(p); console.log(`  Deleted: ${path.basename(p)}`); } catch { /* not found */ }
  }
}

async function processScene(name) {
  const scene = SCENES[name];
  if (!scene) {
    console.error(`\nUnknown scene: "${name}". Available: ${Object.keys(SCENES).join(", ")}`);
    return;
  }

  const videoAbsPath = path.join(MANIM_DIR, "output", "videos", ...scene.video.split("/"));
  const baseName     = path.basename(videoAbsPath, ".mp4");

  // Verify video exists
  try {
    await access(videoAbsPath);
  } catch {
    console.error(`\n[SKIP] Video not found: ${videoAbsPath}`);
    return;
  }

  console.log(`\n${"=".repeat(60)}`);
  console.log(`Processing: ${scene.topic}`);
  console.log(`  Video: ${scene.video}`);
  console.log(`  Voice: Adam (auq43ws1oslv0tO4BDa7)`);
  console.log(`${"=".repeat(60)}`);

  // Delete cached version so it regenerates
  await deleteExisting(baseName);

  const start = Date.now();
  try {
    const narrPath = await narrateVideo(videoAbsPath, scene.topic, groq);
    const elapsed  = ((Date.now() - start) / 1000).toFixed(1);
    console.log(`\n  SUCCESS: ${narrPath} (${elapsed}s)`);
    console.log(`  -> Verify Adam male voice and narration sync in: /narrated/${path.basename(narrPath)}`);
  } catch (err) {
    console.error(`\n  FAILED: ${err.message}`);
    throw err;
  }
}

// ── Main ──────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const toProcess = args.length > 0 ? args : ["eigen"]; // default: just eigen

console.log(`\nFeynman Narration Regenerator`);
console.log(`Voice: Adam — auq43ws1oslv0tO4BDa7`);
console.log(`Scenes to process: ${toProcess.join(", ")}`);

for (const name of toProcess) {
  try {
    await processScene(name);
  } catch (err) {
    console.error(`Fatal error on "${name}": ${err.message}`);
    process.exit(1);
  }
}

console.log(`\nAll done.`);
