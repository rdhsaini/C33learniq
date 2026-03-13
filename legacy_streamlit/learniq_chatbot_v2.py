"""
LearnIQ — AI Tutor for CBSE Science
Streamlit chatbot using ChromaDB + OpenAI (no LangChain dependency)

Run:  streamlit run learniq_chatbot.py
"""

import os
import numpy as np
import streamlit as st
from openai import OpenAI
import chromadb
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# ── SECTION 1: CONFIGURATION ──────────────────────────────────────────────────
# ✏️  Change this 1 variable to switch subject/grade:
SUBJECT_LABEL   = "CBSE Class 10 Science"

CHROMA_PERSIST  = "./learniq_chroma_db"          # must match learniq_ingest.py
COLLECTION_NAME = "ncert_class10_science"        # must match learniq_ingest.py
EMBEDDER_CACHE  = "./learniq_chroma_db/tfidf_embedder.pkl"
TOP_K           = 4                              # chunks retrieved per query

# System prompt — strictly grounded in textbook only
SYSTEM_PROMPT = """You are LearnIQ, an AI tutor for CBSE students.
Only answer from retrieved context. If the answer is not found in the provided context, say:
'I could not find this in the NCERT textbook. Please check your chapter or ask your teacher.'

Rules:
- Always cite the chapter source at the end of your answer.
- Use simple language suitable for Grade 8–10 students.
- Break explanations into short numbered steps where helpful.
- Never guess or add information beyond the retrieved context."""

# ── SECTION 2: LOAD CHROMADB + EMBEDDER ───────────────────────────────────────
@st.cache_resource(show_spinner="📚 Loading LearnIQ knowledge base...")
def load_resources():
    """Load ChromaDB collection and TF-IDF embedder from disk (built by ingest script)."""
    # Load ChromaDB
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST)
    collection = chroma_client.get_collection(name=COLLECTION_NAME)

    # Load saved TF-IDF embedder if it exists, else rebuild from stored docs
    if os.path.exists(EMBEDDER_CACHE):
        with open(EMBEDDER_CACHE, "rb") as f:
            embedder = pickle.load(f)
    else:
        # Rebuild embedder from all stored documents
        all_docs = collection.get(include=["documents"])["documents"]
        embedder = TfidfVectorizer(max_features=512, ngram_range=(1, 2), sublinear_tf=True)
        embedder.fit(all_docs)
        os.makedirs(CHROMA_PERSIST, exist_ok=True)
        with open(EMBEDDER_CACHE, "wb") as f:
            pickle.dump(embedder, f)

    return collection, embedder

def embed_query(query: str, embedder) -> list:
    """Embed a single query string using the TF-IDF vectorizer."""
    vec = embedder.transform([query]).toarray().astype(float)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec[0].tolist()

# ── SECTION 3: RETRIEVAL ───────────────────────────────────────────────────────
def retrieve_chunks(query: str, collection, embedder, k: int = TOP_K):
    """Return top-k relevant chunks + their metadata from ChromaDB."""
    q_vec = embed_query(query, embedder)
    results = collection.query(
        query_embeddings=[q_vec],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    chunks   = results["documents"][0]
    metas    = results["metadatas"][0]
    distances = results["distances"][0]
    return chunks, metas, distances

# ── SECTION 4: OPENAI ANSWER GENERATION ───────────────────────────────────────
def generate_answer(question: str, chunks: list, metas: list, client: OpenAI) -> str:
    """Send retrieved context + question to GPT-4o-mini and return the answer."""
    # Build context block with chapter labels
    context_parts = []
    for i, (chunk, meta) in enumerate(zip(chunks, metas), 1):
        context_parts.append(f"[Source {i} — {meta.get('chapter','Unknown')}]\n{chunk}")
    context_block = "\n\n".join(context_parts)

    user_message = f"""Context from NCERT {SUBJECT_LABEL} textbook:

{context_block}

---
Student Question: {question}

Answer based only on the context above. End your answer with a 'Source:' line listing the chapters used."""

    # 💰 Cost control: GPT-4o-mini (~$0.00015/1K input tokens)
    # Swap model here to change cost/quality:
    response = client.chat.completions.create(
        model="gpt-4o-mini",          # ← change model here if needed
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message}
        ],
        temperature=0.2,              # low temp = more factual, less creative
        max_tokens=600
    )
    return response.choices[0].message.content

