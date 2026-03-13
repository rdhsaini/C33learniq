"""
LearnIQ — PDF Ingestion Pipeline
=================================
Loads all NCERT Class 8 Science PDFs from a folder, splits into overlapping chunks,
embeds with OpenAI text-embedding-3-small, and persists to ChromaDB on disk.

Usage:
    python learniq_ingest.py

This script runs ONCE to build the vector store. The Streamlit chatbot then
reads from the persisted ChromaDB directory at runtime (zero additional cost).
"""

import os
import sys
import glob
import time
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
# NEW (correct)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# ── Load .env file for OPENAI_API_KEY ─────────────────────────────────────────
load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Configuration
# ══════════════════════════════════════════════════════════════════════════════

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ CHECKPOINT #3 — CHANGE THIS 1 VARIABLE FOR A DIFFERENT SUBJECT/GRADE     ║
# ║ Update PDF_DIR to your new textbook folder path.                          ║
# ╚════════════════════════════════════════════════════════════════════════════╝
PDF_DIR = os.path.join(os.path.dirname(__file__), "..", "NCERT Class 8 Science PDF")

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")  # ChromaDB on-disk store
EMBEDDING_MODEL = "text-embedding-3-small"  # $0.02/1M tokens — cheapest OpenAI embedding
CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 50     # overlap between consecutive chunks

# Chapter metadata mapping — maps PDF filenames to human-readable chapter names.
# These names appear as chapter source badges in the chatbot UI.
CHAPTER_MAP = {
    "ncert_class8_science1":  "Chapter 1 – Crop Production and Management",
    "ncert_class8_science2":  "Chapter 2 – Microorganisms: Friend and Foe",
    "ncert_class8_science3":  "Chapter 3 – Synthetic Fibres and Plastics",
    "ncert_class8_science4":  "Chapter 4 – Materials: Metals and Non-Metals",
    "ncert_class8_science5":  "Chapter 5 – Coal and Petroleum",
    "ncert_class8_science6":  "Chapter 6 – Combustion and Flame",
    "ncert_class8_science7":  "Chapter 7 – Conservation of Plants and Animals",
    "ncert_class8_science8":  "Chapter 8 – Cell: Structure and Functions",
    "ncert_class8_science9":  "Chapter 9 – Reproduction in Animals",
    "ncert_class8_science10": "Chapter 10 – Reaching the Age of Adolescence",
    "ncert_class8_science11": "Chapter 11 – Force and Pressure",
    "ncert_class8_science12": "Chapter 12 – Friction",
    "ncert_class8_science13": "Chapter 13 – Sound",
    "ncert_class8_science14": "Chapter 14 – Chemical Effects of Electric Current",
    "ncert_class8_science15": "Chapter 15 – Some Natural Phenomena",
}


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — PDF Loading
# ══════════════════════════════════════════════════════════════════════════════

def load_all_pdfs(pdf_dir):
    """
    Loads every PDF in pdf_dir using LangChain's PyPDFLoader.
    Tags each page with chapter name and source filename for citation.
    Returns a flat list of Document objects.
    """
    all_docs = []
    pdf_paths = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))

    if not pdf_paths:
        print(f"ERROR: No PDFs found in '{pdf_dir}'.")
        print("Place your NCERT Class 8 Science chapter PDFs in that folder.")
        sys.exit(1)

    for pdf_path in pdf_paths:
        filename = os.path.basename(pdf_path)
        stem = os.path.splitext(filename)[0]
        chapter_name = CHAPTER_MAP.get(stem, stem)

        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Attach chapter metadata for citation badges
        for page in pages:
            page.metadata["chapter"] = chapter_name
            page.metadata["source_file"] = filename

        all_docs.extend(pages)
        print(f"  Loaded {filename:40s} -> {len(pages):3d} pages  [{chapter_name}]")

    return all_docs


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Text Chunking
# ══════════════════════════════════════════════════════════════════════════════

