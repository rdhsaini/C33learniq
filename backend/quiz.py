"""
LearnIQ — Quiz Generator
========================
Generates a single adaptive MCQ based on the last answer context.
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

QUIZ_PROMPT_TEMPLATE = """You are LearnIQ, an AI tutor for CBSE Class 8 Science.

Based on the following answer that was just given to a student, generate ONE multiple choice question to test their understanding.

PREVIOUS ANSWER:
{answer}

RULES:
1. Generate exactly 4 options labelled A, B, C, D
2. Only one option is correct
3. Keep language simple for a Class 8 student
4. Return ONLY valid JSON in this exact format, nothing else:
{{
  "question": "the question text",
  "options": {{
    "A": "option text",
    "B": "option text", 
    "C": "option text",
    "D": "option text"
  }},
  "correct": "A",
  "explanation": "brief explanation of why this is correct"
}}"""

QUIZ_PROMPT = PromptTemplate(
    template=QUIZ_PROMPT_TEMPLATE,
    input_variables=["answer"],
)

def generate_quiz(answer: str) -> dict:
    """Generate a MCQ based on the provided answer text."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set.")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=512,
        openai_api_key=api_key,
    )

    prompt = QUIZ_PROMPT.format(answer=answer)
    response = llm.invoke(prompt)
    
    import json
    content = response.content.strip()
    # Strip markdown code fences if present
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    
    return json.loads(content.strip())