# ── SECTION 5: STREAMLIT UI ───────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="LearnIQ — CBSE AI Tutor",
        page_icon="🎓",
        layout="centered"
    )

    # ── Header ──
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem 0'>
        <h1 style='font-size:2.2rem; margin-bottom:0'>🎓 LearnIQ</h1>
        <p style='color:#888; font-size:1rem; margin-top:0.2rem'>
            AI Tutor · CBSE Class 10 Science · Answers from NCERT textbook only
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # ── API Key handling ──
    # 🖥️  OS-specific API key setup:
    #   macOS/Linux: export OPENAI_API_KEY="sk-..."  in terminal or add to ~/.zshrc
    #   Windows CMD: set OPENAI_API_KEY=sk-...
    #   Windows PS:  $env:OPENAI_API_KEY="sk-..."
    #   OR: create a .env file with OPENAI_API_KEY=sk-... and use python-dotenv
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        api_key = st.sidebar.text_input(
            "🔑 OpenAI API Key",
            type="password",
            help="Get your key at platform.openai.com"
        )
    if not api_key:
        st.warning("⚠️ Please set your OpenAI API key to start chatting.")
        st.stop()

    openai_client = OpenAI(api_key=api_key)

    # ── Load resources ──
    try:
        collection, embedder = load_resources()
    except Exception as e:
        st.error(f"❌ Could not load knowledge base: {e}\n\nPlease run `python3 learniq_ingest.py` first.")
        st.stop()

    # ── Sidebar info ──
    with st.sidebar:
        st.markdown("### 📖 About LearnIQ")
        st.markdown(f"""
        - **Subject:** {SUBJECT_LABEL}
        - **Source:** NCERT Textbook
        - **Model:** GPT-4o-mini
        - **Chunks loaded:** {collection.count():,}
        - **Top-K retrieval:** {TOP_K} chunks
        """)
        st.divider()
        st.markdown("### 💡 Sample Questions")
        sample_questions = [
            "What is a chemical reaction?",
            "Explain photosynthesis",
            "How does the human eye work?",
            "What is Ohm's Law?",
            "What are metals and non-metals?",
        ]
        for q in sample_questions:
            if st.button(q, use_container_width=True):
                st.session_state["prefill"] = q
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()

    # ── Chat history init ──
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # ── Display chat history ──
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Show chapter source badge for assistant messages
            if msg["role"] == "assistant" and msg.get("sources"):
                cols = st.columns(len(msg["sources"]))
                for i, src in enumerate(msg["sources"]):
                    cols[i].markdown(
                        f"<span style='background:#1a73e8;color:white;padding:2px 8px;"
                        f"border-radius:12px;font-size:0.72rem'>📖 {src}</span>",
                        unsafe_allow_html=True
                    )

    # ── Chat input ──
    prefill = st.session_state.pop("prefill", "")
    user_input = st.chat_input("Ask any question from your NCERT Science textbook…")
    question = prefill or user_input

    if question:
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve + generate
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching textbook…"):
                chunks, metas, distances = retrieve_chunks(question, collection, embedder)
                answer = generate_answer(question, chunks, metas, openai_client)

            st.markdown(answer)

            # Chapter source badges
            unique_chapters = list(dict.fromkeys(
                m.get("chapter", "Unknown") for m in metas
            ))
            badge_cols = st.columns(len(unique_chapters))
            for i, ch in enumerate(unique_chapters):
                badge_cols[i].markdown(
                    f"<span style='background:#1a73e8;color:white;padding:2px 8px;"
                    f"border-radius:12px;font-size:0.72rem'>📖 {ch}</span>",
                    unsafe_allow_html=True
                )

            # Confidence indicator (based on retrieval similarity)
            avg_sim = round(1 - np.mean(distances), 2)
            if avg_sim > 0.3:
                conf_label = "🟢 High confidence — found in textbook"
            elif avg_sim > 0.15:
                conf_label = "🟡 Medium confidence — partial match"
            else:
                conf_label = "🔴 Low confidence — answer may be limited"
            st.caption(f"{conf_label}  ·  Avg similarity: {avg_sim}")

        # Save to history
        st.session_state["messages"].append({
            "role": "assistant",
            "content": answer,
            "sources": unique_chapters
        })

if __name__ == "__main__":
    main()
