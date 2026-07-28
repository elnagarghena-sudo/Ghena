"""
06_retrieve_context.py
------------------------
Step 6 of the RAG pipeline: given a user question, embed it with the same
model used for the chunks, then query ChromaDB for the most similar chunks.

Run (quick test):
    python 06_retrieve_context.py
"""

import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"
import chromadb

from importlib import import_module

# reuse the same embedding model helper from step 4
vector_representation = import_module("04_vector_representation")

CHROMA_PATH = "./chroma_store"
COLLECTION_NAME = "first_aid_book"

_client = None
_collection = None


def get_collection():
    """Lazily connect to the persistent Chroma collection."""
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def retrieve_context(query: str, n_results: int = 3):
    """
    Return a list of the most relevant text chunks (and their distances)
    for the given query.
    """
    model = vector_representation.get_model()
    query_embedding = model.encode([query]).tolist()

    collection = get_collection()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    documents = results["documents"][0]
    distances = results.get("distances", [[None] * len(documents)])[0]
    return list(zip(documents, distances))


if __name__ == "__main__":
    test_question = "ما هي أعراض الكسر؟"
    retrieved = retrieve_context(test_question)
    for i, (chunk, dist) in enumerate(retrieved):
        print(f"--- Result {i + 1} (distance={dist}) ---")
        print(chunk[:300])
        print()
