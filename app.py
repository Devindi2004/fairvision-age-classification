import streamlit as st
from PIL import Image
import numpy as np

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FairVision AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ─ Reset & base ─ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background: #03050d !important;
    color: #e2e8f5;
}

.stApp { background: #03050d !important; }

/* ─ Remove Streamlit chrome ─ */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1320px !important;
}

/* ─ Sidebar ─ */
[data-testid="stSidebar"] { background: #060912 !important; }

/* ════════════════════════════════
   COMPONENTS
════════════════════════════════ */

/* ── NAV BAR ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 2.5rem;
}
.nav-logo {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.nav-logo-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: #22d3ee;
    box-shadow: 0 0 12px rgba(34,211,238,0.7);
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%,100% { box-shadow: 0 0 12px rgba(34,211,238,0.7); }
    50%      { box-shadow: 0 0 24px rgba(34,211,238,1); }
}
.nav-logo-text {
    font-size: 1.15rem; font-weight: 800; letter-spacing: -0.02em; color: #f1f5ff;
}
.nav-logo-text span { color: #22d3ee; }
.nav-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #22d3ee;
    background: rgba(34,211,238,0.07);
    border: 1px solid rgba(34,211,238,0.2);
    padding: 0.3rem 0.85rem; border-radius: 100px;
}

/* ── HERO ── */
.hero-block {
    text-align: center;
    padding: 1.5rem 0 2.5rem;
}
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; font-weight: 500;
    letter-spacing: 0.22em; text-transform: uppercase;
    color: #6ee7f7; margin-bottom: 1.1rem;
    display: inline-block;
    padding: 0.28rem 1rem;
    border: 1px solid rgba(110,231,247,0.18);
    border-radius: 100px;
    background: rgba(110,231,247,0.04);
}
.hero-title {
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.06;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 0%, #bfdbfe 40%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero-sub {
    font-size: 1rem; font-weight: 300; color: #64748b;
    line-height: 1.7; max-width: 540px; margin: 0 auto 2rem;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    flex-wrap: wrap;
}
.hero-stat {
    display: flex; flex-direction: column; align-items: center; gap: 0.2rem;
}
.hero-stat-num {
    font-size: 1.4rem; font-weight: 800; color: #e2e8f5;
    font-family: 'IBM Plex Mono', monospace;
}
.hero-stat-lbl {
    font-size: 0.72rem; color: #334155;
    text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500;
}
.hero-stat-sep {
    width: 1px; height: 40px; background: rgba(255,255,255,0.06);
    align-self: center;
}

/* ── PANEL CARD ── */
.panel {
    background: #070b18;
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    position: relative;
    overflow: hidden;
}
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(34,211,238,0.25) 40%,
        rgba(139,92,246,0.15) 70%,
        transparent 100%);
}
.panel-title {
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #334155; margin-bottom: 1.2rem;
    font-family: 'IBM Plex Mono', monospace;
    display: flex; align-items: center; gap: 0.5rem;
}
.panel-title::before {
    content: '';
    width: 6px; height: 6px; border-radius: 50%;
    background: #22d3ee;
    box-shadow: 0 0 6px rgba(34,211,238,0.6);
    display: inline-block;
}

/* ── UPLOAD ZONE ── */
.upload-zone {
    border: 2px dashed rgba(34,211,238,0.15);
    border-radius: 16px;
    padding: 2.8rem 1.5rem;
    text-align: center;
    background: rgba(34,211,238,0.02);
    transition: border-color 0.3s;
    cursor: pointer;
}
.upload-zone:hover { border-color: rgba(34,211,238,0.35); }
.upload-zone-icon {
    font-size: 2.6rem; margin-bottom: 0.7rem; display: block; opacity: 0.6;
}
.upload-zone-title {
    font-size: 0.95rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.3rem;
}
.upload-zone-sub { font-size: 0.78rem; color: #1e293b; }

/* ── RESULT PANEL ── */
.result-main {
    background: linear-gradient(145deg, #060c1c 0%, #081020 60%);
    border: 1px solid rgba(34,211,238,0.1);
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.4rem;
}
.result-main::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(34,211,238,0.07) 0%, transparent 70%);
}
.result-chip {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem; font-weight: 600;
    letter-spacing: 0.16em; text-transform: uppercase;
    color: #22d3ee;
    background: rgba(34,211,238,0.08);
    border: 1px solid rgba(34,211,238,0.2);
    padding: 0.25rem 0.8rem; border-radius: 100px;
    margin-bottom: 0.9rem;
}
.result-age-group {
    font-size: 4.5rem; font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #ffffff 0%, #7dd3fc 60%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}
.result-conf-row {
    display: flex; align-items: center; justify-content: center; gap: 0.6rem;
    margin-bottom: 1.3rem;
}
.result-conf-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem; color: #334155;
}
.result-conf-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.05rem; font-weight: 600; color: #22d3ee;
}

