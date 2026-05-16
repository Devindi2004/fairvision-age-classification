import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import io

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="FairVision · Age Classification",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* Dark background */
  .stApp {
    background: #0d0f14;
    color: #e8eaf0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #13161e;
    border-right: 1px solid #1e2232;
  }

  /* Hero banner */
  .hero-banner {
    background: linear-gradient(135deg, #0f2027 0%, #1a1f35 50%, #0f1624 100%);
    border: 1px solid #1e2a4a;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(16,185,129,0.10) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 40%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin: 0 0 0.5rem 0;
  }
  .hero-sub {
    font-size: 1.05rem;
    color: #94a3b8;
    font-weight: 300;
    letter-spacing: 0.01em;
    margin: 0;
  }
  .hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    margin-bottom: 1rem;
  }

  /* Metric cards */
  .metric-card {
    background: #13161e;
    border: 1px solid #1e2232;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: border-color 0.2s;
  }
  .metric-card:hover { border-color: #3730a3; }
  .metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #a5b4fc;
  }
  .metric-label {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
  }

  /* Section headers */
  .section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 1.5rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .section-divider {
    height: 1px;
    background: linear-gradient(90deg, #1e2232 0%, transparent 100%);
    margin: 0.5rem 0 1.5rem 0;
  }

  /* Upload area */
  .upload-zone {
    background: #0d1117;
    border: 2px dashed #1e2a4a;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    transition: border-color 0.2s;
  }
  .upload-zone:hover { border-color: #4f46e5; }

  /* Prediction result card */
  .result-card {
    background: linear-gradient(135deg, #0f172a 0%, #131b2e 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 2rem;
    margin-top: 1rem;
  }
  .pred-age-label {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #34d399;
    margin: 0;
  }
  .pred-confidence {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 0.3rem;
  }

  /* Bar chart for probabilities */
  .prob-bar-container {
    margin: 0.4rem 0;
  }
  .prob-bar-label {
    font-size: 0.82rem;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.25rem;
  }
  .prob-bar-track {
    background: #1e2232;
    border-radius: 100px;
    height: 8px;
    overflow: hidden;
  }
  .prob-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #4f46e5, #34d399);
    transition: width 0.6s ease;
  }

  /* Model comparison table */
  .compare-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    font-size: 0.9rem;
  }
  .compare-table thead tr {
    background: #1a1f35;
    color: #a5b4fc;
    font-weight: 600;
  }
  .compare-table thead th {
    padding: 0.9rem 1rem;
    text-align: left;
  }
  .compare-table tbody tr {
    border-bottom: 1px solid #1e2232;
    color: #cbd5e1;
    transition: background 0.15s;
  }
  .compare-table tbody tr:hover { background: #131929; }
  .compare-table tbody td {
    padding: 0.85rem 1rem;
  }
  .badge-green {
    background: rgba(52,211,153,0.12);
    color: #34d399;
    border: 1px solid rgba(52,211,153,0.25);
    padding: 0.15rem 0.55rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
  }
  .badge-blue {
    background: rgba(99,102,241,0.12);
    color: #a5b4fc;
    border: 1px solid rgba(99,102,241,0.25);
    padding: 0.15rem 0.55rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
  }

  /* Info panels */
  .info-panel {
    background: #0f172a;
    border-left: 3px solid #4f46e5;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.6;
  }
  .info-panel strong { color: #e2e8f0; }

  /* Streamlit overrides */
  [data-testid="stFileUploader"] {
    border: none !important;
  }
  .stButton button {
    background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    transition: opacity 0.2s !important;
  }
  .stButton button:hover { opacity: 0.85 !important; }

  /* Selectbox / slider labels */
  label { color: #94a3b8 !important; font-size: 0.88rem !important; }

  /* Tabs */
  [data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    color: #64748b;
  }
  [data-testid="stTabs"] [aria-selected="true"] {
    color: #a5b4fc !important;
  }
</style>
""", unsafe_allow_html=True)


# ─── Constants ────────────────────────────────────────────────────────────────
AGE_NAMES = ['0-2', '3-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']
GENDER_NAMES = ['Male', 'Female']
RACE_NAMES = ['White', 'Black', 'Latino_Hispanic', 'East Asian',
              'Southeast Asian', 'Indian', 'Middle Eastern']
NUM_CLASSES = len(AGE_NAMES)
IMG_SIZE = 64
MEAN = [0.485, 0.456, 0.406]
STD  = [0.229, 0.224, 0.225]


# ─── CNN Model Definition (must match training architecture) ──────────────────
class FairFaceCNN(nn.Module):
    def __init__(self, num_classes=9):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout2d(0.1),

            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout2d(0.15),

            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(),
            nn.MaxPool2d(2), nn.Dropout2d(0.2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 8 * 8, 512), nn.ReLU(), nn.Dropout(0.4),
            nn.Linear(512, 256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


# ─── Transform ────────────────────────────────────────────────────────────────
eval_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])


# ─── Model Loader ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model(checkpoint_path, device):
    model = FairFaceCNN(num_classes=NUM_CLASSES)
    ckpt = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    return model


def predict(model, image: Image.Image, device):
    tensor = eval_transform(image.convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(tensor)
        probs  = torch.softmax(logits, dim=1)[0].cpu().numpy()
    top_idx = int(np.argmax(probs))
    return AGE_NAMES[top_idx], float(probs[top_idx]), probs


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;
    color:#a5b4fc;margin-bottom:0.3rem;">⚙️ Configuration</div>
    <div style="font-size:0.82rem;color:#475569;margin-bottom:1.5rem;">
    Model & inference settings
    </div>
    """, unsafe_allow_html=True)

    model_choice = st.selectbox(
        "Model Variant",
        ["Baseline CNN", "Weighted Loss (Mitigation 1)", "Balanced Sampling (Mitigation 2)"],
        help="Choose which trained model checkpoint to use for inference."
    )

    checkpoint_map = {
        "Baseline CNN": "best_fairface_baseline.pt",
        "Weighted Loss (Mitigation 1)": "best_fairface_weighted.pt",
        "Balanced Sampling (Mitigation 2)": "best_fairface_balanced.pt",
    }
    selected_checkpoint = checkpoint_map[model_choice]

    st.markdown("---")

    st.markdown("""<div style="font-size:0.82rem;color:#475569;text-transform:uppercase;
    letter-spacing:0.08em;margin-bottom:0.8rem;">About This Project</div>""",
    unsafe_allow_html=True)

    st.markdown("""
    <div class="info-panel">
    <strong>FairVision</strong> trains a CNN on the <strong>FairFace</strong> dataset
    to classify facial age groups across 9 categories.<br><br>
    It audits bias across <strong>race & gender</strong>, then applies two
    fairness mitigations: weighted loss and balanced sampling.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1.5rem;font-size:0.78rem;color:#334155;">
    Dataset · HuggingFaceM4/FairFace<br>
    Framework · PyTorch<br>
    Task · Age Classification (9 classes)
    </div>
    """, unsafe_allow_html=True)


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-badge">AI Fairness Research</div>
  <h1 class="hero-title">FairVision<br>Age Classification</h1>
  <p class="hero-sub">
    Bias-aware facial age estimation across race & gender demographics
    using the FairFace benchmark dataset.
  </p>
</div>
""", unsafe_allow_html=True)


# ─── Summary Metrics ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
      <div class="metric-value">9</div>
      <div class="metric-label">Age Classes</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
      <div class="metric-value">86K</div>
      <div class="metric-label">Training Samples</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
      <div class="metric-value">7</div>
      <div class="metric-label">Race Groups</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card">
      <div class="metric-value">3</div>
      <div class="metric-label">Model Variants</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Live Prediction", "📊 Model Comparison", "ℹ️ Dataset Info"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LIVE PREDICTION
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-header'>📸 Upload a Face Image</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    upload_col, result_col = st.columns([1, 1], gap="large")

    with upload_col:
        uploaded = st.file_uploader(
            "Drop a face image here (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )

        if uploaded:
            image = Image.open(io.BytesIO(uploaded.read()))
            st.image(image, caption="Uploaded Image", use_container_width=True,
                     output_format="auto")

            run_btn = st.button("🚀 Run Prediction", use_container_width=True)
        else:
            st.markdown("""
            <div class="upload-zone">
              <div style="font-size:2.5rem;margin-bottom:0.8rem;">🖼️</div>
              <div style="font-size:1rem;color:#475569;font-weight:500;">
                Drag & drop or click Browse files
              </div>
              <div style="font-size:0.82rem;color:#334155;margin-top:0.4rem;">
                Supports JPG · PNG · WEBP
              </div>
            </div>
            """, unsafe_allow_html=True)
            run_btn = False

    with result_col:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        if uploaded and run_btn:
            device = torch.device("cpu")

            try:
                model = load_model(selected_checkpoint, device)
                pred_age, confidence, all_probs = predict(model, image, device)

                st.markdown(f"""
                <div class="result-card">
                  <div style="font-size:0.78rem;color:#475569;text-transform:uppercase;
                  letter-spacing:0.1em;margin-bottom:0.8rem;">Predicted Age Group</div>
                  <div class="pred-age-label">{pred_age}</div>
                  <div class="pred-confidence">Confidence: {confidence*100:.1f}%</div>
                  <div style="margin-top:0.6rem;font-size:0.8rem;color:#334155;">
                    Model: {model_choice}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:0.88rem;color:#64748b;font-weight:600;"
                            "text-transform:uppercase;letter-spacing:0.08em;"
                            "margin-bottom:0.8rem;'>All Class Probabilities</div>",
                            unsafe_allow_html=True)

                # Draw probability bars
                bars_html = ""
                sorted_indices = np.argsort(all_probs)[::-1]
                for idx in sorted_indices:
                    pct = float(all_probs[idx]) * 100
                    is_top = idx == int(np.argmax(all_probs))
                    color = "linear-gradient(90deg,#4f46e5,#34d399)" if is_top else \
                            "linear-gradient(90deg,#1e2a4a,#1e3a5f)"
                    name_color = "#34d399" if is_top else "#64748b"
                    bars_html += f"""
                    <div class="prob-bar-container">
                      <div class="prob-bar-label">
                        <span style="color:{name_color};font-weight:{'600' if is_top else '400'}">
                          {AGE_NAMES[idx]}
                        </span>
                        <span style="color:{'#34d399' if is_top else '#475569'}">{pct:.1f}%</span>
                      </div>
                      <div class="prob-bar-track">
                        <div class="prob-bar-fill"
                             style="width:{pct:.1f}%;background:{color};"></div>
                      </div>
                    </div>
                    """
                st.markdown(bars_html, unsafe_allow_html=True)

            except FileNotFoundError:
                st.markdown(f"""
                <div class="info-panel" style="border-left-color:#ef4444;">
                  <strong>⚠️ Checkpoint not found</strong><br>
                  Could not locate <code>{selected_checkpoint}</code>.<br>
                  Please train the model first or place the checkpoint in the app directory.
                </div>
                """, unsafe_allow_html=True)

        elif uploaded and not run_btn:
            st.markdown("""
            <div style="text-align:center;padding:3rem 1rem;color:#334155;">
              <div style="font-size:2rem;margin-bottom:0.5rem;">⬅️</div>
              <div style="font-size:0.9rem;">Click <strong style="color:#a5b4fc">
              Run Prediction</strong> to classify</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem 1rem;color:#1e2232;">
              <div style="font-size:3rem;margin-bottom:0.8rem;">👁️</div>
              <div style="font-size:0.9rem;color:#334155;">
                Upload an image to begin
              </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MODEL COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>📈 Fairness & Accuracy Comparison</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-panel">
    The table below summarises the three trained model variants.
    <strong>Overall Acc</strong> measures raw classification performance;
    <strong>Race Gap</strong> = max minus min per-race accuracy (lower → fairer).
    Fill in actual results from your training run.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table class="compare-table">
      <thead>
        <tr>
          <th>Model</th>
          <th>Overall Acc (%)</th>
          <th>Race Gap (%)</th>
          <th>Male Acc (%)</th>
          <th>Female Acc (%)</th>
          <th>Δ vs Baseline</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge-blue">Baseline CNN</span></td>
          <td>—</td><td>—</td><td>—</td><td>—</td>
          <td style="color:#475569">Reference</td>
        </tr>
        <tr>
          <td><span class="badge-green">Weighted Loss</span></td>
          <td>—</td><td>—</td><td>—</td><td>—</td>
          <td>—</td>
        </tr>
        <tr>
          <td><span class="badge-green">Balanced Sampling</span></td>
          <td>—</td><td>—</td><td>—</td><td>—</td>
          <td>—</td>
        </tr>
      </tbody>
    </table>
    <div style="font-size:0.78rem;color:#334155;margin-top:0.6rem;">
      ℹ️ Replace "—" cells with actual values from your training notebook output.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🌍 Per-Race Accuracy</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    race_header = "".join(
        f"<th>{r}</th>" for r in RACE_NAMES
    )
    st.markdown(f"""
    <table class="compare-table">
      <thead>
        <tr>
          <th>Model</th>
          {race_header}
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge-blue">Baseline</span></td>
          {"".join("<td>—</td>" for _ in RACE_NAMES)}
        </tr>
        <tr>
          <td><span class="badge-green">Weighted</span></td>
          {"".join("<td>—</td>" for _ in RACE_NAMES)}
        </tr>
        <tr>
          <td><span class="badge-green">Balanced</span></td>
          {"".join("<td>—</td>" for _ in RACE_NAMES)}
        </tr>
      </tbody>
    </table>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DATASET INFO
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>🗂️ FairFace Dataset Overview</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    d1, d2 = st.columns(2, gap="large")

    with d1:
        st.markdown("""
        <div class="info-panel" style="border-left-color:#34d399;">
          <strong>Age Groups (9 classes)</strong><br><br>
          0–2 · 3–9 · 10–19 · 20–29 · 30–39<br>
          40–49 · 50–59 · 60–69 · 70+
        </div>
        <div class="info-panel" style="border-left-color:#f59e0b;margin-top:0.8rem;">
          <strong>Gender Groups (2)</strong><br><br>
          Male · Female
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="info-panel" style="border-left-color:#a5b4fc;">
          <strong>Race Groups (7)</strong><br><br>
          White · Black · Latino/Hispanic<br>
          East Asian · Southeast Asian · Indian · Middle Eastern
        </div>
        <div class="info-panel" style="border-left-color:#ec4899;margin-top:0.8rem;">
          <strong>Dataset Size (0.25 config)</strong><br><br>
          ~86K train samples · ~11K test samples<br>
          Intentionally balanced across race groups
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>⚖️ Fairness Methodology</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3, gap="medium")
    for col, title, icon, desc, color in [
        (m1, "Baseline CNN", "🏗️",
         "Standard cross-entropy loss with data augmentation (flip, rotation, colour jitter). "
         "Establishes the fairness gap benchmark.",
         "#4f46e5"),
        (m2, "Weighted Loss", "⚖️",
         "Class-frequency inverse weights applied to the loss function, "
         "penalising errors on underrepresented age groups more heavily.",
         "#f59e0b"),
        (m3, "Balanced Sampling", "🎲",
         "WeightedRandomSampler rebalances the training dataloader so every "
         "age class appears with equal frequency per epoch.",
         "#34d399"),
    ]:
        with col:
            col.markdown(f"""
            <div class="metric-card" style="text-align:left;">
              <div style="font-size:1.8rem;margin-bottom:0.6rem;">{icon}</div>
              <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
              color:{color};margin-bottom:0.5rem;">{title}</div>
              <div style="font-size:0.83rem;color:#64748b;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;font-size:0.8rem;color:#1e2232;padding:1.5rem 0;
border-top:1px solid #1e2232;">
  FairVision · Age Classification · Built with Streamlit & PyTorch ·
  <span style="color:#334155;">AI Fairness Project</span>
</div>
""", unsafe_allow_html=True)
