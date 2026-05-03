import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def extract_text_from_url(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Try to get title
    title = ""
    if soup.title:
        title = soup.title.string or ""

    # Extract main content
    main_content = ""
    for tag in ["article", "main", "div"]:
        container = soup.find(tag)
        if container:
            main_content = container.get_text(separator=" ")
            break

    if not main_content:
        main_content = soup.get_text(separator=" ")

    cleaned = clean_text(main_content)

    return {
        "source": url,
        "source_type": "blog",
        "title": title.strip(),
        "fetched_at": datetime.utcnow().isoformat(),
        "full_text": cleaned
    }


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


if __name__ == "__main__":
    url = input("Enter blog/article URL: ").strip()
    result = extract_text_from_url(url)
    print(f"\n✅ Extracted {len(result['full_text'])} characters from {result['title']}")
    print(f"Preview:\n{result['full_text'][:500]}")