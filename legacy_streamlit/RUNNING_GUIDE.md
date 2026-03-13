# LearnIQ — Step-by-Step Running Guide

## Prerequisites

- Python 3.9 or higher
- An OpenAI API key (get one at https://platform.openai.com/api-keys)
- NCERT Class 8 Science PDFs (should already be in `../NCERT Class 8 Science PDF/`)

---

## Step 1: Install Python Dependencies

Open a terminal and navigate to the app folder:

```bash
cd learniq_chatbot_app
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import streamlit, langchain, chromadb; print('All packages installed!')"
```

---

## Step 2: Set Up Your OpenAI API Key

### Option A: .env file (Recommended — works on all OS)
```bash
cp .env.example .env
```
Edit `.env` and replace `sk-your-key-here` with your actual key:
```
OPENAI_API_KEY=sk-proj-abc123...
```

### Option B: Environment variable

**macOS / Linux:**
```bash
export OPENAI_API_KEY="sk-proj-abc123..."
```
To make it permanent, add the line above to `~/.zshrc` (macOS) or `~/.bashrc` (Linux), then:
```bash
source ~/.zshrc   # or source ~/.bashrc
```

**Windows CMD:**
```cmd
set OPENAI_API_KEY=sk-proj-abc123...
```

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-proj-abc123..."
```

### Option C: Paste in the app
If no key is set, the chatbot will show a text input in the sidebar where you can paste your key.

**Verify:**
```bash
# macOS/Linux
echo $OPENAI_API_KEY

# Windows CMD
echo %OPENAI_API_KEY%

# Windows PowerShell
echo $env:OPENAI_API_KEY
```

---

## Step 3: Verify PDF Files

Make sure the NCERT PDFs exist in the parent directory:

```bash
ls "../NCERT Class 8 Science PDF/"
```

You should see files like:
```
ncert_class8_science1.pdf
ncert_class8_science2.pdf
...
ncert_class8_science15.pdf
```

---

## Step 4: Run the Ingestion Pipeline (One-Time)

This step loads PDFs, chunks them, embeds with OpenAI, and saves to ChromaDB:

```bash
python learniq_ingest.py
```

**Expected output:**
```
===============================================================
  LearnIQ — PDF Ingestion Pipeline
  NCERT Class 8 Science -> ChromaDB Vector Store
===============================================================

STEP 1 — Loading PDFs from: ../NCERT Class 8 Science PDF
  Loaded ncert_class8_science1.pdf  ->  XX pages  [Chapter 1 – Crop Production...]
  ...

STEP 2 — Chunking (size=500, overlap=50)
  Total chunks created: XXX

STEP 3 — Embedding with text-embedding-3-small + persisting to ChromaDB
  Done in XX.Xs

STEP 4 — Verification
  ...

  INGESTION COMPLETE
```

**Verify:** A `chroma_db/` folder should now exist:
```bash
ls chroma_db/
```

**Cost:** This step costs approximately $0.01-0.04 (one-time only).

---

## Step 5: Launch the Chatbot

```bash
streamlit run learniq_chatbot.py
```

The app will open in your browser at `http://localhost:8501`.

**Test with these questions:**

| # | Question | Expected |
|---|----------|----------|
| 1 | What is the difference between kharif and rabi crops? | Answer with chapter badge |
| 2 | How does friction affect motion? | Answer with Chapter 12 badge |
| 3 | What is Newton's third law? | "I couldn't find this..." (not in Class 8) |
| 4 | What causes sound? | Answer with Chapter 13 badge |

Question 3 should trigger the hallucination guard (Grade 8 textbook doesn't cover Newton's Third Law in detail).

---

## Step 6: Open the Teacher Dashboard

### From the chatbot:
Click **"Open Teacher Dashboard"** button in the sidebar.

### Standalone:
```bash
streamlit run teacher_dashboard.py
```

**What to check:**
- 50 rows of Q&A data loaded
- Topic distribution bar chart displayed
- Low-confidence questions highlighted (confidence < 85%)
- Per-student summary table

---

## Step 7: Open the Student Dashboard

### From the chatbot:
Click **"Open Student Dashboard"** button in the sidebar.

### Standalone:
```bash
streamlit run student_dashboard.py
```

---

## Step 8: Monitor Costs

After testing, check your OpenAI usage:
1. Go to https://platform.openai.com/usage
2. Verify cost is under $0.10 after initial testing
3. Budget math: $5 budget supports approximately 2,000 student questions

---

## Troubleshooting

### "Vector store not found"
Run the ingestion script first: `python learniq_ingest.py`

### "OPENAI_API_KEY not set"
Set your key using one of the methods in Step 2.

### "No PDFs found"
Ensure PDFs are in `../NCERT Class 8 Science PDF/` relative to this folder.

### ChromaDB errors on re-run
Delete the `chroma_db/` folder and re-run ingestion:
```bash
rm -rf chroma_db/
python learniq_ingest.py
```

### Port already in use
```bash
streamlit run learniq_chatbot.py --server.port 8502
```

---

## Changing Subject or Grade

1. Place new textbook PDFs in a folder
2. In `learniq_ingest.py`: Update `PDF_DIR` and `CHAPTER_MAP`
3. In `learniq_chatbot.py`: Update `SUBJECT_CONFIG`
4. Delete `chroma_db/` and re-run `python learniq_ingest.py`

---

## Swapping ChromaDB for Pinecone

1. Install: `pip install langchain-pinecone pinecone-client`
2. Add to `.env`: `PINECONE_API_KEY=your-pinecone-key`
3. In both `learniq_ingest.py` and `learniq_chatbot.py`, change 2 lines (marked with CHECKPOINT #2 comments)
