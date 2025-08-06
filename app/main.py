# app/main.py

from fastapi import FastAPI
from app.router import router

app = FastAPI(
    title="LLM Query Retrieval System",
    version="1.0.0",
    description="Processes documents and answers natural language questions using Gemini."
)

app.include_router(router, prefix="/api/v1")
