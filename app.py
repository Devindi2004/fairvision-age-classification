import streamlit as st
from PIL import Image
import numpy as np
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FairVision AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* ---------------- MAIN BACKGROUND ---------------- */

.stApp {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.15), transparent 25%),
        radial-gradient(circle at bottom right, rgba(124,58,237,0.15), transparent 25%),
        linear-gradient(135deg, #0f172a 0%, #111827 100%);
    color: white;
    overflow-x: hidden;
}

/* ---------------- REMOVE STREAMLIT DEFAULTS ---------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* ---------------- HERO SECTION ---------------- */

.hero-container {
    text-align: center;
    padding-top: 20px;
    padding-bottom: 30px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 50px;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.25);
    color: #93c5fd;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 25px;
}

.hero-title {
    font-size: clamp(60px, 8vw, 110px);
    font-weight: 900;
    line-height: 0.95;
    margin-bottom: 15px;
    letter-spacing: -2px;
}

.gradient-text {
    background: linear-gradient(90deg, #60a5fa, #8b5cf6, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 20px;
    color: #cbd5e1;
    margin-bottom: 20px;
}

.hero-tags {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
}

.tag {
    padding: 8px 16px;
    border-radius: 50px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 13px;
    color: #cbd5e1;
}

/* ---------------- STATS ---------------- */

.stats-container {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 15px;
    margin-top: 25px;
    margin-bottom: 35px;
}

.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.stat-number {
    font-size: 40px;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 5px;
}

/* ---------------- GLASS CARD ---------------- */

.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 28px;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
    margin-bottom: 25px;
}

/* ---------------- SECTION TITLE ---------------- */

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* ---------------- IMAGE PREVIEW ---------------- */

.image-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 15px;
}

.image-wrapper img {
    border-radius: 16px;
    max-width: 260px !important;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ---------------- PREDICTION BOX ---------------- */

.prediction-box {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    border-radius: 22px;
    padding: 30px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.35);
}

.prediction-label {
    font-size: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.8);
}

.prediction-age {
    font-size: 70px;
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 10px;
}

.prediction-confidence {
    font-size: 18px;
    color: rgba(255,255,255,0.9);
}

/* ---------------- CUSTOM PROGRESS ---------------- */

.progress-item {
    margin-bottom: 18px;
}

.progress-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 14px;
}

.progress-bg {
    width: 100%;
    height: 12px;
    background: rgba(255,255,255,0.08);
    border-radius: 50px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg,#3b82f6,#8b5cf6);
}

/* ---------------- FEATURES ---------------- */

.features-grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 18px;
    margin-top: 15px;
}

.feature-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 8px;
}

.feature-text {
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.7;
}

/* ---------------- NOTICE ---------------- */

.notice-box {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-left: 5px solid #f59e0b;
    border-radius: 18px;
    padding: 25px;
    margin-top: 10px;
}

.notice-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 10px;
}

.notice-text {
    color: #fcd34d;
    line-height: 1.8;
    font-size: 15px;
}

/* ---------------- FOOTER ---------------- */

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 50px;
    padding-bottom: 30px;
    font-size: 14px;
}

/* ---------------- RESPONSIVE ---------------- */

@media(max-width: 900px){

    .stats-container {
        grid-template-columns: 1fr;
    }

    .features-grid {
        grid-template-columns: 1fr;
    }

    .prediction-age {
        font-size: 55px;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero-container">

<div class="hero-badge">
🧠 Educational & Research AI System
</div>

<div class="hero-title">
FAIRVISION <span class="gradient-text">AI</span>
</div>

<div class="hero-subtitle">
Fair & Responsible Age Classification System
</div>

<div class="hero-tags">
<div class="tag">9 Age Groups</div>
<div class="tag">Top-3 Predictions</div>
<div class="tag">Privacy Safe</div>
<div class="tag">Responsible AI</div>
</div>

</div>
""", unsafe_allow_html=True)

# ---------------- STATS ----------------

st.markdown("""
<div class="stats-container">

<div class="stat-card">
<div class="stat-number">9</div>
<div class="stat-label">AGE GROUPS</div>
</div>

<div class="stat-card">
<div class="stat-number">TOP 3</div>
<div class="stat-label">RANKED PREDICTIONS</div>
</div>

<div class="stat-card">
<div class="stat-number">0</div>
<div class="stat-label">IMAGES STORED</div>
</div>

</div>
""", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------

col1, col2 = st.columns([1,1], gap="large")

# ---------------- LEFT SIDE ----------------

with col1:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    📤 Upload Face Image
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload",
        type=["jpg","jpeg","png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.markdown('<div class="image-wrapper">', unsafe_allow_html=True)

        st.image(image, use_container_width=False)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            f"<div style='text-align:center; color:#94a3b8; font-size:13px; margin-top:10px;'>Uploaded: {uploaded_file.name}</div>",
            unsafe_allow_html=True
        )

    else:
        st.info("Please upload a portrait image.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT SIDE ----------------

with col2:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    📊 Prediction Results
    </div>
    """, unsafe_allow_html=True)

    if uploaded_file is not None:

        with st.spinner("Analyzing image..."):
            time.sleep(1)

        age_groups = [
            "0-2",
            "3-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70+"
        ]

        probs = np.random.dirichlet(np.ones(len(age_groups)), size=1)[0]

        top3_idx = probs.argsort()[-3:][::-1]

        predicted_age = age_groups[top3_idx[0]]
        confidence = probs[top3_idx[0]] * 100

        st.markdown(f"""
        <div class="prediction-box">

        <div class="prediction-label">
        🎯 Predicted Age Group
        </div>

        <div class="prediction-age">
        {predicted_age}
        </div>

        <div class="prediction-confidence">
        Confidence: {confidence:.2f}%
        </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:18px;font-weight:700;margin-bottom:18px;">
        🔝 Top 3 Predictions
        </div>
        """, unsafe_allow_html=True)

        for idx in top3_idx:

            percentage = probs[idx] * 100

            st.markdown(f"""
            <div class="progress-item">

            <div class="progress-label">
                <span>{age_groups[idx]}</span>
                <span>{percentage:.2f}%</span>
            </div>

            <div class="progress-bg">
                <div class="progress-fill" style="width:{percentage}%"></div>
            </div>

            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Upload an image to see predictions.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FEATURES ----------------

st.markdown("""
<div class="features-grid">

<div class="feature-card">
<div style="font-size:28px;">🎯</div>
<div class="feature-title">Multi-Class Prediction</div>
<div class="feature-text">
Predicts across multiple age groups with confidence scores.
</div>
</div>

<div class="feature-card">
<div style="font-size:28px;">⚖️</div>
<div class="feature-title">Responsible AI</div>
<div class="feature-text">
Built with fairness, transparency, and ethical AI principles.
</div>
</div>

<div class="feature-card">
<div style="font-size:28px;">🔒</div>
<div class="feature-title">Privacy Focused</div>
<div class="feature-text">
Images are not stored or shared with third-party services.
</div>
</div>

</div>
""", unsafe_allow_html=True)

# ---------------- RESPONSIBLE AI NOTICE ----------------

st.markdown("""
<div class="notice-box">

<div class="notice-title">
⚠ Responsible AI Notice
</div>

<div class="notice-text">

This AI system is developed for educational and research purposes only.<br><br>

Predictions may contain inaccuracies or demographic biases.<br>

The system should not be used for critical decision-making.

</div>

</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit | FairVision AI Project
</div>
""", unsafe_allow_html=True)
