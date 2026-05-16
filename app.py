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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main Background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(99,102,241,0.25), transparent 25%),
        radial-gradient(circle at bottom right, rgba(14,165,233,0.20), transparent 25%),
        linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e293b 100%);
    color: white;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Header */
.main-title {
    text-align: center;
    font-size: 3.7rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0;
}

.main-subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-top: -5px;
    margin-bottom: 20px;
}

/* Divider */
.custom-line {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin-bottom: 30px;
}

/* Glass Card */
.glass-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 22px;
    backdrop-filter: blur(14px);
    box-shadow: 0px 8px 32px rgba(0,0,0,0.25);
    transition: 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-3px);
}

/* Prediction Box */
.prediction-box {
    background: linear-gradient(135deg, #7dd3fc, #3b82f6);
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    color: white;
    box-shadow: 0px 8px 25px rgba(59,130,246,0.25);
    margin-bottom: 20px;
}

.prediction-label {
    font-size: 1rem;
    opacity: 0.95;
}

.prediction-age {
    font-size: 3rem;
    font-weight: 800;
    margin-top: 5px;
    margin-bottom: 0;
}

.prediction-confidence {
    font-size: 1rem;
    margin-top: -5px;
}

/* Upload Box */
.upload-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Top Predictions */
.top-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Progress Bar */
.stProgress > div > div > div > div {
    background: linear-gradient(to right, #60a5fa, #38bdf8);
}

/* Notice Box */
.notice-box {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.2);
}

.notice-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 12px;
}

.notice-text {
    color: #e2e8f0;
    line-height: 1.7;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 35px;
    color: #cbd5e1;
    font-size: 14px;
}

/* Responsive */
@media screen and (max-width: 768px) {

    .main-title {
        font-size: 2.5rem;
    }

    .prediction-age {
        font-size: 2.2rem;
    }

}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-title">🧠 FairVision AI</div>
<div class="main-subtitle">
Fair & Responsible Age Classification System
</div>
<div class="custom-line"></div>
""", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
left_col, right_col = st.columns([1,1], gap="large")

# ---------------- LEFT SIDE ----------------
with left_col:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="upload-title">📤 Upload Face Image</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose Image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            use_container_width=True
        )

        st.success(f"Uploaded: {uploaded_file.name}")

    else:
        st.info("Upload JPG or PNG image")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT SIDE ----------------
with right_col:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="upload-title">📊 Prediction Results</div>',
        unsafe_allow_html=True
    )

    if uploaded_file is not None:

        with st.spinner("Analyzing image..."):
            time.sleep(1.5)

        # ---------------- DEMO PREDICTION ----------------
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

        # ---------------- MAIN RESULT ----------------
        st.markdown(f"""
        <div class="prediction-box">
            <div class="prediction-label">
                Predicted Age Group
            </div>

            <div class="prediction-age">
                {predicted_age}
            </div>

            <div class="prediction-confidence">
                Confidence: {confidence:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ---------------- TOP 3 ----------------
        st.markdown(
            '<div class="top-title">Top 3 Predictions</div>',
            unsafe_allow_html=True
        )

        for idx in top3_idx:

            st.write(age_groups[idx])

            st.progress(float(probs[idx]))

            st.write(f"{probs[idx]*100:.2f}%")

    else:
        st.info("Upload an image to view predictions")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESPONSIBLE AI ----------------
st.markdown("""
<div class="notice-box">

<div class="notice-title">
⚖ Responsible AI Notice
</div>

<div class="notice-text">
Warning: This AI system is developed for educational and research purposes only.
Predictions may contain inaccuracies or demographic biases.
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
