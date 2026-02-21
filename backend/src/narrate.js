/**
 * Narration pipeline for Feynman — Scene-Aware 6-Segment Version
 *
 * 1. Read the actual Manim scene .py file to understand what is animated
 * 2. Ask Groq to write 6 narration segments that describe those exact visuals
 * 3. Convert each segment to audio via ElevenLabs (Adam voice)
 * 4. Concatenate the 6 segments into one audio track via ffmpeg
 * 5. Merge audio + video → narrated MP4
 * 6. Cache result in manim/output/narrated/
 *
 * gTTS fallback is DISABLED — if ElevenLabs fails entirely, an error is thrown.
 */

import { writeFile, readFile, access, mkdir, unlink } from "fs/promises";
import { exec }           from "child_process";
import { promisify }      from "util";
import path               from "path";
import { fileURLToPath }  from "url";

const execAsync = promisify(exec);
const __dirname  = path.dirname(fileURLToPath(import.meta.url));

const MANIM_DIR   = path.resolve(__dirname, "../../manim");
const NARR_DIR    = path.join(MANIM_DIR, "output", "narrated");

// ── Voice configuration ────────────────────────────────────────────────────
// Primary: Adam library voice (requires paid ElevenLabs plan)
// Fallback: Adam pre-made voice (available on all plans including free)
const VOICE_ID_PRIMARY  = "auq43ws1oslv0tO4BDa7"; // Adam (paid plan)
const VOICE_ID_FALLBACK = "pNInz6obpgDQGcFmaJgB"; // Adam (all plans)
const ELEVEN_MODEL       = "eleven_turbo_v2_5";    // Fast English TTS

// ── ffmpeg — use system installation (C:\ffmpeg\bin\ffmpeg.exe) ───────────
// Falls back to imageio_ffmpeg if system ffmpeg not found
const FFMPEG_SYSTEM = "C:\\ffmpeg\\bin\\ffmpeg.exe";

let _ffmpegExe = null;
async function getFfmpegExe() {
  if (_ffmpegExe) return _ffmpegExe;
  // Try system ffmpeg first (C:\ffmpeg\bin\ffmpeg.exe)
  try {
    const { stdout } = await execAsync(`"${FFMPEG_SYSTEM}" -version`, { timeout: 10_000 });
    if (stdout.includes("ffmpeg version") || stdout.includes("built with")) {
      _ffmpegExe = FFMPEG_SYSTEM;
      return _ffmpegExe;
    }
  } catch { /* not found there */ }
  // Fall back to imageio_ffmpeg
  try {
    const { stdout } = await execAsync(
      'python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"',
      { timeout: 15_000 }
    );
    _ffmpegExe = stdout.trim();
  } catch {
    _ffmpegExe = "C:\\ffmpeg\\bin\\ffmpeg.exe"; // last resort
  }
  return _ffmpegExe;
}

// ── Read scene Python file from the video's folder name ───────────────────
// videoAbsPath: …/manim/output/videos/la_16_eigen/480p15/EigenScene.mp4
// → scene file: …/manim/scenes/la_16_eigen.py
async function readSceneFile(videoAbsPath) {
  const parts       = videoAbsPath.split(path.sep);
  const videosIdx   = parts.lastIndexOf("videos");
  if (videosIdx === -1) return null;
  const sceneDirName = parts[videosIdx + 1];          // e.g. "la_16_eigen"
  const sceneFile    = path.join(MANIM_DIR, "scenes", `${sceneDirName}.py`);
  try {
    const code = await readFile(sceneFile, "utf8");
    return code.slice(0, 7000); // trim to fit Groq context
  } catch {
    return null;
  }
}

