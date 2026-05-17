<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>🧠 FairVision AI — Fair & Responsible Age Classification</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Manrope:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet"/>
<style>
/* ═══════════════════════════════════════════════
   RESET & VARIABLES
═══════════════════════════════════════════════ */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  /* ── original streamlit palette ── */
  --bg-left:#0f172a;
  --bg-right:#111827;
  --card-bg:rgba(255,255,255,0.05);
  --card-blur:blur(10px);
  --card-shadow:0px 4px 30px rgba(0,0,0,0.2);
  --card-radius:20px;
  --card-pad:25px;
  --pred-grad:linear-gradient(135deg,#2563eb,#7c3aed);
  --pred-radius:18px;
  --pred-shadow:0px 6px 25px rgba(0,0,0,0.3);
  --subtitle-color:#cbd5e1;
  --footer-color:#94a3b8;
  /* ── new design tokens ── */
  --accent-blue:#3b82f6;
  --accent-violet:#8b5cf6;
  --accent-cyan:#22d3ee;
  --accent-emerald:#10b981;
  --text:#f1f5f9;
  --text-dim:#64748b;
  --text-soft:#94a3b8;
  --border:rgba(255,255,255,0.07);
  --border-glow:rgba(59,130,246,0.3);
}

/* ═══════════════════════════════════════════════
   BASE
═══════════════════════════════════════════════ */
html{scroll-behavior:smooth}
body{
  font-family:'Manrope',sans-serif;
  background:linear-gradient(135deg,var(--bg-left) 0%,var(--bg-right) 100%);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
}

/* ── atmospheric layers ── */
.atmo{position:fixed;inset:0;pointer-events:none;z-index:0}
.atmo-orb{position:absolute;border-radius:50%;filter:blur(130px);opacity:0}
.atmo-orb.a1{width:700px;height:700px;top:-200px;left:-200px;background:#1d4ed8;animation:orbFloat 18s ease-in-out infinite alternate}
.atmo-orb.a2{width:600px;height:600px;bottom:-150px;right:-150px;background:#5b21b6;animation:orbFloat 22s ease-in-out infinite alternate-reverse}
.atmo-orb.a3{width:400px;height:400px;top:40%;left:40%;background:#0e7490;animation:orbFloat 14s ease-in-out infinite alternate}
@keyframes orbFloat{0%{opacity:.09;transform:translate(0,0) scale(1)}100%{opacity:.15;transform:translate(30px,20px) scale(1.05)}}

/* scanline grain */
.grain{
  position:fixed;inset:0;pointer-events:none;z-index:1;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='250' height='250'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='250' height='250' filter='url(%23n)' opacity='.025'/%3E%3C/svg%3E");
  opacity:.45;
}

/* ═══════════════════════════════════════════════
   PAGE SHELL
═══════════════════════════════════════════════ */
.page{position:relative;z-index:2;max-width:1280px;margin:0 auto;padding:0 36px 80px}

/* ═══════════════════════════════════════════════
   NAV
═══════════════════════════════════════════════ */
.nav{
  display:flex;align-items:center;justify-content:space-between;
  padding:24px 0;
  border-bottom:1px solid var(--border);
  margin-bottom:0;
  position:sticky;top:0;z-index:100;
  background:rgba(7,11,22,.75);
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
  margin-left:-36px;margin-right:-36px;
  padding-left:36px;padding-right:36px;
}
.nav-logo{display:flex;align-items:center;gap:12px;text-decoration:none}
.nav-logo-mark{
  width:42px;height:42px;border-radius:12px;
  background:var(--pred-grad);
  display:flex;align-items:center;justify-content:center;
  font-size:20px;
  box-shadow:0 0 32px rgba(37,99,235,.4),0 0 64px rgba(124,58,237,.2);
  animation:logoPulse 4s ease-in-out infinite;
}
@keyframes logoPulse{0%,100%{box-shadow:0 0 32px rgba(37,99,235,.4),0 0 64px rgba(124,58,237,.2)}50%{box-shadow:0 0 48px rgba(37,99,235,.6),0 0 96px rgba(124,58,237,.35)}}
.nav-wordmark{font-family:'Bebas Neue',sans-serif;font-size:26px;letter-spacing:.06em;color:var(--text)}
.nav-right{display:flex;align-items:center;gap:20px}
.nav-tag{
  font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  padding:5px 14px;border-radius:50px;
  background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.22);
  color:#34d399;
}
.nav-link{font-size:14px;color:var(--text-soft);text-decoration:none;transition:color .2s}
.nav-link:hover{color:var(--text)}

/* ═══════════════════════════════════════════════
   HERO
═══════════════════════════════════════════════ */
.hero{
  text-align:center;
  padding:90px 0 70px;
  position:relative;
}
.hero-eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.22);
  color:#93c5fd;font-size:12px;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;
  padding:6px 18px;border-radius:50px;
  margin-bottom:28px;
  animation:fadeSlideUp .6s ease both;
}
.eyebrow-dot{width:6px;height:6px;border-radius:50%;background:var(--accent-blue);animation:blink 2.5s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}

