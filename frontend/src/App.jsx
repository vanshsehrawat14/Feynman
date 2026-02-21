import { useState, useEffect, useCallback } from "react";

const API = "http://localhost:3001";

const FEYNMAN_PHOTO = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Feynman-richard_p.jpg";

const GROUPS = [
  {
    label: "Calculus",
    cat: "calculus",
    color: "#4a90c4",
    topics: ["Derivatives", "Integrals", "Limits", "Chain Rule"],
  },
  {
    label: "Linear Algebra",
    cat: "linalg",
    color: "#7c6fa0",
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
    cat: "ml",
    color: "#3a8c6e",
    topics: [
      "Neural Networks", "Gradient Descent", "Backpropagation", "Loss Functions",
      "Overfitting And Underfitting", "Activation Functions", "Learning Rate",
      "CNNs", "Attention Mechanism", "Embeddings", "PCA",
    ],
  },
  {
    label: "Algorithms",
    cat: "algo",
    color: "#b8860b",
    topics: [
      "Bubble Sort", "Quicksort", "Merge Sort", "Binary Search",
      "Depth First Search", "Breadth First Search", "Big O Notation",
      "Recursion", "Dynamic Programming", "Hash Tables", "Dijkstra",
      "Minimum Spanning Tree",
    ],
  },
  {
    label: "Electrodynamics",
    cat: "electro",
    color: "#8b3a3a",
    topics: [
      "Electric Fields", "Magnetic Fields", "Electromagnetic Induction",
      "Maxwell's Equations", "Wave Propagation",
    ],
  },
  {
    label: "Macroeconomics",
    cat: "macro",
    color: "#4a6fa0",
    topics: ["Supply And Demand", "GDP And Growth", "Inflation", "Interest Rates", "Game Theory"],
  },
];

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
  const [photoError, setPhotoError] = useState(false);

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

  const tabLabels = { formulas: "Key Formulas", misconceptions: "Misconceptions", summary: "Summary" };

  return (
    <div className="app">
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <header className="site-header">
        <div className="logo-row" onClick={goHome} title="Back to home">
          {!photoError ? (
            <img
              className="logo-avatar"
              src={FEYNMAN_PHOTO}
              alt="Richard Feynman"
              onError={() => setPhotoError(true)}
            />
          ) : (
            <div className="logo-avatar-fallback" style={{ display: "flex" }}>
              <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <circle cx="24" cy="24" r="23" fill="#1a1a24" stroke="#58c4dd" strokeWidth="2" />
                <text x="24" y="31" textAnchor="middle" fill="#e8e8f0" fontFamily="'CMU Serif','Lora','Georgia',serif" fontSize="24" fontWeight="400">F</text>
              </svg>
            </div>
          )}
          <span className="logo-title">Feynman</span>
        </div>

        <p className="tagline">Mathematics and sciences with a distinct visual perspective</p>

        <div className="search-wrap">
          <input
            className="search-input"
            placeholder="What do you want to understand?"
            value={topic}
            onChange={e => setTopic(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleGenerate()}
          />
          <button
            className="search-btn"
            onClick={() => handleGenerate()}
            disabled={loading || !topic.trim()}
          >
            Generate
          </button>
        </div>

        <div className="angle-row">
          <button className="angle-toggle" onClick={() => setShowAngle(v => !v)}>
            {showAngle ? "▲ Hide" : "▼ Personalize angle"}
          </button>
          {showAngle && (
            <input
              className="angle-input"
              placeholder="e.g. emphasize CS applications, connect to ML, focus on engineering"
              value={angle}
              onChange={e => setAngle(e.target.value)}
            />
          )}
        </div>

        {loading && (
          <div className="loading-state">
            <div className="spinner" />
            <p className="loading-text">Generating your explanation...</p>
          </div>
        )}
        {error && <p className="error-text">{error}</p>}
      </header>

      {/* ── Video result ───────────────────────────────────────────────── */}
      {videoUrl && (
        <section className="result-section">
          <div className="video-col">
            <video
              className="video-player"
              key={useNarrated && narratedUrl ? narratedUrl : videoUrl}
              src={useNarrated && narratedUrl ? narratedUrl : videoUrl}
              controls
              autoPlay
            />
            <p className="video-title-text">{displayTitle}</p>
            <div className="video-meta-row">
              {narratedUrl && (
                <button
                  className="narr-btn"
                  style={{
                    background: useNarrated ? "#58c4dd" : "#1a1a24",
                    color: useNarrated ? "#0d0d12" : "#8888a8",
                  }}
                  onClick={() => setUseNarrated(v => !v)}
                >
                  {useNarrated ? "🔊 Narrated" : "🔇 Silent"}
                </button>
              )}
            </div>
            <div className="video-divider" />
            {explanation && (
              <div className="expl-card">
                <p className="expl-text">{explanation}</p>
              </div>
            )}
          </div>

          <aside className="knowledge-panel">
            <div className="k-tabs">
              {["formulas", "misconceptions", "summary"].map(t => (
                <button
                  key={t}
                  className={`k-tab${knowledgeTab === t ? " active" : ""}`}
                  onClick={() => setKnowledgeTab(t)}
                >
                  {tabLabels[t]}
                </button>
              ))}
            </div>
            <div className="k-tab-content">
              {loadingKnowledge ? (
                <div className="skel-list">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="skel-card">
                      <div className="skel-line" />
                      <div className="skel-line" style={{ width: "65%", marginTop: 8 }} />
                    </div>
                  ))}
                </div>
              ) : (
                <>
                  {knowledgeTab === "formulas" && (
                    <div className="formula-list">
                      {knowledge.formulas.map((f, i) => (
                        <div key={i} className="formula-card">
                          <span className="formula-text">{f.formula}</span>
                          <span className="formula-meaning">{f.meaning}</span>
                          <button className="copy-btn" onClick={() => navigator.clipboard?.writeText(f.formula + " — " + (f.meaning || ""))}>Copy</button>
                        </div>
                      ))}
                    </div>
                  )}
                  {knowledgeTab === "misconceptions" && (
                    <div className="miscon-list">
                      {knowledge.misconceptions.map((m, i) => (
                        <div key={i} className="miscon-card">
                          <span className="miscon-wrong">✗ {m.wrong}</span>
                          <span className="miscon-right">✓ {m.correct}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  {knowledgeTab === "summary" && <p className="summary-text">{knowledge.summary}</p>}
                </>
              )}
            </div>
          </aside>
        </section>
      )}

      {/* ── Divider + Topic chips ──────────────────────────────────────── */}
      {!videoUrl && !loading && (
        <>
          <div className="divider-row">
            <div className="divider-line" />
            <span className="divider-label">or explore a topic</span>
            <div className="divider-line" />
          </div>

          <main className="topics-main">
            {GROUPS.map(g => (
              <div key={g.label}>
                <h2 className="group-label" style={{ color: g.color }}>{g.label}</h2>
                <div className="chips-row">
                  {g.topics.map(t => (
                    <button
                      key={t}
                      className="chip"
                      data-cat={g.cat}
                      onClick={() => { setTopic(t); handleGenerate(t); }}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </main>
        </>
      )}

      {/* ── Footer quote ───────────────────────────────────────────────── */}
      <footer className="site-footer">
        <p className="footer-quote">
          &ldquo;If you cannot explain something simply, you do not understand it yet.&rdquo;
        </p>
        <p className="footer-by">— Richard Feynman</p>
      </footer>
    </div>
  );
}
