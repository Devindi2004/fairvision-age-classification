import streamlit as st
from PIL import Image
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FairVision AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Manrope:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

/* ---- BASE ---- */
html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
    background-attachment: fixed;
}

/* ---- HIDE STREAMLIT DEFAULTS ---- */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

/* ---- TITLE ---- */
.title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 90px;
    font-weight: 400;
    text-align: center;
    color: white;
    margin-top: 10px;
    letter-spacing: 0.04em;
    line-height: 0.95;
    background: linear-gradient(90deg, #f1f5f9, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ---- SUBTITLE ---- */
.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 20px;
    margin-bottom: 30px;
    font-weight: 300;
    letter-spacing: 0.03em;
}

/* ---- CARD ---- */
.card {
    background-color: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0px 4px 30px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.07);
    transition: border-color 0.3s, box-shadow 0.3s;
}
.card:hover {
    border-color: rgba(255,255,255,0.13);
    box-shadow: 0px 8px 48px rgba(0,0,0,0.35);
}

/* ---- PREDICTION BOX ---- */
.prediction-box {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.prediction-box::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 65% 20%, rgba(255,255,255,0.1), transparent 60%);
    pointer-events: none;
    border-radius: 18px;
}
.prediction-box h2 {
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    opacity: 0.85 !important;
    margin-bottom: 6px !important;
}
.prediction-box h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 80px !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    letter-spacing: 0.04em !important;
    margin-bottom: 8px !important;
    text-shadow: 0 4px 24px rgba(0,0,0,0.35) !important;
}
.prediction-box h3 {
    font-size: 16px !important;
    font-weight: 500 !important;
    opacity: 0.9 !important;
    font-family: 'Fira Code', monospace !important;
}

/* ---- STREAMLIT SUBHEADER ---- */
.stApp h2 {
    font-family: 'Manrope', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.01em;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 18px;
}

/* ---- FILE UPLOADER ---- */
[data-testid="stFileUploader"] {
    background: rgba(99,102,241,0.04);
    border: 2px dashed rgba(99,102,241,0.32);
    border-radius: 16px;
    padding: 8px;
    transition: all 0.25s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,0.65);
    background: rgba(99,102,241,0.08);
}
[data-testid="stFileUploader"] label {
    color: #94a3b8 !important;
    font-size: 14px !important;
}

/* ---- PROGRESS BAR ---- */
[data-testid="stProgressBar"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 50px !important;
    height: 8px !important;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    border-radius: 50px !important;
    transition: width 0.8s cubic-bezier(0.4,0,0.2,1) !important;
}

/* ---- ST.WRITE (age label rows) ---- */
.stMarkdown p, .stText {
    color: #cbd5e1;
    font-size: 14px;
    font-family: 'Fira Code', monospace;
    margin-top: 4px;
}

/* ---- INFO BOX ---- */
[data-testid="stInfo"] {
    background: rgba(6,182,212,0.07) !important;
    border: 1px solid rgba(6,182,212,0.2) !important;
    border-radius: 14px !important;
    color: #67e8f9 !important;
}
[data-testid="stInfo"] p {
    color: #67e8f9 !important;
    font-family: 'Manrope', sans-serif !important;
}

/* ---- WARNING BOX ---- */
[data-testid="stWarning"] {
    background: rgba(245,158,11,0.07) !important;
    border: 1px solid rgba(245,158,11,0.2) !important;
    border-left: 4px solid #f59e0b !important;
    border-radius: 14px !important;
}
[data-testid="stWarning"] p {
    color: #fcd34d !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 300 !important;
}

/* ---- IMAGE ---- */
[data-testid="stImage"] img {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stImage"] div {
    color: #64748b !important;
    font-size: 12px !important;
    font-style: italic !important;
    text-align: center !important;
    margin-top: 6px !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

/* ---- FOOTER ---- */
.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">FairVision AI</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Fair & Responsible Age Classification System</div>',
    unsafe_allow_html=True
)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 1])

# ---------------- LEFT SIDE ----------------
with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📤 Upload Face Image")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT SIDE ----------------
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Prediction Results")

    if uploaded_file is not None:

        # ---------------- DUMMY PREDICTION ----------------
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
            <h2>🎯 Predicted Age Group</h2>
            <h1>{predicted_age}</h1>
            <h3>Confidence: {confidence:.2f}%</h3>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.subheader("🔝 Top 3 Predictions")

        for idx in top3_idx:
            st.progress(float(probs[idx]))
            st.write(f"{age_groups[idx]} — {probs[idx]*100:.2f}%")

    else:
        st.info("Upload an image to see predictions.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESPONSIBLE AI ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("⚖ Responsible AI Notice")

st.warning("""
This AI system is developed for educational and research purposes only.

Predictions may contain inaccuracies or demographic biases.
The system should not be used for critical decision-making.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit | FairVision AI Project
</div>
""", unsafe_allow_html=True)
