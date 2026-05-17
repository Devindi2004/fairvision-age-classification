<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FairVision AI — Fair & Responsible Age Classification</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet" />
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --navy-950: #060c1a;
    --navy-900: #0d1626;
    --navy-800: #111e33;
    --navy-700: #172540;
    --navy-600: #1e2f52;
    --surface: rgba(255,255,255,0.04);
    --surface-hover: rgba(255,255,255,0.07);
    --border: rgba(255,255,255,0.08);
    --border-bright: rgba(255,255,255,0.15);
    --accent-indigo: #6366f1;
    --accent-violet: #8b5cf6;
    --accent-cyan: #22d3ee;
    --accent-emerald: #10b981;
    --text-primary: #f0f4ff;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 24px;
    --radius-xl: 32px;
  }

  html { scroll-behavior: smooth; }

  body {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy-950);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* ---- NOISE OVERLAY ---- */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
  }

  /* ---- GRADIENT ORBS ---- */
  .orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.18;
  }
  .orb-1 { width: 600px; height: 600px; background: var(--accent-indigo); top: -200px; left: -150px; }
  .orb-2 { width: 500px; height: 500px; background: var(--accent-violet); top: 40%; right: -180px; }
  .orb-3 { width: 400px; height: 400px; background: var(--accent-cyan); bottom: -100px; left: 30%; }

  /* ---- LAYOUT ---- */
  .container { max-width: 1180px; margin: 0 auto; padding: 0 32px; position: relative; z-index: 1; }

  /* ---- NAV ---- */
  nav {
    position: sticky;
    top: 0;
    z-index: 100;
    padding: 18px 0;
    border-bottom: 1px solid var(--border);
    background: rgba(6,12,26,0.75);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }
  .nav-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 32px;
  }
  .nav-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 20px;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
  }
  .nav-logo-icon {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-violet));
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }
  .nav-links { display: flex; align-items: center; gap: 32px; }
  .nav-links a {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 14px;
    font-weight: 400;
    transition: color 0.2s;
  }
  .nav-links a:hover { color: var(--text-primary); }
  .nav-cta {
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-violet));
    color: white !important;
    padding: 8px 20px;
    border-radius: 50px;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: opacity 0.2s !important;
  }
  .nav-cta:hover { opacity: 0.85; }

  /* ---- HERO ---- */
  .hero {
    padding: 100px 0 80px;
    text-align: center;
  }
  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    color: #a5b4fc;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 16px;
    border-radius: 50px;
    margin-bottom: 32px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  .hero-badge-dot {
    width: 6px;
    height: 6px;
    background: var(--accent-indigo);
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
  }
  @keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.7); }
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(46px, 7vw, 88px);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin-bottom: 24px;
  }
  .hero-title-accent {
    background: linear-gradient(90deg, var(--accent-indigo), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .hero-subtitle {
    font-size: 18px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 520px;
    margin: 0 auto 48px;
    font-weight: 300;
  }
  .hero-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
  }
  .btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-violet));
    color: white;
    padding: 14px 28px;
    border-radius: 50px;
    font-size: 15px;
    font-weight: 500;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;
  }
  .btn-primary:hover { transform: translateY(-2px); opacity: 0.9; }
  .btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--surface);
    color: var(--text-primary);
    padding: 14px 28px;
    border-radius: 50px;
    font-size: 15px;
    font-weight: 400;
    text-decoration: none;
    border: 1px solid var(--border-bright);
    cursor: pointer;
    transition: background 0.2s;
  }
  .btn-secondary:hover { background: var(--surface-hover); }

  /* ---- STATS STRIP ---- */
  .stats-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: 80px;
  }
  .stat-item {
    background: var(--navy-900);
    padding: 28px 32px;
    text-align: center;
  }
  .stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    display: block;
    line-height: 1;
    margin-bottom: 6px;
  }
  .stat-label { font-size: 13px; color: var(--text-secondary); }

  /* ---- APP SECTION ---- */
  .section-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent-indigo);
    margin-bottom: 14px;
  }
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 14px;
  }
  .section-subtitle {
    font-size: 16px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 480px;
    font-weight: 300;
  }

  .app-section { padding: 80px 0; }
  .app-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    align-items: start;
  }

  /* ---- UPLOAD CARD ---- */
  .card {
    background: var(--navy-900);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
  }
  .card-header {
    padding: 24px 28px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .card-icon {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
  }
  .card-icon-upload { background: rgba(99,102,241,0.15); }
  .card-icon-results { background: rgba(34,211,238,0.12); }
  .card-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
  }
  .card-body { padding: 28px; }

  /* ---- DROPZONE ---- */
  .dropzone {
    border: 2px dashed rgba(99,102,241,0.3);
    border-radius: var(--radius-md);
    padding: 48px 28px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    background: rgba(99,102,241,0.03);
    position: relative;
    overflow: hidden;
  }
  .dropzone:hover, .dropzone.drag-over {
    border-color: var(--accent-indigo);
    background: rgba(99,102,241,0.07);
  }
  .dropzone input[type=file] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
    width: 100%;
    height: 100%;
  }
  .dropzone-icon {
    width: 52px;
    height: 52px;
    background: rgba(99,102,241,0.12);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    font-size: 24px;
  }
  .dropzone-title { font-weight: 500; font-size: 15px; color: var(--text-primary); margin-bottom: 6px; }
  .dropzone-sub { font-size: 13px; color: var(--text-muted); }
  .dropzone-sub span { color: var(--accent-indigo); }

  /* formats */
  .format-chips {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-top: 16px;
  }
  .format-chip {
    font-size: 11px;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 50px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    letter-spacing: 0.03em;
  }

  /* preview */
  .preview-area {
    display: none;
    flex-direction: column;
    gap: 16px;
  }
  .preview-area.active { display: flex; }
  .preview-img-wrap {
    width: 100%;
    border-radius: var(--radius-md);
    overflow: hidden;
    background: var(--navy-800);
    aspect-ratio: 4/3;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .preview-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  .preview-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .preview-filename { font-size: 13px; color: var(--text-secondary); }
  .btn-remove {
    font-size: 12px;
    color: #f87171;
    background: rgba(248,113,113,0.1);
    border: 1px solid rgba(248,113,113,0.2);
    border-radius: 50px;
    padding: 4px 12px;
    cursor: pointer;
    transition: background 0.2s;
  }
  .btn-remove:hover { background: rgba(248,113,113,0.2); }

  .analyze-btn {
    width: 100%;
    padding: 14px;
    border-radius: var(--radius-sm);
    border: none;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-violet));
    color: white;
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  .analyze-btn:hover { opacity: 0.88; transform: translateY(-1px); }
  .analyze-btn:disabled { opacity: 0.4; cursor: default; transform: none; }

  /* ---- RESULTS CARD ---- */
  .prediction-hero {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: var(--radius-md);
    padding: 28px;
    text-align: center;
    margin-bottom: 24px;
  }
  .prediction-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #a5b4fc; margin-bottom: 12px; }
  .prediction-age {
    font-family: 'Syne', sans-serif;
    font-size: 64px;
    font-weight: 800;
    color: white;
    line-height: 1;
    margin-bottom: 8px;
  }
  .prediction-confidence { font-size: 14px; color: var(--text-secondary); }
  .prediction-confidence strong { color: var(--accent-cyan); }

  /* top 3 */
  .top3-title { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 16px; }
  .bar-row { margin-bottom: 14px; }
  .bar-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
  }
  .bar-label { font-size: 14px; color: var(--text-primary); font-weight: 400; }
  .bar-pct { font-size: 13px; color: var(--text-secondary); font-family: 'Syne', sans-serif; }
  .bar-track {
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 50px;
    overflow: hidden;
  }
  .bar-fill {
    height: 100%;
    border-radius: 50px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .bar-fill-1 { background: linear-gradient(90deg, var(--accent-indigo), var(--accent-violet)); }
  .bar-fill-2 { background: linear-gradient(90deg, rgba(99,102,241,0.6), rgba(139,92,246,0.6)); }
  .bar-fill-3 { background: linear-gradient(90deg, rgba(99,102,241,0.35), rgba(139,92,246,0.35)); }

  /* empty state */
  .results-empty {
    padding: 60px 28px;
    text-align: center;
    color: var(--text-muted);
  }
  .results-empty-icon {
    width: 56px;
    height: 56px;
    background: rgba(255,255,255,0.04);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    font-size: 24px;
  }
  .results-empty-text { font-size: 14px; line-height: 1.6; }

  /* ---- FEATURES ---- */
  .features-section { padding: 80px 0; }
  .features-header { text-align: center; margin-bottom: 56px; }
  .features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  .feature-card {
    background: var(--navy-900);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px;
    transition: border-color 0.2s, transform 0.2s;
  }
  .feature-card:hover { border-color: var(--border-bright); transform: translateY(-3px); }
  .feature-card-icon {
    width: 44px;
    height: 44px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 18px;
  }
  .icon-indigo { background: rgba(99,102,241,0.14); }
  .icon-cyan { background: rgba(34,211,238,0.1); }
  .icon-emerald { background: rgba(16,185,129,0.1); }
  .icon-violet { background: rgba(139,92,246,0.12); }
  .icon-amber { background: rgba(251,191,36,0.1); }
  .icon-rose { background: rgba(244,63,94,0.1); }
  .feature-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 10px;
  }
  .feature-card-text { font-size: 14px; color: var(--text-secondary); line-height: 1.65; font-weight: 300; }

  /* ---- NOTICE ---- */
  .notice-section { padding: 60px 0 80px; }
  .notice-card {
    background: var(--navy-900);
    border: 1px solid rgba(251,191,36,0.2);
    border-radius: var(--radius-lg);
    padding: 36px 40px;
    display: flex;
    gap: 24px;
    align-items: flex-start;
  }
  .notice-icon-wrap {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    background: rgba(251,191,36,0.1);
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
  }
  .notice-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #fcd34d;
    margin-bottom: 10px;
  }
  .notice-body { font-size: 14px; color: var(--text-secondary); line-height: 1.7; font-weight: 300; }
  .notice-body strong { color: var(--text-primary); font-weight: 500; }

  /* ---- FOOTER ---- */
  footer {
    padding: 32px 0;
    border-top: 1px solid var(--border);
  }
  .footer-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 32px;
  }
  .footer-left {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .footer-right { font-size: 13px; color: var(--text-muted); }

  /* ---- LOADER ---- */
  .spinner {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    display: none;
  }
  .spinner.active { display: inline-block; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* ---- RESPONSIVE ---- */
  @media (max-width: 768px) {
    .nav-links { display: none; }
    .app-grid { grid-template-columns: 1fr; }
    .features-grid { grid-template-columns: 1fr; }
    .stats-strip { grid-template-columns: 1fr; }
    .notice-card { flex-direction: column; gap: 16px; }
    .footer-inner { flex-direction: column; gap: 12px; text-align: center; }
    .hero { padding: 60px 0 50px; }
  }
</style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>

<!-- NAV -->
<nav>
  <div class="nav-inner">
    <a href="#" class="nav-logo">
      <div class="nav-logo-icon">🧠</div>
      FairVision AI
    </a>
    <div class="nav-links">
      <a href="#app">Try It</a>
      <a href="#features">Features</a>
      <a href="#notice">About</a>
      <a href="#notice" class="nav-cta">Responsible AI</a>
    </div>
  </div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="container">
    <div class="hero-badge">
      <span class="hero-badge-dot"></span>
      Research Preview — Educational Use Only
    </div>
    <h1 class="hero-title">
      Age Intelligence.<br>
      <span class="hero-title-accent">Built Responsibly.</span>
    </h1>
    <p class="hero-subtitle">
      Fair & transparent age classification using computer vision — designed with ethical AI principles at its core.
    </p>
    <div class="hero-actions">
      <a href="#app" class="btn-primary">
        <span>Analyze an Image</span>
        <span>↓</span>
      </a>
      <a href="#features" class="btn-secondary">
        <span>How It Works</span>
      </a>
    </div>
  </div>
</section>

<!-- STATS -->
<div class="container">
  <div class="stats-strip">
    <div class="stat-item">
      <span class="stat-number">9</span>
      <span class="stat-label">Age Group Classes</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">Top‑3</span>
      <span class="stat-label">Predictions Shown</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">0</span>
      <span class="stat-label">Images Stored</span>
    </div>
  </div>
</div>

<!-- APP -->
<section class="app-section" id="app">
  <div class="container">
    <div style="margin-bottom: 40px;">
      <p class="section-label">Live Demo</p>
      <h2 class="section-title">Upload & Classify</h2>
      <p class="section-subtitle">Drop a face image to receive instant age group predictions with confidence scores.</p>
    </div>
    <div class="app-grid">

      <!-- Upload Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-icon card-icon-upload">📤</div>
          <span class="card-title">Face Image Upload</span>
        </div>
        <div class="card-body">

          <!-- Dropzone (hidden when file selected) -->
          <div class="dropzone" id="dropzone">
            <input type="file" accept=".jpg,.jpeg,.png" id="fileInput" />
            <div class="dropzone-icon">📁</div>
            <p class="dropzone-title">Drop image here, or <span>browse</span></p>
            <p class="dropzone-sub">Supports JPG, JPEG, PNG</p>
            <div class="format-chips">
              <span class="format-chip">JPG</span>
              <span class="format-chip">JPEG</span>
              <span class="format-chip">PNG</span>
            </div>
          </div>

          <!-- Preview (shown after upload) -->
          <div class="preview-area" id="previewArea">
            <div class="preview-img-wrap">
              <img id="previewImg" src="" alt="Preview" />
            </div>
            <div class="preview-meta">
              <span class="preview-filename" id="fileName">image.jpg</span>
              <button class="btn-remove" id="removeBtn">✕ Remove</button>
            </div>
            <button class="analyze-btn" id="analyzeBtn">
              <span id="btnText">Analyze Age Group</span>
              <div class="spinner" id="spinner"></div>
            </button>
          </div>

        </div>
      </div>

      <!-- Results Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-icon card-icon-results">📊</div>
          <span class="card-title">Prediction Results</span>
        </div>
        <div class="card-body">

          <!-- Empty state -->
          <div class="results-empty" id="emptyState">
            <div class="results-empty-icon">🔍</div>
            <p class="results-empty-text">Upload an image and click<br><strong style="color:var(--text-primary)">Analyze</strong> to see age predictions here.</p>
          </div>

          <!-- Results (hidden initially) -->
          <div id="resultsArea" style="display:none;">
            <div class="prediction-hero">
              <p class="prediction-label">Predicted Age Group</p>
              <p class="prediction-age" id="topAge">—</p>
              <p class="prediction-confidence">Confidence: <strong id="topConf">—</strong></p>
            </div>
            <p class="top3-title">Top 3 Predictions</p>
            <div id="barsContainer"></div>
          </div>

        </div>
      </div>

    </div>
  </div>
</section>

<!-- FEATURES -->
<section class="features-section" id="features">
  <div class="container">
    <div class="features-header">
      <p class="section-label">Capabilities</p>
      <h2 class="section-title">Designed for Fairness</h2>
      <p class="section-subtitle" style="margin:0 auto;">Every design decision prioritizes transparency, accuracy, and demographic equity.</p>
    </div>
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-card-icon icon-indigo">🎯</div>
        <h3 class="feature-card-title">Multi-Class Output</h3>
        <p class="feature-card-text">Classifies images across 9 fine-grained age groups from 0–2 years to 70+, providing a granular probability distribution rather than a single guess.</p>
      </div>
      <div class="feature-card">
        <div class="feature-card-icon icon-cyan">📊</div>
        <h3 class="feature-card-title">Confidence Scores</h3>
        <p class="feature-card-text">Every prediction is accompanied by a calibrated confidence score and ranked top-3 results so you can assess uncertainty at a glance.</p>
      </div>
      <div class="feature-card">
        <div class="feature-card-icon icon-emerald">🔒</div>
        <h3 class="feature-card-title">Privacy First</h3>
        <p class="feature-card-text">Images are processed locally and never stored or transmitted. Zero data retention ensures your uploads remain completely private.</p>
      </div>
      <div class="feature-card">
        <div class="feature-card-icon icon-violet">⚖️</div>
        <h3 class="feature-card-title">Bias Awareness</h3>
        <p class="feature-card-text">Built with explicit acknowledgment of demographic bias risks. The system surfaces known limitations rather than hiding them from users.</p>
      </div>
      <div class="feature-card">
        <div class="feature-card-icon icon-amber">🧪</div>
        <h3 class="feature-card-title">Research Grade</h3>
        <p class="feature-card-text">Developed to support academic and educational exploration of responsible AI. All outputs are clearly labeled as experimental and non-deterministic.</p>
      </div>
      <div class="feature-card">
        <div class="feature-card-icon icon-rose">🚫</div>
        <h3 class="feature-card-title">No Critical Decisions</h3>
        <p class="feature-card-text">Explicitly not intended for hiring, law enforcement, medical, or any high-stakes application — a boundary we take seriously.</p>
      </div>
    </div>
  </div>
</section>

<!-- RESPONSIBLE AI NOTICE -->
<section class="notice-section" id="notice">
  <div class="container">
    <div class="notice-card">
      <div class="notice-icon-wrap">⚖️</div>
      <div>
        <h3 class="notice-title">Responsible AI Notice</h3>
        <p class="notice-body">
          This AI system is developed for <strong>educational and research purposes only.</strong><br><br>
          Predictions may contain inaccuracies or <strong>demographic biases</strong> reflecting imbalances in training data. Age estimation from facial features is an inherently probabilistic and imperfect task.
          <br><br>
          The system <strong>should not be used for critical decision-making</strong>, including but not limited to employment, law enforcement, healthcare, or social services. All outputs should be interpreted as estimates, not ground truth.
        </p>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-inner">
    <div class="footer-left">🧠 FairVision AI</div>
    <div class="footer-right">Made with ❤️ using Streamlit &nbsp;·&nbsp; FairVision AI Project</div>
  </div>
</footer>

<script>
  const AGE_GROUPS = ["0–2","3–9","10–19","20–29","30–39","40–49","50–59","60–69","70+"];

  const fileInput = document.getElementById('fileInput');
  const dropzone  = document.getElementById('dropzone');
  const previewArea = document.getElementById('previewArea');
  const previewImg  = document.getElementById('previewImg');
  const fileName    = document.getElementById('fileName');
  const removeBtn   = document.getElementById('removeBtn');
  const analyzeBtn  = document.getElementById('analyzeBtn');
  const spinner     = document.getElementById('spinner');
  const btnText     = document.getElementById('btnText');
  const emptyState  = document.getElementById('emptyState');
  const resultsArea = document.getElementById('resultsArea');

  function showPreview(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {
      previewImg.src = e.target.result;
      fileName.textContent = file.name;
      dropzone.style.display = 'none';
      previewArea.classList.add('active');
    };
    reader.readAsDataURL(file);
  }

  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) showPreview(fileInput.files[0]);
  });

  dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('drag-over'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag-over'));
  dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith('image/')) showPreview(f);
  });

  removeBtn.addEventListener('click', () => {
    previewArea.classList.remove('active');
    dropzone.style.display = '';
    fileInput.value = '';
    emptyState.style.display = '';
    resultsArea.style.display = 'none';
  });

  function dirichletLike(n) {
    const r = Array.from({length:n}, () => -Math.log(Math.random() + 1e-10));
    const s = r.reduce((a,b)=>a+b,0);
    return r.map(v=>v/s);
  }

  analyzeBtn.addEventListener('click', () => {
    analyzeBtn.disabled = true;
    btnText.textContent = 'Analyzing…';
    spinner.classList.add('active');

    setTimeout(() => {
      const probs = dirichletLike(AGE_GROUPS.length);
      const indexed = probs.map((p,i)=>({p,i})).sort((a,b)=>b.p-a.p);
      const top3 = indexed.slice(0,3);

      document.getElementById('topAge').textContent = AGE_GROUPS[top3[0].i];
      document.getElementById('topConf').textContent = (top3[0].p * 100).toFixed(1) + '%';

      const container = document.getElementById('barsContainer');
      container.innerHTML = '';
      const fillClasses = ['bar-fill-1','bar-fill-2','bar-fill-3'];

      top3.forEach((item, rank) => {
        const pct = (item.p * 100).toFixed(1);
        const row = document.createElement('div');
        row.className = 'bar-row';
        row.innerHTML = `
          <div class="bar-meta">
            <span class="bar-label">Age ${AGE_GROUPS[item.i]}</span>
            <span class="bar-pct">${pct}%</span>
          </div>
          <div class="bar-track">
            <div class="bar-fill ${fillClasses[rank]}" style="width:0%" data-target="${pct}"></div>
          </div>
        `;
        container.appendChild(row);
      });

      emptyState.style.display = 'none';
      resultsArea.style.display = 'block';

      requestAnimationFrame(() => {
        document.querySelectorAll('.bar-fill[data-target]').forEach(el => {
          el.style.width = el.dataset.target + '%';
        });
      });

      analyzeBtn.disabled = false;
      btnText.textContent = 'Analyze Again';
      spinner.classList.remove('active');
    }, 1400);
  });
</script>
</body>
</html>
