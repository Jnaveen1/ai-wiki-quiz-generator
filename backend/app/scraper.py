import requests
from bs4 import BeautifulSoup
import re


def scrape_wikipedia(url: str):
    # Wikipedia blocks requests without User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Wikipedia page. Status: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # TITLE
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # MAIN CONTENT CONTAINERS
    content_div = soup.find("div", id="mw-content-text")
    parser_output = soup.find("div", class_="mw-parser-output")

    if not content_div or not parser_output:
        raise Exception("Wikipedia page structure not found")

    # PARAGRAPHS (SUMMARY + CONTENT)
    paragraphs = content_div.find_all("p")

    cleaned_paragraphs = []
    for p in paragraphs:
        text = p.get_text(" ", strip=True)

        # Remove citation markers like [1], [23]
        text = re.sub(r"\[\d+\]", "", text)

        # Skip junk / metadata
        if len(text) < 40:
            continue
        if text.lower().startswith("coordinates"):
            continue

        cleaned_paragraphs.append(text)

    if not cleaned_paragraphs:
        raise Exception("No valid article content extracted")

    # Summary = first meaningful paragraph
    summary = cleaned_paragraphs[0]

    # Full content for LLM grounding
    content = " ".join(cleaned_paragraphs)

    # SECTION HEADINGS
    sections = []
    for h2 in parser_output.find_all("h2"):
        span = h2.find("span", class_="mw-headline")
        if span:
            sections.append(span.get_text(strip=True))

    # FINAL STRUCTURED OUTPUT
    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "content": content
    }
