# app/router.py

from fastapi import APIRouter, HTTPException, Request
from app.schema import DocumentInput, QueryRequest, QueryResponse, RunResponse
from app.parser import process_document, parse_document
from app.embedder import embed_chunks, build_vector_store, search_similar_chunks
from app.evaluator import generate_json_answer
from app.retriever import ClauseRetriever
from app.matcher import filter_clauses
from pathlib import Path
import uuid

router = APIRouter(prefix="/api/v1")

@router.post("/hackrx/run", response_model=RunResponse)
async def run_query(request: QueryRequest):
    try:
        doc_path = await process_document(request.documents)

        chunks = await embed_chunks(doc_path)
        index = await build_vector_store(chunks)

        all_answers = []
        for question in request.questions:
            top_chunks = await search_similar_chunks(question, index, chunks)
            result = generate_json_answer(question, top_chunks)
            all_answers.append(result["answer"])  # Only 'answer' key required in output

        return {"answers": all_answers}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hackrx/run", response_model=RunResponse)
def run_submission(payload: DocumentInput, request: Request):
    # Download and parse document
    try:
        chunks = parse_document(payload.documents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    retriever = ClauseRetriever(chunks)
    answers = []
    for question in payload.questions:
        retrieved = retriever.search(question, top_k=8)
        filtered = filter_clauses(question, retrieved)
        result = generate_json_answer(question, filtered)
        answers.append(result["answer"])
    return RunResponse(answers=answers)
