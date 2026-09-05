import html

import streamlit as st


def configure_page():
    st.set_page_config(page_title="AI Study Assistant", page_icon="🤖", layout="wide")
    st.markdown(
        """
        <style>
        :root {
            --ink: #f4f7fb;
            --muted: #9ca8b8;
            --panel: #151b24;
            --line: #293241;
            --accent: #62d6c7;
            --accent-dark: #102d2d;
        }
        .stApp {
            background: radial-gradient(circle at 10% 0%, #1b2930 0%, #0d1118 42%, #090c11 100%);
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 0.35rem;
        }
        .brand-mark {
            display: grid;
            width: 2.5rem;
            height: 2.5rem;
            place-items: center;
            border: 1px solid #62d6c7;
            border-radius: 12px;
            color: #62d6c7;
            font-size: 1.35rem;
            background: #102d2d;
        }
        .brand h1 {
            margin: 0;
            color: var(--ink);
            font-size: 2.25rem;
            letter-spacing: 0;
        }
        .subtitle {
            margin: 0 0 2rem 3.3rem;
            color: var(--muted);
            font-size: 1rem;
        }
        div[data-testid="stRadio"] > label,
        div[data-testid="stTextArea"] > label {
            color: var(--ink);
            font-weight: 650;
        }
        div[data-testid="stRadio"] > div {
            gap: 0.65rem;
        }
        div[data-testid="stRadio"] label {
            min-height: 3.1rem;
            padding: 0.8rem 1rem;
            border: 1px solid var(--line);
            border-radius: 10px;
            background: rgba(21, 27, 36, 0.86);
        }
        div[data-testid="stRadio"] label:has(input:checked) {
            border-color: var(--accent);
            background: var(--accent-dark);
        }
        div[data-testid="stTextArea"] textarea {
            border: 1px solid var(--line);
            border-radius: 10px;
            background: var(--panel);
            color: var(--ink);
        }
        div[data-testid="stTextArea"] textarea:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent);
        }
        .section-label {
            margin: 1.5rem 0 0.55rem;
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        div.stButton > button[kind="primary"] {
            position: relative;
            overflow: hidden;
            width: 100%;
            min-height: 3rem;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 999px;
            background: #101010;
            color: #f4f7fb;
            font-weight: 750;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.2),
                inset 0 8px 16px rgba(255, 255, 255, 0.05),
                0 8px 20px rgba(0, 0, 0, 0.2);
            transition: border-color 400ms ease, box-shadow 400ms ease, transform 180ms ease;
        }
        div.stButton > button[kind="primary"]::before {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: linear-gradient(120deg, transparent 20%, rgba(98, 214, 199, 0.45), transparent 80%);
            background-size: 220% 100%;
            opacity: 0.35;
            pointer-events: none;
            animation: generate-sweep 3.2s ease-in-out infinite;
        }
        div.stButton > button[kind="primary"] p {
            position: relative;
            z-index: 1;
        }
        div.stButton > button[kind="primary"]:hover {
            border-color: rgba(98, 214, 199, 0.8);
            background: #151c1d;
            color: #ffffff;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.24),
                0 0 24px rgba(98, 214, 199, 0.22);
            transform: translateY(-1px);
        }
        div.stButton > button[kind="primary"]:active {
            transform: translateY(1px) scale(0.99);
        }
        @keyframes generate-sweep {
            0%, 35% { background-position: 180% 0; }
            70%, 100% { background-position: -20% 0; }
        }
        .result-title {
            margin-top: 2.25rem;
            padding-bottom: 0.7rem;
            border-bottom: 1px solid var(--line);
            color: var(--ink);
            font-size: 1.35rem;
            font-weight: 700;
        }
        .dashboard-intro {
            margin: 0 0 1.5rem;
            color: var(--muted);
        }
        .sidebar-title {
            color: var(--ink);
            font-size: 1.2rem;
            font-weight: 750;
        }
        .sidebar-copy {
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.5;
        }
        .status-dot {
            display: inline-block;
            width: 0.55rem;
            height: 0.55rem;
            margin-right: 0.4rem;
            border-radius: 50%;
            background: var(--accent);
        }
        .stats-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 2rem;
            max-width: 760px;
            margin: 0 auto 2rem;
            padding: 1.6rem 0 1.8rem;
            text-align: center;
            border-bottom: 1px solid rgba(156, 168, 184, 0.2);
        }
        .stat-label {
            color: var(--muted);
            font-size: 0.76rem;
            font-weight: 500;
        }
        .stat-value {
            min-height: 2.35rem;
            color: var(--ink);
            font-size: clamp(1.7rem, 4vw, 2.25rem);
            font-weight: 800;
            line-height: 1;
            letter-spacing: -0.02em;
            animation: stat-reveal 700ms ease both;
        }
        .stat-item:nth-child(2) .stat-value { animation-delay: 120ms; }
        .stat-item:nth-child(3) .stat-value { animation-delay: 240ms; }
        @keyframes stat-reveal {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (max-width: 640px) {
            .block-container { padding-top: 2rem; }
            .brand h1 { font-size: 1.8rem; }
            .subtitle { margin-left: 0; }
            div[data-testid="stRadio"] > div { flex-direction: column; }
            .stats-strip { gap: 0.8rem; }
            .stat-value { font-size: 1.45rem; }
        }
        .bento-card {
            min-height: 8.5rem;
            padding: 1rem 1.1rem 0.9rem;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: rgba(21, 27, 36, 0.72);
            transition: border-color 180ms ease, transform 180ms ease;
        }
        .bento-card:hover {
            border-color: var(--accent);
            transform: translateY(-2px);
        }
        .bento-icon {
            display: grid;
            width: 2.25rem;
            height: 2.25rem;
            margin-bottom: 0.8rem;
            place-items: center;
            border-radius: 9px;
            background: var(--accent-dark);
            color: var(--accent);
            font-size: 1.1rem;
        }
        .bento-title {
            color: var(--ink);
            font-size: 1rem;
            font-weight: 700;
        }
        .bento-subtitle {
            margin: 0.25rem 0 0;
            color: var(--muted);
            font-size: 0.78rem;
        }
        /* Workspace refresh */
        .stApp {
            background:
                radial-gradient(circle at 84% 4%, rgba(98, 214, 199, 0.12), transparent 28rem),
                linear-gradient(145deg, #080d12 0%, #0d141b 52%, #111820 100%);
        }
        .block-container {
            max-width: 1040px;
            padding-top: 3.2rem;
            padding-bottom: 4rem;
        }
        .hero {
            margin-bottom: 2.2rem;
        }
        .eyebrow {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: #7f909f;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        .live-dot {
            width: 0.45rem;
            height: 0.45rem;
            border-radius: 50%;
            background: #f4b860;
            box-shadow: 0 0 0 4px rgba(244, 184, 96, 0.12);
        }
        .hero-row {
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 2rem;
            margin-top: 0.8rem;
        }
        .hero h1 {
            max-width: 650px;
            margin: 0;
            color: #f6f8f8;
            font-size: clamp(2.2rem, 6vw, 4.8rem);
            font-weight: 800;
            line-height: 0.98;
            letter-spacing: -0.055em;
        }
        .hero h1 em {
            color: #62d6c7;
            font-style: normal;
        }
        .hero-copy {
            max-width: 440px;
            margin: 1rem 0 0;
            color: #91a0ad;
            font-size: 1rem;
            line-height: 1.6;
        }
        .model-chip {
            flex: 0 0 auto;
            padding: 0.65rem 0.85rem;
            border: 1px solid rgba(156, 168, 184, 0.22);
            border-radius: 999px;
            color: #b6c2cc;
            background: rgba(255, 255, 255, 0.035);
            font-size: 0.72rem;
            font-weight: 700;
        }
        .stats-strip {
            max-width: none;
            margin: 0 0 2.2rem;
            padding: 1.1rem 0;
            border-top: 1px solid rgba(156, 168, 184, 0.16);
            border-bottom: 1px solid rgba(156, 168, 184, 0.16);
        }
        .stat-value {
            color: #f6f8f8;
            font-size: clamp(1.35rem, 3vw, 2rem);
        }
        .stat-label {
            margin-top: 0.35rem;
            color: #71818f;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .section-heading {
            margin: 0 0 0.75rem;
            color: #e9eeee;
            font-size: 1.05rem;
            font-weight: 750;
        }
        .section-note {
            margin: -0.35rem 0 1rem;
            color: #7f909f;
            font-size: 0.86rem;
        }
        div[data-testid="stRadio"] > div {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
        }
        div[data-testid="stRadio"] label {
            min-height: 4.1rem;
            padding: 1rem 1.05rem;
            border: 1px solid rgba(156, 168, 184, 0.2);
            border-radius: 14px;
            background: rgba(19, 28, 37, 0.78);
            color: #bcc7ce;
            transition: border-color 180ms ease, background 180ms ease, transform 180ms ease;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: rgba(98, 214, 199, 0.65);
            transform: translateY(-2px);
        }
        div[data-testid="stRadio"] label:has(input:checked) {
            border-color: #62d6c7;
            background: linear-gradient(145deg, rgba(19, 66, 65, 0.95), rgba(16, 44, 47, 0.9));
            color: #f4fbfa;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.18), 0 0 0 1px rgba(98, 214, 199, 0.08);
        }
        div[data-testid="stExpander"] {
            margin-top: 0.65rem;
            border: 1px solid rgba(156, 168, 184, 0.16);
            border-radius: 12px;
            background: rgba(10, 16, 22, 0.42);
        }
        div[data-testid="stTextArea"] {
            margin-top: 1.25rem;
            padding: 0.85rem 1rem 0.75rem;
            border: 1px solid rgba(156, 168, 184, 0.2);
            border-radius: 12px;
            background: rgba(19, 28, 37, 0.7);
        }
        div[data-testid="stTextArea"] textarea {
            min-height: 82px;
            border: 0;
            background: transparent;
            font-size: 0.95rem;
            line-height: 1.45;
        }
        div[data-testid="stTextArea"] textarea:focus {
            border: 0;
            box-shadow: none;
        }
        .prompt-hint {
            margin: 0.7rem 0 0;
            color: #71818f;
            font-size: 0.75rem;
        }
        .result-title {
            margin-top: 2.4rem;
            padding: 1rem 0 0.8rem;
            border-top: 1px solid rgba(156, 168, 184, 0.2);
            border-bottom: 0;
            color: #f4f7fb;
            font-size: 1.1rem;
            letter-spacing: -0.01em;
        }
        div.stButton > button[kind="primary"] {
            margin-top: 0.75rem;
            min-height: 3.25rem;
            border-color: rgba(98, 214, 199, 0.45);
            background: #143e3e;
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.14);
        }
        @media (max-width: 700px) {
            .block-container { padding-top: 2rem; }
            .hero-row { display: block; }
            .model-chip { display: inline-block; margin-top: 1.2rem; }
            div[data-testid="stRadio"] > div { grid-template-columns: 1fr; }
            .stats-strip { gap: 0.7rem; }
        }
        /* Light workspace palette */
        :root {
            --ink: #1d2b2a;
            --muted: #687875;
            --panel: #ffffff;
            --line: #d9e3de;
            --accent: #148f83;
            --accent-dark: #e4f3ef;
        }
        .stApp {
            background:
                radial-gradient(circle at 88% 0%, rgba(244, 184, 96, 0.2), transparent 25rem),
                linear-gradient(145deg, #f7f8f3 0%, #eef5f1 54%, #f9f8f4 100%);
        }
        .hero h1 { color: #1d2b2a; }
        .hero h1 em { color: #148f83; }
        .eyebrow { color: #71817c; }
        .live-dot { background: #d8874d; box-shadow: 0 0 0 4px rgba(216, 135, 77, 0.14); }
        .hero-copy { color: #657570; }
        .model-chip {
            border-color: #d4e0da;
            color: #49605b;
            background: rgba(255, 255, 255, 0.7);
        }
        .stats-strip { border-color: #d7e1dc; }
        .stat-value { color: #1d2b2a; }
        .stat-label { color: #75847f; }
        .section-heading { color: #243532; }
        .section-note { color: #6b7b76; }
        div[data-testid="stRadio"] label {
            border-color: #d5e0db;
            background: rgba(255, 255, 255, 0.78);
            color: #50615c;
            box-shadow: 0 4px 14px rgba(46, 79, 69, 0.04);
        }
        div[data-testid="stRadio"] label:hover {
            border-color: #73b7aa;
            background: #ffffff;
        }
        div[data-testid="stRadio"] label:has(input:checked) {
            border-color: #148f83;
            background: linear-gradient(145deg, #e6f5f0, #d9eee8);
            color: #145e56;
            box-shadow: 0 10px 24px rgba(20, 143, 131, 0.1), 0 0 0 1px rgba(20, 143, 131, 0.08);
        }
        div[data-testid="stExpander"] {
            border-color: #d7e1dc;
            background: rgba(255, 255, 255, 0.6);
        }
        div[data-testid="stTextArea"] {
            border-color: #d3dfda;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 6px 16px rgba(42, 73, 64, 0.05);
        }
        div[data-testid="stTextArea"] textarea { color: #1d2b2a; }
        .prompt-hint { color: #788782; }
        .result-title { border-color: #d7e1dc; color: #243532; }
        div.stButton > button[kind="primary"] {
            border-color: #148f83;
            background: #148f83;
            color: #ffffff;
            box-shadow: 0 10px 22px rgba(20, 143, 131, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.24);
        }
        div.stButton > button[kind="primary"]::before {
            background: linear-gradient(120deg, transparent 20%, rgba(255, 255, 255, 0.52), transparent 80%);
        }
        div.stButton > button[kind="primary"]:hover {
            border-color: #0e756b;
            background: #0f7f74;
            color: #ffffff;
            box-shadow: 0 0 24px rgba(20, 143, 131, 0.24);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(model):
    model_name = html.escape(model.replace("google/", ""))
    st.markdown(
        f'''<div class="hero">
            <div class="eyebrow"><span class="live-dot"></span> AI study assistant / workspace</div>
            <div class="hero-row">
                <div>
                    <h1>Make studying feel <em>lighter.</em></h1>
                    <p class="hero-copy">Ask better questions, shape your notes, and turn recall into a daily habit.</p>
                </div>
                <div class="model-chip">{model_name} · online</div>
            </div>
        </div>''',
        unsafe_allow_html=True,
    )

def render_sidebar(model, api_configured):
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Study desk</div>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-copy">Your focused workspace for questions, summaries, and revision.</p>', unsafe_allow_html=True)
        st.divider()
        status = "Connected" if api_configured else "Needs API key"
        st.markdown(
            f'<p class="sidebar-copy"><span class="status-dot"></span>{status}</p>',
            unsafe_allow_html=True,
        )
        st.caption("Model")
        st.code(model, language=None)
        st.divider()
        st.caption("Session tips")
        st.markdown("- Start with a specific topic\n- Use summaries for revision\n- Generate MCQs to test recall")



def render_stats(model):
    history = st.session_state.get("history", [])
    latest = history[-1]["mode"] if history else "No activity yet"
    response_count = len(history)
    model_name = model.replace("google/", "")
    stats = [
        ("Responses", f'<span class="counter" data-target="{response_count}">0</span>'),
        ("Latest task", html.escape(latest)),
        ("Model", html.escape(model_name)),
    ]
    stat_markup = "".join(
        f'<div class="stat-item"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>'
        for label, value in stats
    )
    st.html(
        f'''<div class="stats-strip">{stat_markup}</div>
        <script>
        document.querySelectorAll('.counter').forEach((counter) => {{
            const target = Number(counter.dataset.target);
            const duration = 700;
            const started = performance.now();
            const update = (now) => {{
                const progress = Math.min((now - started) / duration, 1);
                counter.textContent = Math.floor(progress * target);
                if (progress < 1) requestAnimationFrame(update);
            }};
            requestAnimationFrame(update);
        }});
        </script>''',
        unsafe_allow_javascript=True,
    )


def render_bento_grid():
    cards = [
        ("?", "Ask a Question", "Get a clear explanation", "Answers tailored for college-level study, with examples when useful."),
        ("≡", "Summarize a Topic", "Turn notes into revision points", "Create a concise, exam-friendly summary with headings and bullet points."),
        ("✓", "Generate MCQs", "Test your recall", "Build five multiple-choice questions with answers and short explanations."),
    ]
    st.markdown('<h2 class="section-heading">What are you working on?</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Pick a mode, then give the assistant something specific to work with.</p>', unsafe_allow_html=True)
    options = [f"{icon}  {title}" for icon, title, _, _ in cards]
    selected = st.radio(
        "Choose a task",
        options,
        horizontal=True,
        key="task_mode",
        label_visibility="collapsed",
    )


def render_controls():
    st.markdown('<h2 class="section-heading">Your prompt</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Be as specific as you like. You can paste notes, a question, or a topic.</p>', unsafe_allow_html=True)
    if "topic" not in st.session_state:
        st.session_state.topic = ""

    topic = st.text_area(
        "Topic or question",
        height=100,
        key="topic",
        label_visibility="collapsed",
        placeholder="What do you want to understand today?",
    )
    st.markdown('<p class="prompt-hint">Press generate when you are ready. Your response will appear below.</p>', unsafe_allow_html=True)
    submitted = st.button("✦  Generate answer", type="primary", use_container_width=True)
    mode = st.session_state.get("task_mode", "?  Ask a Question").split("  ", 1)[-1]
    return mode, topic, submitted


def record_activity(mode, topic):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({"mode": mode, "topic": topic})


def show_result(result):
    st.markdown('<div class="result-title">Result</div>', unsafe_allow_html=True)
    st.write(result)


def show_error(error):
    message = str(error)
    if "401" in message:
        st.error("The OpenRouter API key is invalid. Create a new key on OpenRouter and update OPENROUTER_API_KEY in .env.")
    elif "rate limit" in message.lower():
        st.warning(message)
    else:
        st.error(f"API error: {message}")
