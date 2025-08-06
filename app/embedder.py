# app/embedder.py

import faiss
import numpy as np
from google import genai
from app.parser import extract_text_chunks
from app.utils import load_env_var

client = genai.Client()

# Global store for simplicity (can use DB later)
CHUNK_STORE = []  # List[Dict] → [{text, metadata}]


def get_embedding(text: str) -> np.ndarray:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text]
    )
    return np.array(result.embeddings[0].values)


def embed_chunks(chunks: list) -> np.ndarray:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunks
    )
    return np.array([emb.values for emb in result.embeddings])


async def embed_chunks(file_path: str):
    """
    Extracts + embeds all chunks from a document.
    Returns the list of {embedding, text, metadata}.
    """
    global CHUNK_STORE
    CHUNK_STORE.clear()  # Reset for each doc

    chunks = await extract_text_chunks(file_path)

    for chunk in chunks:
        content = chunk["text"]
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=[content]
        )
        embedding = response.embeddings[0].values

        CHUNK_STORE.append({
            "text": content,
            "metadata": chunk["metadata"],
            "vector": np.array(embedding, dtype=np.float32)
        })

    return CHUNK_STORE


async def build_vector_store(chunks) -> faiss.IndexFlatL2:
    """
    Builds a FAISS index from embedded chunks.
    Returns the FAISS index object.
    """
    dim = len(chunks[0]["vector"])
    index = faiss.IndexFlatL2(dim)

    vectors = np.array([c["vector"] for c in chunks], dtype=np.float32)
    index.add(vectors)

    return index


async def search_similar_chunks(query: str, index, chunks, top_k=5):
    """
    Embed the query → search FAISS → return top-k matching chunks
    """
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[query]
    )
    query_vector = np.array(response.embeddings[0].values, dtype=np.float32).reshape(1, -1)

    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        results.append({
            "text": chunks[idx]["text"],
            "metadata": chunks[idx]["metadata"]
        })

    return results
