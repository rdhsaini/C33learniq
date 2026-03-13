"""
LearnIQ — Teacher Dashboard
============================
Standalone Streamlit dashboard for teachers to review student Q&A performance.
Analyzes student_qa_logs_chapter1.json for topic gaps, low-confidence answers,
and student engagement metrics.

Run:  streamlit run teacher_dashboard.py
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
    .main .block-container { padding-top: 1.5rem; max-width: 1100px; }
    .dash-header {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .dash-header h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    .dash-header p { margin: 0.3rem 0 0 0; font-size: 0.95rem; opacity: 0.9; }
    .alert-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
    }
    @media (max-width: 768px) {
        .main .block-container { padding-left: 1rem; padding-right: 1rem; }
        .dash-header h1 { font-size: 1.4rem; }
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
        page_title="LearnIQ - Teacher Dashboard",
        page_icon="📋",
        layout="wide",
    )
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

    # Header
    st.markdown(
        """<div class="dash-header">
            <h1>📋 LearnIQ Teacher Dashboard</h1>
            <p>Student performance insights — CBSE Grade 8 Science, Chapter 1</p>
        </div>""",
        unsafe_allow_html=True,
    )

    df = load_data()

    # ── Key Metrics Row ───────────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Questions", len(df))
    col2.metric("Unique Students", df["student_id"].nunique())
    col3.metric("Topics Covered", df["topic_tag"].nunique())
    col4.metric("Avg Confidence", f"{df['confidence'].mean():.2f}")
    low_conf_count = int((df["confidence"] < 0.85).sum())
    col5.metric("Low Confidence", low_conf_count, delta=f"-{low_conf_count}" if low_conf_count else "0")

    st.markdown("---")

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Topic Analysis",
        "⚠️ At-Risk Answers",
        "👩‍🎓 Student View",
        "📋 Full Q&A Log",
    ])

    with tab1:
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Questions per Topic")
            topic_counts = df["topic_tag"].value_counts()
            st.bar_chart(topic_counts, color="#667eea", height=400)

        with col_right:
            st.subheader("Average Confidence per Topic")
            topic_conf = df.groupby("topic_tag")["confidence"].mean().sort_values()
            st.bar_chart(topic_conf, color="#ff6b6b", height=400)

        st.subheader("Confidence Score Distribution")
        hist_data = df["confidence"].value_counts(bins=10).sort_index()
        st.bar_chart(hist_data, color="#fdcb6e")

    with tab2:
        st.subheader("Questions Where AI Confidence < 85%")
        st.caption("These answers may need teacher review or follow-up.")

        low_conf_df = df[df["confidence"] < 0.85].sort_values("confidence")
        if len(low_conf_df) > 0:
            for _, row in low_conf_df.iterrows():
                with st.expander(f"🔴 {row['student_id']} — Confidence: {row['confidence']:.0%}"):
                    st.markdown(f"**Question:** {row['question']}")
                    st.markdown(f"**AI Answer:** {row['ai_answer']}")
                    st.markdown(f"**Topic:** `{row['topic_tag']}`")
        else:
            st.success("All questions were answered with high confidence!")

    with tab3:
        st.subheader("Per-Student Summary")
        student_stats = df.groupby("student_id").agg(
            questions=("question", "count"),
            avg_confidence=("confidence", "mean"),
            topics=("topic_tag", "nunique"),
        ).sort_values("avg_confidence")

        st.dataframe(student_stats, use_container_width=True)

    with tab4:
        st.subheader("Complete Question Log")

        # Filters
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            topic_filter = st.multiselect(
                "Filter by Topic",
                options=sorted(df["topic_tag"].unique()),
                default=[],
            )
        with col_f2:
            conf_threshold = st.slider("Min Confidence", 0.0, 1.0, 0.0, 0.05)

        filtered = df.copy()
        if topic_filter:
            filtered = filtered[filtered["topic_tag"].isin(topic_filter)]
        filtered = filtered[filtered["confidence"] >= conf_threshold]

        st.dataframe(
            filtered[["student_id", "question", "ai_answer", "confidence", "topic_tag"]],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(f"Showing {len(filtered)} of {len(df)} records")

    # ── Sidebar ────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔗 Navigation")
        st.caption("Run the chatbot:")
        st.code("streamlit run learniq_chatbot.py", language="bash")
        st.markdown("---")
        st.markdown("### 📌 Key Insights")
        most_asked = df["topic_tag"].value_counts().index[0]
        lowest_conf_topic = df.groupby("topic_tag")["confidence"].mean().idxmin()
        st.markdown(f"- **Most asked topic:** `{most_asked}`")
        st.markdown(f"- **Weakest topic:** `{lowest_conf_topic}`")
        st.markdown(f"- **{low_conf_count}** answers need review")


if __name__ == "__main__":
    main()
