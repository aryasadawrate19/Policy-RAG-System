# app/evaluator.py

import google.generativeai as genai
from app.utils import load_env_var
import json
import re

# Load Gemini API key
genai.configure(api_key=load_env_var("GEMINI_API_KEY"))

# Load Gemini 2.5 Flash model
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_json_answer(question: str, retrieved_chunks: list) -> dict:
    """
    Sends a prompt to Gemini to generate a structured JSON answer based on retrieved chunks.
    """

    # Combine retrieved document chunks into a context string
    context = "\n\n".join(
        [f"[Clause {i+1}]\n{chunk['text']}" for i, chunk in enumerate(retrieved_chunks)]
    )

    # Prompt template
    prompt = f"""
You are an intelligent assistant answering questions based on policy or legal documents.

### Context:
{context}

### Question:
{question}

### Instructions:
- Read the above clauses carefully.
- Answer the question clearly and briefly.
- Provide a short explanation with citation to clause(s).
- Return response ONLY in the following JSON format:
{{
  "answer": "<yes/no/short answer>",
  "reasoning": "<short explanation with clause reference>",
  "source_clauses": [
    {{
      "text": "<matching clause text>",
      "metadata": {{
        "page": <page number or paragraph>,
        "section": "<optional section title>"
      }}
    }}
  ]
}}
Do not include anything else outside this JSON.
"""

    # Send to Gemini
    response = model.generate_content(prompt)

    raw_text = response.text
    # Remove Markdown code block markers if present
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    # Parse Gemini's JSON-only output
    try:
        json_start = cleaned.find("{")
        json_response = json.loads(cleaned[json_start:])
        return json_response
    except Exception as e:
        raise ValueError(
            f"Failed to parse Gemini response as JSON: {e}\n\nRaw response:\n{response.text}"
        )
