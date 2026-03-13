"""
LearnIQ — AI Tutor for CBSE Science
Uses LangChain RetrievalQA + ChromaDB + OpenAI (as per original spec)

ROOT CAUSE OF ERROR:
  LangChain v0.2+ split into sub-packages. Old single-package imports are broken.
  Fix = install the correct sub-packages + use new import paths (see Section 2).

Install (run once):
  pip3 install langchain langchain-openai langchain-chroma langchain-community
  pip3 install openai chromadb streamlit pypdf tiktoken

Run:
  streamlit run learniq_chatbot.py
"""

import os
import streamlit as st

# ── SECTION 1: CONFIGURATION ──────────────────────────────────────────────────
# ✏️  CHECKPOINT 3 — Change this 1 variable to switch subject/grade:
SUBJECT_LABEL   = "CBSE Class 10 Science"

CHROMA_PERSIST  = "./learniq_chroma_db"      # must match learniq_ingest.py
COLLECTION_NAME = "ncert_class10_science"    # must match learniq_ingest.py
TOP_K           = 4                          # number of source chunks to retrieve per query

# ── SECTION 2: LANGCHAIN IMPORTS (correct paths for LangChain v0.2+) ──────────
#
# ❌ OLD broken imports (LangChain v0.1 — causes your ModuleNotFoundError):
#     from langchain.chains import RetrievalQA              ← BROKEN in v0.2
#     from langchain.embeddings import OpenAIEmbeddings     ← BROKEN in v0.2
#     from langchain.vectorstores import Chroma             ← BROKEN in v0.2
#     from langchain.chat_models import ChatOpenAI          ← BROKEN in v0.2
#
# ✅ NEW correct imports (LangChain v0.2+):
from langchain.chains import RetrievalQA                    # still in core langchain ✅
from langchain_openai import ChatOpenAI, OpenAIEmbeddings   # pip: langchain-openai  ✅
from langchain_chroma import Chroma                         # pip: langchain-chroma  ✅
from langchain.prompts import PromptTemplate                # still in core langchain ✅

# ── SECTION 3: SYSTEM PROMPT ───────────────────────────────────────────────────
# Spec requires: 'Only answer from retrieved context. If not found, say so.'
PROMPT_TEMPLATE = """You are LearnIQ, an AI tutor for CBSE students studying """ + SUBJECT_LABEL + """.

Only answer from retrieved context. If the answer is not found in the provided \
context, say: "I could not find this topic in the NCERT textbook. Please check \
your chapter or ask your teacher."

Rules:
- Always end your answer with a line: Source: <chapter name>
- Use simple language suitable for Grade 8-10 students
- Break explanations into short numbered steps where helpful
- Never add information beyond the retrieved context

Context:
{context}

Student Question: {question}

Answer:"""

QA_PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

# ── SECTION 4: LOAD LANGCHAIN RETRIEVAL CHAIN ─────────────────────────────────
@st.cache_resource(show_spinner="📚 Loading LearnIQ knowledge base...")
def load_qa_chain(api_key: str):
    """
    Builds the LangChain RetrievalQA chain:
      ChromaDB (persisted chunks) → OpenAI embeddings retriever → GPT-4o-mini LLM

    CHECKPOINT 2 — Swap ChromaDB → Pinecone in 2 lines:
      Line 1: from langchain_pinecone import PineconeVectorStore
      Line 2: vectorstore = PineconeVectorStore(index_name="learniq", embedding=embeddings)
    """

    # OpenAI text-embedding-3-small — cheapest + best for retrieval
    # 💰 Cost: ~$0.00002 per 1K tokens (well within $5 budget)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )

    # Load ChromaDB vector store persisted to disk by learniq_ingest.py
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST
    )

    # GPT-4o-mini for answer generation
    # 💰 Cost control: GPT-4o-mini = $0.00015/1K input tokens vs $0.005 for GPT-4o (33x cheaper)
    llm = ChatOpenAI(
        model="gpt-4o-mini",        # ← swap to "gpt-4o" here for higher quality
        temperature=0.2,            # low temp = more factual, less creative
        max_tokens=600,
        openai_api_key=api_key
    )

    # LangChain RetrievalQA chain — the core of the spec
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",                             # stuffs all chunks into one prompt
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": TOP_K}                  # fetch 4 source chunks per query
        ),
        return_source_documents=True,                   # needed for chapter badges
        chain_type_kwargs={"prompt": QA_PROMPT}
    )

    return qa_chain

