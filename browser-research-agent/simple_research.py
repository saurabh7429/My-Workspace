"""
Simple Research Agent - Step 1 (Baseline, non-agentic)
--------------------------------------------------------
Tum ek URL aur ek question/topic doge.
Script us page ko Playwright se kholega, text extract karega,
aur local Qwen2.5:3b (Ollama) ko de kar research/summary karwayega.

Run: python simple_research.py
"""

import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


def fetch_page_text(url: str, max_chars: int = 6000) -> str:
    """Playwright se page kholo aur clean text nikaalo."""
    print(f"[+] Opening: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)  # JS render hone do thoda
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Noise hatao - script, style, nav, footer, ads
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    clean_text = "\n".join(lines)

    print(f"[+] Extracted {len(clean_text)} characters")
    return clean_text[:max_chars]


def ask_qwen(context_text: str, question: str) -> str:
    """Qwen ko context + question do, answer wapas lo."""
    prompt = f"""Tum ek research assistant ho. Neeche diya gaya webpage content padho, aur uske base par diya gaya question/topic ka clear, structured answer do. Agar content mein relevant info nahi hai to saaf bata do.

WEBPAGE CONTENT:
{context_text}

QUESTION/TOPIC: {question}

Apna answer points mein, clear Hinglish/English mix mein do:"""

    print("[+] Asking Qwen2.5:3b...")
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_ctx": 4096,
            },
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]


def main():
    print("=== Simple Research Agent (Step 1) ===\n")
    url = input("URL daalo: ").strip()
    question = input("Kya jaanna hai (topic/question): ").strip()

    print()
    page_text = fetch_page_text(url)

    if not page_text:
        print("[!] Page se text nahi mila. URL check karo ya page JS-heavy ho sakta hai.")
        return

    answer = ask_qwen(page_text, question)

    print("\n" + "=" * 50)
    print("RESEARCH RESULT")
    print("=" * 50)
    print(answer)
    print("=" * 50)


if __name__ == "__main__":
    main()
