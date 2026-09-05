# ================================================================
# AI Resume Analyzer & Job Recommendations — Streamlit Application
# ================================================================
#
# COMPONENT MAP (top → bottom):
#   1. Imports & Page Config          — L1-16
#   2. Helper: _raw()                 — strips blank lines from HTML
#   3. Global CSS <style>             — all UI styling
#      ├─ Reset & base                — box-sizing, hide Streamlit chrome
#      ├─ .ui-background + keyframes  — fixed SVG bg, 6 animations
#      ├─ .hero                       — full-viewport hero section
#      ├─ .st-key-upload_section      — upload container + file uploader
#      ├─ .st-key-process_section     — (hidden, steps moved to footer)
#      ├─ .step-card / .steps-grid    — 3-column step cards
#      ├─ Analyze button CSS          — centered, large red pill button
#      ├─ .upload-warning             — red inline error text
#      ├─ Results CSS                 — metrics, skills, jobs, AI advice
#      ├─ Mobile @media               — responsive breakpoints 900/600px
#      └─ prefers-reduced-motion      — accessibility: disables animations
#   4. Background SVG                 — geometric shapes + patterns
#   5. render_background()            — injects SVG into fixed div
#   6. Hero Section                   — badge, title, subtitle
#   7. Upload Section                 — eyebrow, heading, file uploader,
#                                       Analyze Resume button
#   8. Session State                  — show_results, analyzed_file_id
#   9. Process Section (hidden)       — HTML exists but hidden via CSS
#  10. Analysis Trigger               — button click → warning or rerun
#  11. Results Section                — resume parsing, skill extraction,
#                                       scoring, metrics, skills box,
#                                       job cards, AI career advice
#  12. Footer — Three Steps           — "How it works" + 3 step cards
#
# SUPPORTING MODULES:
#   modules/resume_parser.py    — extract_text() reads PDF/DOCX
#   modules/skill_extractor.py  — extract_skills() via regex matching
#   modules/job_matcher.py      — recommend_jobs(), calculate_resume_score()
#   modules/ai_advisor.py       — generate_advice() via OpenRouter API
#   utils/helpers.py            — clean_text() utility (unused here)
# ================================================================

import html  # Used for escaping user-generated text in HTML output
import re
import streamlit as st  # Core UI framework

# --- Project module imports ---
from modules.ai_advisor import generate_advice        # LLM-powered career advice via OpenRouter
from modules.job_matcher import calculate_resume_score, recommend_jobs  # Score + job matching
from modules.resume_parser import extract_text         # PDF/DOCX text extraction (PyMuPDF + python-docx)
from modules.skill_extractor import extract_skills     # Regex-based skill detection from resume text


# --- Page configuration (must be the first Streamlit command) ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _raw(markup: str) -> str:
    """Strip blank lines from multiline HTML so st.markdown renders cleanly."""
    return "\n".join(line for line in markup.splitlines() if line.strip())


# ============================================================
# GLOBAL UI — All CSS styles injected as a single <style> block.
# Covers: reset, background animations, hero, upload, process,
#         step cards, analyze button, results, responsive, a11y.
# ============================================================

