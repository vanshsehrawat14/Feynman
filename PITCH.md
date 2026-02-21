# Feynman — Rebel Hacks Pitch Script

**Event:** Rebel Hacks @ UNLV  
**Theme:** Las Vegas  
**Time:** ~2–3 min pitch + live demo

---

## Hook (5 seconds)

**"3Blue1Brown makes one video a month. Feynman makes one in two minutes. On anything."**

---

## Problem (20 seconds)

Complex math and CS concepts — linear algebra, calculus, algorithms — are hard because they need **geometric intuition**, not just formulas.

- **ChatGPT** gives you text. Text doesn’t build geometric intuition.
- **YouTube** has great 3B1B videos, but they’re static. One video per month, made over weeks.
- Most students never get that “aha” moment because they never see the geometry.

---

## Solution (15 seconds)

**Feynman** is an AI-powered visual learning platform. You type any topic — derivatives, eigenvalues, SVD, chain rule — and Feynman generates a 3–5 minute **3Blue1Brown-style animated video** in under two minutes.

Same tool 3B1B uses: **Manim**. Same quality. On demand. For any topic you type.

---

## Live Demo (60–90 seconds)

### Before you start
- Have the app open on a topic chip (e.g., **eigenvalues**).
- Make sure the video has been pre-rendered or is ready to generate quickly.

### Demo flow

1. **"Quick question — raise your hand if you've taken linear algebra."**
   - *Pause. Let hands go up.*

2. **"Keep it raised if you understood eigenvalues the first time you saw them."**
   - *Pause. Many hands go down.*

3. **"Eigenvalues are one of those concepts that feels like magic until you see the geometry. Watch."**
   - Type **eigenvalues** and hit Generate (or click the chip).
   - Let the video play for 30–60 seconds.

4. **"That’s a 3Blue1Brown-style video. Generated in about two minutes. For any topic you type."**
   - Show the topic chips: calculus, foundations, transformations, eigenvalues, SVD, etc.
   - Optionally generate another topic live if time allows.

5. **"Below the video you get an AI explanation summary. Same platform, same topic — but now you *see* it."**

---

## Las Vegas / Nevada Angle (30 seconds)

**"Why does this matter in Nevada?"**

- Nevada ranks **48th in education** in the US.
- CCSD is one of the most underfunded school districts in the country.
- Great teachers and great content are uneven. Not every student has access to 3B1B-style explanations.

**"Feynman changes that. Personalized visual learning, on demand. Same quality for every student, regardless of school funding or tutoring budget."**

---

## Tech Stack (20 seconds — only if asked)

- **Frontend:** React + Vite, dark theme
- **Backend:** Node.js + Express
- **Animation:** Manim (same as 3B1B)
- **AI:** Groq + Llama 3 for script and animation code
- **Video:** ffmpeg for stitching
- **Narration:** gTTS / ElevenLabs for text-to-speech

---

## Why We Win (15 seconds)

| ChatGPT | YouTube | Feynman |
|--------|---------|---------|
| Text only | Static videos | **Visual intuition on demand** |
| No animation | Weeks per video | **~2 minutes per video** |
| Formulas first | One-off topics | **Any topic you type** |

---

## Scaling Vision (optional, 15 seconds)

Start with math and CS. Expand to physics, chemistry, biology, economics.  
Sell to CCSD, universities, tutoring platforms, and directly to students.

---

## Closing Line

**"Feynman gives every student what used to take a genius teacher. Instant visual intuition — no matter where they learn."**

---

## Backup Talking Points

- Named after **Richard Feynman** — legendary explainer, Feynman technique, Feynman diagrams.
- 4 calculus scenes + 23 linear algebra scenes built.
- 60+ topic aliases mapped; Groq powers dynamic generation for unknown topics.
- Future: practice problems, key formulas panel, common misconceptions, personalized context (e.g. “emphasize CS connections” or “focus on engineering applications”).

---

## Checklist Before Presenting

- [ ] Backend running (`npm run dev` or equivalent)
- [ ] Frontend running
- [ ] GROQ_API_KEY set
- [ ] Manim installed and working
- [ ] Pre-generate "eigenvalues" video so demo is instant
- [ ] Test audio/video output on presentation machine
