"""
01_documents.py
----------------
Step 1 of the RAG pipeline: load the raw PDF, convert each page to an image,
and run OCR (Arabic) to extract the raw text of the document.

Output:
    raw_book_text.txt  -> the raw OCR text of the whole book, page by page.

Run:
    python 01_documents.py
"""

import os
from pdf2image import convert_from_path
import pytesseract

# ---- Config ----
PDF_PATH = "first_aid_book.pdf"
RAW_TEXT_PATH = "raw_book_text.txt"
OCR_LANG = "ara"
DPI = 200


def load_pdf_pages(pdf_path: str = PDF_PATH, dpi: int = DPI):
    """Convert every page of the PDF into a PIL image."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=dpi)
    print(f"Total pages: {len(pages)}")
    return pages


def extract_text_from_pages(pages, lang: str = OCR_LANG):
    """Run OCR on each page image and return a list of extracted text (one per page)."""
    extracted_pages = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, lang=lang)
        extracted_pages.append(text)
        print(f"Processed page {i + 1}/{len(pages)}")
    return extracted_pages


def save_raw_text(extracted_pages, output_path: str = RAW_TEXT_PATH):
    """Save all extracted pages into a single raw text file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, text in enumerate(extracted_pages):
            f.write(f"\n--- Page {i + 1} ---\n")
            f.write(text)
    print(f"Saved successfully to {output_path}")


def main():
    pages = load_pdf_pages()
    extracted_pages = extract_text_from_pages(pages)
    save_raw_text(extracted_pages)


if __name__ == "__main__":
    main()
