# LearnIQ - AI Tutoring Platform for CBSE Grade 8 Science

LearnIQ is an AI-powered tutoring chatbot that answers student questions exclusively from the NCERT Class 8 Science textbook. Every answer includes chapter source citations so students can verify and study further.

## Features

- **RAG-powered Q&A**: Retrieval-Augmented Generation ensures answers come only from the textbook
- **Chapter Source Citations**: Every answer displays which chapter(s) the information came from
- **Teacher Dashboard**: Analytics on student questions, topic gaps, and low-confidence answers
- **Student Dashboard**: Personal learning progress, mastered topics, and areas to improve
- **Cost-efficient**: Uses GPT-4o-mini (~$0.15/1M input tokens) and text-embedding-3-small ($0.02/1M tokens)
- **Rate Limiter**: Built-in session limit to stay within the $5 demo budget
- **Mobile Responsive**: Works on phones, tablets, and desktops

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | GPT-4o-mini (OpenAI) |
| Embeddings | text-embedding-3-small (OpenAI) |
| Vector Store | ChromaDB (persisted to disk) |
| RAG Framework | LangChain RetrievalQA |
| Frontend | Streamlit |
| Data | NCERT Class 8 Science PDFs |

## Project Structure

```
learniq_chatbot_app/
├── learniq_chatbot.py      # Main chatbot app (Streamlit)
├── learniq_ingest.py       # PDF ingestion pipeline
├── teacher_dashboard.py    # Standalone teacher analytics
├── student_dashboard.py    # Standalone student progress tracker
├── requirements.txt        # Python dependencies
├── .env.example            # API key template
├── README.md               # This file
├── RUNNING_GUIDE.md        # Step-by-step setup and run instructions
└── chroma_db/              # (created after ingestion) Vector store
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your OpenAI API key
cp .env.example .env
# Edit .env and add your real key

# 3. Ingest the textbook PDFs (run once)
python learniq_ingest.py

# 4. Launch the chatbot
streamlit run learniq_chatbot.py
```

See [RUNNING_GUIDE.md](RUNNING_GUIDE.md) for detailed step-by-step instructions.

## Checkpoints

### Checkpoint 1: OS-Specific API Key Setup
- **macOS/Linux**: `export OPENAI_API_KEY="sk-..."` (add to `~/.zshrc` or `~/.bashrc`)
- **Windows CMD**: `set OPENAI_API_KEY=sk-...`
- **Windows PowerShell**: `$env:OPENAI_API_KEY="sk-..."`
- **Cross-platform** (recommended): Use a `.env` file (works everywhere)

### Checkpoint 2: Swap ChromaDB for Pinecone (2 lines)
In `learniq_ingest.py` and `learniq_chatbot.py`, change:
```python
# Line 1: Change the import/class
from langchain_pinecone import PineconeVectorStore

# Line 2: Remove persist_directory, add index_name
vectorstore = PineconeVectorStore.from_documents(chunks, embeddings, index_name="learniq")
```
Also: `pip install langchain-pinecone pinecone-client` and set `PINECONE_API_KEY` in `.env`.

### Checkpoint 3: Change Subject/Grade (1 variable)
In `learniq_ingest.py`, update `PDF_DIR` to point to your new textbook folder.
In `learniq_chatbot.py`, update `SUBJECT_CONFIG` dictionary.

## Cost Estimates

| Operation | Cost |
|-----------|------|
| Embedding 280 pages (one-time) | ~$0.01-0.04 |
| Per student question | ~$0.001-0.003 |
| 20 test questions | ~$0.03-0.05 |
| Full demo (~2000 questions) | ~$3-5 |

## Risk Review

| Risk | Description | Fix |
|------|-------------|-----|
| Hallucination | GPT-4o-mini may generate answers beyond textbook content | System prompt enforces "only answer from retrieved context"; test with out-of-scope questions to verify refusal |
| Cost Overrun | Student spam loop could exhaust the $5 budget | Rate limiter caps queries per session; max_tokens=512 limits output length |
| Deployment | ChromaDB local persist won't work on Streamlit Cloud (ephemeral filesystem) | Use `st.cache_resource` for session persistence; swap to Pinecone (2-line change) for cloud deployment |

## License

Educational project for CBSE Grade 8 Science tutoring.
