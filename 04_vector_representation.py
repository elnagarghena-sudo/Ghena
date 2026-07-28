"""
04_vector_representation.py
----------------------------
Step 4 of the RAG pipeline: turn each text chunk into a vector embedding
using a multilingual sentence-transformers model (supports Arabic).

Input:
    chunks.json

Output:
    embeddings.npy  -> numpy array of embeddings (same order as chunks.json)

Run:
    python 04_vector_representation.py
"""

import json
import numpy as np
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "chunks.json"
EMBEDDINGS_PATH = "embeddings.npy"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

_model = None


def get_model():
    """Load (once) and return the sentence-transformers model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_chunks(chunks):
    model = get_model()
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings


def main():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = embed_chunks(chunks)
    print(f"Embeddings created: {len(embeddings)}")

    np.save(EMBEDDINGS_PATH, embeddings)
    print(f"Saved: {EMBEDDINGS_PATH}")


if __name__ == "__main__":
    main()
