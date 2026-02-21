import { useState, useEffect, useCallback } from "react";

const API = "http://localhost:3001";
const SERIF = "'Noto Serif', Georgia, serif";

const GROUPS = [
  {
    label: "Calculus",
    color: "#58C4DD",
    topics: ["Derivatives", "Integrals", "Limits", "Chain Rule"],
  },
  {
    label: "Linear Algebra",
    color: "#A78BFA",
    topics: [
      "Vectors", "Vector Addition", "Scalar Multiplication", "Dot Product", "Cross Product",
      "Matrix Multiplication", "Linear Transformations", "Rotation Matrices",
      "Shear Transformations", "Projection", "Determinants", "Span",
      "Linear Independence", "Basis Vectors", "Change Of Basis",
      "Eigenvalues And Eigenvectors", "SVD", "Null Space", "Column Space",
      "Row Reduction", "What Matrices Do Geometrically",
      "Why Determinant Zero Means No Inverse", "Why Eigenvectors Matter",
    ],
  },
  {
    label: "Machine Learning",
    color: "#34D399",
    topics: [
      "Neural Networks", "Gradient Descent", "Backpropagation", "Loss Functions",
      "Overfitting And Underfitting", "Activation Functions", "Learning Rate",
      "CNNs", "Attention Mechanism", "Embeddings", "PCA",
    ],
  },
  {
    label: "Algorithms",
    color: "#F59E0B",
    topics: [
      "Bubble Sort", "Quicksort", "Merge Sort", "Binary Search",
      "Depth First Search", "Breadth First Search", "Big O Notation",
      "Recursion", "Dynamic Programming", "Hash Tables", "Dijkstra",
      "Minimum Spanning Tree",
    ],
  },
  {
    label: "Electrodynamics",
    color: "#F472B6",
    topics: [
      "Electric Fields", "Magnetic Fields", "Electromagnetic Induction",
      "Maxwell's Equations", "Wave Propagation",
    ],
  },
  {
    label: "Macroeconomics",
    color: "#60A5FA",
    topics: ["Supply And Demand", "GDP And Growth", "Inflation", "Interest Rates", "Game Theory"],
  },
];

function resetState(setters) {
  setters.forEach(fn => fn());
}

