"""
LearnIQ — Unified Portal
=========================
Single frontend hub that provides access to all 3 LearnIQ apps:
  - AI Chatbot (port 8501)
  - Teacher Dashboard (port 8502)
  - Student Dashboard (port 8503)

Run:  streamlit run portal.py --server.port 8500
"""

import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LearnIQ Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Server URLs ────────────────────────────────────────────────────────────────
SERVERS = {
    "chatbot": {"url": "http://localhost:8501", "port": 8501},
    "teacher": {"url": "http://localhost:8502", "port": 8502},
    "student": {"url": "http://localhost:8503", "port": 8503},
}

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Remove Streamlit default padding for full-width iframe */
    .main .block-container {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 100%;
    }

    /* ── Portal header ─────────────────────────────────────────────────── */
    .portal-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem 2rem;
        border-radius: 14px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .portal-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; }
    .portal-header p  { margin: 0.2rem 0 0 0; font-size: 0.9rem; opacity: 0.85; }

    /* ── Nav cards (landing view) ──────────────────────────────────────── */
    .nav-card {
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        color: white;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .nav-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .nav-card .icon  { font-size: 3rem; margin-bottom: 0.6rem; }
    .nav-card .title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem; }
    .nav-card .desc  { font-size: 0.85rem; opacity: 0.9; line-height: 1.4; }

    .card-chatbot  { background: linear-gradient(135deg, #667eea, #764ba2); }
    .card-teacher  { background: linear-gradient(135deg, #ff6b6b, #ee5a24); }
    .card-student  { background: linear-gradient(135deg, #00b894, #00cec9); }

    /* ── Embedded iframe ───────────────────────────────────────────────── */
    .app-frame {
        width: 100%;
        height: 82vh;
        border: none;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }

    /* ── Back button area ──────────────────────────────────────────────── */
    .back-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.8rem;
    }

    /* ── Mobile responsive ─────────────────────────────────────────────── */
    @media (max-width: 768px) {
        .main .block-container { padding: 0.8rem 1rem; }
        .portal-header h1 { font-size: 1.4rem; }
        .nav-card { min-height: 160px; padding: 1.2rem 1rem; }
        .nav-card .icon { font-size: 2.2rem; }
        .nav-card .title { font-size: 1.1rem; }
        .app-frame { height: 75vh; }
    }
</style>
""", unsafe_allow_html=True)

# ── Session state for navigation ───────────────────────────────────────────────
if "active_view" not in st.session_state:
    st.session_state.active_view = "home"


def set_view(view):
    st.session_state.active_view = view


# ── Header (always visible) ───────────────────────────────────────────────────
st.markdown(
    """<div class="portal-header">
        <h1>🎓 LearnIQ Portal</h1>
        <p>CBSE Grade 8 Science &mdash; AI Tutoring Platform</p>
    </div>""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
# HOME VIEW — Three navigation cards
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_view == "home":
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            """<div class="nav-card card-chatbot">
                <div class="icon">🔬</div>
                <div class="title">AI Chatbot</div>
                <div class="desc">Ask any question from your NCERT Science textbook. Get answers with chapter citations.</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Open Chatbot", key="btn_chatbot", use_container_width=True, type="primary"):
            set_view("chatbot")
            st.rerun()

    with col2:
        st.markdown(
            """<div class="nav-card card-teacher">
                <div class="icon">📋</div>
                <div class="title">Teacher Dashboard</div>
                <div class="desc">Review student performance, topic gaps, and low-confidence answers.</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Open Teacher Dashboard", key="btn_teacher", use_container_width=True, type="primary"):
            set_view("teacher")
            st.rerun()

    with col3:
        st.markdown(
            """<div class="nav-card card-student">
                <div class="icon">📈</div>
                <div class="title">Student Dashboard</div>
                <div class="desc">Track your learning progress, mastered topics, and areas to improve.</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Open Student Dashboard", key="btn_student", use_container_width=True, type="primary"):
            set_view("student")
            st.rerun()

    st.markdown("---")
    st.caption("All three apps are running locally. Click any card above to open it embedded in this portal.")

# ══════════════════════════════════════════════════════════════════════════════
# EMBEDDED APP VIEWS — iframe with back navigation
# ══════════════════════════════════════════════════════════════════════════════
else:
    view = st.session_state.active_view
    labels = {
        "chatbot": ("🔬 AI Chatbot", SERVERS["chatbot"]["url"]),
        "teacher": ("📋 Teacher Dashboard", SERVERS["teacher"]["url"]),
        "student": ("📈 Student Dashboard", SERVERS["student"]["url"]),
    }
    label, url = labels[view]

    # Navigation bar: back button + quick-switch tabs
    nav_cols = st.columns([1, 1, 1, 1])
    with nav_cols[0]:
        if st.button("← Home", use_container_width=True):
            set_view("home")
            st.rerun()
    with nav_cols[1]:
        if st.button("🔬 Chatbot", use_container_width=True,
                      type="primary" if view == "chatbot" else "secondary"):
            set_view("chatbot")
            st.rerun()
    with nav_cols[2]:
        if st.button("📋 Teacher", use_container_width=True,
                      type="primary" if view == "teacher" else "secondary"):
            set_view("teacher")
            st.rerun()
    with nav_cols[3]:
        if st.button("📈 Student", use_container_width=True,
                      type="primary" if view == "student" else "secondary"):
            set_view("student")
            st.rerun()

    # Embedded iframe
    st.markdown(
        f'<iframe src="{url}" class="app-frame" title="{label}"></iframe>',
        unsafe_allow_html=True,
    )
