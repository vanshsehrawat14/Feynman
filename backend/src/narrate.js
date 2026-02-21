/**
 * Narration pipeline for Feynman — Professor-Style, Sync-Aware
 *
 * 1. Read the actual Manim scene .py file
 * 2. Ask Groq to write 6 narration segments as flowing professor speech
 * 3. Convert each segment to audio via ElevenLabs (voice auq43ws1oslv0tO4BDa7)
 * 4. Concatenate segments into one audio track
 * 5. Measure audio vs video duration — slow video, pad audio, or merge directly
 * 6. Output synced narrated MP4
 *
 * gTTS fallback is DISABLED. No other voice fallback. ElevenLabs only.
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

const ELEVEN_MODEL   = "eleven_turbo_v2_5";
const FFMPEG_PATH    = "C:\\ffmpeg\\bin\\ffmpeg.exe";
const FFPROBE_PATH   = "C:\\ffmpeg\\bin\\ffprobe.exe";

// ── Read scene Python file ─────────────────────────────────────────────────
async function readSceneFile(videoAbsPath) {
  const parts       = videoAbsPath.split(path.sep);
  const videosIdx   = parts.lastIndexOf("videos");
  if (videosIdx === -1) return null;
  const sceneDirName = parts[videosIdx + 1];
  const sceneFile    = path.join(MANIM_DIR, "scenes", `${sceneDirName}.py`);
  try {
    const code = await readFile(sceneFile, "utf8");
    return code.slice(0, 7000);
  } catch {
    return null;
  }
}

// ── Professor-style 6-segment narration via Groq ──────────────────────────
async function getNarrationSegments(topic, sceneCode, groq) {
  const sceneContext = sceneCode
    ? `\n\nHere is the Manim code for this animation — use it to understand what is shown visually so your narration can reference and explain those visuals:\n\`\`\`python\n${sceneCode}\n\`\`\``
    : "";

  const resp = await groq.chat.completions.create({
    model: "llama-3.3-70b-versatile",
    messages: [
      {
        role: "system",
        content: `You are a calm, clear university professor writing a voiceover narration for a Manim educational animation about "${topic}".

Your narration teaches the concept as the animation plays. It sounds like a natural lecture — not a reading of what is on screen.

STYLE RULES — follow strictly:
- Write flowing prose only. No bullet points. No numbered lists. No formulas read character by character.
- Sound warm, curious, and authoritative — like a Richard Feynman or Gilbert Strang lecture.
- Reference visuals naturally ("notice how the arrow...", "what you're seeing here is...") but frame everything as teaching, not describing.
- Build intuition first, then connect to the math.
- Use second person naturally: "you", "notice", "think about", "consider".
- Every segment must be complete, flowing sentences — never truncated.

The video has exactly 6 sections. Write one narration segment per section.
Output ONLY a valid JSON object with exactly these 6 keys (no markdown, no extra text):

{
  "hook": "~100 words. Open with a compelling question or surprising observation that makes the viewer curious. Reference the opening visual but frame it as a hook, not a description.",
  "intuition": "~225 words. Explain the geometric or visual intuition being built. Reference the visuals as a professor would — explaining what they reveal about the concept. Build the idea step by step in flowing prose.",
  "notation": "~150 words. Introduce the mathematical notation intuitively. Explain what each symbol captures about the idea. Do not read formulas aloud — explain what they mean.",
  "example": "~225 words. Walk through the worked example as a teacher. Explain why each step matters and what it reveals. Make the numbers meaningful, not mechanical.",
  "insight": "~150 words. Share the deeper application and why this concept matters. Connect it to real uses the viewer would care about. Make it feel profound.",
  "summary": "~75 words. Close warmly. Remind the viewer of the single most important insight. Leave them with something to think about."
}`,
      },
      {
        role: "user",
        content: `Write the 6-segment narration for: "${topic}"${sceneContext}\n\nReturn the JSON object only.`,
      },
    ],
    temperature: 0.5,
    max_tokens: 2500,
  });

  let content = resp.choices[0].message.content.trim();
  content = content.replace(/^```json\s*/im, "").replace(/^```\s*/im, "").replace(/```\s*$/im, "").trim();
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