def chunk_documents(docs):
    """
    Splits documents into overlapping chunks of CHUNK_SIZE characters.
    Overlap of CHUNK_OVERLAP prevents answers from being split across chunks.
    Uses smart separators: paragraph > newline > sentence > word > character.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    return chunks


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Embedding + ChromaDB Persistence
# ══════════════════════════════════════════════════════════════════════════════

def build_vector_store(chunks):
    """
    Embeds all chunks with OpenAI text-embedding-3-small and persists to ChromaDB.

    ╔════════════════════════════════════════════════════════════════════════════╗
    ║ CHECKPOINT #2 — SWAP ChromaDB FOR Pinecone (2 lines to change):          ║
    ║                                                                          ║
    ║   Line 1: from langchain_pinecone import PineconeVectorStore             ║
    ║   Line 2: vectorstore = PineconeVectorStore.from_documents(              ║
    ║               chunks, embeddings, index_name="learniq")                  ║
    ║                                                                          ║
    ║   Also: pip install langchain-pinecone pinecone-client                   ║
    ║   And set PINECONE_API_KEY in your .env                                  ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = Chroma.from_documents(       # <- Line 1: change to PineconeVectorStore
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,          # <- Line 2: remove for Pinecone
    )

    return vectorstore


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Main Pipeline
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # Validate API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set.")
        print("  Option A: Create a .env file with OPENAI_API_KEY=sk-...")
        print("  Option B: export OPENAI_API_KEY='sk-...'  (macOS/Linux)")
        print("  Option C: set OPENAI_API_KEY=sk-...        (Windows CMD)")
        sys.exit(1)

    print("=" * 65)
    print("  LearnIQ — PDF Ingestion Pipeline")
    print("  NCERT Class 8 Science -> ChromaDB Vector Store")
    print("=" * 65)

    # Check if vector store already exists
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        print(f"\n  Vector store already exists at: {PERSIST_DIR}/")
        print("  Delete that folder and re-run to rebuild from scratch.")
        print("  Or just run the chatbot: streamlit run learniq_chatbot.py")
        return

    # Step 1: Load PDFs
    print(f"\nSTEP 1 — Loading PDFs from: {PDF_DIR}")
    print("-" * 65)
    docs = load_all_pdfs(PDF_DIR)
    print(f"\n  Total pages loaded: {len(docs)}")

    # Step 2: Chunk documents
    print(f"\nSTEP 2 — Chunking (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print("-" * 65)
    chunks = chunk_documents(docs)
    print(f"  Total chunks created: {len(chunks)}")
    total_chars = sum(len(c.page_content) for c in chunks)
    print(f"  Total characters: {total_chars:,}")

    # Step 3: Embed and persist
    print(f"\nSTEP 3 — Embedding with {EMBEDDING_MODEL} + persisting to ChromaDB")
    print("-" * 65)
    print(f"  Persist directory: {PERSIST_DIR}")
    t0 = time.time()
    vectorstore = build_vector_store(chunks)
    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")

    # Step 4: Verification
    print(f"\nSTEP 4 — Verification (test retrieval)")
    print("-" * 65)
    test_queries = [
        "What is the difference between kharif and rabi crops?",
        "How does friction affect motion?",
        "What causes sound?",
    ]
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    for q in test_queries:
        results = retriever.invoke(q)
        chapters = set(d.metadata.get("chapter", "?") for d in results)
        print(f"  Q: {q}")
        print(f"     Sources: {', '.join(chapters)}")

    # Cost estimate
    est_tokens = total_chars / 4  # rough char-to-token ratio
    est_cost = (est_tokens / 1_000_000) * 0.02
    print(f"\n{'=' * 65}")
    print(f"  INGESTION COMPLETE")
    print(f"{'=' * 65}")
    print(f"  Chunks indexed  : {len(chunks)}")
    print(f"  ChromaDB path   : {PERSIST_DIR}/")
    print(f"  Est. embed cost : ${est_cost:.4f}")
    print(f"\n  Next step: streamlit run learniq_chatbot.py")


if __name__ == "__main__":
    main()
