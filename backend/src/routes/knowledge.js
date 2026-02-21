/**
 * POST /api/knowledge
 * { topic: string, angle?: string }
 * → { formulas: [...], misconceptions: [...], summary: string }
 */
import { Router } from "express";
import Groq from "groq-sdk";

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
export const knowledgeRoute = Router();

knowledgeRoute.post("/", async (req, res) => {
  const topic = (req.body.topic ?? "").trim();
  const angle = (req.body.angle ?? "").trim();
  if (!topic) return res.status(400).json({ error: "topic is required" });

  const angleCtx = angle ? ` Focus/angle: ${angle}.` : "";

  try {
    const [formulasResp, misconceptionsResp, summaryResp] = await Promise.all([
      groq.chat.completions.create({
        model: "llama-3.3-70b-versatile",
        messages: [
          {
            role: "system",
            content: `List 4-6 key formulas for the topic. For each: formula (plain text) + one line plain English description of what it means intuitively. Output JSON: { "formulas": [{ "formula": "...", "meaning": "..." }] }`,
          },
          { role: "user", content: `Topic: ${topic}.${angleCtx} JSON only.` },
        ],
        temperature: 0.3,
        max_tokens: 600,
      }),
      groq.chat.completions.create({
        model: "llama-3.3-70b-versatile",
        messages: [
          {
            role: "system",
            content: `List 3-5 common misconceptions. For each: misconception (what students wrongly think) and correct intuition. Output JSON: { "misconceptions": [{ "wrong": "...", "correct": "..." }] }`,
          },
          { role: "user", content: `Topic: ${topic}.${angleCtx} JSON only.` },
        ],
        temperature: 0.4,
        max_tokens: 600,
      }),
      groq.chat.completions.create({
        model: "llama-3.3-70b-versatile",
        messages: [
          {
            role: "system",
            content: `Summarize the topic in 5 bullet points. Each bullet is one important takeaway. Be concise.`,
          },
          { role: "user", content: `Topic: ${topic}.${angleCtx}` },
        ],
        temperature: 0.5,
        max_tokens: 300,
      }),
    ]);

    const parseJson = (text) => {
      let t = text.trim().replace(/^```json\s*/i, "").replace(/```\s*$/i, "").trim();
      try {
        return JSON.parse(t);
      } catch {
        return { formulas: [], misconceptions: [] };
      }
    };

    const formulasData = parseJson(formulasResp.choices[0].message.content);
    const misconceptionsData = parseJson(misconceptionsResp.choices[0].message.content);
    const summary = summaryResp.choices[0].message.content.trim();

    const formulas = Array.isArray(formulasData.formulas)
      ? formulasData.formulas
      : (formulasData.formulas ? [formulasData.formulas] : []);
    const misconceptions = Array.isArray(misconceptionsData.misconceptions)
      ? misconceptionsData.misconceptions
      : (misconceptionsData.misconceptions ? [misconceptionsData.misconceptions] : []);

    return res.json({
      formulas: formulas.slice(0, 6),
      misconceptions: misconceptions.slice(0, 5),
      summary,
    });
  } catch (err) {
    console.error("[knowledge]", err.message);
    return res.status(500).json({ error: "Failed to generate knowledge", detail: err.message });
  }
});
