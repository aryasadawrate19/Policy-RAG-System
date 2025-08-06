# app/utils.py

import os
from typing import List
from dotenv import load_dotenv
import re

load_dotenv()

def load_env_var(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing environment variable: {key}")
    return value


def detect_file_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return "pdf"
    elif ext == ".docx":
        return "docx"
    elif ext in [".eml", ".msg"]:
        return "email"
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def chunk_text(text: str, max_words: int = 120) -> List[str]:
    """
    Splits a long string into smaller chunks of `max_words` length.
    """
    words = text.split()
    chunks = [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
    return chunks

def chunk_text_by_sentences(text: str, chunk_size: int = 500) -> list:
    """
    Splits text into chunks by sentences, with a fallback to fixed size chunks.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current = ''
    for sentence in sentences:
        if len(current) + len(sentence) < chunk_size:
            current += sentence + ' '
        else:
            chunks.append(current.strip())
            current = sentence + ' '
    if current:
        chunks.append(current.strip())
    return chunks
