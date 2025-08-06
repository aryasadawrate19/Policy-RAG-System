# app/schema.py

from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class QueryRequest(BaseModel):
    documents: HttpUrl
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

class DocumentInput(BaseModel):
    documents: str  # URL or path to document
    questions: List[str]

class ClauseMetadata(BaseModel):
    page: Optional[int]
    section: Optional[str]

class Clause(BaseModel):
    text: str
    metadata: ClauseMetadata

class AnswerResponse(BaseModel):
    answer: str
    reasoning: str
    source_clauses: List[Clause]

class RunResponse(BaseModel):
    answers: List[str]
