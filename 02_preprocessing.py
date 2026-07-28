"""
02_preprocessing.py
--------------------
Step 2 of the RAG pipeline: clean the raw OCR text
(remove page markers, extra blank lines, repeated spaces/dots, empty lines).

Input:
    raw_book_text.txt

Output:
    cleaned_book_text.txt

Run:
    python 02_preprocessing.py
"""

import re

RAW_TEXT_PATH = "raw_book_text.txt"
CLEANED_TEXT_PATH = "cleaned_book_text.txt"


def clean_text(text: str) -> str:
    text = re.sub(r"--- Page \d+ ---", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"[.]{3,}", " ", text)
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line != ""]
    return "\n".join(lines)


def main():
    with open(RAW_TEXT_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()
    print(f"Raw text length: {len(raw_text)}")

    cleaned_text = clean_text(raw_text)
    print(f"Cleaned text length: {len(cleaned_text)}")

    with open(CLEANED_TEXT_PATH, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"Saved: {CLEANED_TEXT_PATH}")


if __name__ == "__main__":
    main()