// ── ElevenLabs TTS — hardcoded voice auq43ws1oslv0tO4BDa7, no fallback ─────
async function elevenLabsTTS(text) {
  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) throw new Error("ELEVENLABS_API_KEY not set");
  if (!text || !text.trim()) throw new Error("Empty narration segment");

  const response = await fetch(
    "https://api.elevenlabs.io/v1/text-to-speech/auq43ws1oslv0tO4BDa7",
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
    console.log(`[narrate] TTS Adam — ${bytes.length} bytes`);
    return bytes;
  }

  const status  = response.status;
  const errText = await response.text().catch(() => "");
  throw new Error(`ElevenLabs ${status}: ${errText.slice(0, 250)}`);
}

// ── ffmpeg: concatenate MP3 segments ─────────────────────────────────────
async function concatAudioSegments(segmentPaths, outputPath) {
  const concatLines = segmentPaths.map(p => `file '${p.replace(/\\/g, "/").replace(/'/g, "\\'")}'`);
  const concatFile  = outputPath.replace(/\.mp3$/, "_concatlist.txt");
  await writeFile(concatFile, concatLines.join("\n"), "utf8");

  const pyScript = [
    "import subprocess, sys",
    `ffmpeg = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
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

// ── Get media duration in seconds via ffprobe ──────────────────────────────
async function getMediaDuration(filePath) {
  const pyScript = [
    "import subprocess",
    `path = r'${filePath.replace(/\\/g, "\\\\")}'`,
    `ffprobe = r'${FFPROBE_PATH.replace(/\\/g, "\\\\")}'`,
    "r = subprocess.run(",
    "  [ffprobe, '-v', 'error', '-show_entries', 'format=duration',",
    "   '-of', 'default=noprint_wrappers=1:nokey=1', path],",
    "  capture_output=True, text=True, timeout=30",
    ")",
    "print(r.stdout.strip() or '0')",
  ].join("\n");

  const tmpPy = path.join(NARR_DIR, "_probe_dur.py");
  await writeFile(tmpPy, pyScript, "utf8");
  try {
    const { stdout } = await execAsync(`python "${tmpPy}"`, { timeout: 30_000 });
    return parseFloat(stdout.trim()) || 0;
  } catch {
    return 0;
  }
}

// ── Sync-aware merge: slow video / pad audio / or direct merge ─────────────
async function mergeAudioVideo(videoPath, audioPath, outputPath) {
  const audioDur = await getMediaDuration(audioPath);
  const videoDur = await getMediaDuration(videoPath);
  const diff = audioDur - videoDur;

  console.log(`[narrate] video: ${videoDur.toFixed(1)}s  audio: ${audioDur.toFixed(1)}s  diff: ${diff.toFixed(1)}s`);

  let pyScript;

  if (diff > 5) {
    // Audio is longer — slow video to match
    const ratio = (audioDur / videoDur).toFixed(6);
    console.log(`[narrate] audio longer by ${diff.toFixed(1)}s — slowing video (ratio ${ratio})`);
    pyScript = [
      "import subprocess, sys, os",
      `ffmpeg = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
      `video  = r'${videoPath.replace(/\\/g, "\\\\")}'`,
      `audio  = r'${audioPath.replace(/\\/g, "\\\\")}'`,
      `output = r'${outputPath.replace(/\\/g, "\\\\")}'`,
      `ratio  = ${ratio}`,
      "cmd = [ffmpeg, '-y', '-i', video, '-i', audio,",
      "       '-filter:v', f'setpts={ratio}*PTS',",
      "       '-c:a', 'aac', '-shortest', output]",
      "result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)",
      "print('merge rc:', result.returncode)",
      "if result.returncode != 0:",
      "    print('stderr:', result.stderr[-600:])",
      "    sys.exit(1)",
      "print('Merge OK, size:', os.path.getsize(output))",
    ].join("\n");

  } else if (diff < -5) {
    // Video is longer — pad audio with silence then merge
    console.log(`[narrate] video longer by ${Math.abs(diff).toFixed(1)}s — padding audio`);
    const paddedPath = audioPath.replace(/\.mp3$/, "_padded.mp3");
    pyScript = [
      "import subprocess, sys, os",
      `ffmpeg     = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
      `video      = r'${videoPath.replace(/\\/g, "\\\\")}'`,
      `audio      = r'${audioPath.replace(/\\/g, "\\\\")}'`,
      `padded     = r'${paddedPath.replace(/\\/g, "\\\\")}'`,
      `output     = r'${outputPath.replace(/\\/g, "\\\\")}'`,
      `video_dur  = ${videoDur.toFixed(3)}`,
      "# Pad audio to video length",
      "r1 = subprocess.run(",
      "  [ffmpeg, '-y', '-i', audio, '-af', f'apad=whole_dur={video_dur}', padded],",
      "  capture_output=True, text=True, timeout=120)",
      "if r1.returncode != 0:",
      "    print('pad err:', r1.stderr[-300:])",
      "    sys.exit(1)",
      "# Merge padded audio with video",
      "r2 = subprocess.run(",
      "  [ffmpeg, '-y', '-i', video, '-i', padded,",
      "   '-c:v', 'copy', '-c:a', 'aac', '-shortest', output],",
      "  capture_output=True, text=True, timeout=600)",
      "print('merge rc:', r2.returncode)",
      "if r2.returncode != 0:",
      "    print('stderr:', r2.stderr[-600:])",
      "    sys.exit(1)",
      "print('Merge OK, size:', os.path.getsize(output))",
      "try: os.unlink(padded)",
      "except: pass",
    ].join("\n");

  } else {
    // Within 5 seconds — direct merge
    console.log(`[narrate] durations close — direct merge`);
    pyScript = [
      "import subprocess, sys, os",
      `ffmpeg = r'${FFMPEG_PATH.replace(/\\/g, "\\\\")}'`,
      `video  = r'${videoPath.replace(/\\/g, "\\\\")}'`,
      `audio  = r'${audioPath.replace(/\\/g, "\\\\")}'`,
      `output = r'${outputPath.replace(/\\/g, "\\\\")}'`,
      "cmd = [ffmpeg, '-y', '-i', video, '-i', audio,",
      "       '-c:v', 'copy', '-c:a', 'aac', '-shortest', output]",
      "result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)",
      "print('merge rc:', result.returncode)",
      "if result.returncode != 0:",
      "    print('stderr:', result.stderr[-600:])",
      "    sys.exit(1)",
      "print('Merge OK, size:', os.path.getsize(output))",
    ].join("\n");
  }

  const tmpPy = path.join(NARR_DIR, "_merge_tmp.py");
  await writeFile(tmpPy, pyScript, "utf8");
  const { stdout, stderr } = await execAsync(`python "${tmpPy}"`, { timeout: 600_000 });
  if (stdout) console.log("[narrate] merge:", stdout.trim());
  if (stderr) console.warn("[narrate] merge stderr:", stderr.trim().slice(0, 200));
}

// ── Clean up temporary segment files ─────────────────────────────────────
async function cleanSegments(paths) {
  for (const p of paths) {
    try { await unlink(p); } catch { /* ignore */ }
  }
  for (const p of paths) {
    const txt = p.replace(/\.mp3$/, "_concatlist.txt");
    try { await unlink(txt); } catch { /* ignore */ }
  }
}

// ── Main export ───────────────────────────────────────────────────────────
/**
 * narrateVideo(videoAbsPath, topic, groq)
 * Generates professor-style 6-segment narration, syncs audio to video.
 * Returns the absolute path to the narrated MP4.
 * ElevenLabs only — no gTTS, no other fallback.
 */
export async function narrateVideo(videoAbsPath, topic, groq) {
  await mkdir(NARR_DIR, { recursive: true });

  const baseName      = path.basename(videoAbsPath, ".mp4");
  const narrPath      = path.join(NARR_DIR, `${baseName}_narrated.mp4`);
  const combinedAudio = path.join(NARR_DIR, `${baseName}_audio.mp3`);

  // Cache check
  try {
    await access(narrPath);
    console.log(`[narrate] cache hit: ${baseName}`);
    return narrPath;
  } catch { /* not cached */ }

  console.log(`[narrate] generating professor narration for "${topic}"...`);

  // 1. Read scene code
  const sceneCode = await readSceneFile(videoAbsPath);
  console.log(sceneCode
    ? `[narrate] scene code loaded (${sceneCode.length} chars)`
    : `[narrate] scene code not found — topic-only narration`
  );

  // 2. Generate 6 narration segments
  const segments = await getNarrationSegments(topic, sceneCode, groq);
  console.log("[narrate] 6 segments generated");

  // 3. TTS each segment
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
  console.log(`[narrate] concatenating ${segmentPaths.length} segments...`);
  if (segmentPaths.length === 1) {
    const buf = await readFile(segmentPaths[0]);
    await writeFile(combinedAudio, buf);
  } else {
    await concatAudioSegments(segmentPaths, combinedAudio);
  }

  // 5. Sync-aware merge
  console.log("[narrate] syncing and merging...");
  await mergeAudioVideo(videoAbsPath, combinedAudio, narrPath);
  console.log(`[narrate] done → ${narrPath}`);

  // 6. Cleanup
  await cleanSegments(segmentPaths);

  return narrPath;
}
