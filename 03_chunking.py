"""
03_chunking.py
--------------
Step 3 of the RAG pipeline: split the cleaned text into overlapping word chunks.

Input:
    cleaned_book_text.txt

Output:
    chunks.json  -> list of text chunks

Run:
    python 03_chunking.py
"""

import json

CLEANED_TEXT_PATH = "cleaned_book_text.txt"
CHUNKS_PATH = "chunks.json"

CHUNK_SIZE = 500
OVERLAP = 50


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks


def main():
    with open(CLEANED_TEXT_PATH, "r", encoding="utf-8") as f:
        cleaned_text = f.read()

    chunks = chunk_text(cleaned_text)
    print(f"Total chunks: {len(chunks)}")

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Saved: {CHUNKS_PATH}")


if __name__ == "__main__":
    main()
