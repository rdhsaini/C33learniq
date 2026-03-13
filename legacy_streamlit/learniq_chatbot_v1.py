"""
LearnIQ — AI Tutoring Chatbot for CBSE Grade 8 Science (NCERT)
================================================================
RAG pipeline: PDF -> Chunks -> Embeddings -> ChromaDB -> RetrievalQA -> Streamlit UI

Features:
  - Chat interface with full history
  - Chapter source citation badges on every answer
  - Sidebar: topic distribution chart from student Q&A logs
  - Sidebar: Teacher Dashboard CTA button -> opens teacher_dashboard.py
  - Rate limiter to stay within $5 budget
  - Mobile-responsive, visually appealing UI

Run:  streamlit run learniq_chatbot.py
Pre-req: python learniq_ingest.py  (run once to build vector store)
"""

import os
import json
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ── Load environment variables ─────────────────────────────────────────────────
load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Configuration
# ══════════════════════════════════════════════════════════════════════════════

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ CHECKPOINT #3 — CHANGE THIS 1 VARIABLE FOR A DIFFERENT SUBJECT/GRADE     ║
# ║ Update SUBJECT_CONFIG with the new subject details and chroma_dir path.   ║
# ╚════════════════════════════════════════════════════════════════════════════╝
SUBJECT_CONFIG = {
    "subject": "Science",
    "grade": "Grade 8",
    "curriculum": "CBSE",
    "chroma_dir": os.path.join(os.path.dirname(__file__), "chroma_db"),
}

PERSIST_DIR = SUBJECT_CONFIG["chroma_dir"]
EMBEDDING_MODEL = "text-embedding-3-small"   # $0.02/1M tokens
LLM_MODEL = "gpt-4o-mini"                   # ~$0.15/1M input, $0.60/1M output
TOP_K = 4                                    # source chunks retrieved per query
MAX_QUERIES_PER_SESSION = 100                # rate limiter for cost control

# Path to student Q&A logs for sidebar dashboard chart
QA_LOGS_PATH = os.path.join(os.path.dirname(__file__), "..", "student_qa_logs_chapter1.json")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Load Vector Store (from pre-built ChromaDB)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner="Loading textbook index...")
def load_vector_store():
    """
    Loads the pre-built ChromaDB vector store from disk.
    Run learniq_ingest.py first to build the store.
    Zero cost — no API calls, just reads from local files.
    """
    if not os.path.exists(PERSIST_DIR) or not os.listdir(PERSIST_DIR):
        st.error(
            "Vector store not found. Run the ingestion script first:\n\n"
            "```\npython learniq_ingest.py\n```"
        )
        st.stop()

    # ╔════════════════════════════════════════════════════════════════════════╗
    # ║ CHECKPOINT #2 — SWAP ChromaDB FOR Pinecone (2 lines to change):      ║
    # ║                                                                      ║
    # ║   Line 1: from langchain_pinecone import PineconeVectorStore         ║
    # ║   Line 2: vectorstore = PineconeVectorStore(                         ║
    # ║               index_name="learniq", embedding=embeddings)            ║
    # ╚════════════════════════════════════════════════════════════════════════╝
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(                            # <- Line 1: change class
        persist_directory=PERSIST_DIR,               # <- Line 2: remove for Pinecone
        embedding_function=embeddings,
    )
    return vectorstore


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — RetrievalQA Chain with Strict System Prompt
# ══════════════════════════════════════════════════════════════════════════════

# System prompt enforces retrieval-only answers — no hallucination
SYSTEM_PROMPT = """You are LearnIQ, an AI tutor for CBSE Grade 8 Science (NCERT textbook).

RULES — follow these strictly:
1. Only answer from retrieved context. If the answer is not found in the context, say:
   "I couldn't find this in the NCERT Grade 8 Science textbook. Please check your textbook or ask your teacher."
2. Do NOT make up facts or use knowledge outside the provided context.
3. Explain concepts in simple language suitable for a Grade 8 student.
4. Use bullet points or numbered steps when explaining processes.
5. Always end your answer by citing the chapter source(s) from the context metadata.

CONTEXT FROM TEXTBOOK:
{context}

STUDENT QUESTION:
{question}

YOUR ANSWER:"""

QA_PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"],
)