# ── SECTION 5: STREAMLIT UI ───────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="LearnIQ — CBSE AI Tutor",
        page_icon="🎓",
        layout="centered"
    )

    # Header
    st.markdown("""
    <div style='text-align:center; padding:1rem 0 0.5rem 0'>
        <h1 style='font-size:2.2rem; margin-bottom:0'>🎓 LearnIQ</h1>
        <p style='color:#888; font-size:1rem; margin-top:0.2rem'>
            AI Tutor · CBSE Class 10 Science · LangChain RetrievalQA + GPT-4o-mini
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # ── API Key ────────────────────────────────────────────────────────────────
    # CHECKPOINT 1 — OS-specific API key setup:
    #   macOS/Linux : export OPENAI_API_KEY="sk-..."   (add to ~/.zshrc to persist)
    #   Windows CMD : set OPENAI_API_KEY=sk-...
    #   Windows PS  : $env:OPENAI_API_KEY="sk-..."
    #   .env file   : add OPENAI_API_KEY=sk-... then run: pip3 install python-dotenv
    #                 and add at top of file: from dotenv import load_dotenv; load_dotenv()
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

    # Load RetrievalQA chain
    try:
        qa_chain = load_qa_chain(api_key)
    except Exception as e:
        st.error(
            f"❌ Could not load knowledge base.\n\n"
            f"**Run this first:** `python3 learniq_ingest.py`\n\n"
            f"Error: {e}"
        )
        st.stop()

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 📖 About LearnIQ")
        st.markdown(f"""
        - **Subject:** {SUBJECT_LABEL}  
        - **Source:** NCERT Textbook  
        - **Chain:** LangChain RetrievalQA  
        - **Embeddings:** text-embedding-3-small  
        - **LLM:** GPT-4o-mini  
        - **Chunks/query:** {TOP_K}  
        """)
        st.divider()
        st.markdown("### 💡 Sample Questions")
        samples = [
            "What is a chemical reaction?",
            "Explain photosynthesis",
            "How does the human eye work?",
            "What is Ohm's Law?",
            "What are acids and bases?",
        ]
        for q in samples:
            if st.button(q, use_container_width=True):
                st.session_state["prefill"] = q
        st.divider()
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()

    # ── Chat history ───────────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                for src in msg["sources"]:
                    st.markdown(
                        f"<span style='background:#1a73e8;color:white;"
                        f"padding:3px 10px;border-radius:12px;"
                        f"font-size:0.72rem;margin-right:6px'>📖 {src}</span>",
                        unsafe_allow_html=True
                    )

    # ── Chat input ─────────────────────────────────────────────────────────────
    prefill    = st.session_state.pop("prefill", "")
    user_input = st.chat_input("Ask any question from your NCERT Science textbook…")
    question   = prefill or user_input

    if question:
        st.session_state["messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching NCERT textbook via LangChain RetrievalQA…"):
                # ── Core LangChain RetrievalQA call ───────────────────────
                result       = qa_chain.invoke({"query": question})
                answer       = result["result"]
                source_docs  = result.get("source_documents", [])

            st.markdown(answer)

            # Chapter source badges from retrieved documents
            unique_chapters = list(dict.fromkeys(
                doc.metadata.get("chapter", "Unknown Chapter")
                for doc in source_docs
            ))
            for ch in unique_chapters:
                st.markdown(
                    f"<span style='background:#1a73e8;color:white;"
                    f"padding:3px 10px;border-radius:12px;"
                    f"font-size:0.72rem;margin-right:6px'>📖 {ch}</span>",
                    unsafe_allow_html=True
                )
            st.caption(f"📄 {len(source_docs)} chunks retrieved · LangChain RetrievalQA")

        st.session_state["messages"].append({
            "role":    "assistant",
            "content": answer,
            "sources": unique_chapters
        })

if __name__ == "__main__":
    main()
