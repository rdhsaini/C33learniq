"""
LearnIQ — Student Dashboard
=============================
Standalone Streamlit dashboard for students to track their learning progress.
Shows topics explored, question history, and confidence trends.

Run:  streamlit run student_dashboard.py
"""

import os
import json
import streamlit as st
import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────
QA_LOGS_PATH = os.path.join(os.path.dirname(__file__), "..", "student_qa_logs_chapter1.json")

# ── Custom CSS ─────────────────────────────────────────────────────────────────
DASHBOARD_CSS = """
<style>
    .main .block-container { padding-top: 1.5rem; max-width: 1000px; }
    .student-header {
        background: linear-gradient(135deg, #00b894, #00cec9);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .student-header h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    .student-header p { margin: 0.3rem 0 0 0; font-size: 0.95rem; opacity: 0.9; }
    .progress-badge {
        display: inline-block;
        background: #d4edda;
        color: #155724;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 4px;
    }
    @media (max-width: 768px) {
        .main .block-container { padding-left: 1rem; padding-right: 1rem; }
        .student-header h1 { font-size: 1.4rem; }
    }
</style>
"""


def load_data():
    """Loads student Q&A logs from JSON file."""
    if not os.path.exists(QA_LOGS_PATH):
        st.error(f"Q&A logs not found at: {QA_LOGS_PATH}")
        st.stop()
    with open(QA_LOGS_PATH, "r") as f:
        return pd.DataFrame(json.load(f))


def main():
    st.set_page_config(
        page_title="LearnIQ - Student Dashboard",
        page_icon="📈",
        layout="centered",
    )
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

    # Header
    st.markdown(
        """<div class="student-header">
            <h1>📈 My Learning Dashboard</h1>
            <p>Track your CBSE Grade 8 Science progress</p>
        </div>""",
        unsafe_allow_html=True,
    )

    df = load_data()

    # ── Student selector ──────────────────────────────────────────────────
    students = sorted(df["student_id"].unique())
    selected_student = st.selectbox("Select your Student ID", ["All Students"] + students)

    if selected_student != "All Students":
        df = df[df["student_id"] == selected_student]

    # ── Summary Metrics ───────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Questions Asked", len(df))
    col2.metric("Topics Covered", df["topic_tag"].nunique())
    col3.metric("Avg Confidence", f"{df['confidence'].mean():.0%}")
    high_conf = int((df["confidence"] >= 0.90).sum())
    col4.metric("Strong Answers (90%+)", high_conf)

    st.markdown("---")

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📊 My Progress", "📝 Question History", "🎯 Areas to Improve"])

    with tab1:
        st.subheader("Topics You've Explored")
        topic_counts = df["topic_tag"].value_counts()
        st.bar_chart(topic_counts, color="#00b894", height=350)

        st.subheader("Your Confidence Scores")
        hist_data = df["confidence"].value_counts(bins=10).sort_index()
        st.bar_chart(hist_data, color="#fdcb6e")

        # Topic badges
        st.subheader("Topics Mastered (Avg Confidence > 90%)")
        topic_avg = df.groupby("topic_tag")["confidence"].mean()
        mastered = topic_avg[topic_avg >= 0.90].index.tolist()
        if mastered:
            badges_html = " ".join(
                f'<span class="progress-badge">✅ {t.replace("_", " ").title()}</span>'
                for t in mastered
            )
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.info("Keep practicing! Mastered topics (90%+ confidence) will appear here.")

    with tab2:
        st.subheader("Your Questions & Answers")
        st.dataframe(
            df[["question", "ai_answer", "confidence", "topic_tag"]].sort_values(
                "confidence", ascending=False
            ),
            use_container_width=True,
            hide_index=True,
        )

    with tab3:
        st.subheader("Topics That Need More Practice")
        st.caption("Focus on topics where AI confidence was below 85%")

        weak_topics = topic_avg[topic_avg < 0.85].sort_values()
        if len(weak_topics) > 0:
            st.bar_chart(weak_topics, color="#e17055")

            st.subheader("Questions to Revisit")
            weak_df = df[df["confidence"] < 0.85][["question", "topic_tag", "confidence"]]
            st.dataframe(weak_df.sort_values("confidence"), use_container_width=True, hide_index=True)
        else:
            st.success("Great job! All your topics are above 85% confidence.")

    # ── Sidebar ────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔗 Navigation")
        st.caption("Back to chatbot:")
        st.code("streamlit run learniq_chatbot.py", language="bash")
        st.markdown("---")
        st.markdown("### 🏆 Quick Stats")
        st.markdown(f"- **{len(df)}** questions asked")
        st.markdown(f"- **{df['topic_tag'].nunique()}** topics explored")
        if len(mastered) > 0:
            st.markdown(f"- **{len(mastered)}** topics mastered")


if __name__ == "__main__":
    main()
