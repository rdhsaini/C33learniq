"""
LearnIQ — PDF Ingestion Pipeline
=================================
Loads NCERT Class 8 Science PDFs, chunks them, embeds with OpenAI, persists to ChromaDB.

Usage:
    cd backend
    python ingest.py

Run this ONCE before starting the FastAPI server.
"""

import os
import sys
import glob
import time
from dotenv import load_dotenv

import pypdf.filters

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Raise pypdf decompression limit for NCERT PDFs with heavy embedded images
pypdf.filters.ZLIB_MAX_OUTPUT_LENGTH = 500 * 1024 * 1024  # 500 MB (default 75 MB)

# ── Configuration ──────────────────────────────────────────────────────────────
# CHECKPOINT #3 — Change PDF_DIR for a different subject/grade
PDF_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "NCERT_PDFs")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

CHAPTER_MAP = {
    "ncert_class8_science1":  "Chapter 1 - Crop Production and Management",
    "ncert_class8_science2":  "Chapter 2 - Microorganisms: Friend and Foe",
    "ncert_class8_science3":  "Chapter 3 - Synthetic Fibres and Plastics",
    "ncert_class8_science4":  "Chapter 4 - Materials: Metals and Non-Metals",
    "ncert_class8_science5":  "Chapter 5 - Coal and Petroleum",
    "ncert_class8_science6":  "Chapter 6 - Combustion and Flame",
    "ncert_class8_science7":  "Chapter 7 - Conservation of Plants and Animals",
    "ncert_class8_science8":  "Chapter 8 - Cell: Structure and Functions",
    "ncert_class8_science9":  "Chapter 9 - Reproduction in Animals",
    "ncert_class8_science10": "Chapter 10 - Reaching the Age of Adolescence",
    "ncert_class8_science11": "Chapter 11 - Force and Pressure",
    "ncert_class8_science12": "Chapter 12 - Friction",
    "ncert_class8_science13": "Chapter 13 - Sound",
    "ncert_class8_science14": "Chapter 14 - Chemical Effects of Electric Current",
    "ncert_class8_science15": "Chapter 15 - Some Natural Phenomena",
}


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set.")
        print("  Create a .env file with: OPENAI_API_KEY=sk-...")
        sys.exit(1)

    print("=" * 65)
    print("  LearnIQ - PDF Ingestion Pipeline")
    print("  NCERT Class 8 Science -> ChromaDB")
    print("=" * 65)

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        print(f"\n  Vector store already exists at: {PERSIST_DIR}/")
        print("  Delete it to rebuild: rm -rf chroma_db/")
        return

    # Step 1: Load PDFs
    print(f"\nSTEP 1 - Loading PDFs from: {PDF_DIR}")
    print("-" * 65)

    pdf_paths = sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf")))
    if not pdf_paths:
        print(f"  ERROR: No PDFs found in '{PDF_DIR}'")
        print(f"  Place NCERT PDFs in: {os.path.abspath(PDF_DIR)}")
        sys.exit(1)

    all_docs = []
    skipped = []
    for pdf_path in pdf_paths:
        filename = os.path.basename(pdf_path)
        stem = os.path.splitext(filename)[0]
        chapter_name = CHAPTER_MAP.get(stem, stem)

        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
        except Exception as e:
            print(f"  WARN: {filename:40s} -> SKIPPED ({type(e).__name__}: {e})")
            skipped.append(filename)
            continue

        for page in pages:
            page.metadata["chapter"] = chapter_name
            page.metadata["source_file"] = filename

        all_docs.extend(pages)
        print(f"  Loaded {filename:40s} -> {len(pages):3d} pages  [{chapter_name}]")

    if skipped:
        print(f"\n  WARNING: {len(skipped)} PDF(s) skipped due to parsing errors: {', '.join(skipped)}")

    print(f"\n  Total pages: {len(all_docs)}")

    # Step 2: Chunk
    print(f"\nSTEP 2 - Chunking (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print("-" * 65)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(all_docs)
    total_chars = sum(len(c.page_content) for c in chunks)
    print(f"  Chunks: {len(chunks)}  |  Characters: {total_chars:,}")

    # Step 3: Embed and persist
    print(f"\nSTEP 3 - Embedding + ChromaDB persist")
    print("-" * 65)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    t0 = time.time()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s -> {PERSIST_DIR}/")

    # Step 4: Verify
    print(f"\nSTEP 4 - Verification")
    print("-" * 65)

    test_queries = [
        "What is crop rotation?",
        "How does friction affect motion?",
        "What causes sound?",
    ]
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    for q in test_queries:
        results = retriever.invoke(q)
        chapters = set(d.metadata.get("chapter", "?") for d in results)
        print(f"  Q: {q}")
        print(f"     -> {', '.join(chapters)}")

    est_cost = (total_chars / 4 / 1_000_000) * 0.02
    print(f"\n{'=' * 65}")
    print(f"  INGESTION COMPLETE")
    print(f"  Chunks: {len(chunks)} | Est. cost: ${est_cost:.4f}")
    print(f"  Next: cd backend && uvicorn main:app --port 8000")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
