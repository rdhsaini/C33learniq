# LearnIQ — Step-by-Step Validation Guide

## Part A: Validate the RAG Chatbot (learniq_app.py)

### Step 1: Environment Setup
```bash
pip install streamlit langchain langchain-openai langchain-community chromadb pypdf openai
export OPENAI_API_KEY="sk-YOUR-KEY-HERE"   # macOS/Linux
# Windows: set OPENAI_API_KEY=sk-YOUR-KEY-HERE
```
✅ Checkpoint: `echo $OPENAI_API_KEY` returns your key (not empty).

---

### Step 2: Place your PDF
- Copy your NCERT Class 8 Science PDF into the same folder as `learniq_app.py`
- Rename it to `ncert_class8_science.pdf`  (or update `SUBJECT_CONFIG["pdf_path"]`)

✅ Checkpoint: `ls ncert_class8_science.pdf` shows the file.

---

### Step 3: First Run (embedding phase — this costs ~$0.04)
```bash
streamlit run learniq_app.py
```
- You will see "Loading and indexing textbook…" spinner
- A folder `chroma_grade8_science/` will appear in your directory
- This only happens ONCE — subsequent restarts skip embedding (zero cost)

✅ Checkpoint: `chroma_grade8_science/` folder exists after first run.

---

### Step 4: Functional Test Questions (run these in the chat)
Test each and verify the answer + source badge appears:

| # | Test Question | Expected Behaviour |
|---|---------------|--------------------|
| 1 | "What is kharif crop?" | Answer with page citation |
| 2 | "Give examples of rabi crops" | 3+ examples cited from textbook |
| 3 | "What is Newton's third law?" | "I couldn't find this in the textbook…" |
| 4 | "Explain photosynthesis" | Should answer IF in textbook |
| 5 | "What is crop rotation?" | Clear answer + page badge |

✅ Checkpoint: Question 3 triggers the "not found" safeguard — this confirms hallucination guard works.

---

### Step 5: Cost Monitoring
After 20 test questions, check your OpenAI dashboard:
- Go to platform.openai.com → Usage
- Expected cost for 20 questions: < $0.05
- GPT-4o-mini rate: ~$0.15/1M input tokens, $0.60/1M output tokens
- Full demo budget: $5 → ~2,000 student questions

✅ Checkpoint: Cost is under $0.10 after initial testing.

---

## Part B: Validate the JSON Dataset (student_qa_logs_chapter1.json)

### Step 6: Load into Pandas
```python
import pandas as pd, json

with open("student_qa_logs_chapter1.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(df.shape)           # Should be (50, 7)
print(df.columns.tolist()) # ['student_id','chapter','question','ai_answer','confidence','topic_tag','timestamp']
print(df['topic_tag'].value_counts())  # Check topic distribution
print(df['confidence'].describe())     # Mean should be ~0.89
```

✅ Checkpoint: Shape is (50, 7) with no null values (`df.isnull().sum()` all zeros).

---

### Step 7: Build Quick Dashboard Chart
```python
import matplotlib.pyplot as plt

# Chart 1: Topic distribution (shows teacher which concepts are most asked)
df['topic_tag'].value_counts().plot(kind='barh', figsize=(10,6), color='steelblue')
plt.title('Most Asked Topics — Chapter 1')
plt.xlabel('Number of Questions')
plt.tight_layout()
plt.savefig('topic_distribution.png')

# Chart 2: Confidence score distribution (low confidence = risky answers)
df['confidence'].hist(bins=10, figsize=(8,4), color='orange', edgecolor='black')
plt.title('AI Confidence Score Distribution')
plt.xlabel('Confidence')
plt.savefig('confidence_distribution.png')
```

✅ Checkpoint: Both PNG files generated without errors.

---

### Step 8: Build Streamlit Teacher Dashboard (minimal version)
```python
# teacher_dashboard.py
import streamlit as st
import pandas as pd, json

with open("student_qa_logs_chapter1.json") as f:
    df = pd.DataFrame(json.load(f))

st.title("📊 LearnIQ Teacher Dashboard")
st.metric("Total Questions", len(df))
st.metric("Avg Confidence", f"{df['confidence'].mean():.2f}")
st.metric("Low Confidence Questions (<0.85)", int((df['confidence'] < 0.85).sum()))

st.subheader("Questions by Topic")
st.bar_chart(df['topic_tag'].value_counts())

st.subheader("Students Needing Help (confidence < 0.85)")
st.dataframe(df[df['confidence'] < 0.85][['student_id','question','confidence','topic_tag']])
```
```bash
streamlit run teacher_dashboard.py
```

✅ Checkpoint: Dashboard shows 50 rows and highlights ~10 low-confidence questions.

---

## Part C: Risk Mitigations

### ⚠️ Risk 1 — Hallucination
**Risk**: GPT-4o-mini may generate plausible-sounding but textbook-incorrect answers.
**Fix**: The system prompt forces "only answer from retrieved context." Test with out-of-scope questions (Step 4, Q3) to confirm the refusal works. Also manually verify 5 answers against the actual textbook.

### 💸 Risk 2 — Cost Overrun
**Risk**: A student in a loop (accidental or otherwise) could spam 500 queries.
**Fix**: Add a rate limiter in `learniq_app.py`:
```python
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if st.session_state.query_count > 50:
    st.warning("Daily limit reached. Please try again tomorrow.")
    st.stop()
st.session_state.query_count += 1
```

### 🚀 Risk 3 — Deployment
**Risk**: ChromaDB's local persist directory won't work on Streamlit Cloud (ephemeral filesystem).
**Fix**: Use `st.cache_resource` (already in the code) + switch to Chroma's hosted service OR swap to Pinecone (2-line change shown in code comments) which works on any cloud.

---

## Quick Validation Checklist

- [ ] App loads without errors
- [ ] PDF embeds successfully (chroma folder created)
- [ ] In-scope questions return answers with page badges
- [ ] Out-of-scope questions return "not found" message
- [ ] JSON loads into Pandas with shape (50, 7)
- [ ] Dashboard shows topic distribution chart
- [ ] OpenAI cost < $0.10 after 20 test questions
- [ ] Rate limiter tested and working
