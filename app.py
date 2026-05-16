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

.main {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
}

.title {
    font-size: 55px;
    font-weight: 800;
    text-align: center;
    color: white;
    margin-top: 10px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 20px;
    margin-bottom: 30px;
}

.card {
    background-color: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 30px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

.prediction-box {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.3);
}

.footer {
    text-align:center;
    color:#94a3b8;
    margin-top:40px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🧠 FairVision AI</div>', unsafe_allow_html=True)

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