// ── 6-segment narration script via Groq ───────────────────────────────────
async function getNarrationSegments(topic, sceneCode, groq) {
  const sceneContext = sceneCode
    ? `\n\nHere is the actual Manim Python code for this animation — read it to write narration that describes EXACTLY what is on screen:\n\`\`\`python\n${sceneCode}\n\`\`\``
    : "";

  const resp = await groq.chat.completions.create({
    model: "llama-3.3-70b-versatile",
    messages: [
      {
        role: "system",
        content: `You are writing a professional voiceover script for a Manim educational animation about "${topic}".
Your narration must precisely describe the specific visuals and animations shown in each section.
Do NOT write generic textbook content — narrate what the viewer is LITERALLY SEEING on screen.

The video has exactly 6 sections. Write one narration segment per section.
Output ONLY a valid JSON object with exactly these 6 keys (no markdown, no extra text):

{
  "hook": "~100 words. Narrate section 1: describe the title card, the opening question text on screen, and the first visual teaser being shown.",
  "intuition": "~225 words. Narrate section 2: describe each geometric animation step-by-step as it appears — arrows, transformations, vectors, grids — exactly as coded.",
  "notation": "~150 words. Narrate section 3: introduce each mathematical symbol as it appears on screen, connecting it to the geometry established visually.",
  "example": "~225 words. Narrate section 4: walk through the exact numbers and algebraic steps shown in the worked example — use the same values from the code.",
  "insight": "~150 words. Narrate section 5: describe the deeper application animation on screen — what is being shown and why it matters.",
  "summary": "~75 words. Narrate section 6: describe the final summary visual on screen and close with the single most important takeaway."
}

Use second person ("Notice how...", "Watch as...", "You can see...").
Be enthusiastic and clear. Reference specific visual elements: arrows, equations, colors, numbers from the code.`,
      },
      {
        role: "user",
        content: `Write the 6-segment narration for: "${topic}"${sceneContext}\n\nReturn the JSON object only.`,
      },
    ],
    temperature: 0.4,
    max_tokens: 2200,
  });

  let content = resp.choices[0].message.content.trim();
  content = content.replace(/^```json\s*/im, "").replace(/^```\s*/im, "").replace(/```\s*$/im, "").trim();
  // Extract first { ... } block
  const match = content.match(/\{[\s\S]*\}/);
  if (match) content = match[0];

  try {
    return JSON.parse(content);
  } catch (e) {
    console.warn("[narrate] JSON parse failed:", e.message.slice(0, 80));
    return {
      hook:      content.slice(0, 600),
      intuition: "",
      notation:  "",
      example:   "",
      insight:   "",
      summary:   "",
    };
  }
}

// ── ElevenLabs TTS ─────────────────────────────────────────────────────────
// Tries VOICE_ID_PRIMARY first; falls back to VOICE_ID_FALLBACK on 402.
// NO gTTS fallback — only ElevenLabs Adam voices are used.
async function elevenLabsTTS(text) {
  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) throw new Error("ELEVENLABS_API_KEY not set");
  if (!text || !text.trim()) throw new Error("Empty narration segment");

  for (const [voiceId, label] of [
    [VOICE_ID_PRIMARY,  "Adam(primary)"],
    [VOICE_ID_FALLBACK, "Adam(fallback)"],
  ]) {
    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
      {
        method: "POST",
        headers: {
          "xi-api-key":   apiKey,
          "Content-Type": "application/json",
          Accept:         "audio/mpeg",
        },
        body: JSON.stringify({
          text:     text.trim(),
          model_id: ELEVEN_MODEL,
          voice_settings: { stability: 0.45, similarity_boost: 0.80 },
        }),
      }
    );

    if (response.ok) {
      const bytes = Buffer.from(await response.arrayBuffer());
      if (bytes.length < 500) throw new Error(`ElevenLabs returned tiny audio (${bytes.length} bytes)`);
      console.log(`[narrate] TTS via ${label} — ${bytes.length} bytes`);
      return bytes;
    }

    const status  = response.status;
    const errText = await response.text().catch(() => "");
    if (status === 402) {
      // Payment required for this voice — try fallback
      console.warn(`[narrate] ${label} (${voiceId}) requires paid plan — trying fallback voice`);
      continue;
    }
    // Any other error is fatal
    throw new Error(`ElevenLabs ${status}: ${errText.slice(0, 250)}`);
  }

  throw new Error("Both ElevenLabs Adam voices failed — check your API key and plan");
}

// ── ffmpeg: concatenate multiple MP3 files into one ────────────────────────
async function concatAudioSegments(segmentPaths, outputPath) {
  const ffmpeg = await getFfmpegExe();
  const concatLines = segmentPaths.map(p => `file '${p.replace(/\\/g, "/").replace(/'/g, "\\'")}'`);
  const concatFile  = outputPath.replace(/\.mp3$/, "_concatlist.txt");
  await writeFile(concatFile, concatLines.join("\n"), "utf8");

  const pyScript = [
    "import subprocess, sys",
    `ffmpeg = r'${ffmpeg.replace(/\\/g, "\\\\")}'`,
    `concat_file = r'${concatFile.replace(/\\/g, "\\\\")}'`,
    `output = r'${outputPath.replace(/\\/g, "\\\\")}'`,
    "cmd = [ffmpeg, '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output]",
    "result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)",
    "print('concat rc:', result.returncode)",
    "if result.returncode != 0:",
    "    print('stderr:', result.stderr[-400:])",
    "    sys.exit(1)",
    "print('Concat OK, size:', __import__('os').path.getsize(output))",
  ].join("\n");

  const tmpPy = path.join(NARR_DIR, "_concat_tmp.py");
  await writeFile(tmpPy, pyScript, "utf8");
  const { stdout, stderr } = await execAsync(`python "${tmpPy}"`, { timeout: 180_000 });
  if (stdout) console.log("[narrate] concat:", stdout.trim());
  if (stderr) console.warn("[narrate] concat stderr:", stderr.trim().slice(0, 200));
}