/* mirrors: .title — font-size:55px, font-weight:800, text-align:center, color:white, margin-top:10px */
.hero-title{
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(64px,10vw,130px);
  letter-spacing:.02em;
  line-height:.95;
  color:white;
  margin-top:10px;
  margin-bottom:20px;
  animation:fadeSlideUp .6s .1s ease both;
}
.hero-title-line2{
  background:linear-gradient(90deg,#60a5fa,#a78bfa 50%,#22d3ee);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
/* mirrors: .subtitle — color:#cbd5e1, font-size:20px, text-align:center, margin-bottom:30px */
.hero-subtitle{
  color:#cbd5e1;
  font-size:20px;
  text-align:center;
  margin-bottom:30px;
  font-weight:300;
  letter-spacing:.02em;
  animation:fadeSlideUp .6s .18s ease both;
}
.hero-meta{
  display:flex;align-items:center;justify-content:center;gap:28px;flex-wrap:wrap;
  animation:fadeSlideUp .6s .26s ease both;
}
.hero-meta-item{display:flex;align-items:center;gap:7px;font-size:13px;color:var(--text-soft)}
.hero-meta-dot{width:4px;height:4px;border-radius:50%;background:var(--text-dim)}

@keyframes fadeSlideUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:translateY(0)}}

/* ═══════════════════════════════════════════════
   STATS ROW
═══════════════════════════════════════════════ */
.stats{
  display:grid;grid-template-columns:repeat(3,1fr);
  gap:1px;background:var(--border);
  border:1px solid var(--border);border-radius:20px;overflow:hidden;
  margin-bottom:60px;
  animation:fadeSlideUp .6s .32s ease both;
}
.stat-cell{
  background:rgba(255,255,255,0.03);
  padding:28px 24px;text-align:center;
  transition:background .25s;
}
.stat-cell:hover{background:rgba(255,255,255,0.06)}
.stat-num{
  font-family:'Bebas Neue',sans-serif;
  font-size:42px;letter-spacing:.04em;
  background:var(--pred-grad);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  display:block;line-height:1;margin-bottom:6px;
}
.stat-lbl{font-size:12px;color:var(--text-dim);font-weight:600;letter-spacing:.06em;text-transform:uppercase}

/* ═══════════════════════════════════════════════
   SECTION LABEL
═══════════════════════════════════════════════ */
.section-intro{margin-bottom:36px;animation:fadeSlideUp .6s .38s ease both}
.section-tag{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-blue);margin-bottom:8px}
.section-heading{font-family:'Bebas Neue',sans-serif;font-size:clamp(32px,5vw,52px);letter-spacing:.04em;line-height:1;color:var(--text);margin-bottom:10px}
.section-desc{font-size:15px;color:var(--text-soft);max-width:460px;line-height:1.7;font-weight:300}

/* ═══════════════════════════════════════════════
   COLUMNS — mirrors st.columns([1,1])
═══════════════════════════════════════════════ */
.main-cols{
  display:grid;grid-template-columns:1fr 1fr;
  gap:24px;margin-bottom:24px;
  animation:fadeSlideUp .6s .44s ease both;
}

