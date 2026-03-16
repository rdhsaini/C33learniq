"""
LearnIQ — RAG Chain Module
============================
Builds and returns a LangChain RetrievalQA chain backed by ChromaDB + GPT-4o-mini.
Used by main.py (FastAPI) to answer student questions from the NCERT textbook.
"""

import os
from functools import lru_cache
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# ── Configuration ──────────────────────────────────────────────────────────────
CHROMA_PERSIST = os.path.join(os.path.dirname(__file__), "chroma_db")
EMBEDDING_MODEL = "text-embedding-3-small"  # $0.02/1M tokens
LLM_MODEL = "gpt-4o-mini"                  # ~$0.15/1M input tokens
TOP_K = 4                                   # source chunks per query

# ── System prompt: strict retrieval-only answers ───────────────────────────────
SYSTEM_PROMPT = """You are LearnIQ, an AI tutor for CBSE Class 10 Science (NCERT textbook).


RULES — follow these strictly:
1. Only answer from retrieved context. If the answer is not found in the context, say:
   "I couldn't find this in the NCERT Class 10 Science textbook. Please check your textbook or ask your teacher."
2. Do NOT make up facts or use knowledge outside the provided context.
3. Explain concepts in simple language suitable for a Class 10 student.
4. Detect the language of the student's question. If the question is in Hindi, respond entirely in Hindi. If in English, respond in English.
5. Use bullet points or numbered steps when explaining processes.
6. Always end your answer by citing the chapter source(s) from the context metadata.

CONTEXT FROM TEXTBOOK:
{context}

STUDENT QUESTION:
{question}

YOUR ANSWER:"""

QA_PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"],
)


@lru_cache(maxsize=1)
def get_qa_chain():
    """
    Builds the RetrievalQA chain. Cached so it's only created once per process.
    The chain loads ChromaDB from disk (built by ingest.py) and uses GPT-4o-mini.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=api_key,
    )

    if not os.path.exists(CHROMA_PERSIST) or not os.listdir(CHROMA_PERSIST):
        raise FileNotFoundError(
            f"ChromaDB not found at {CHROMA_PERSIST}. "
            "Run 'python ingest.py' first to build the vector store."
        )

    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST,
        embedding_function=embeddings,
    )

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0.2,
        max_tokens=512,
        openai_api_key=api_key,
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
