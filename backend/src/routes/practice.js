/**
 * POST /api/practice-problems
 * { topic: string, angle?: string }
 * → { problems: [{ difficulty, problem }] }
 *
 * POST /api/solution
 * { topic: string, problem: string, difficulty: string }
 * → { solution: string }
 */
import { Router } from "express";
import Groq from "groq-sdk";

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
export const practiceRoute = Router();

practiceRoute.post("/problems", async (req, res) => {
  const topic = (req.body.topic ?? "").trim();
  const angle = (req.body.angle ?? "").trim();
  if (!topic) return res.status(400).json({ error: "topic is required" });

  const angleCtx = angle
    ? ` Tailor problems to this angle: "${angle}".`
    : "";

  try {
    const resp = await groq.chat.completions.create({
      model: "llama-3.3-70b-versatile",
      messages: [
        {
          role: "system",
          content: `You are a math tutor. Generate exactly 3 practice problems for the topic.
- EASY: Direct application of the concept, straightforward.
- MEDIUM: Requires combining the concept with one prerequisite.
- HARD: Requires creative thinking and extension of the concept.

Each problem must be a REAL mathematical problem requiring actual work (not multiple choice).
Output JSON only: { "easy": "problem text", "medium": "problem text", "hard": "problem text" }`,
        },
        {
          role: "user",
          content: `Topic: ${topic}.${angleCtx} Generate 3 problems (easy, medium, hard). JSON only.`,
        },
      ],
      temperature: 0.6,
      max_tokens: 800,
    });
    let text = resp.choices[0].message.content.trim();
    text = text.replace(/^```json\s*/i, "").replace(/```\s*$/i, "").trim();
    const parsed = JSON.parse(text);
    const problems = [
      { difficulty: "easy", problem: parsed.easy ?? parsed.Easy ?? "" },
      { difficulty: "medium", problem: parsed.medium ?? parsed.Medium ?? "" },
      { difficulty: "hard", problem: parsed.hard ?? parsed.Hard ?? "" },
    ];
    return res.json({ problems });
  } catch (err) {
    console.error("[practice-problems]", err.message);
    return res.status(500).json({ error: "Failed to generate problems", detail: err.message });
  }
});

practiceRoute.post("/solution", async (req, res) => {
  const { topic, problem, difficulty } = req.body;
  if (!topic || !problem) return res.status(400).json({ error: "topic and problem required" });

  try {
    const resp = await groq.chat.completions.create({
      model: "llama-3.3-70b-versatile",
      messages: [
        {
          role: "system",
          content: `You are a Feynman-style tutor. Give a FULL step-by-step solution.
- Emphasize geometric intuition FIRST, algebra second.
- Use the same visual language as 3Blue1Brown videos.
- Walk through each step clearly. Do not skip steps.`,
        },
        {
          role: "user",
          content: `Topic: ${topic}. Problem (${difficulty}): ${problem}\n\nGive the complete worked solution with intuition.`,
        },
      ],
      temperature: 0.4,
      max_tokens: 1200,
    });
    const solution = resp.choices[0].message.content.trim();
    return res.json({ solution });
  } catch (err) {
    console.error("[solution]", err.message);
    return res.status(500).json({ error: "Failed to generate solution", detail: err.message });
  }
});
