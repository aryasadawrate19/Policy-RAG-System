# FAISS search

import faiss
import numpy as np
from app.embedder import embed_chunks

class ClauseRetriever:
    def __init__(self, chunks: list):
        self.chunks = chunks
        self.embeddings = embed_chunks(chunks)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings.astype('float32'))

    def search(self, query: str, top_k: int = 5) -> list:
        query_emb = embed_chunks([query])[0].astype('float32')
        D, I = self.index.search(np.array([query_emb]), top_k)
        return [self.chunks[i] for i in I[0]]