// ── ffmpeg: merge video + audio → narrated MP4 ────────────────────────────
async function mergeAudioVideo(videoPath, audioPath, outputPath) {
  const ffmpeg = await getFfmpegExe();

  const pyScript = [
    "import subprocess, sys, os",
    `ffmpeg = r'${ffmpeg.replace(/\\/g, "\\\\")}'`,
    `video  = r'${videoPath.replace(/\\/g, "\\\\")}'`,
    `audio  = r'${audioPath.replace(/\\/g, "\\\\")}'`,
    `output = r'${outputPath.replace(/\\/g, "\\\\")}'`,
    "cmd = [ffmpeg, '-y', '-i', video, '-i', audio,",
    "       '-c:v', 'copy', '-c:a', 'aac',",
    "       '-map', '0:v:0', '-map', '1:a:0', '-shortest', output]",
    "result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)",
    "print('merge rc:', result.returncode)",
    "if result.returncode != 0:",
    "    print('stderr:', result.stderr[-600:])",
    "    sys.exit(1)",
    "print('Merge OK, size:', os.path.getsize(output))",
  ].join("\n");

  const tmpPy = path.join(NARR_DIR, "_merge_tmp.py");
  await writeFile(tmpPy, pyScript, "utf8");
  const { stdout, stderr } = await execAsync(`python "${tmpPy}"`, { timeout: 300_000 });
  if (stdout) console.log("[narrate] merge:", stdout.trim());
  if (stderr) console.warn("[narrate] merge stderr:", stderr.trim().slice(0, 200));
}

// ── Clean up temporary segment files ──────────────────────────────────────
async function cleanSegments(paths) {
  for (const p of paths) {
    try { await unlink(p); } catch { /* ignore */ }
  }
  // Clean concat list file
  for (const p of paths) {
    const txt = p.replace(/\.mp3$/, "_concatlist.txt");
    try { await unlink(txt); } catch { /* ignore */ }
  }
}

// ── Main export ────────────────────────────────────────────────────────────
/**
 * narrateVideo(videoAbsPath, topic, groq)
 *
 * Generates scene-aware 6-segment narration using Adam voice.
 * Returns the absolute path to the narrated MP4.
 * Throws if ElevenLabs fails — gTTS is NOT used.
 */
export async function narrateVideo(videoAbsPath, topic, groq) {
  await mkdir(NARR_DIR, { recursive: true });

  const baseName      = path.basename(videoAbsPath, ".mp4");
  const narrPath      = path.join(NARR_DIR, `${baseName}_narrated.mp4`);
  const combinedAudio = path.join(NARR_DIR, `${baseName}_audio.mp3`);

  // Return cached result
  try {
    await access(narrPath);
    console.log(`[narrate] cache hit: ${baseName}`);
    return narrPath;
  } catch { /* not cached */ }

  console.log(`[narrate] generating scene-aware narration for "${topic}"...`);

  // 1. Read the actual Manim scene Python file
  const sceneCode = await readSceneFile(videoAbsPath);
  console.log(sceneCode
    ? `[narrate] scene code loaded (${sceneCode.length} chars)`
    : `[narrate] scene code not found — using topic-only narration`
  );

  // 2. Generate 6-segment narration via Groq
  const segments = await getNarrationSegments(topic, sceneCode, groq);
  console.log("[narrate] 6 segments generated");

  // 3. Convert each segment to audio via ElevenLabs
  const SEGMENT_ORDER = [
    { key: "hook",      label: "S1-Hook"      },
    { key: "intuition", label: "S2-Intuition" },
    { key: "notation",  label: "S3-Notation"  },
    { key: "example",   label: "S4-Example"   },
    { key: "insight",   label: "S5-Insight"   },
    { key: "summary",   label: "S6-Summary"   },
  ];

  const segmentPaths = [];
  for (const [i, { key, label }] of SEGMENT_ORDER.entries()) {
    const text = segments[key];
    if (!text || !text.trim()) {
      console.warn(`[narrate] ${label} is empty — skipping`);
      continue;
    }
    const wordCount = text.trim().split(/\s+/).length;
    console.log(`[narrate] TTS ${label} (${wordCount} words)...`);
    const audioBytes = await elevenLabsTTS(text);
    const segPath    = path.join(NARR_DIR, `${baseName}_seg${i + 1}.mp3`);
    await writeFile(segPath, audioBytes);
    segmentPaths.push(segPath);
  }

  if (segmentPaths.length === 0) {
    throw new Error("All narration segments were empty");
  }

  // 4. Concatenate segments
  console.log(`[narrate] concatenating ${segmentPaths.length} audio segments...`);
  if (segmentPaths.length === 1) {
    const buf = await readFile(segmentPaths[0]);
    await writeFile(combinedAudio, buf);
  } else {
    await concatAudioSegments(segmentPaths, combinedAudio);
  }

  // 5. Merge audio + video
  console.log("[narrate] merging audio + video...");
  await mergeAudioVideo(videoAbsPath, combinedAudio, narrPath);
  console.log(`[narrate] done → ${narrPath}`);

  // 6. Clean up segment files
  await cleanSegments(segmentPaths);

  return narrPath;
}