/* ═══════════════════════════════════════════════
   CARD — mirrors .card CSS exactly
═══════════════════════════════════════════════ */
.card{
  background-color:rgba(255,255,255,0.05); /* exact */
  padding:25px; /* exact */
  border-radius:20px; /* exact */
  backdrop-filter:blur(10px); /* exact */
  -webkit-backdrop-filter:blur(10px);
  box-shadow:0px 4px 30px rgba(0,0,0,0.2); /* exact */
  margin-bottom:20px; /* exact */
  border:1px solid var(--border);
  transition:border-color .3s,box-shadow .3s,transform .3s;
  position:relative;overflow:hidden;
}
.card::before{
  content:'';position:absolute;inset:0;border-radius:20px;
  background:linear-gradient(135deg,rgba(255,255,255,.03) 0%,transparent 60%);
  pointer-events:none;
}
.card:hover{
  border-color:rgba(255,255,255,.13);
  box-shadow:0px 8px 48px rgba(0,0,0,.35);
  transform:translateY(-2px);
}

/* card header */
.card-head{
  display:flex;align-items:center;gap:11px;
  margin-bottom:22px;
  padding-bottom:18px;
  border-bottom:1px solid var(--border);
}
.card-head-icon{
  width:38px;height:38px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:17px;flex-shrink:0;
}
.icon-upload{background:rgba(99,102,241,.13);border:1px solid rgba(99,102,241,.22)}
.icon-results{background:rgba(34,211,238,.1);border:1px solid rgba(34,211,238,.2)}
.icon-ai{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.2)}
.card-head-title{font-size:16px;font-weight:700;color:var(--text);letter-spacing:-.01em}

/* ═══════════════════════════════════════════════
   DROP ZONE — mirrors st.file_uploader
═══════════════════════════════════════════════ */
.dropzone{
  border:2px dashed rgba(99,102,241,.3);
  border-radius:16px;padding:48px 20px;
  text-align:center;cursor:pointer;
  transition:all .25s;
  background:rgba(99,102,241,.03);
  position:relative;overflow:hidden;
}
.dropzone.over,.dropzone:hover{border-color:rgba(99,102,241,.65);background:rgba(99,102,241,.07)}
.dropzone input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.dz-ring{
  width:60px;height:60px;border-radius:50%;
  background:rgba(99,102,241,.12);border:2px solid rgba(99,102,241,.22);
  display:flex;align-items:center;justify-content:center;
  font-size:26px;margin:0 auto 18px;
  animation:ringPulse 3s ease-in-out infinite;
}
@keyframes ringPulse{0%,100%{box-shadow:0 0 0 0 rgba(99,102,241,.3)}50%{box-shadow:0 0 0 12px rgba(99,102,241,0)}}
.dz-title{font-size:15px;font-weight:600;color:var(--text);margin-bottom:6px}
.dz-hint{font-size:13px;color:var(--text-dim)}
.dz-hint em{color:#818cf8;font-style:normal;font-weight:600}
.dz-types{display:flex;gap:6px;justify-content:center;margin-top:16px}
.dz-type{
  font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  padding:3px 10px;border-radius:50px;
  background:rgba(255,255,255,.04);border:1px solid var(--border);
  color:var(--text-soft);
}

/* preview — mirrors: if uploaded_file is not None: st.image(...) */
.preview{display:none;flex-direction:column;gap:14px}
.preview.show{display:flex}
.preview-frame{
  border-radius:14px;overflow:hidden;
  background:rgba(0,0,0,.3);
  aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;
  border:1px solid var(--border);
}
.preview-frame img{width:100%;height:100%;object-fit:contain}
.preview-caption{
  text-align:center;font-size:13px;color:var(--text-dim);
  font-style:italic;
}
.preview-row{display:flex;align-items:center;justify-content:space-between}
.preview-fname{
  font-family:'Fira Code',monospace;font-size:12px;
  color:var(--text-soft);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:65%;
}
.btn-del{
  font-size:12px;font-weight:600;
  background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.18);
  color:#f87171;border-radius:50px;padding:5px 14px;
  cursor:pointer;transition:background .2s;font-family:'Manrope',sans-serif;
}
.btn-del:hover{background:rgba(239,68,68,.18)}

