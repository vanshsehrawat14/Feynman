import "dotenv/config";
import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import { generateRoute } from "./routes/generate.js";
import { practiceRoute } from "./routes/practice.js";
import { knowledgeRoute } from "./routes/knowledge.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app  = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Serve rendered Manim videos
const videoDir = path.resolve(__dirname, "../../manim/output/videos");
app.use("/videos", express.static(videoDir));

// Serve narrated videos (audio-merged)
const narrDir = path.resolve(__dirname, "../../manim/output/narrated");
app.use("/narrated", express.static(narrDir));

app.use("/api/generate", generateRoute);
app.use("/api/practice", practiceRoute);
app.use("/api/knowledge", knowledgeRoute);

app.listen(PORT, () =>
  console.log(`Feynman backend running on http://localhost:${PORT}`)
);
