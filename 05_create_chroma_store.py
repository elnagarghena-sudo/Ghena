"""
05_create_chroma_store.py
--------------------------
Step 5 of the RAG pipeline: store the chunks + their embeddings inside a
persistent ChromaDB collection on disk, so we don't need to re-embed every time.

Input:
    chunks.json
    embeddings.npy

Output:
    ./chroma_store/  -> persistent Chroma database folder

Run:
    python 05_create_chroma_store.py
"""

import os
import json
import numpy as np

os.environ["ANONYMIZED_TELEMETRY"] = "False"
import chromadb

CHUNKS_PATH = "chunks.json"
EMBEDDINGS_PATH = "embeddings.npy"
CHROMA_PATH = "./chroma_store"
COLLECTION_NAME = "first_aid_book"


def get_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)


def build_store():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    embeddings = np.load(EMBEDDINGS_PATH)

    client = get_client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids,
    )
    print(f"Total items stored in Chroma: {collection.count()}")
    return collection


if __name__ == "__main__":
    build_store()
