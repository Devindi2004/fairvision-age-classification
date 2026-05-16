import streamlit as st
from PIL import Image
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FairVision AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS (PROFESSIONAL & BALANCED) ----------------
st.markdown("""
<style>
/* Global styles and modern dark background */
.stApp {
    background: linear-gradient(135deg, #1e2633, #0f141c);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}

/* Header Section */
.title-container {
    text-align: center;
    padding: 20px 0 10px 0;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
}
.subtitle {
    color: #94a3b8;
    font-size: 16px;
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* Glassmorphism Cards */
.custom-card {
    background: rgba(30, 41, 59, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

/* Image Wrapper to limit size and center it */
.image-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(15, 23, 42, 0.6);
    padding: 20px;
    border-radius: 12px;
    border: 1px dashed rgba(255, 255, 255, 0.1);
    max-width: 450px;
    margin: 0 auto;
}

/* Section Sub-headers */
.section-header {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Prediction Result Box */
.prediction-hero {
    background: linear-gradient(135deg, #3a7bd5, #3a6073);
    background: linear-gradient(135deg, #4b7cb2, #2c4c70);
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.prediction-label {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.85;
    margin-bottom: 4px;
}
.prediction-value {
    font-size: 52px;
    font-weight: 800;
    line-height: 1;
    margin: 10px 0;
}
.prediction-conf {
    font-size: 14px;
    opacity: 0.9;
}

/* Progress bar container styling */
.progress-container {
    margin-bottom: 12px;
}
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 4px;
}

/* Responsible AI Notice */
.notice-card {
    background: rgba(30, 41, 59, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    margin-top: 10px;
}
.notice-header {
    font-size: 16px;
    font-weight: 600;
    color: #cbd5e1;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.notice-text {
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.5;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 40px;
    padding: 20px 0;
    font-size: 13px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}
.footer a {
    color: #94a3b8;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="title-container">
    <div class="main-title">🧠 FairVision AI</div>
    <div class="subtitle">Fair & Responsible Age Classification System</div>
</div>
""", unsafe_allow_html=True)

st.write("") # Spacer

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 1], gap="large")

# ---------------- LEFT COLUMN: UPLOAD ----------------
with col1:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📤 Upload Face Image</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file (JPG, PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    st.write("")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Image එක මැදට කර ප්‍රමාණය පාලනය කිරීමට wrapper එකක් භාවිත කර ඇත
        st.markdown('<div class="image-wrapper">', unsafe_allow_html=True)
        # මෙහි width එක 320px ලෙස සීමා කර ඇත (Image Size එක අඩු කිරීමට)
        st.image(image, use_container_width=False, width=320)
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("<center>Uploaded: " + uploaded_file.name + "</center>", unsafe_allow_html=True)
    else:
        # Placeholder info box when no image is uploaded
        st.info("Please upload a portrait image to begin analysis.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT COLUMN: RESULTS ----------------
with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Prediction Results</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # ---------------- DUMMY PREDICTION LOGIC ----------------
        age_groups = ["0-2", "3-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]
        
        # Seed සකසා ඇත්තේ හැමවිටම එකම dummy අගයක් පෙන්වීමටයි (ඔබේ Model එක මෙතනට ආදේශ කරන්න)
        probs = np.random.dirichlet(np.ones(len(age_groups)), size=1)[0]
        top3_idx = probs.argsort()[-3:][::-1]
        
        predicted_age = age_groups[top3_idx[0]]
        confidence = probs[top3_idx[0]] * 100
        
        # Display Hero Prediction Box
        st.markdown(f"""
        <div class="prediction-hero">
            <div class="prediction-label">Predicted Age Group</div>
            <div class="prediction-value">{predicted_age}</div>
            <div class="prediction-conf">Confidence: {confidence:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="font-size: 16px; font-weight:600; margin-bottom:15px; color:#ffffff;">Top 3 Predictions</div>', unsafe_allow_html=True)
        
        # Progress Bars for Top 3
        for idx in top3_idx:
            val_pct = probs[idx] * 100
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-label">
                    <span>{age_groups[idx]}</span>
                    <span>{val_pct:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(float(probs[idx]))
            
    else:
        st.markdown("""
        <div style="color: #64748b; text-align: center; padding: 40px 0;">
            Upload an image on the left to view the age group classification breakdown.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESPONSIBLE AI NOTICE (BOTTOM FULL WIDTH) ----------------
st.markdown("""
<div class="notice-card">
    <div class="notice-header">⚖️ Responsible AI Notice</div>
    <div class="notice-text">
        <strong>Warning:</strong> This AI system is developed for educational and research purposes only. 
        Predictions may contain inaccuracies or demographic biases. The system should not be used for 
        critical automated decision-making or legal age verification.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    Made with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a> | <strong>FairVision AI Project</strong>
</div>
""", unsafe_allow_html=True)
