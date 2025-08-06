# Clause filtering (semantic + keyword)

from typing import List
import re

def keyword_match(query: str, clause: str) -> bool:
    keywords = re.findall(r'\w+', query.lower())
    clause_text = clause.lower()
    return any(k in clause_text for k in keywords)

def filter_clauses(query: str, clauses: List[str]) -> List[str]:
    # Semantic + keyword filtering
    return [c for c in clauses if keyword_match(query, c)]