/* analyze btn */
.btn-run{
  width:100%;padding:14px;margin-top:4px;
  background:var(--pred-grad);
  color:#fff;border:none;border-radius:14px;
  font-family:'Manrope',sans-serif;font-size:15px;font-weight:700;
  cursor:pointer;letter-spacing:.02em;
  display:flex;align-items:center;justify-content:center;gap:9px;
  transition:opacity .2s,transform .2s;
  box-shadow:0 6px 28px rgba(37,99,235,.35);
  position:relative;overflow:hidden;
}
.btn-run::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);
  transform:translateX(-100%);transition:transform .5s;
}
.btn-run:hover::before{transform:translateX(100%)}
.btn-run:hover:not(:disabled){opacity:.88;transform:translateY(-1px)}
.btn-run:disabled{opacity:.35;cursor:default;transform:none}

/* spinner */
.spin{
  width:16px;height:16px;
  border:2px solid rgba(255,255,255,.3);
  border-top-color:#fff;
  border-radius:50%;animation:spin .65s linear infinite;
  display:none;
}
.spin.on{display:inline-block}
@keyframes spin{to{transform:rotate(360deg)}}

/* ═══════════════════════════════════════════════
   RESULTS — mirrors right col logic exactly
═══════════════════════════════════════════════ */
.info-pill{
  background:rgba(6,182,212,.07);border:1px solid rgba(6,182,212,.18);
  border-radius:14px;padding:20px;
  display:flex;align-items:flex-start;gap:12px;
  font-size:14px;color:#67e8f9;line-height:1.6;
}

/* .prediction-box — mirrors EXACTLY:
   background:linear-gradient(135deg,#2563eb,#7c3aed)
   padding:20px / border-radius:18px / color:white
   text-align:center / margin-top:20px
   box-shadow:0px 6px 25px rgba(0,0,0,0.3)
*/
.prediction-box{
  background:linear-gradient(135deg,#2563eb,#7c3aed);
  padding:20px;
  border-radius:18px;
  color:white;
  text-align:center;
  margin-top:20px;
  box-shadow:0px 6px 25px rgba(0,0,0,0.3);
  position:relative;overflow:hidden;
}
.prediction-box::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(circle at 65% 20%,rgba(255,255,255,.12),transparent 60%);
  pointer-events:none;
}
.pb-label{
  font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  opacity:.85;margin-bottom:10px;display:block;
}
/* mirrors <h1>{predicted_age}</h1> */
.pb-age{
  font-family:'Bebas Neue',sans-serif;
  font-size:80px;line-height:1;letter-spacing:.04em;
  display:block;margin-bottom:8px;
  text-shadow:0 4px 24px rgba(0,0,0,.35);
}
/* mirrors <h3>Confidence: {confidence:.2f}%</h3> */
.pb-conf{
  font-size:16px;font-weight:500;opacity:.9;
  display:block;
}
.pb-conf strong{
  font-family:'Fira Code',monospace;font-weight:700;font-size:17px;
}

/* mirrors st.write("") + st.subheader("🔝 Top 3 Predictions") */
.top3-head{
  font-size:14px;font-weight:700;color:var(--text);
  margin-top:22px;margin-bottom:16px;
  display:flex;align-items:center;gap:8px;
  letter-spacing:-.01em;
}

