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

/* ---------------- GLOBAL ---------------- */

.stApp {
    background: linear-gradient(180deg, #2b3a4a 0%, #1e2630 100%);
    color: white;
    font-family: "Segoe UI", sans-serif;
}

/* Hide Streamlit Default UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------------- HEADER ---------------- */

.title {
    font-size: clamp(34px, 4vw, 52px);
    font-weight: 800;
    text-align: center;
    color: white;
    margin-top: 10px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: clamp(15px, 2vw, 20px);
    margin-bottom: 35px;
}

/* ---------------- CARDS ---------------- */

.custom-card {
    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 18px;

    padding: 24px;

    backdrop-filter: blur(12px);

    box-shadow: 0px 8px 30px rgba(0,0,0,0.25);

    margin-bottom: 20px;
}

/* ---------------- SECTION TITLE ---------------- */

.section-header {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 18px;
    color: white;
}

/* ---------------- FILE UPLOADER ---------------- */

div[data-testid="stFileUploader"] {

    background-color: rgba(0,0,0,0.12);

    border: 1px dashed rgba(255,255,255,0.18);

    border-radius: 12px;

    padding: 8px;
}

div[data-testid="stFileUploaderDropzone"] {
    padding: 0.6rem !important;
}

div[data-testid="stFileUploader"] button {

    border-radius: 8px !important;

    padding: 0.35rem 0.9rem !important;

    font-size: 14px !important;
}

/* ---------------- IMAGE SECTION ---------------- */

.image-container {

    display: flex;

    justify-content: center;

    align-items: center;

    margin-top: 10px;

    margin-bottom: 10px;
}

.image-container div[data-testid="stImage"] {

    width: auto !important;

    display: flex;

    justify-content: center;
}

.image-container div[data-testid="stImage"] img {

    width: 220px !important;

    max-width: 100%;

    height: auto !important;

    border-radius: 14px;

    object-fit: cover;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0px 8px 25px rgba(0,0,0,0.28);
}

/* Remove extra spacing */
[data-testid="stImageContainer"] {

    padding: 0 !important;

    margin: 0 !important;
}

/* ---------------- PREDICTION BOX ---------------- */

.prediction-box {

    background: linear-gradient(
        135deg,
        #67c7d8 0%,
        #3f8abf 100%
    );

    border-radius: 16px;

    padding: 25px;

    text-align: center;

    margin-bottom: 25px;

    box-shadow: 0px 6px 20px rgba(0,0,0,0.25);
}

.prediction-label {

    font-size: 14px;

    letter-spacing: 1px;

    text-transform: uppercase;

    color: rgba(255,255,255,0.85);
}

.prediction-value {

    font-size: clamp(40px, 5vw, 58px);

    font-weight: 800;

    margin-top: 8px;

    margin-bottom: 6px;
}

.prediction-confidence {

    font-size: 15px;

    color: rgba(255,255,255,0.92);
}

/* ---------------- TOP PREDICTIONS ---------------- */

.top-title {

    font-size: 20px;

    font-weight: 700;

    margin-bottom: 18px;
}

.progress-container {

    margin-bottom: 18px;
}

.progress-label-row {

    display: flex;

    justify-content: space-between;

    margin-bottom: 6px;

    color: #e2e8f0;

    font-size: 14px;
}

.custom-progress-bg {

    width: 100%;

    height: 14px;

    background: rgba(255,255,255,0.08);

    border-radius: 10px;

    overflow: hidden;
}

.custom-progress-fill {

    height: 100%;

    border-radius: 10px;

    background: linear-gradient(
        to right,
        #7dd3fc,
        #3b82f6
    );
}

/* ---------------- NOTICE BOX ---------------- */

.notice-box {

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 18px;

    padding: 22px;

    margin-top: 10px;

    box-shadow: 0px 6px 20px rgba(0,0,0,0.2);
}

.notice-title {

    font-size: 22px;

    font-weight: 700;

    margin-bottom: 12px;
}

.notice-text {

    color: #cbd5e1;

    line-height: 1.7;

    font-size: 15px;
}

/* ---------------- FOOTER ---------------- */

.footer {

    text-align: center;

    color: #94a3b8;

    margin-top: 40px;

    font-size: 14px;
}

/* ---------------- RESPONSIVE ---------------- */

@media screen and (max-width: 768px) {

    .custom-card {
        padding: 18px;
    }

    .prediction-box {
        padding: 20px;
    }

    .section-header {
        font-size: 21px;
    }

}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    '<div class="title">🧠 FairVision AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Fair & Responsible Age Classification System</div>',
    unsafe_allow_html=True
)

# ---------------- MAIN LAYOUT ----------------

col1, col2 = st.columns([1,1], gap="large")

# ---------------- LEFT SIDE ----------------

with col1:

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-header">📤 Upload Face Image</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.markdown(
            '<div class="image-container">',
            unsafe_allow_html=True
        )

        st.image(image, width=220)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                color:#94a3b8;
                font-size:13px;
                margin-top:5px;
            ">
                Uploaded: {uploaded_file.name}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.info("Please upload a portrait image.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT SIDE ----------------

with col2:

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-header">📊 Prediction Results</div>',
        unsafe_allow_html=True
    )

    if uploaded_file is not None:

        # Dummy Predictions
        top3_results = [
            {"age": "20-29", "prob": 0.8534},
            {"age": "30-39", "prob": 0.0912},
            {"age": "10-19", "prob": 0.0554}
        ]

        predicted_age = top3_results[0]["age"]
        confidence = top3_results[0]["prob"] * 100

        # Main Prediction Box
        st.markdown(f"""
        <div class="prediction-box">

            <div class="prediction-label">
                Predicted Age Group
            </div>

            <div class="prediction-value">
                {predicted_age}
            </div>

            <div class="prediction-confidence">
                Confidence: {confidence:.2f}%
            </div>

        </div>
        """, unsafe_allow_html=True)

        # Top Predictions
        st.markdown(
            '<div class="top-title">Top 3 Predictions</div>',
            unsafe_allow_html=True
        )

        for res in top3_results:

            percentage = res["prob"] * 100

            st.markdown(f"""

            <div class="progress-container">

                <div class="progress-label-row">
                    <span>{res["age"]}</span>
                    <span>{percentage:.2f}%</span>
                </div>

                <div class="custom-progress-bg">

                    <div
                        class="custom-progress-fill"
                        style="width:{percentage}%;">
                    </div>

                </div>

            </div>

            """, unsafe_allow_html=True)

    else:
        st.info("Upload an image to see predictions.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESPONSIBLE AI NOTICE ----------------

st.markdown("""

<div class="notice-box">

    <div class="notice-title">
        ⚖ Responsible AI Notice
    </div>

    <div class="notice-text">
        This AI system is developed for educational and research purposes only.
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
