# LLM Query System

A system for querying documents using LLMs, semantic search, and clause matching.

## Structure
- `app/`: Main application code
- `data/docs/`: Raw downloaded documents
- `data/embeddings/`: FAISS index files
- `.env`: API keys
- `requirements.txt`: Python dependencies

## Features
- PDF/DOCX/Email parsing
- Gemini embedding and logic evaluation
- FAISS-based retrieval
- Clause filtering (semantic + keyword)
