import streamlit as st
from PIL import Image
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FairVision AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS (WITH RESPONSIVE IMAGE CONTROL) ----------------
st.markdown("""
<style>
/* Global styles and full responsive container */
.stApp {
    background: linear-gradient(180deg, #2b3a4a 0%, #1e2630 100%);
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Header Styles */
.title {
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-top: 10px;
    margin-bottom: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: clamp(16px, 2vw, 20px);
    margin-bottom: 35px;
}

/* Glassmorphism Card Style */
.custom-card {
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.25);
    margin-bottom: 24px;
}

/* --- IMAGE CENTER & SIZE CONTROL --- */
.image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-top: 15px;
    margin-bottom: 10px;
}

/* This forces the Streamlit image element inside to obey the sizing */
.image-container div[data-testid="stImage"] img {
    max-width: 260px !important; /* Image එක ලස්සනට කුඩා මට්ටමක තබා ගැනීමට */
    height: auto !important;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Prediction Header Box (Teal/Blue Gradient from Image) */
.prediction-box {
    background: linear-gradient(90deg, #4fa3b3 0%, #295b7b 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
}

.prediction-box .label {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 5px;
}

.prediction-box .value {
    font-size: 48px;
    font-weight: 700;
    margin: 5px 0;
}

.prediction-box .confidence {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.9);
}

/* Custom Progress Bar Layout */
.progress-container {
    margin-bottom: 15px;
}

.progress-label-row {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 4px;
}

.custom-progress-bar-bg {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    width: 100%;
    height: 12px;
    overflow: hidden;
}

.custom-progress-bar-fill {
    background-color: #4b6584;
    height: 100%;
    border-radius: 6px;
}

/* Section Subheaders */
.section-header {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #ffffff;
}

/* Responsible AI Alert Box */
.notice-box {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}

.notice-title {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}

.notice-text {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
}

/* Footer Style */
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 50px;
    padding-bottom: 20px;
    font-size: 13px;
}

.footer a {
    color: #94a3b8;
    text-decoration: none;
}

/* Styling native Streamlit elements to fit the UI */
div[data-testid="stFileUploader"] {
    background-color: rgba(0, 0, 0, 0.1);
    border: 1px dashed rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🧠 FairVision AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Fair & Responsible Age Classification System</div>', unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 1], gap="large")

# ---------------- LEFT SIDE: UPLOAD ----------------
with col1:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📤 Upload Face Image</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Image එක පාලනය කළ හැකි Div එකක් ඇතුලට දමා ඇත
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div style="text-align:center; color:#94a3b8; font-size:13px;">Uploaded: {uploaded_file.name}</div>', unsafe_allow_html=True)
    else:
        st.info("Please upload a portrait image to proceed.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT SIDE: PREDICTIONS ----------------
with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Prediction Results</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Mock Results matching the UI image
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
            <div class="label">Predicted Age Group</div>
            <div class="value">{predicted_age}</div>
            <div class="confidence">Confidence: {confidence:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="font-size:16px; font-weight:600; margin-bottom:15px;">Top 3 Predictions</div>', unsafe_allow_html=True)
        
        # Progress Bars
        for res in top3_results:
            percentage = res["prob"] * 100
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-label-row">
                    <span>{res["age"]}</span>
                    <span>{percentage:.2f}%</span>
                </div>
                <div class="custom-progress-bar-bg">
                    <div class="custom-progress-bar-fill" style="width: {percentage}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("Upload an image to see predictions.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESPONSIBLE AI NOTICE ----------------
st.markdown(f"""
<div class="notice-box">
    <div class="notice-title">⚖ Responsible AI Notice</div>
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
Made with ❤️ using Streamlit | <a href="#" target="_blank">FairVision AI Project</a>
</div>
""", unsafe_allow_html=True)