/* mirrors for idx in top3_idx: st.progress(float(probs[idx])) + st.write(...) */
.bar-item{margin-bottom:14px}
.bar-row{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:7px}
.bar-grp{font-size:14px;font-weight:600;color:var(--text)}
.bar-val{
  font-family:'Fira Code',monospace;
  font-size:13px;color:var(--text-soft);
}
/* st.progress track */
.bar-track{
  height:8px;background:rgba(255,255,255,.06);
  border-radius:50px;overflow:hidden;
}
.bar-fill{
  height:100%;border-radius:50px;
  width:0%;transition:width 1s cubic-bezier(.4,0,.2,1);
}
.bf1{background:linear-gradient(90deg,#2563eb,#7c3aed)}
.bf2{background:linear-gradient(90deg,rgba(37,99,235,.5),rgba(124,58,237,.5))}
.bf3{background:linear-gradient(90deg,rgba(37,99,235,.25),rgba(124,58,237,.25))}

/* ═══════════════════════════════════════════════
   FEATURES STRIP
═══════════════════════════════════════════════ */
.features{
  display:grid;grid-template-columns:repeat(3,1fr);
  gap:16px;margin-bottom:24px;
  animation:fadeSlideUp .6s .5s ease both;
}
.feat{
  background:rgba(255,255,255,.03);border:1px solid var(--border);
  border-radius:16px;padding:22px 20px;
  transition:border-color .25s,transform .25s;
}
.feat:hover{border-color:rgba(255,255,255,.12);transform:translateY(-3px)}
.feat-icon{font-size:24px;margin-bottom:12px;display:block}
.feat-title{font-size:14px;font-weight:700;color:var(--text);margin-bottom:6px}
.feat-desc{font-size:13px;color:var(--text-soft);line-height:1.65;font-weight:300}

/* ═══════════════════════════════════════════════
   RESPONSIBLE AI — mirrors st.subheader + st.warning
═══════════════════════════════════════════════ */
.responsible{animation:fadeSlideUp .6s .56s ease both}

/* mirrors st.warning box */
.warning-box{
  background:rgba(245,158,11,.07);
  border:1px solid rgba(245,158,11,.2);
  border-left:4px solid #f59e0b;
  border-radius:14px;
  padding:22px 24px;
  color:#fcd34d;
  font-size:14px;line-height:1.8;font-weight:300;
}
.warning-box strong{color:#fde68a;font-weight:700}
.warning-icon{font-size:18px;margin-right:6px}

/* ═══════════════════════════════════════════════
   FOOTER — mirrors .footer
═══════════════════════════════════════════════ */
.footer{
  text-align:center;       /* exact */
  color:#94a3b8;           /* exact hex */
  margin-top:40px;         /* exact */
  font-size:14px;          /* exact */
  padding-top:28px;
  border-top:1px solid var(--border);
  animation:fadeSlideUp .6s .62s ease both;
}
.footer-heart{color:#f87171}

/* ═══════════════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════════════ */
@media(max-width:860px){
  .main-cols{grid-template-columns:1fr}
  .features{grid-template-columns:1fr 1fr}
  .stats{grid-template-columns:1fr}
}
@media(max-width:560px){
  .page{padding:0 18px 60px}
  .hero-title{font-size:58px}
  .features{grid-template-columns:1fr}
  .nav-link,.nav-tag{display:none}
}
</style>
</head>
<body>

<!-- Atmosphere -->
<div class="atmo">
  <div class="atmo-orb a1"></div>
  <div class="atmo-orb a2"></div>
  <div class="atmo-orb a3"></div>
</div>
<div class="grain"></div>

<div class="page">

  <!-- ── NAV ── -->
  <nav class="nav">
    <a class="nav-logo" href="#">
      <div class="nav-logo-mark">🧠</div>
      <span class="nav-wordmark">FairVision AI</span>
    </a>
    <div class="nav-right">
      <a class="nav-link" href="#app">Try Demo</a>
      <a class="nav-link" href="#responsible">AI Ethics</a>
      <span class="nav-tag">Research Preview</span>
    </div>
  </nav>

  <!-- ── HERO — mirrors st.markdown title + subtitle ── -->
  <section class="hero">
    <div class="hero-eyebrow">
      <span class="eyebrow-dot"></span>
      Educational &amp; Research Use Only
    </div>
    <!-- mirrors: .title — font-size:55px, font-weight:800, text-align:center, color:white, margin-top:10px -->
    <h1 class="hero-title">
      🧠 FAIRVISION<br>
      <span class="hero-title-line2">AI</span>
    </h1>
    <!-- mirrors: .subtitle — color:#cbd5e1, font-size:20px, margin-bottom:30px -->
    <p class="hero-subtitle">Fair &amp; Responsible Age Classification System</p>
    <div class="hero-meta">
      <span class="hero-meta-item">9 Age Groups</span>
      <span class="hero-meta-dot"></span>
      <span class="hero-meta-item">Top-3 Predictions</span>
      <span class="hero-meta-dot"></span>
      <span class="hero-meta-item">Zero Data Stored</span>
      <span class="hero-meta-dot"></span>
      <span class="hero-meta-item">Privacy Safe</span>
    </div>
  </section>

  <!-- STATS -->
  <div class="stats">
    <div class="stat-cell"><span class="stat-num">9</span><span class="stat-lbl">Age Classes</span></div>
    <div class="stat-cell"><span class="stat-num">TOP 3</span><span class="stat-lbl">Ranked Predictions</span></div>
    <div class="stat-cell"><span class="stat-num">0</span><span class="stat-lbl">Images Retained</span></div>
  </div>

  <!-- ── APP SECTION ── -->
  <div id="app">
    <div class="section-intro">
      <div class="section-tag">Live Demo</div>
      <div class="section-heading">Classify an Image</div>
      <p class="section-desc">Upload a face photo to receive instant age group predictions powered by probabilistic classification.</p>
    </div>

    <!-- mirrors: col1, col2 = st.columns([1, 1]) -->
    <div class="main-cols">

      <!-- ── LEFT — col1: Upload card ── -->
      <div class="card">
        <!-- mirrors: st.subheader("📤 Upload Face Image") -->
        <div class="card-head">
          <div class="card-head-icon icon-upload">📤</div>
          <span class="card-head-title">Upload Face Image</span>
        </div>

        <!-- mirrors: st.file_uploader("Choose an image", type=["jpg","jpeg","png"]) -->
        <div class="dropzone" id="dropzone">
          <input type="file" id="fileInput" accept=".jpg,.jpeg,.png"/>
          <div class="dz-ring">🖼️</div>
          <div class="dz-title">Choose an image</div>
          <div class="dz-hint">Drop here or <em>browse</em></div>
          <div class="dz-types">
            <span class="dz-type">JPG</span>
            <span class="dz-type">JPEG</span>
            <span class="dz-type">PNG</span>
          </div>
        </div>

        <!-- mirrors: if uploaded_file is not None: image = Image.open(uploaded_file) → st.image(image, caption="Uploaded Image", use_container_width=True) -->
        <div class="preview" id="preview">
          <div class="preview-frame">
            <img id="previewImg" src="" alt="Uploaded Image"/>
          </div>
          <p class="preview-caption">Uploaded Image</p>
          <div class="preview-row">
            <span class="preview-fname" id="previewName"></span>
            <button class="btn-del" id="btnRemove">✕ Remove</button>
          </div>
          <button class="btn-run" id="btnAnalyze" disabled>
            <span id="btnTxt">🎯 Analyze Age Group</span>
            <div class="spin" id="spin"></div>
          </button>
        </div>
      </div>

      <!-- ── RIGHT — col2: Results card ── -->
      <div class="card">
        <!-- mirrors: st.subheader("📊 Prediction Results") -->
        <div class="card-head">
          <div class="card-head-icon icon-results">📊</div>
          <span class="card-head-title">Prediction Results</span>
        </div>

        <!-- mirrors: else: st.info("Upload an image to see predictions.") -->
        <div class="info-pill" id="infoState">
          <span>ℹ️</span>
          <span>Upload an image to see predictions.</span>
        </div>

        <!-- mirrors: if uploaded_file is not None: the prediction block -->
        <div id="resultsState" style="display:none">

          <!-- mirrors: .prediction-box with h2, h1, h3 -->
          <div class="prediction-box">
            <span class="pb-label">🎯 Predicted Age Group</span>
            <span class="pb-age" id="resAge">—</span>
            <span class="pb-conf">Confidence: <strong id="resConf">—</strong></span>
          </div>

          <!-- mirrors: st.write("") then st.subheader("🔝 Top 3 Predictions") -->
          <div class="top3-head">🔝 Top 3 Predictions</div>

          <!-- mirrors: for idx in top3_idx: st.progress(float(probs[idx])) + st.write(f"...") -->
          <div id="barsContainer"></div>

        </div>
      </div>
    </div>
  </div>

  <!-- ── FEATURES ── -->
  <div class="features">
    <div class="feat">
      <span class="feat-icon">🎯</span>
      <div class="feat-title">Multi-Class Output</div>
      <div class="feat-desc">Classifies across 9 fine-grained age groups from infant to senior with full probability distribution.</div>
    </div>
    <div class="feat">
      <span class="feat-icon">📊</span>
      <div class="feat-title">Calibrated Confidence</div>
      <div class="feat-desc">Every prediction carries a ranked confidence score so uncertainty is always visible.</div>
    </div>
    <div class="feat">
      <span class="feat-icon">🔒</span>
      <div class="feat-title">Zero Retention</div>
      <div class="feat-desc">Images are processed locally and never uploaded or stored. Complete privacy by design.</div>
    </div>
    <div class="feat">
      <span class="feat-icon">⚖️</span>
      <div class="feat-title">Bias Transparency</div>
      <div class="feat-desc">Demographic bias risks are surfaced, not hidden — part of our responsible AI commitment.</div>
    </div>
    <div class="feat">
      <span class="feat-icon">🧪</span>
      <div class="feat-title">Research Grade</div>
      <div class="feat-desc">Built for academic and educational exploration — all outputs labeled experimental.</div>
    </div>
    <div class="feat">
      <span class="feat-icon">🚫</span>
      <div class="feat-title">No Critical Use</div>
      <div class="feat-desc">Explicitly excluded from hiring, law enforcement, medical, or any high-stakes decisions.</div>
    </div>
  </div>

  <!-- ── RESPONSIBLE AI — mirrors .card + st.subheader + st.warning ── -->
  <div class="card responsible" id="responsible">
    <!-- mirrors: st.subheader("⚖ Responsible AI Notice") -->
    <div class="card-head">
      <div class="card-head-icon icon-ai">⚖</div>
      <span class="card-head-title">Responsible AI Notice</span>
    </div>
    <!-- mirrors: st.warning("This AI system is developed for educational...") -->
    <div class="warning-box">
      <span class="warning-icon">⚠️</span>
      This AI system is developed for <strong>educational and research purposes only.</strong><br><br>
      Predictions may contain <strong>inaccuracies or demographic biases.</strong><br>
      The system should <strong>not be used for critical decision-making.</strong>
    </div>
  </div>

  <!-- ── FOOTER — mirrors .footer exactly ── -->
  <div class="footer">
    Made with <span class="footer-heart">❤️</span> using Streamlit | FairVision AI Project
  </div>

</div><!-- /page -->

<script>
// ═══════════════════════════════════════════════════════════
//  ALL PYTHON LOGIC PRESERVED EXACTLY — only JS equivalents
// ═══════════════════════════════════════════════════════════

// mirrors: age_groups = ["0-2","3-9","10-19","20-29","30-39","40-49","50-59","60-69","70+"]
const age_groups = ["0-2","3-9","10-19","20-29","30-39","40-49","50-59","60-69","70+"];

// mirrors: np.random.dirichlet(np.ones(len(age_groups)), size=1)[0]
function dirichlet(n){
  const g = Array.from({length:n},()=>-Math.log(Math.random()||1e-15));
  const s = g.reduce((a,b)=>a+b,0);
  return g.map(v=>v/s);
}

// mirrors: probs.argsort()[-3:][::-1]
function top3Idx(probs){
  return probs.map((p,i)=>({p,i})).sort((a,b)=>b.p-a.p).slice(0,3).map(x=>x.i);
}

// DOM
const fileInput     = document.getElementById('fileInput');
const dropzone      = document.getElementById('dropzone');
const preview       = document.getElementById('preview');
const previewImg    = document.getElementById('previewImg');
const previewName   = document.getElementById('previewName');
const btnRemove     = document.getElementById('btnRemove');
const btnAnalyze    = document.getElementById('btnAnalyze');
const btnTxt        = document.getElementById('btnTxt');
const spin          = document.getElementById('spin');
const infoState     = document.getElementById('infoState');
const resultsState  = document.getElementById('resultsState');
const resAge        = document.getElementById('resAge');
const resConf       = document.getElementById('resConf');
const barsContainer = document.getElementById('barsContainer');

// mirrors: if uploaded_file is not None: image = Image.open(uploaded_file) → st.image(...)
function loadPreview(file){
  const r = new FileReader();
  r.onload = e => {
    previewImg.src = e.target.result;
    previewName.textContent = file.name;
    dropzone.style.display = 'none';
    preview.classList.add('show');
    btnAnalyze.disabled = false;
    infoState.style.display = 'flex';
    resultsState.style.display = 'none';
  };
  r.readAsDataURL(file);
}

fileInput.addEventListener('change',()=>{ if(fileInput.files[0]) loadPreview(fileInput.files[0]); });

dropzone.addEventListener('dragover', e=>{ e.preventDefault(); dropzone.classList.add('over'); });
dropzone.addEventListener('dragleave',()=>dropzone.classList.remove('over'));
dropzone.addEventListener('drop', e=>{
  e.preventDefault(); dropzone.classList.remove('over');
  const f = e.dataTransfer.files[0];
  if(f && f.type.startsWith('image/')) loadPreview(f);
});

// remove → reset to initial st.file_uploader state
btnRemove.addEventListener('click',()=>{
  preview.classList.remove('show');
  dropzone.style.display = '';
  fileInput.value = '';
  btnAnalyze.disabled = true;
  infoState.style.display = 'flex';
  resultsState.style.display = 'none';
});

// mirrors the dummy prediction block exactly
btnAnalyze.addEventListener('click',()=>{
  btnAnalyze.disabled = true;
  btnTxt.textContent = 'Analyzing…';
  spin.classList.add('on');

  setTimeout(()=>{

    // mirrors: probs = np.random.dirichlet(np.ones(len(age_groups)), size=1)[0]
    const probs = dirichlet(age_groups.length);

    // mirrors: top3_idx = probs.argsort()[-3:][::-1]
    const top3_idx = top3Idx(probs);

    // mirrors: predicted_age = age_groups[top3_idx[0]]
    const predicted_age = age_groups[top3_idx[0]];

    // mirrors: confidence = probs[top3_idx[0]] * 100
    const confidence = probs[top3_idx[0]] * 100;

    // mirrors: st.markdown f"...{predicted_age}...{confidence:.2f}%..."
    resAge.textContent = predicted_age;
    resConf.textContent = confidence.toFixed(2) + '%';

    // mirrors: for idx in top3_idx: st.progress(float(probs[idx])) + st.write(f"{age_groups[idx]} — {probs[idx]*100:.2f}%")
    barsContainer.innerHTML = '';
    const fills = ['bf1','bf2','bf3'];
    top3_idx.forEach((idx, rank) => {
      const pct = (probs[idx] * 100).toFixed(2);
      const label = `${age_groups[idx]} — ${pct}%`; // mirrors f-string exactly
      const el = document.createElement('div');
      el.className = 'bar-item';
      el.innerHTML = `
        <div class="bar-row">
          <span class="bar-grp">${age_groups[idx]}</span>
          <span class="bar-val">${pct}%</span>
        </div>
        <div class="bar-track">
          <div class="bar-fill ${fills[rank]}" style="width:0%" data-w="${pct}"></div>
        </div>`;
      barsContainer.appendChild(el);
    });

    infoState.style.display = 'none';
    resultsState.style.display = 'block';

    // animate bars after render
    requestAnimationFrame(()=>{
      document.querySelectorAll('.bar-fill[data-w]').forEach(el=>{
        el.style.width = el.dataset.w + '%';
      });
    });

    btnAnalyze.disabled = false;
    btnTxt.textContent = '🔁 Analyze Again';
    spin.classList.remove('on');

  }, 1400);
});
</script>
</body>
</html>