export default function App() {
  const [topic, setTopic]               = useState("");
  const [angle, setAngle]               = useState("");
  const [videoUrl, setVideo]            = useState(null);
  const [narratedUrl, setNarratedUrl]   = useState(null);
  const [useNarrated, setUseNarrated]   = useState(false);
  const [explanation, setExplanation]   = useState(null);
  const [displayTitle, setDisplayTitle] = useState(null);
  const [rawTopic, setRawTopic]         = useState(null);
  const [loading, setLoading]           = useState(false);
  const [error, setError]               = useState(null);

  const [knowledge, setKnowledge]         = useState({ formulas: [], misconceptions: [], summary: "" });
  const [knowledgeTab, setKnowledgeTab]   = useState("formulas");
  const [loadingKnowledge, setLoadingKnowledge] = useState(false);

  const [showAngle, setShowAngle] = useState(false);

  const topicForApi = rawTopic || topic;

  const goHome = useCallback(() => {
    setVideo(null);
    setNarratedUrl(null);
    setUseNarrated(false);
    setExplanation(null);
    setDisplayTitle(null);
    setRawTopic(null);
    setError(null);
    setKnowledge({ formulas: [], misconceptions: [], summary: "" });
    setTopic("");
  }, []);

  const handleGenerate = useCallback(async (t) => {
    const q = t ?? topic;
    if (!q.trim()) return;
    setLoading(true);
    setError(null);
    setVideo(null);
    setNarratedUrl(null);
    setUseNarrated(false);
    setExplanation(null);
    setDisplayTitle(null);
    setRawTopic(null);
    setKnowledge({ formulas: [], misconceptions: [], summary: "" });
    try {
      const res  = await fetch(`${API}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: q, angle: angle.trim() || undefined }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail ?? data.error ?? "Unknown error");
      setVideo(`${API}${data.videoUrl}`);
      if (data.narratedVideoUrl) {
        setNarratedUrl(`${API}${data.narratedVideoUrl}`);
        setUseNarrated(true);
      }
      setExplanation(data.explanation);
      setDisplayTitle(data.displayTitle ?? q);
      setRawTopic(data.topic ?? q);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [topic, angle]);

  useEffect(() => {
    if (!videoUrl || !topicForApi) return;
    setLoadingKnowledge(true);
    fetch(`${API}/api/knowledge`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: topicForApi, angle: angle.trim() || undefined }),
    })
      .then(r => r.json())
      .then(k => setKnowledge({ formulas: k.formulas || [], misconceptions: k.misconceptions || [], summary: k.summary || "" }))
      .catch(() => {})
      .finally(() => setLoadingKnowledge(false));
  }, [videoUrl, topicForApi, angle]);

  return (
    <div style={s.root}>
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <header style={s.header}>
        <h1 style={s.logo} onClick={goHome} title="Back to home">Feynman</h1>
        <p style={s.tagline}>Visual explanations of anything, instantly</p>

        <div style={s.searchWrap}>
          <input
            style={s.searchInput}
            placeholder="What do you want to understand today?"
            value={topic}
            onChange={e => setTopic(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleGenerate()}
          />
          <button
            style={{ ...s.searchBtn, opacity: loading || !topic.trim() ? 0.45 : 1 }}
            onClick={() => handleGenerate()}
            disabled={loading || !topic.trim()}
          >
            {loading ? "Thinking…" : "Explain"}
          </button>
        </div>

        <div style={s.angleRow}>
          <button style={s.angleToggle} onClick={() => setShowAngle(v => !v)}>
            {showAngle ? "▲ Hide" : "▼ Personalize angle"}
          </button>
          {showAngle && (
            <input
              style={s.angleInput}
              placeholder="e.g. emphasize CS applications, connect to ML, focus on engineering"
              value={angle}
              onChange={e => setAngle(e.target.value)}
            />
          )}
        </div>

        {loading && <p style={s.hint}>Generating animation — this takes ~5 s for pre-built topics…</p>}
        {error   && <p style={s.errTxt}>{error}</p>}
      </header>

      {/* ── Video result ───────────────────────────────────────────────── */}
      {videoUrl && (
        <section style={s.resultSection}>
          <div style={s.videoCol}>
            <video
              key={useNarrated && narratedUrl ? narratedUrl : videoUrl}
              src={useNarrated && narratedUrl ? narratedUrl : videoUrl}
              controls
              autoPlay
              style={s.video}
            />
            <div style={s.videoMeta}>
              <p style={s.videoTitle}>{displayTitle}</p>
              {narratedUrl && (
                <button
                  style={{ ...s.narrBtn, background: useNarrated ? "#58C4DD" : "#1E1E2E", color: useNarrated ? "#0A0A0F" : "#6E6E8A" }}
                  onClick={() => setUseNarrated(v => !v)}
                >
                  {useNarrated ? "🔊 Narrated" : "🔇 Silent"}
                </button>
              )}
            </div>
            {explanation && (
              <div style={s.explCard}>
                <p style={s.explText}>{explanation}</p>
              </div>
            )}
          </div>

          <aside style={s.knowledgePanel}>
            <div style={s.tabs}>
              {["formulas", "misconceptions", "summary"].map(t => (
                <button key={t} style={{ ...s.tab, ...(knowledgeTab === t ? s.tabActive : {}) }} onClick={() => setKnowledgeTab(t)}>
                  {t === "formulas" ? "Key Formulas" : t === "misconceptions" ? "Misconceptions" : "Summary"}
                </button>
              ))}
            </div>
            <div style={s.tabContent}>
              {loadingKnowledge ? (
                <div style={s.skeletonList}>
                  {[1, 2, 3].map(i => (
                    <div key={i} style={s.skeletonCard}>
                      <div style={s.skeletonLine} />
                      <div style={{ ...s.skeletonLine, width: "65%", marginTop: 8 }} />
                    </div>
                  ))}
                </div>
              ) : (
                <>
                  {knowledgeTab === "formulas" && (
                    <div style={s.formulaList}>
                      {knowledge.formulas.map((f, i) => (
                        <div key={i} style={s.formulaCard}>
                          <span style={s.formulaText}>{f.formula}</span>
                          <span style={s.formulaMeaning}>{f.meaning}</span>
                          <button style={s.copyBtn} onClick={() => navigator.clipboard?.writeText(f.formula + " — " + (f.meaning || ""))}>Copy</button>
                        </div>
                      ))}
                    </div>
                  )}
                  {knowledgeTab === "misconceptions" && (
                    <div style={s.misconList}>
                      {knowledge.misconceptions.map((m, i) => (
                        <div key={i} style={s.misconCard}>
                          <span style={s.misconWrong}>✗ {m.wrong}</span>
                          <span style={s.misconRight}>✓ {m.correct}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  {knowledgeTab === "summary" && <p style={s.summaryText}>{knowledge.summary}</p>}
                </>
              )}
            </div>
          </aside>
        </section>
      )}

      {/* ── Topic chips ────────────────────────────────────────────────── */}
      {!videoUrl && !loading && (
        <main style={s.topicsMain}>
          {GROUPS.map(g => (
            <div key={g.label} style={s.group}>
              <h2 style={{ ...s.groupLabel, color: g.color }}>{g.label}</h2>
              <div style={s.chips}>
                {g.topics.map(t => (
                  <button
                    key={t}
                    style={{ ...s.chip, borderColor: g.color + "55", color: g.color }}
                    onClick={() => { setTopic(t); handleGenerate(t); }}
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </main>
      )}

      {/* ── Footer quote ───────────────────────────────────────────────── */}
      <footer style={s.footer}>
        <p style={s.quote}>
          &ldquo;If you cannot explain something simply, you do not understand it yet.&rdquo;
        </p>
        <p style={s.quoteBy}>— Richard Feynman</p>
      </footer>
    </div>
  );
}

const s = {
  root: { fontFamily: SERIF, background: "#0A0A0F", minHeight: "100vh", color: "#E8E8F0", display: "flex", flexDirection: "column", alignItems: "center" },
  header: { width: "100%", maxWidth: 720, textAlign: "center", padding: "56px 24px 32px" },
  logo: { fontFamily: SERIF, fontSize: 56, fontWeight: 700, margin: "0 0 8px", letterSpacing: -1, color: "#E8E8F0", cursor: "pointer", display: "inline-block" },
  tagline: { fontFamily: SERIF, fontSize: 16, color: "#6E6E8A", margin: "0 0 36px", fontStyle: "italic" },
  searchWrap: { display: "flex", gap: 10, width: "100%" },
  searchInput: { flex: 1, fontFamily: SERIF, fontSize: 17, padding: "14px 20px", background: "#13131F", border: "1px solid #1E1E2E", borderRadius: 10, color: "#E8E8F0", outline: "none" },
  searchBtn: { fontFamily: SERIF, fontSize: 16, fontWeight: 700, padding: "14px 28px", background: "#58C4DD", color: "#0A0A0F", border: "none", borderRadius: 10, cursor: "pointer", whiteSpace: "nowrap" },
  angleRow: { marginTop: 12, display: "flex", flexDirection: "column", alignItems: "center", gap: 8 },
  angleToggle: { fontFamily: SERIF, fontSize: 13, background: "none", border: "none", color: "#6E6E8A", cursor: "pointer", padding: 0 },
  angleInput: { width: "100%", fontFamily: SERIF, fontSize: 14, padding: "10px 16px", background: "#13131F", border: "1px solid #1E1E2E", borderRadius: 8, color: "#E8E8F0", outline: "none" },
  hint: { fontFamily: SERIF, color: "#6E6E8A", fontSize: 14, margin: "12px 0 0" },
  errTxt: { fontFamily: SERIF, color: "#F472B6", marginTop: 10, fontSize: 14 },
  resultSection: { display: "flex", gap: 24, width: "100%", maxWidth: 1200, padding: "0 24px 40px", flexWrap: "wrap" },
  videoCol: { flex: 1, minWidth: 400 },
  video: { width: "100%", borderRadius: 12, boxShadow: "0 8px 48px rgba(0,0,0,0.7)" },
  videoMeta: { display: "flex", alignItems: "center", gap: 12, marginTop: 10, flexWrap: "wrap" },
  videoTitle: { fontFamily: SERIF, margin: 0, fontSize: 18, color: "#E8E8F0", flex: 1, fontStyle: "italic" },
  narrBtn: { fontFamily: SERIF, fontSize: 13, fontWeight: 600, padding: "5px 14px", border: "none", borderRadius: 20, cursor: "pointer" },
  explCard: { marginTop: 16, background: "#0F0F1A", borderRadius: 10, padding: "16px 20px", borderLeft: "3px solid #58C4DD" },
  explText: { fontFamily: SERIF, margin: 0, color: "#B8B8CC", lineHeight: 1.7, fontSize: 15 },
  knowledgePanel: { width: 320, minWidth: 280, background: "#0F0F1A", borderRadius: 12, overflow: "hidden", border: "1px solid #1E1E2E", alignSelf: "flex-start" },
  tabs: { display: "flex", borderBottom: "1px solid #1E1E2E" },
  tab: { flex: 1, fontFamily: SERIF, padding: "11px 8px", background: "transparent", border: "none", color: "#6E6E8A", cursor: "pointer", fontSize: 12, fontWeight: 600 },
  tabActive: { background: "#13131F", color: "#E8E8F0" },
  tabContent: { padding: 16, maxHeight: 460, overflowY: "auto" },
  formulaList: { display: "flex", flexDirection: "column", gap: 12 },
  formulaCard: { background: "#13131F", padding: 12, borderRadius: 8, borderLeft: "3px solid #58C4DD" },
  formulaText: { fontFamily: SERIF, display: "block", color: "#E8E8F0", fontWeight: 600, fontSize: 14 },
  formulaMeaning: { fontFamily: SERIF, display: "block", fontSize: 13, color: "#6E6E8A", marginTop: 4 },
  copyBtn: { fontFamily: SERIF, marginTop: 8, padding: "4px 10px", fontSize: 11, background: "#1E1E2E", color: "#6E6E8A", border: "none", borderRadius: 4, cursor: "pointer" },
  misconList: { display: "flex", flexDirection: "column", gap: 12 },
  misconCard: { background: "#13131F", padding: 12, borderRadius: 8 },
  misconWrong: { fontFamily: SERIF, display: "block", color: "#F472B6", fontSize: 13 },
  misconRight: { fontFamily: SERIF, display: "block", color: "#34D399", marginTop: 6, fontSize: 13 },
  summaryText: { fontFamily: SERIF, color: "#B8B8CC", lineHeight: 1.7, fontSize: 14, whiteSpace: "pre-wrap" },
  topicsMain: { width: "100%", maxWidth: 900, padding: "0 24px 48px", display: "flex", flexDirection: "column", gap: 28 },
  group: {},
  groupLabel: { fontFamily: SERIF, fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1.5, margin: "0 0 10px" },
  chips: { display: "flex", gap: 8, flexWrap: "wrap" },
  chip: { fontFamily: SERIF, padding: "6px 14px", borderRadius: 20, background: "#0F0F1A", border: "1px solid", cursor: "pointer", fontSize: 13, fontWeight: 400 },
  skeletonList: { display: "flex", flexDirection: "column", gap: 12 },
  skeletonCard: { background: "#13131F", padding: 12, borderRadius: 8, borderLeft: "3px solid #1E1E2E" },
  skeletonLine: { height: 11, background: "#1E1E2E", borderRadius: 3, width: "100%" },
  footer: { width: "100%", textAlign: "center", padding: "32px 24px 40px", borderTop: "1px solid #1E1E2E", marginTop: "auto" },
  quote: { fontFamily: SERIF, fontStyle: "italic", fontSize: 16, color: "#6E6E8A", margin: "0 0 8px" },
  quoteBy: { fontFamily: SERIF, fontSize: 14, color: "#3A3A5C", margin: 0 },
};
