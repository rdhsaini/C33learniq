# LearnIQ — AI-Powered Tutoring for CBSE Grade 8 Science

LearnIQ is an intelligent tutoring platform that uses Retrieval-Augmented Generation (RAG) to answer student questions grounded in NCERT Class 8 Science textbooks. It combines a modern React frontend with a Python/LangChain backend.

## Architecture

```
Browser (React + Vite)
   |
   |  POST /api/chat  { question, chapter? }
   v
FastAPI  (port 8000)
   |
   |  LangChain RetrievalQA (stuff chain)
   v
ChromaDB  ──>  OpenAI text-embedding-3-small
   |
   v
GPT-4o-mini  ──>  { answer, citations[] }
```

**Frontend** — React 18, TypeScript, TailwindCSS, shadcn/ui, React Router, Recharts
**Backend** — FastAPI, LangChain, ChromaDB, OpenAI GPT-4o-mini

## Features

| Role    | Feature           | Status       |
|---------|-------------------|--------------|
| Student | AI Chat (RAG)     | Real backend |
| Student | Quiz (MCQ)        | Mock data    |
| Student | Progress tracking | Mock data    |
| Teacher | Dashboard/Heatmap | Mock data    |
| Teacher | Student list      | Mock data    |
| Admin   | Overview/Billing  | Mock data    |

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **OpenAI API key** (for embeddings + GPT-4o-mini)
- **NCERT PDFs** — 15 chapter PDFs for Class 8 Science (placed in `data/NCERT_PDFs/`)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/minakshi23286/learneriq.git
cd learneriq
```

### 2. Set up the backend

```bash
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Edit .env and add your OpenAI API key:
#   OPENAI_API_KEY=sk-...
```

### 3. Ingest NCERT PDFs

Place your NCERT Class 8 Science PDFs in `data/NCERT_PDFs/` with filenames:
`ncert_class8_science1.pdf` through `ncert_class8_science15.pdf`

```bash
cd backend
python ingest.py
```

This will chunk the PDFs, embed them with OpenAI, and persist the vector store to `backend/chroma_db/`. Run this once — it costs approximately $0.01.

### 4. Start the backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Verify it's running:
```bash
curl http://localhost:8000/api/health
# {"status":"ok","service":"LearnIQ API"}
```

### 5. Set up and start the frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server starts at **http://localhost:8080** and proxies all `/api/*` requests to FastAPI at port 8000.

### 6. Use the app

1. Open **http://localhost:8080**
2. Click **Login** and sign in as a **Student** (any email/password)
3. Navigate to **AI Chat**
4. Ask a science question (e.g., "What is crop rotation?")
5. Get a real RAG-powered answer with chapter citations

## Project Structure

```
learneriq/
├── frontend/                   React + Vite + TypeScript
│   ├── src/
│   │   ├── pages/
│   │   │   ├── student/
│   │   │   │   ├── Chat.tsx    <- Connected to real /api/chat
│   │   │   │   ├── Quiz.tsx    (mock data)
│   │   │   │   └── Progress.tsx (mock data)
│   │   │   ├── teacher/        (mock data)
│   │   │   ├── admin/          (mock data)
│   │   │   ├── Landing.tsx
│   │   │   ├── Login.tsx
│   │   │   └── ...
│   │   ├── data/mockData.ts    Mock data for non-chat features
│   │   ├── contexts/AuthContext.tsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts          Dev proxy: /api -> localhost:8000
│
├── backend/                    Python FastAPI + LangChain
│   ├── main.py                 FastAPI server (/api/chat, /api/health)
│   ├── rag_chain.py            LangChain RetrievalQA chain
│   ├── ingest.py               PDF ingestion pipeline
│   ├── requirements.txt
│   ├── .env.example
│   └── chroma_db/              (gitignored, built by ingest.py)
│
├── data/
│   ├── NCERT_PDFs/             (gitignored, add your PDFs here)
│   └── student_qa_logs_chapter1.json
│
├── .gitignore
└── README.md
```

## API Reference

### POST /api/chat

Send a student question and receive a RAG-grounded answer.

**Request:**
```json
{
  "question": "What is crop rotation?",
  "chapter": null
}
```

**Response:**
```json
{
  "answer": "Crop rotation is the practice of growing different crops...",
  "citations": [
    { "chapter": "Chapter 1 - Crop Production and Management", "page": 5, "source_file": "ncert_class8_science1.pdf" }
  ],
  "chunks_retrieved": 4
}
```

### GET /api/health

Returns `{"status": "ok", "service": "LearnIQ API"}` when the server is running.

## Configuration

| Setting | Location | Default |
|---------|----------|---------|
| OpenAI API key | `backend/.env` | (required) |
| LLM model | `backend/rag_chain.py` | gpt-4o-mini |
| Embedding model | `backend/rag_chain.py` | text-embedding-3-small |
| Chunk size | `backend/ingest.py` | 500 chars |
| Chunk overlap | `backend/ingest.py` | 50 chars |
| Retrieved chunks | `backend/rag_chain.py` | 4 |
| Frontend port | `frontend/vite.config.ts` | 8080 |
| Backend port | CLI flag | 8000 |

## Cost Estimate

| Operation | Model | Cost |
|-----------|-------|------|
| PDF ingestion (one-time) | text-embedding-3-small | ~$0.01 |
| Per student question | GPT-4o-mini + embedding | ~$0.001 |

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, shadcn/ui, React Router, Recharts
- **Backend:** FastAPI, LangChain, ChromaDB, OpenAI API
- **PDF Processing:** PyPDF, RecursiveCharacterTextSplitter
- **Vector Store:** ChromaDB (local, persistent)

## License

MIT
