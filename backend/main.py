"""
LearnIQ — FastAPI Backend
==========================
REST API that wraps the LangChain RetrievalQA chain for the React frontend.

Endpoints:
  POST /api/chat   — Send a student question, get an answer with chapter citations
  GET  /api/health — Health check

Run:
  uvicorn main:app --reload --port 8000
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_chain import get_qa_chain

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learniq")

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="LearnIQ API",
    description="AI Tutoring backend for CBSE Grade 8 Science (NCERT)",
    version="1.0.0",
)

# CORS — allow React dev server (Vite on 8080) and production origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ──────────────────────────────────────────────────
class ChatRequest(BaseModel):
    question: str
    chapter: Optional[int] = None  # optional chapter filter (not used in retrieval yet)


class Citation(BaseModel):
    chapter: str
    page: int
    source_file: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    chunks_retrieved: int


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    """Simple health check — returns OK if the server is running."""
    return {"status": "ok", "service": "LearnIQ API"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Accepts a student question, runs it through the LangChain RetrievalQA chain,
    and returns the answer with chapter source citations.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        chain = get_qa_chain()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    logger.info(f"Question: {request.question[:100]}...")

    try:
        result = chain.invoke({"query": request.question})
    except Exception as e:
        logger.error(f"Chain error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {e}")

    answer = result["result"]
    source_docs = result.get("source_documents", [])

    # Extract unique citations from source documents
    seen = set()
    citations = []
    for doc in source_docs:
        chapter = doc.metadata.get("chapter", "Unknown")
        page = doc.metadata.get("page", 0)
        source_file = doc.metadata.get("source_file", "")
        key = f"{chapter}:{page}"
        if key not in seen:
            seen.add(key)
            citations.append(Citation(
                chapter=chapter,
                page=page + 1,  # convert 0-indexed to 1-indexed
                source_file=source_file,
            ))

    logger.info(f"Answer length: {len(answer)} chars, Citations: {len(citations)}")

    return ChatResponse(
        answer=answer,
        citations=citations,
        chunks_retrieved=len(source_docs),
    )


# ── Startup event ──────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    """Pre-load the QA chain at startup so the first request is fast."""
    try:
        get_qa_chain()
        logger.info("QA chain loaded successfully.")
    except Exception as e:
        logger.warning(f"QA chain not loaded at startup: {e}")
        logger.warning("Run 'python ingest.py' to build the vector store.")