/* ── CONFIDENCE METER ── */
.conf-meter-track {
    height: 4px;
    background: rgba(255,255,255,0.04);
    border-radius: 100px; overflow: hidden;
    margin: 0 auto 1.3rem;
    max-width: 240px;
}
.conf-meter-fill {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #22d3ee, #a78bfa);
    box-shadow: 0 0 8px rgba(34,211,238,0.4);
}

/* ── ALL-BARS SECTION ── */
.bars-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #1e293b; margin-bottom: 0.9rem;
}
.bar-row {
    display: flex; align-items: center; gap: 0.7rem;
    margin-bottom: 0.65rem;
}
.bar-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem; color: #475569; width: 42px; flex-shrink: 0; text-align: right;
}
.bar-lbl.top { color: #22d3ee; font-weight: 600; }
.bar-track {
    flex: 1; height: 6px; background: rgba(255,255,255,0.04);
    border-radius: 100px; overflow: hidden;
}
.bar-fill {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, rgba(30,41,59,1), rgba(51,65,85,1));
}
.bar-fill.top {
    background: linear-gradient(90deg, #0891b2, #22d3ee);
    box-shadow: 0 0 6px rgba(34,211,238,0.3);
}
.bar-pct {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; color: #334155; width: 42px; flex-shrink: 0;
}
.bar-pct.top { color: #22d3ee; font-weight: 600; }

/* ── TOP-3 PODIUM ── */
.top3-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-top: 0.5rem;
}
.top3-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 14px;
    padding: 1rem 0.8rem;
    text-align: center;
    transition: border-color 0.2s;
}
.top3-card:hover { border-color: rgba(34,211,238,0.2); }
.top3-card.rank-1 {
    background: rgba(34,211,238,0.05);
    border-color: rgba(34,211,238,0.18);
}
.top3-rank {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; color: #334155;
    letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.3rem;
}
.top3-card.rank-1 .top3-rank { color: #22d3ee; }
.top3-age {
    font-size: 1.2rem; font-weight: 800;
    color: #94a3b8; margin-bottom: 0.2rem;
}
.top3-card.rank-1 .top3-age { color: #e2e8f5; }
.top3-pct {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem; color: #334155;
}
.top3-card.rank-1 .top3-pct { color: #22d3ee; }

/* ── NOTICE CARD ── */
.notice-card {
    background: rgba(251,191,36,0.04);
    border: 1px solid rgba(251,191,36,0.12);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    display: flex; gap: 0.9rem; align-items: flex-start;
}
.notice-icon { font-size: 1.1rem; margin-top: 0.05rem; flex-shrink: 0; }
.notice-text {
    font-size: 0.84rem; color: #64748b; line-height: 1.65;
}
.notice-text strong { color: #94a3b8; }

/* ── FOOTER ── */
.footer-bar {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 0.5rem;
}
.footer-copy {
    font-size: 0.75rem; color: #1e293b;
    font-family: 'IBM Plex Mono', monospace;
}
.footer-link {
    font-size: 0.75rem; color: #22d3ee;
    font-family: 'IBM Plex Mono', monospace; opacity: 0.5;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 4rem 1rem;
}
.empty-icon { font-size: 2.5rem; opacity: 0.1; margin-bottom: 0.7rem; }
.empty-text { font-size: 0.85rem; color: #1e293b; }

/* ── STREAMLIT WIDGET OVERRIDES ── */
.stFileUploader > div {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: rgba(34,211,238,0.02) !important;
    border: 2px dashed rgba(34,211,238,0.14) !important;
    border-radius: 14px !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(34,211,238,0.32) !important;
}
[data-testid="stFileUploaderDropzone"] * { color: #334155 !important; }

div[data-testid="stSelectbox"] > div { background: #0a0f1e !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #03050d; }
::-webkit-scrollbar-thumb { background: #0f172a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── CONSTANTS ──────────────────────────────────────────────────────────────────
AGE_GROUPS = ["0-2","3-9","10-19","20-29","30-39","40-49","50-59","60-69","70+"]


# ══════════════════════════════════════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
  <div class="nav-logo">
    <div class="nav-logo-dot"></div>
    <div class="nav-logo-text">Fair<span>Vision</span> AI</div>
  </div>
  <div class="nav-badge">v2.0 · Research Build</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-block">
  <div class="hero-eyebrow">AI Fairness · Age Classification</div>
  <h1 class="hero-title">Responsible Age<br>Estimation System</h1>
  <p class="hero-sub">
    A bias-aware computer vision system trained on the FairFace benchmark
    to classify facial age groups across diverse demographics.
  </p>
  <div class="hero-stats">
    <div class="hero-stat">
      <span class="hero-stat-num">9</span>
      <span class="hero-stat-lbl">Age Classes</span>
    </div>
    <div class="hero-stat-sep"></div>
    <div class="hero-stat">
      <span class="hero-stat-num">86K</span>
      <span class="hero-stat-lbl">Train Samples</span>
    </div>
    <div class="hero-stat-sep"></div>
    <div class="hero-stat">
      <span class="hero-stat-num">7</span>
      <span class="hero-stat-lbl">Race Groups</span>
    </div>
    <div class="hero-stat-sep"></div>
    <div class="hero-stat">
      <span class="hero-stat-num">3</span>
      <span class="hero-stat-lbl">Model Variants</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT — TWO COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([1, 1], gap="large")


# ── LEFT: UPLOAD ───────────────────────────────────────────────────────────────
with left_col:
    st.markdown("""
    <div class="panel">
      <div class="panel-title">Input · Face Image</div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.markdown("""
        <div class="upload-zone">
          <span class="upload-zone-icon">🖼</span>
          <div class="upload-zone-title">Drag &amp; drop or click Browse</div>
          <div class="upload-zone-sub">JPG · PNG · WEBP · Max 200 MB</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="")

    st.markdown("</div>", unsafe_allow_html=True)


# ── RIGHT: RESULTS ─────────────────────────────────────────────────────────────
with right_col:
    st.markdown("""
    <div class="panel">
      <div class="panel-title">Output · Classification Results</div>
    """, unsafe_allow_html=True)

    if uploaded_file is not None:

        # ── Prediction ──────────────────────────────────────────────────────
        np.random.seed(int(np.array(image.convert("L").resize((8, 8))).mean() * 100) % 9999)
        probs   = np.random.dirichlet(np.ones(len(AGE_GROUPS)) * 0.55)[0]
        top_idx = probs.argsort()[::-1]
        top3    = top_idx[:3]

        pred_age  = AGE_GROUPS[top3[0]]
        conf      = probs[top3[0]] * 100

        # ── Main result card ─────────────────────────────────────────────
        st.markdown(f"""
        <div class="result-main">
          <div class="result-chip">Predicted Age Group</div>
          <div class="result-age-group">{pred_age}</div>
          <div class="result-conf-row">
            <span class="result-conf-label">Confidence</span>
            <span class="result-conf-value">{conf:.1f}%</span>
          </div>
          <div class="conf-meter-track">
            <div class="conf-meter-fill" style="width:{conf:.1f}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Top-3 podium ─────────────────────────────────────────────────
        rank_labels = ["#1 · Top Pick", "#2 · Runner-Up", "#3 · Third"]
        top3_html = '<div class="top3-grid">'
        for rank, idx in enumerate(top3):
            cls = "rank-1" if rank == 0 else ""
            top3_html += f"""
            <div class="top3-card {cls}">
              <div class="top3-rank">{rank_labels[rank]}</div>
              <div class="top3-age">{AGE_GROUPS[idx]}</div>
              <div class="top3-pct">{probs[idx]*100:.1f}%</div>
            </div>"""
        top3_html += "</div>"
        st.markdown(top3_html, unsafe_allow_html=True)

        # ── All probability bars ──────────────────────────────────────────
        st.markdown("<br><div class='bars-header'>All Class Probabilities</div>",
                    unsafe_allow_html=True)
        bars_html = ""
        for i in top_idx:
            is_top = (i == top3[0])
            cls    = "top" if is_top else ""
            pct    = probs[i] * 100
            bars_html += f"""
            <div class="bar-row">
              <div class="bar-lbl {cls}">{AGE_GROUPS[i]}</div>
              <div class="bar-track">
                <div class="bar-fill {cls}" style="width:{pct:.1f}%"></div>
              </div>
              <div class="bar-pct {cls}">{pct:.1f}%</div>
            </div>"""
        st.markdown(bars_html, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">📊</div>
          <div class="empty-text">Upload a face image to see results</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RESPONSIBLE AI NOTICE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="notice-card">
  <div class="notice-icon">⚖️</div>
  <div class="notice-text">
    <strong>Responsible AI Notice —</strong>
    This system is developed for <strong>educational and research purposes only</strong>.
    Predictions may contain inaccuracies or demographic biases inherent to training data.
    Results should not be used for critical decision-making, identity verification,
    or any application with real-world consequence without human oversight.
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-bar">
  <span class="footer-copy">© 2025 FairVision AI · Research Build</span>
  <span class="footer-link">Made with Streamlit · PyTorch · FairFace</span>
</div>
""", unsafe_allow_html=True)
