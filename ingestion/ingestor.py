from ingestion.pdf_ingestor import extract_text_from_pdf
from ingestion.blog_ingestor import extract_text_from_url
import os


def ingest(source: str) -> dict:
    """
    Universal ingestor — detects if source is a PDF path or URL
    and routes to the correct ingestor.
    """
    if source.startswith("http://") or source.startswith("https://"):
        print(f"🌐 Detected URL — using blog ingestor")
        return extract_text_from_url(source)

    elif source.endswith(".pdf") and os.path.exists(source):
        print(f"📄 Detected PDF — using PDF ingestor")
        return extract_text_from_pdf(source)

    else:
        raise ValueError(f"Unsupported source: {source}. Must be a URL or valid PDF path.")


def ingest_batch(sources: list) -> list:
    """
    Ingest multiple sources at once.
    Returns list of results.
    """
    results = []
    for source in sources:
        try:
            print(f"\n⏳ Ingesting: {source}")
            result = ingest(source)
            results.append({"status": "success", "data": result})
            print(f"✅ Done: {result['source']}")
        except Exception as e:
            print(f"❌ Failed: {source} — {e}")
            results.append({"status": "failed", "source": source, "error": str(e)})
    return results


if __name__ == "__main__":
    print("=== ThreatLens Ingestor ===")
    print("1. Ingest PDF")
    print("2. Ingest Blog URL")
    choice = input("Choose (1/2): ").strip()

    if choice == "1":
        path = input("PDF path: ").strip()
        result = ingest(path)
    elif choice == "2":
        url = input("Blog URL: ").strip()
        result = ingest(url)
    else:
        print("Invalid choice")
        exit()

    print(f"\n✅ Ingested: {result['source']}")
    print(f"Preview:\n{result['full_text'][:500]}")