st.markdown(
    _raw(
        """
        <style>
        *, *::before, *::after { box-sizing: border-box; }
        html { scroll-behavior: smooth; background: #fff !important; }
        html, body {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            min-width: 0 !important;
            overflow-x: hidden !important;
        }
        body {
            font-family: "Plus Jakarta Sans", "Trebuchet MS", Arial, sans-serif;
            background: #fff !important;
        }
        [data-testid="stToolbar"],
        [data-testid="stHeader"],
        [data-testid="stStatusWidget"],
        [data-testid="stDecoration"],
        #MainMenu,
        footer { display: none !important; }
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main {
            background: transparent !important;
            overflow-x: hidden !important;
        }
        .block-container {
            width: 100% !important;
            max-width: none !important;
            margin: 0 !important;
            padding: 0 !important;
            background: #fff0 !important;
        }

        /* Fixed background is purely decorative. */
        .ui-background {
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            overflow: hidden;
            pointer-events: none;
        }
        .ui-background svg { width: 100%; height: 100%; display: block; }
        .bg-float-slow { animation: floatSlow 12s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }
        .bg-float-medium { animation: floatMedium 8s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }
        .bg-spin { animation: softSpin 22s linear infinite; transform-box: fill-box; transform-origin: center; }
        .bg-pulse { animation: softPulse 5s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
        .bg-drift-left { animation: driftLeft 10s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }
        .bg-drift-right { animation: driftRight 11s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }
        @keyframes floatSlow { from { transform: translate(-8px,-6px) rotate(-1deg); } to { transform: translate(12px,14px) rotate(2deg); } }
        @keyframes floatMedium { from { transform: translate(8px,0) rotate(1deg); } to { transform: translate(-12px,-15px) rotate(-2deg); } }
        @keyframes softSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes softPulse { 0%,100% { opacity:.83; transform:scale(1); } 50% { opacity:1; transform:scale(1.035); } }
        @keyframes driftLeft { from { transform:translateX(0); } to { transform:translateX(-18px); } }
        @keyframes driftRight { from { transform:translateX(0); } to { transform:translateX(18px); } }

        /* Hero */
        .hero {
            position: relative;
            z-index: 2;
            min-height: 65vh;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            text-align: center;
        }
        .hero-content {
            width: min(500px, 82vw);
            transform: translateY(2vh);
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 13px;
            border: 1px solid rgba(255,255,255,.5);
            border-radius: 999px;
            background: rgba(255,255,255,.12);
            backdrop-filter: blur(8px);
            color: #fff;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: .1em;
        }
        .hero-dot { width:6px; height:6px; border-radius:50%; background:#fff; box-shadow:0 0 14px #fff; }
        .hero h1 {
            margin: 17px 0 0;
            color:#fff !important;
            font-size: clamp(25px, 3.3vw, 45px);
            line-height:1.06;
            letter-spacing:-.04em;
            font-weight:900;
        }
        .hero p {
            margin: 15px auto 0;
            color:rgba(255,255,255,.95) !important;
            font-size: clamp(8px, .85vw, 12px);
            line-height:1.5;
            font-weight:700;
            letter-spacing:.14em;
            text-transform:uppercase;
        }

        /* The key-generated containers are the actual sections. */
        .st-key-upload_section,
        .st-key-process_section {
            position: relative !important;
            z-index: 3 !important;
            width: 100% !important;
            max-width: none !important;
            margin: 0 !important;
        }

        /* Upload section naturally flows under hero */
        .st-key-upload_section {
            padding: 40px 24px 80px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
        }
        .st-key-upload_section > div { width: 100% !important; }
        .upload-copy {
            width:min(720px,92vw);
            margin:0 auto 30px;
            text-align:center;
        }
        .eyebrow {
            margin:0 0 9px;
            color:#ff4747;
            font-size:11px;
            line-height:1.2;
            font-weight:900;
            letter-spacing:.16em;
            text-transform:uppercase;
        }
        .upload-copy h2,
        .process-copy h2 {
            margin:0;
            color:#17233f;
            font-size:clamp(28px,3.4vw,46px);
            line-height:1.08;
            letter-spacing:-.04em;
            font-weight:900;
        }
        .upload-copy p:last-child,
        .process-copy p:last-child {
            max-width:620px;
            margin:13px auto 0;
            color:#687289;
            font-size:13px;
            line-height:1.65;
        }

                /* ============================================================
           CUSTOM LOADING SCREEN
           ============================================================ */
        .analysis-loader {
            width: min(620px, 90vw);
            margin: 35px auto;
            padding: 45px 25px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            border: 1px solid rgba(255,255,255,.7);
            border-radius: 24px;
            background: rgba(255,255,255,.88);
            box-shadow: 0 20px 60px rgba(41,51,91,.14);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        .analysis-loader-spinner {
            width: 58px;
            height: 58px;
            border: 6px solid #e8ebf3;
            border-top: 6px solid #ff4747;
            border-right: 6px solid #874fff;
            border-radius: 50%;
            animation: resumeLoaderSpin 0.85s linear infinite;
            margin-bottom: 22px;
        }

        .analysis-loader-title {
            margin: 0;
            color: #17233f;
            font-size: 20px;
            font-weight: 900;
        }

        .analysis-loader-text {
            margin: 9px 0 0;
            color: #6f788d;
            font-size: 13px;
            line-height: 1.6;
        }

        @keyframes resumeLoaderSpin {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }
        /* Streamlit uploader, but no absolute-positioning tricks. */
        .st-key-upload_section [data-testid="stFileUploader"] {
            width:min(620px,92vw) !important;
            margin:0 auto !important;
        }
        .st-key-upload_section [data-testid="stFileUploader"] section {
            position:relative !important;
            width:100% !important;
            min-height:300px !important;
            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
            padding:28px !important;
            border:1.5px dashed rgba(66,75,105,.34) !important;
            border-radius:26px !important;
            background:rgba(255,255,255,.82) !important;
            box-shadow:0 24px 70px rgba(41,51,91,.10), inset 0 1px 0 rgba(255,255,255,.95) !important;
            backdrop-filter:blur(14px);
            transition:.25s ease !important;
        }
        .st-key-upload_section [data-testid="stFileUploader"] section:hover {
            transform:translateY(-3px);
            border-color:rgba(255,71,71,.6) !important;
            box-shadow:0 28px 80px rgba(41,51,91,.14) !important;
        }
        .st-key-upload_section [data-testid="stFileUploader"] section::before {
            content:"Drop your resume here";
            position:absolute;
            top:55px; left:0; right:0;
            color:#1b2744;
            font-size:clamp(17px,1.55vw,23px);
            font-weight:900;
            text-align:center;
            pointer-events:none;
        }
        .st-key-upload_section [data-testid="stFileUploader"] section::after {
            content:"PDF or DOCX  •  Max 200 MB";
            position:absolute;
            top:94px; left:0; right:0;
            color:#788197;
            font-size:11px;
            font-weight:600;
            text-align:center;
            pointer-events:none;
        }
        .st-key-upload_section [data-testid="stFileUploaderDropzoneInstructions"] { visibility:hidden !important; height:0 !important; }
        .st-key-upload_section [data-testid="stFileUploaderDropzone"] { width:100% !important; background:transparent !important; }
        .st-key-upload_section [data-testid="stFileUploaderDropzone"] > span {
            width:100% !important;
            margin-top:130px !important;
            min-height:110px !important;
            display:flex !important;
            flex-direction:column !important;
            align-items:center !important;
            justify-content:center !important;
            gap:12px !important;
        }
        .st-key-upload_section [data-testid="stFileUploader"] section:has([data-testid="stFileUploaderFile"]) [data-testid="stFileUploaderDropzone"] > span {
            width:100% !important;
            min-height:110px !important;
            margin-top:130px !important;
            gap:12px !important;
        }
        .st-key-upload_section [data-testid="stFileUploaderFile"] {
            order:1 !important;
            width:min(100%, 420px) !important;
            min-height:56px !important;
            margin:0 auto !important;
            overflow:hidden !important;
        }
        .st-key-upload_section [data-testid="stFileUploaderFile"] * {
            max-width:100% !important;
            overflow:hidden !important;
            text-overflow:ellipsis !important;
        }
        .st-key-upload_section [data-testid="stFileUploaderDropzone"] > span button {
            order:2 !important;
            min-height:90px !important;
                       padding:24px 60px !important;
                       border:0 !important;
                       border-radius:999px !important;
                       background:#ff4747 !important;
                       color:#fff !important;
                       font-size:24px !important;
                       font-weight:900 !important;
                       box-shadow:0 14px 32px rgba(255,71,71,.27) !important;
        }
        .st-key-upload_section [data-testid="stFileUploaderDropzone"] > span button:hover { background:#f53d3d !important; }

        /* Analysis flow sits directly after the Analyze Resume button. */
        .st-key-process_section {
            padding:0 !important;
            margin:0 !important;
            width:100% !important;
            display:block !important;
            background:transparent !important;
        }
        .process-copy { display:none; }
        .steps-grid { display:none !important; }
        .footer-steps-grid {
            width:min(1100px,94vw);
            margin:0 auto;
            display:grid;
            grid-template-columns:repeat(3,minmax(0,1fr));
            gap:18px;
        }
        .step-card {
            min-height:180px;
            padding:25px 23px;
            border:1px solid rgba(211,215,228,.95);
            border-radius:22px;
            background:rgba(255,255,255,.84);
            box-shadow:0 18px 54px rgba(38,48,87,.09);
            backdrop-filter:blur(13px);
            text-align:left;
            transition:transform .23s ease, box-shadow .23s ease;
        }
        .step-card:hover { transform:translateY(-5px); box-shadow:0 25px 65px rgba(38,48,87,.13); }
        .step-number {
            width:36px; height:36px;
            display:inline-flex;
            align-items:center; justify-content:center;
            border-radius:50%;
            background:#eef2ff;
            color:#3150e6;
            font-size:11px;
            font-weight:900;
        }
        .step-card h3 { margin:18px 0 8px; color:#1a2743; font-size:18px; font-weight:900; }
        .step-card p { margin:0; color:#6f788d; font-size:12px; line-height:1.65; }

        /* Analyze button — inside upload section, centered + large */
        .st-key-upload_section [data-testid="stButton"],
        .st-key-ai_advice_section [data-testid="stButton"] 
        { display:flex !important; width:792px !important; max-width:calc(100vw - 32px) !important; justify-content:center !important; margin:20px auto 0 !important; }

        .st-key-upload_section [data-testid="stButton"] > div,
        .st-key-ai_advice_section [data-testid="stButton"] > div {
            width:100% !important;
        }
        
        .st-key-upload_section [data-testid="stButton"] button,
        .st-key-ai_advice_section [data-testid="stButton"] button {
            width:100% !important;
            max-width:none !important;
            min-height:90px !important;
            padding:24px 60px !important;
            border:0 !important;
            border-radius:999px !important;
            background:#ff4747 !important;
            color:#fff !important;
            font-size:24px !important;
            font-weight:900 !important;
            box-shadow:0 14px 32px rgba(255,71,71,.27) !important;
        }
        .st-key-upload_section [data-testid="stButton"] button:hover,
        .st-key-ai_advice_section [data-testid="stButton"] button:hover { background:#f53d3d !important; transform:translateY(-2px); }
        .upload-warning { text-align:center; margin-top:12px; color:#d32f2f; font-size:14px; font-weight:700; }

        /*  AI Advice Section centering */
        .st-key-ai_advice_section {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }
        .st-key-ai_advice_section > div {
            width: min(720px, 92vw) !important;
            margin: 0 auto !important;
            text-align: center;
        }
        .st-key-ai_advice_section [data-testid="stSelectbox"] label,
        .st-key-ai_advice_section [data-testid="stTextInput"] label {
            display: none !important; /* Hide standard Streamlit labels to look cleaner */
        }
        
        /* Light mode styling for inputs (Dropdown and Text Input) */
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"],
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"] > div > div {
            min-height: 54px !important;
             border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 14px !important;
             background: rgba(255, 255, 255, 0.78) !important;
             color: #111827 !important;
            font-size: 14px !important;
             font-weight: 600 !important;
             box-shadow: 0 12px 30px rgba(31, 41, 55, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
             backdrop-filter: blur(14px) !important;
             -webkit-backdrop-filter: blur(14px) !important;
        }
         .st-key-ai_advice_section [data-testid="stSelectbox"] {
             width: max-content !important;
             min-width: 320px !important;
             max-width: 78vw !important;
             margin: 0 auto !important;
            align-self: center !important;
            color-scheme: light !important;
        }
        .st-key-ai_advice_section [data-testid="stSelectbox"] > div,
        .st-key-ai_advice_section [data-testid="stSelectbox"] [role="combobox"] {
            width: fit-content !important;
            min-width: 100% !important;
            max-width: 100% !important;
            background-color: #ffffff !important;
            color: #111827 !important;
            color-scheme: light !important;
         }
        /* Ensure dropdown text explicitly renders dark */
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"] *,
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"] svg {
                   color: #111827 !important;
               fill: #111827 !important;
               stroke: #111827 !important;
        }
        .st-key-ai_advice_section [data-testid="stSelectbox"],
        .st-key-ai_advice_section [data-testid="stSelectbox"] > div,
        .st-key-ai_advice_section [data-testid="stSelectbox"] > div > div,
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"] div {
            background: rgba(255, 255, 255, 0.78) !important;
            color: #111827 !important;
        }
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"] span,
        .st-key-ai_advice_section [data-testid="stSelectbox"] [data-baseweb="select"] input {
            white-space: nowrap !important;
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
        }
        .st-key-ai_advice_section [data-testid="stSelectbox"] [role="combobox"],
        .st-key-ai_advice_section [data-testid="stSelectbox"] [role="combobox"] *,
        .st-key-ai_advice_section [data-testid="stSelectbox"] [aria-selected="true"] {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
        }
        .st-key-ai_advice_section [data-testid="stTextInput"] input {
            min-height: 54px !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 14px !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            font-size: 14px !important;
            padding-left: 16px !important;
        }
        /* Light-mode dropdown menu and custom-question input */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"] {
            background:#ffffff !important;
            color:#000000 !important;
        }
        [role="option"] {
            color:#111827 !important;
            background:#ffffff !important;
            font-size:14px !important;
        }
        [role="option"]:hover,
        [role="option"][aria-selected="true"] {
            background:#f1f5f9 !important;
            color:#000000 !important;
        }
        .st-key-ai_advice_section [data-testid="stTextInput"] > div {
            background:#ffffff !important;
            border-radius:14px !important;
        }

        /* Results - removed white gradient background to blend with main SVG like Step 1 */
        #analysis-results { scroll-margin-top: 20px; }
        .results-wrap {
            position:relative;
            z-index:5;
            width:75%;
            margin:0 auto;
            padding:40px 24px 100px;
            background:transparent !important;
            border-top:none !important;
        }
        .results-inner { width:min(1100px,94vw); margin:0 auto; }
        .results-inner h2 { margin:0; color:#19243e; font-size:clamp(29px,3.2vw,43px); font-weight:900; letter-spacing:-.04em; }
        .results-inner .lead { color:#6a7388; line-height:1.6; margin:10px 0 28px; }
        .st-key-metrics_section {
            width:75% !important;
            margin:0 auto !important;
        }
        .st-key-metrics_section [data-testid="stMetric"] {
            width:100% !important;
        }
        .results-section-title {
            display:block !important;
            width:75% !important;
            margin:28px auto 14px !important;
            color:#1a2743 !important;
            font-size:24px !important;
            font-weight:900 !important;
            line-height:1.25 !important;
            text-align:left !important;
        }
        [data-testid="stMetric"] {
            width:75% !important;
            margin-left:auto !important;
            margin-right:auto !important;
            padding:20px !important;
            border:1px solid #e3e7ef !important;
            border-radius:18px !important;
            background:#fff !important;
            box-shadow:0 12px 34px rgba(37,46,79,.06) !important;
        }
        [data-testid="stMetricLabel"] { color:#6e7689 !important; }
        [data-testid="stMetricValue"] { color:#1a2743 !important; font-weight:900 !important; }
        .skill-box { width:75%; margin:0 auto; padding:18px 20px; border:1px solid #e2e6ef; border-radius:16px; background:#fff; color:#313b53; line-height:1.8; }
        .job-card 
        { 
         width:75%; margin:14px auto; padding:18px 20px; border:1px solid #e2e6ef; border-radius:18px; background:#fff; box-shadow:0 10px 30px rgba(41,49,78,.05); }
        .job-title 
        { margin-bottom:9px; color:#1b2744; font-weight:900; }
        .job-meta 
        { color:#737c90; font-size:12px; line-height:1.55; }
        
        /* Red → yellow → green gradient for every job match progress bar */
        [data-testid="stProgress"] [role="progressbar"] > div,
        [data-testid="stProgress"] > div > div,
        [data-testid="stProgress"] > div > div > div {
            background:linear-gradient(90deg, #ef4444 0%, #f59e0b 50%, #22c55e 100%) !important;
            border-radius:999px !important;
        }
        [data-testid="stProgress"] > div {
            width:75% !important;
            margin-left:auto !important;
            margin-right:auto !important;
            background:#e8edf3 !important;
            border-radius:999px !important;
        }
        .ai-response { margin-top:30px; padding:24px 28px; border:1px solid #ffd0cb; border-left:5px solid #ff4747; border-radius:16px; background:#fff7f6; color:#263049; line-height:1.75; overflow-wrap:anywhere; text-align:left; }
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label { color:#1a2238; }

        @media (max-width: 900px) {
            .steps-grid { grid-template-columns:1fr; width:min(560px,92vw); }
            .step-card { min-height:150px; }
        }
        @media (max-width: 600px) {
            .hero-content { width:min(330px,84vw); }
            .hero h1 { font-size:clamp(23px,7.8vw,34px); }
            .hero p { font-size:7px; letter-spacing:.09em; }
            .st-key-upload_section, .st-key-process_section { padding-left:16px !important; padding-right:16px !important; }
            .upload-copy h2, .process-copy h2 { font-size:clamp(25px,8vw,34px); }
            .upload-copy p:last-child, .process-copy p:last-child { font-size:12px; }
            .st-key-upload_section [data-testid="stFileUploader"] { width:92vw !important; }
            .st-key-upload_section [data-testid="stFileUploader"] section { min-height:260px !important; border-radius:20px !important; padding:20px !important; }
            .st-key-upload_section [data-testid="stFileUploader"] section::before { top:45px; font-size:16px; }
            .st-key-upload_section [data-testid="stFileUploader"] section::after { top:78px; font-size:9px; }
            .st-key-upload_section [data-testid="stFileUploaderDropzone"] > span { margin-top:108px !important; }
            .steps-grid { width:92vw; gap:12px; }
            .footer-steps-grid { width:92vw; grid-template-columns:1fr; gap:12px; }
            .step-card { padding:20px; border-radius:18px; }
            .st-key-upload_section [data-testid="stButton"] button,
            .st-key-ai_advice_section [data-testid="stButton"] button { min-height:70px !important; padding:18px 40px !important; font-size:18px !important; }
            .results-wrap { padding:60px 16px 74px; }
            .results-wrap,
            .results-section-title,
            .skill-box,
            .job-card,
            [data-testid="stMetric"],
            [data-testid="stProgress"] > div { width:92% !important; }
            .st-key-metrics_section { width:92% !important; }
            .st-key-metrics_section [data-testid="stMetric"] { width:100% !important; }
            .results-section-title { width:92% !important; margin-left:auto !important; margin-right:auto !important; }
        }
        @media (prefers-reduced-motion: reduce) {
            html { scroll-behavior:auto; }
            .bg-float-slow, .bg-float-medium, .bg-spin, .bg-pulse, .bg-drift-left, .bg-drift-right { animation:none !important; }
            .step-card, .st-key-upload_section [data-testid="stFileUploader"] section { transition:none !important; }
        }
        </style>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# BACKGROUND — Decorative SVG with geometric shapes, patterns,
# and 6 CSS animation classes (float, spin, pulse, drift).
# Renders as a fixed full-viewport layer behind all content.
# ============================================================
BACKGROUND_SVG = """
<svg
    viewBox="0 0 1000 600"
    preserveAspectRatio="xMidYMid slice"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
>
    <defs>
        <pattern id="diagonal-stripe" width="10" height="10"
                 patternTransform="rotate(45 0 0)"
                 patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="10"
                  stroke="#b9c9ff" stroke-width="4.5"/>
        </pattern>

        <pattern id="dot-grid" width="12" height="12"
                 patternUnits="userSpaceOnUse">
            <circle cx="3" cy="3" r="1.6" fill="#6956dc"/>
        </pattern>
    </defs>

    <!-- Top-left moving geometry -->
    <g class="bg-drift-left">
        <polygon points="270,-20 350,-20 295,45 225,45" fill="#3056ee"/>
        <polygon points="350,-20 430,-20 230,125 150,125" fill="#9336fd"/>
    </g>

    <!-- Top-right moving geometry -->
    <g class="bg-drift-right">
        <polygon points="705,110 705,140 677,135"
                 stroke="#2541b2" stroke-width="2"/>
        <polygon points="728,110 728,140 700,135"
                 stroke="#2541b2" stroke-width="2"/>
        <path d="M775 75 Q785 65 795 75 T815 75 T835 75"
              stroke="#874fff" stroke-width="2.5"
              stroke-linecap="round"/>
    </g>

    <!-- Left textures -->
    <g class="bg-float-slow">
        <rect x="25" y="185" width="58" height="105"
              fill="url(#diagonal-stripe)"/>
        <rect x="36" y="120" width="86" height="38"
              fill="url(#dot-grid)" opacity="0.65"/>
    </g>

    <!-- Small left orbit -->
    <circle cx="190" cy="205" r="7"
            stroke="#ff4747" stroke-width="2"/>

    <!-- Center circle -->
    <g class="bg-pulse">
        <circle cx="485" cy="292" r="190"
                stroke="#ff4d4d" stroke-width="2"/>
        <circle cx="485" cy="292" r="168"
                fill="#ff4d4d"/>
    </g>

    <!-- Inner orbit -->
    <g class="bg-spin">
        <circle cx="485" cy="292" r="178"
                stroke="#ffffff"
                stroke-opacity="0.13"
                stroke-width="1.5"
                stroke-dasharray="8 14"/>
    </g>

    <!-- Lower-left geometry -->
    <g class="bg-drift-left">
        <polygon points="-10,450 145,320 225,320 70,450" fill="#9336fd"/>
        <polygon points="-10,620 155,430 220,430 45,620" fill="#3056ee"/>
        <polygon points="20,450 145,270 205,270 75,450"
                 stroke="#ff4747" stroke-width="2"/>
    </g>

    <!-- Right-side geometry -->
    <g class="bg-float-medium">
        <rect x="888" y="280" width="54" height="108"
              fill="url(#diagonal-stripe)"/>
        <rect x="642" y="200" width="60" height="38"
              fill="url(#dot-grid)" opacity="0.6"/>
        <polygon points="780,290 880,190 955,190 850,290"
                 fill="#3056ee"/>
        <polygon points="735,250 855,135 955,135 955,145 840,250"
                 stroke="#874fff" stroke-width="2"/>
        <polygon points="785,250 955,95 955,130 815,250"
                 stroke="#2541b2" stroke-width="2"/>
    </g>

    <circle cx="764" cy="330" r="7"
            stroke="#874fff" stroke-width="2"/>

    <!-- Bottom-right -->
    <g class="bg-drift-right">
        <polygon points="570,620 740,380 810,380 640,620"
                 fill="#ff4d4d"/>
        <polygon points="650,620 770,430 835,430 715,620"
                 stroke="#2541b2" stroke-width="2"/>
        <rect x="840" y="460" width="100" height="40"
              fill="url(#dot-grid)" opacity="0.75"/>
    </g>

    <!-- Bottom accents -->
    <path d="M565 515 Q575 505 585 515 T605 515 T625 515"
          stroke="#874fff" stroke-width="2.5"
          stroke-linecap="round"/>

    <g class="bg-float-medium">
        <polygon points="0,-10 70,-10 25,35 0,35" fill="#3056ee"/>
        <polygon points="1000,-10 1000,55 920,55 985,-10" fill="#9336fd"/>
        <polygon points="0,555 75,490 125,490 20,600 0,600" fill="#9336fd"/>
        <polygon points="0,600 0,570 105,470 150,470 20,600" fill="#3056ee"/>
        <polygon points="900,600 1000,500 1000,600" fill="#ff4d4d"/>
        <polygon points="820,600 920,500 965,500 865,600"
                 stroke="#2541b2" stroke-width="2"/>
    </g>

    <circle cx="260" cy="375" r="6"
            stroke="#874fff" stroke-width="2"/>
    <circle cx="384" cy="500" r="7"
            stroke="#ff4747" stroke-width="2"/>
</svg>
"""


def render_background():
    """Inject the decorative SVG into a fixed div behind all page content."""
    st.markdown(
        _raw(f'<div class="ui-background" aria-hidden="true">{BACKGROUND_SVG}</div>'),
        unsafe_allow_html=True,
    )


render_background()


# ============================================================
# HERO — Full-viewport landing section with badge, title, and
# subtitle. Sits on top of the background SVG (z-index: 2).
# ============================================================

st.markdown(
    _raw(
        """
        <section class="hero">
            <div class="hero-content">
                <div class="hero-badge"><span class="hero-dot"></span> AI-POWERED CAREER ANALYSIS</div>
                <h1>AI Resume Analyzer &amp;<br>Job Recommendations</h1>
                <p>NLP • ML • LLM-powered career assistant</p>
            </div>
        </section>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# UPLOAD SECTION — Contains the eyebrow label, heading, file
# uploader (PDF/DOCX drag-and-drop), and the centered
# "Analyze Resume" button directly below the uploader.
# ============================================================

with st.container(key="upload_section"):
    st.markdown(
        _raw(
            """
            <div class="upload-copy">
                <p class="eyebrow">Step 01 • Upload</p>
                <h2>Start with your resume</h2>
                <p>Upload a clean PDF or DOCX and let the analyzer identify skills, estimate resume strength, and recommend relevant job roles.</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )

    # Analyze button — centered right below the uploader
    analyze_clicked = st.button(
        "Analyze Resume",
        icon=":material/auto_awesome:",
        type="primary",
        key="analyze_resume_button",
    )


# ============================================================
# STATE — Session state management. Tracks whether results are
# visible and which file was last analyzed. Resets results when
# the user uploads a different file.
# ============================================================

if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "analyzed_file_id" not in st.session_state:
    st.session_state.analyzed_file_id = None

current_file_id = (
    f"{uploaded_file.name}-{uploaded_file.size}"
    if uploaded_file is not None
    else None
)

if current_file_id != st.session_state.analyzed_file_id:
    st.session_state.show_results = False


# ============================================================
# PROCESS SECTION (HIDDEN) — The 3-step cards HTML still exists
# here but is hidden via CSS (display:none on .process-copy and
# .steps-grid). The steps are now rendered in the footer instead.
# ============================================================

with st.container(key="process_section"):
    st.markdown(
        _raw(
            """
            <div class="process-copy">
                <p class="eyebrow">Step 02 • Analyze</p>
                <h2>Three steps. One clear direction.</h2>
                <p>Follow a simple workflow from resume upload to analysis and recommendations without crowding the screen.</p>
            </div>
            <div class="steps-grid">
                <article class="step-card">
                    <span class="step-number">01</span>
                    <h3>Upload</h3>
                    <p>Add your latest PDF or DOCX resume and keep the analysis grounded in your actual resume content.</p>
                </article>
                <article class="step-card">
                    <span class="step-number">02</span>
                    <h3>Analyze</h3>
                    <p>Extract skills, calculate the resume score, and compare your profile with supported job roles.</p>
                </article>
                <article class="step-card">
                    <span class="step-number">03</span>
                    <h3>Get Recommendations</h3>
                    <p>Review matching roles, missing skills, and personalized AI career guidance.</p>
                </article>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# ANALYSIS TRIGGER — Handles "Analyze Resume" button click.
# If no file uploaded: shows a red inline warning below button.
# If file uploaded: sets show_results=True and reruns the app.
# ============================================================

if analyze_clicked:
    if uploaded_file is None:
        st.markdown(
            '<p class="upload-warning">⚠ Upload a PDF or DOCX resume first.</p>',
            unsafe_allow_html=True,
        )
    else:
        st.session_state.show_results = True
        st.session_state.analyzed_file_id = current_file_id
        st.rerun()


# ============================================================
# RESULTS — Shown only after successful analysis. Pipeline:
#   1. extract_text()         → read resume content
#   2. extract_skills()       → detect skills via regex
#   3. calculate_resume_score → compute score out of 100
#   4. Render: metrics cards, skills box, job cards with
#      match %, and AI career advice via OpenRouter LLM.
# ============================================================

if st.session_state.show_results and uploaded_file is not None:
    loader_placeholder = st.empty()

    loader_placeholder.markdown(
        """
        <div class="analysis-loader">
            <div class="analysis-loader-spinner"></div>
            <p class="analysis-loader-title">Analyzing Your Resume</p>
            <p class="analysis-loader-text">
                Extracting text, detecting skills, calculating your resume score,
                and preparing job recommendations...
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # --- Single spinner wrapping the entire analysis pipeline ---
    
        # Step 1: Extract text from uploaded PDF/DOCX
    try:
        resume_text = extract_text(uploaded_file)
    except Exception as error:
        st.error(f"Could not process the resume: {error}")
        st.stop()
    loader_placeholder.empty()
    if not resume_text or not resume_text.strip():
        st.error("Could not extract text from the uploaded resume.")
        st.stop()

        # Step 2: Detect skills using regex keyword matching
    try:
        skills = extract_skills(resume_text)
    except Exception as error:
        st.error(f"Skill extraction failed: {error}")
        st.stop()

        # Step 3: Calculate resume score (0-100)
    try:
        score = calculate_resume_score(resume_text, skills)
    except Exception as error:
        st.error(f"Resume scoring failed: {error}")
        st.stop()

    # --- Step 02 header banner: directly below the Analyze Resume button ---
    st.markdown('<div id="analysis-results"></div>', unsafe_allow_html=True)
    st.markdown(
        _raw(
            """
            <section class="results-wrap">
                <div class="upload-copy">
                    <p class="eyebrow">Step 02 • Analyze</p>
                    <h2>Analyze</h2>
                    <p>Extract skills, calculate the resume score, and compare your profile with supported job roles.</p>
                </div>
            </section>
            """
        ),
        unsafe_allow_html=True,
    )

    # --- Metric cards: Score, Skills Count, Word Count ---
    with st.container(key="metrics_section"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Resume Score", f"{score}/100")
        col2.metric("Skills Detected", len(skills))
        col3.metric("Resume Words", len(resume_text.split()))

    # --- Detected skills list (comma-separated in styled box) ---
    st.markdown('<div class="results-section-title">🧠 Detected Skills</div>', unsafe_allow_html=True)
    if skills:
        st.markdown(
            f'<div class="skill-box">{html.escape(", ".join(map(str, skills)))}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No supported skills were detected.")

    # --- Job recommendations: cards with match % + progress bars ---
    st.markdown('<div class="results-section-title">💼 Recommended Jobs</div>', unsafe_allow_html=True)
    try:
        jobs = recommend_jobs(skills)
    except Exception as error:
        st.error(f"Job recommendation failed: {error}")
        jobs = []

    if jobs:
        for job in jobs:
            title = job.get("title", "Unknown Job")
            match = job.get("match", 0)
            missing = job.get("missing", [])
            try:
                match_value = float(match)
            except (TypeError, ValueError):
                match_value = 0.0
            match_value = max(0.0, min(match_value, 100.0))
            st.markdown(
                f'<div class="job-card"><div class="job-title">{html.escape(str(title))} — {match_value:.0f}% match</div><div class="job-meta">Missing skills: {html.escape(", ".join(map(str, missing)) if missing else "None")}</div></div>',
                unsafe_allow_html=True,
            )
            st.progress(match_value / 100)
    else:
        st.info("No matching jobs found.")

    # --- Step 03 header: AI-powered recommendations ---
    st.markdown(
        _raw(
            """
            <div class="upload-copy" style="margin-top:50px;">
                <p class="eyebrow">Step 03 • Get Recommendations</p>
                <h2>Get Recommendations</h2>
                <p>Review matching roles, missing skills, and personalized AI career guidance.</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # --- AI Career Advice: text input + Generate button → OpenRouter LLM ---
    with st.container(key="ai_advice_section"):
        # We don't need the st.subheader because the Step 03 Header introduces this section
        # st.subheader("🤖 AI Career Advice")

        suggested_questions = [
            "How can I improve this resume for my target job?",
            "What are the most critical skills I'm missing?",
            "How can I make my experience sound more impactful?",
            "Write a short professional summary based on my resume.",
            "Custom question (type below)"
        ]
        
        selected_q = st.selectbox(
            "Suggested questions",
            options=suggested_questions,
            key="career_question_select",
        )

        selectbox_width_chars = max(32, len(selected_q) + 8)
        st.markdown(
            f"""
            <style>
            .st-key-ai_advice_section [data-testid="stSelectbox"],
            .st-key-ai_advice_section [data-testid="stSelectbox"] > div,
            .st-key-ai_advice_section [data-testid="stSelectbox"] [role="combobox"] {{
                width: {selectbox_width_chars}ch !important;
                max-width: 78vw !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        if selected_q == "Custom question (type below)":
            question = st.text_input(
                "Ask for personalized advice",
                placeholder="Type your custom question here...",
                key="career_question"
            )
        else:
            question = selected_q

        if st.button(
            "Generate Advice",
            type="primary",
            icon=":material/auto_awesome:",
            key="generate_advice_button",
        ):
            if not question.strip():
                st.warning("Please enter a question first.")
            else:

                advice_loader = st.empty()

                advice_loader.markdown(
                    """
                    <div class="analysis-loader">
                        <div class="analysis-loader-spinner"></div>
                        <p class="analysis-loader-title">Generating AI Career Advice</p>
                        <p class="analysis-loader-text">
                            Your resume is being reviewed by the AI.
                            Please wait while your personalized recommendations are generated...
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                try:
                    advice = generate_advice(resume_text, skills, question)
                except Exception as error:
                    st.error(f"AI advice generation failed: {error}")
                    advice = None
                finally:
                    advice_loader.empty()
                if advice:
                    cleaned_advice = str(advice)

                    cleaned_advice = re.sub(
                        r"(?m)^\s*\*+\s+",
                        "• ",
                        cleaned_advice,
                    )

                    cleaned_advice = re.sub(
                        r"\*+",
                        "",
                        cleaned_advice,
                    )

                    formatted_advice = html.escape(
                        cleaned_advice
                    ).replace("\n", "<br>")
                    st.markdown(
                        _raw(f'<div class="ai-response">{formatted_advice}</div>'),
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("No AI advice was generated.")


# ============================================================
# FOOTER — "How it works" section at the very bottom.
# It appears only after a successful Analyze Resume click.
# ============================================================

if st.session_state.get("show_results", False):
    st.markdown(
        _raw(
            """
            <footer style="position:relative; z-index:3; width:100%; padding:60px 24px 40px; background:linear-gradient(180deg,rgba(248,249,253,.98),rgba(241,243,250,1)); border-top:1px solid #e1e5ef; margin-top:40px;">
                <div style="width:min(1100px,94vw); margin:0 auto; text-align:center;">
                    <p class="eyebrow">How it works</p>
                    <h2 style="margin:0 0 8px; color:#17233f; font-size:clamp(24px,3vw,38px); font-weight:900; letter-spacing:-.04em;">Three steps. One clear direction.</h2>
                    <p style="max-width:620px; margin:0 auto 30px; color:#687289; font-size:13px; line-height:1.65;">Follow a simple workflow from resume upload to analysis and recommendations without crowding the screen.</p>
                </div>
                <div class="footer-steps-grid">
                    <article class="step-card">
                        <span class="step-number">01</span>
                        <h3>Upload</h3>
                        <p>Add your latest PDF or DOCX resume and keep the analysis grounded in your actual resume content.</p>
                    </article>
                    <article class="step-card">
                        <span class="step-number">02</span>
                        <h3>Analyze</h3>
                        <p>Extract skills, calculate the resume score, and compare your profile with supported job roles.</p>
                    </article>
                    <article class="step-card">
                        <span class="step-number">03</span>
                        <h3>Get Recommendations</h3>
                        <p>Review matching roles, missing skills, and personalized AI career guidance.</p>
                    </article>
                </div>
                <p style="text-align:center; margin:30px 0 0; color:#a0a8b8; font-size:11px;">AI Resume Analyzer &amp; Job Recommendations · NLP • ML • LLM</p>
            </footer>
            """
        ),
        unsafe_allow_html=True,
    )