def get_qa_chain(vectorstore):
    """
    Builds RetrievalQA chain: GPT-4o-mini LLM + ChromaDB retriever (top-4 chunks).
    Temperature=0.2 for factual, deterministic answers.
    max_tokens=512 to control output cost.
    """
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0.2,
        max_tokens=512,
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_PROMPT},
    )
    return chain


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Helper Functions
# ══════════════════════════════════════════════════════════════════════════════

def extract_chapters(source_docs):
    """Extracts unique chapter names from retrieved source documents."""
    chapters = []
    seen = set()
    for doc in source_docs:
        ch = doc.metadata.get("chapter", "Unknown")
        if ch not in seen:
            seen.add(ch)
            chapters.append(ch)
    return chapters


def load_qa_logs():
    """Loads student Q&A logs JSON for sidebar dashboard chart."""
    if not os.path.exists(QA_LOGS_PATH):
        return None
    with open(QA_LOGS_PATH, "r") as f:
        return json.load(f)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Custom CSS for Visual Appeal + Mobile Responsiveness
# ══════════════════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
    /* ── Global font and spacing ─────────────────────────────────────────── */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }

    /* ── Header styling ──────────────────────────────────────────────────── */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .app-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .app-header p {
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.9;
    }

    /* ── Chapter source badge ────────────────────────────────────────────── */
    .chapter-badge {
        display: inline-block;
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        color: #2e7d32;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 4px 4px 4px 0;
        border: 1px solid #a5d6a7;
    }

    /* ── Chat message styling ────────────────────────────────────────────── */
    .stChatMessage {
        border-radius: 12px;
    }

    /* ── Sidebar styling ─────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #eef1ff 100%);
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #4a4e69;
    }

    /* ── Dashboard CTA button ────────────────────────────────────────────── */
    .dashboard-cta {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        border: none;
        width: 100%;
        margin: 8px 0;
        transition: transform 0.2s;
    }
    .dashboard-cta:hover {
        transform: scale(1.02);
    }

    /* ── Metric cards ────────────────────────────────────────────────────── */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-card .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }
    .metric-card .label {
        font-size: 0.78rem;
        color: #6c757d;
    }

    /* ── Mobile responsive ───────────────────────────────────────────────── */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .app-header h1 {
            font-size: 1.5rem;
        }
        .app-header p {
            font-size: 0.82rem;
        }
    }
