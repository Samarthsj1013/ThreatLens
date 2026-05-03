import fitz  # PyMuPDF
import os
import re


def extract_text_from_pdf(pdf_path: str) -> dict:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    full_text = ""
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        cleaned = clean_text(text)
        pages.append({"page": page_num + 1, "text": cleaned})
        full_text += cleaned + "\n"

    doc.close()

    return {
        "source": os.path.basename(pdf_path),
        "source_type": "pdf",
        "total_pages": len(pages),
        "pages": pages,
        "full_text": full_text.strip()
    }


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def extract_text_from_multiple_pdfs(pdf_folder: str) -> list:
    results = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            print(f"📄 Processing: {filename}")
            result = extract_text_from_pdf(path)
            results.append(result)
    return results


if __name__ == "__main__":
    test_path = input("Enter path to a PDF file: ").strip()
    result = extract_text_from_pdf(test_path)
    print(f"\n✅ Extracted {len(result['full_text'])} characters from {result['source']}")
    print(f"Preview:\n{result['full_text'][:500]}")