</style>
"""


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Streamlit App: Chat UI + Sidebar Dashboard + Teacher CTA
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # ── Page configuration ─────────────────────────────────────────────────
    st.set_page_config(
        page_title="LearnIQ - CBSE Grade 8 Science Tutor",
        page_icon="🔬",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # ── Inject custom CSS ──────────────────────────────────────────────────
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ── App header ─────────────────────────────────────────────────────────
    st.markdown(
        """<div class="app-header">
            <h1>🔬 LearnIQ</h1>
            <p>AI Tutor for CBSE Grade 8 Science &mdash; Answers from your NCERT textbook only</p>
        </div>""",
        unsafe_allow_html=True,
    )

    # ╔════════════════════════════════════════════════════════════════════════╗
    # ║ CHECKPOINT #1 — OS-SPECIFIC API KEY SETUP                            ║
    # ║                                                                      ║
    # ║ Option A (recommended): Create a .env file in this folder with:      ║
    # ║   OPENAI_API_KEY=sk-...                                              ║
    # ║   Works identically on macOS, Linux, and Windows.                    ║
    # ║                                                                      ║
    # ║ Option B: Set as system environment variable:                        ║
    # ║   macOS/Linux : export OPENAI_API_KEY="sk-..."  (add to ~/.zshrc)   ║
    # ║   Windows CMD : set OPENAI_API_KEY=sk-...                            ║
    # ║   Windows PS  : $env:OPENAI_API_KEY="sk-..."                         ║
    # ║                                                                      ║
    # ║ Option C: Paste into Streamlit sidebar (fallback below).             ║
    # ╚════════════════════════════════════════════════════════════════════════╝
    api_key = os.getenv("OPENAI_API_KEY", "")

    if not api_key:
        with st.sidebar:
            api_key = st.text_input(
                "🔑 OpenAI API Key",
                type="password",
                placeholder="sk-...",
                help="Paste your OpenAI API key. It is NOT stored anywhere.",
            )
            if not api_key:
                st.warning("Enter your OpenAI API key to start chatting.")
                st.stop()
            os.environ["OPENAI_API_KEY"] = api_key

    # ── Load vector store and build QA chain ──────────────────────────────
    vectorstore = load_vector_store()
    qa_chain = get_qa_chain(vectorstore)

    # ── Initialize session state ──────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I'm **LearnIQ**, your AI tutor for CBSE Grade 8 Science. 🎓\n\n"
                    "Ask me anything from your NCERT textbook — I'll find the answer "
                    "and tell you which chapter it's from!"
                ),
                "chapters": [],
            }
        ]
    if "query_count" not in st.session_state:
        st.session_state.query_count = 0
    if "show_teacher_dashboard" not in st.session_state:
        st.session_state.show_teacher_dashboard = False

    # ══════════════════════════════════════════════════════════════════════
    # SIDEBAR — Dashboard Chart + Teacher Dashboard CTA
    # ══════════════════════════════════════════════════════════════════════
    with st.sidebar:
        st.markdown("### 📊 Student Activity")

        # Load Q&A logs for sidebar chart
        qa_logs = load_qa_logs()
        if qa_logs:
            import pandas as pd
            df = pd.DataFrame(qa_logs)

            # Metric cards
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f'<div class="metric-card">'
                    f'<div class="value">{len(df)}</div>'
                    f'<div class="label">Questions Asked</div></div>',
                    unsafe_allow_html=True,
                )
            with col2:
                avg_conf = df["confidence"].mean()
                st.markdown(
                    f'<div class="metric-card">'
                    f'<div class="value">{avg_conf:.0%}</div>'
                    f'<div class="label">Avg Confidence</div></div>',
                    unsafe_allow_html=True,
                )

            # Topic distribution chart
            st.markdown("**Top Topics Asked**")
            topic_counts = df["topic_tag"].value_counts().head(8)
            st.bar_chart(topic_counts, color="#667eea")

            # Low confidence alert
            low_conf = int((df["confidence"] < 0.85).sum())
            if low_conf > 0:
                st.warning(f"⚠️ {low_conf} questions with low AI confidence (<85%)")

        else:
            st.info("No Q&A logs found yet. Student activity will appear here.")

        st.markdown("---")

        # ── Teacher Dashboard CTA Button ──────────────────────────────────
        st.markdown("### 🎓 For Teachers")
        if st.button("📋 Open Teacher Dashboard", use_container_width=True, type="primary"):
            st.session_state.show_teacher_dashboard = True

        if st.button("📈 Open Student Dashboard", use_container_width=True):
            st.session_state.show_student_dashboard = True

        st.markdown("---")

        # Tips section
        st.markdown("### 💡 Try asking:")
        st.markdown(
            "- *What is crop rotation?*\n"
            "- *How does friction affect motion?*\n"
            "- *What causes sound?*\n"
            "- *Explain the nitrogen cycle*"
        )

        st.markdown("---")
        st.caption(
            f"Model: GPT-4o-mini | Embeddings: text-embedding-3-small\n"
            f"Queries this session: {st.session_state.query_count}/{MAX_QUERIES_PER_SESSION}"
        )

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [st.session_state.messages[0]]
            st.session_state.query_count = 0
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # MAIN AREA — Teacher/Student Dashboard OR Chat
    # ══════════════════════════════════════════════════════════════════════

    # If teacher dashboard CTA was clicked, show it inline
    if st.session_state.get("show_teacher_dashboard"):
        _render_teacher_dashboard()
        if st.button("← Back to Chat"):
            st.session_state.show_teacher_dashboard = False
            st.rerun()
        return

    if st.session_state.get("show_student_dashboard"):
        _render_student_dashboard()
        if st.button("← Back to Chat"):
            st.session_state.show_student_dashboard = False
            st.rerun()
        return

    # ══════════════════════════════════════════════════════════════════════
    # CHAT INTERFACE
    # ══════════════════════════════════════════════════════════════════════

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("chapters"):
                badges = " ".join(
                    f'<span class="chapter-badge">📖 {ch}</span>'
                    for ch in msg["chapters"]
                )
                st.markdown(badges, unsafe_allow_html=True)

    # Handle new user input
    if question := st.chat_input("Ask a Science question..."):
        # Rate limiter for cost control
        if st.session_state.query_count >= MAX_QUERIES_PER_SESSION:
            st.error(
                f"Session limit of {MAX_QUERIES_PER_SESSION} questions reached. "
                "Clear chat or restart to continue."
            )
            st.stop()

        # Display user message
        st.session_state.messages.append(
            {"role": "user", "content": question, "chapters": []}
        )
        with st.chat_message("user"):
            st.markdown(question)

        # Get answer from RetrievalQA chain
        with st.chat_message("assistant"):
            with st.spinner("Searching your textbook..."):
                result = qa_chain.invoke({"query": question})
                answer = result["result"]
                source_docs = result.get("source_documents", [])
                chapters = extract_chapters(source_docs)

            st.markdown(answer)

            # Show chapter source badges
            if chapters:
                badges = " ".join(
                    f'<span class="chapter-badge">📖 {ch}</span>'
                    for ch in chapters
                )
                st.markdown(badges, unsafe_allow_html=True)

        # Save to chat history and increment counter
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "chapters": chapters}
        )
        st.session_state.query_count += 1


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — Inline Teacher Dashboard (shown on CTA click)
# ══════════════════════════════════════════════════════════════════════════════

def _render_teacher_dashboard():
    """Renders the teacher dashboard inline when CTA is clicked."""
    import pandas as pd

    st.markdown(
        """<div class="app-header" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24);">
            <h1>📋 Teacher Dashboard</h1>
            <p>Student performance insights from Q&A logs</p>
        </div>""",
        unsafe_allow_html=True,
    )

    qa_logs = load_qa_logs()
    if not qa_logs:
        st.warning("No Q&A logs found. Place student_qa_logs_chapter1.json in the parent folder.")
        return

    df = pd.DataFrame(qa_logs)

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Questions", len(df))
    col2.metric("Unique Students", df["student_id"].nunique())
    col3.metric("Avg Confidence", f"{df['confidence'].mean():.0%}")
    col4.metric("Low Confidence (<85%)", int((df["confidence"] < 0.85).sum()))

    st.markdown("---")

    # Topic distribution
    tab1, tab2, tab3 = st.tabs(["📊 Topic Analysis", "⚠️ At-Risk Questions", "📋 Full Log"])

    with tab1:
        st.subheader("Questions by Topic")
        topic_counts = df["topic_tag"].value_counts()
        st.bar_chart(topic_counts, color="#667eea")

        st.subheader("Confidence by Topic")
        topic_conf = df.groupby("topic_tag")["confidence"].mean().sort_values()
        st.bar_chart(topic_conf, color="#ff6b6b")

    with tab2:
        st.subheader("Questions with Low AI Confidence (<85%)")
        low_conf_df = df[df["confidence"] < 0.85][
            ["student_id", "question", "confidence", "topic_tag"]
        ].sort_values("confidence")
        if len(low_conf_df) > 0:
            st.dataframe(low_conf_df, use_container_width=True, hide_index=True)
        else:
            st.success("All questions answered with high confidence!")

    with tab3:
        st.subheader("Complete Q&A Log")
        st.dataframe(
            df[["student_id", "question", "ai_answer", "confidence", "topic_tag"]],
            use_container_width=True,
            hide_index=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — Inline Student Dashboard (shown on CTA click)
# ══════════════════════════════════════════════════════════════════════════════

def _render_student_dashboard():
    """Renders the student analytics dashboard inline."""
    import pandas as pd

    st.markdown(
        """<div class="app-header" style="background: linear-gradient(135deg, #00b894, #00cec9);">
            <h1>📈 Student Dashboard</h1>
            <p>Your learning progress and question history</p>
        </div>""",
        unsafe_allow_html=True,
    )

    qa_logs = load_qa_logs()
    if not qa_logs:
        st.warning("No Q&A logs found yet.")
        return

    df = pd.DataFrame(qa_logs)

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Questions Asked", len(df))
    col2.metric("Topics Covered", df["topic_tag"].nunique())
    col3.metric("Avg Score", f"{df['confidence'].mean():.0%}")

    st.markdown("---")

    # Topic coverage
    st.subheader("Topics You've Explored")
    topic_counts = df["topic_tag"].value_counts()
    st.bar_chart(topic_counts, color="#00b894")

    # Confidence distribution
    st.subheader("Answer Confidence Distribution")
    hist_data = df["confidence"].value_counts(bins=10).sort_index()
    st.bar_chart(hist_data, color="#fdcb6e")

    # Recent questions
    st.subheader("Recent Questions")
    st.dataframe(
        df[["question", "ai_answer", "confidence", "topic_tag"]].tail(10),
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()
