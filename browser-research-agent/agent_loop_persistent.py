"""
Research Agent - Step 3 (TRUE Agentic Loop)
--------------------------------------------------------
Ab Qwen khud decide karta hai kaunsa tool kab use karna hai.
Python sirf "hands and eyes" hai - Qwen "brain" hai.

Tools available to Qwen:
  - search_web(query)       -> DuckDuckGo search results
  - open_url(url)           -> page kholo
  - read_page_text()        -> current page ka text content
  - read_page_links()       -> current page ke clickable links/buttons (text + index)
  - click_element(index)    -> link/button pe click karo (index from read_page_links)
  - done(answer)            -> final answer do, loop khatam

NOTE: 3B model ke saath ye unreliable ho sakta hai - invalid JSON,
galat tool names, ya loops mein stuck hona possible hai. Ye EXPECTED hai,
isi se hum dekhenge ki bigger model (7B) kyun zaroori hota hai agentic
tasks ke liye.

Run: python agent_loop.py
"""

import json
import os
import platform
import re
import time

import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"
MAX_STEPS = 10
HEADLESS = False
USE_BRAVE_IF_AVAILABLE = True

CHALLENGE_MARKERS = [
    "just a moment", "checking your browser", "verify you are human",
    "captcha", "unusual traffic", "cf-browser-verification",
]

SYSTEM_PROMPT = """Tum ek autonomous browser research agent ho. Tumhare paas ye tools hain:

1. search_web(query) - DuckDuckGo pe search karo
2. open_url(url) - kisi specific URL ko kholo
3. read_page_text() - current page ka text content padho
4. read_page_links(max_items) - current page ke clickable links/buttons dekho (text + index ke saath)
5. click_element(index) - read_page_links se mila index use karke click karo
6. done(answer) - jab task complete ho jaye, final answer do

RULES:
- Tumhe HAMESHA sirf ek valid JSON object respond karna hai, kuch aur nahi (no explanation, no markdown).
- Format: {"tool": "<tool_name>", "args": {...}}
- Examples:
  {"tool": "search_web", "args": {"query": "surat weather today"}}
  {"tool": "open_url", "args": {"url": "https://example.com"}}
  {"tool": "read_page_text", "args": {}}
  {"tool": "read_page_links", "args": {"max_items": 15}}
  {"tool": "click_element", "args": {"index": 3}}
  {"tool": "done", "args": {"answer": "final answer yahan"}}
- Ek baar mein sirf EK tool call karo.
- Pehle search_web ya open_url se shuru karo, fir read_page_text se content padho.
- Jab tumhare paas kaafi information ho jaye, "done" tool call karo answer ke saath.
- Agar same tool baar baar fail ho raha hai, dusra approach try karo.
- Maximum steps limited hain, isliye efficient raho.
"""


def get_brave_path():
    system = platform.system()
    if system == "Linux":
        candidates = ["/opt/brave.com/brave/brave", "/usr/bin/brave-browser",
                      "/usr/bin/brave", "/snap/bin/brave"]
    elif system == "Windows":
        candidates = [r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"]
    elif system == "Darwin":
        candidates = ["/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"]
    else:
        return None
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def looks_like_challenge_page(html: str) -> bool:
    lowered = html.lower()
    return any(marker in lowered for marker in CHALLENGE_MARKERS)


class BrowserAgent:
    def __init__(self):
        self.p = sync_playwright().start()
        launch_args = {
            "headless": HEADLESS,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--mute-audio",
            ],
            "ignore_default_args": ["--enable-automation"],
        }
        if USE_BRAVE_IF_AVAILABLE:
            brave_path = get_brave_path()
            if brave_path:
                launch_args["executable_path"] = brave_path
                print(f"[+] Using Brave: {brave_path}")

        self.browser = self.p.chromium.launch(**launch_args)
        self.context = self.browser.new_context(
            viewport=None if not HEADLESS else {"width": 1366, "height": 768}
        )
        self.context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.page = self.context.new_page()
        self.page.set_default_timeout(30000)
        self.last_links = []  # store (locator, text) for click_element

    def close(self):
        try:
            self.context.close()
            self.browser.close()
            self.p.stop()
        except Exception:
            pass

    def _current_html(self):
        return self.page.content()

    def _wait_and_handle_challenge(self):
        html = self._current_html()
        if looks_like_challenge_page(html):
            print("[!] Challenge page detect hua, 6s wait...")
            self.page.wait_for_timeout(6000)

    # ---- TOOLS ----

    def search_web(self, query: str) -> str:
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        try:
            self.page.goto(url, timeout=30000, wait_until="domcontentloaded")
            self.page.wait_for_timeout(1500)
            self._wait_and_handle_challenge()
            return f"Search results page khul gaya for '{query}'. Ab read_page_text ya read_page_links use karo."
        except Exception as e:
            return f"ERROR: search fail hua - {e}"

    def open_url(self, url: str) -> str:
        try:
            self.page.goto(url, timeout=30000, wait_until="domcontentloaded")
            self.page.wait_for_timeout(1500)
            self._wait_and_handle_challenge()
            return f"Page khul gaya: {url}"
        except Exception as e:
            return f"ERROR: page open nahi hua - {e}"

    def read_page_text(self, max_chars: int = 3000) -> str:
        try:
            html = self._current_html()
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            clean = "\n".join(lines)
            return clean[:max_chars] if clean else "Page khaali hai ya text nahi mila."
        except Exception as e:
            return f"ERROR: text read nahi hua - {e}"

    def read_page_links(self, max_items: int = 15) -> str:
        try:
            elements = self.page.locator("a, button").all()
            self.last_links = []
            output_lines = []
            count = 0
            for el in elements:
                if count >= max_items:
                    break
                try:
                    if not el.is_visible():
                        continue
                    text = el.inner_text(timeout=500).strip()
                    if not text:
                        continue
                    self.last_links.append(el)
                    output_lines.append(f"[{count}] {text[:80]}")
                    count += 1
                except Exception:
                    continue
            if not output_lines:
                return "Koi clickable links/buttons nahi mile."
            return "\n".join(output_lines)
        except Exception as e:
            return f"ERROR: links read nahi hue - {e}"

    def click_element(self, index: int) -> str:
        try:
            if index < 0 or index >= len(self.last_links):
                return f"ERROR: invalid index {index}. Pehle read_page_links call karo."
            self.last_links[index].click(timeout=5000)
            self.page.wait_for_timeout(1500)
            self._wait_and_handle_challenge()
            return f"Index {index} pe click ho gaya."
        except Exception as e:
            return f"ERROR: click fail hua - {e}"


def call_qwen(messages: list) -> str:
    """Ollama chat-style API call with conversation history."""
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.2, "num_ctx": 8192},
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def extract_json(text: str) -> dict:
    """Qwen ke response se JSON nikaalo, even if extra text ho around it."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in response")
    return json.loads(match.group(0))


def run_agent(agent, messages, task: str):
    messages.append({"role": "user", "content": f"TASK: {task}"})

    tools_map = {
        "search_web": lambda args: agent.search_web(args.get("query", "")),
        "open_url": lambda args: agent.open_url(args.get("url", "")),
        "read_page_text": lambda args: agent.read_page_text(args.get("max_chars", 3000)),
        "read_page_links": lambda args: agent.read_page_links(args.get("max_items", 15)),
        "click_element": lambda args: agent.click_element(args.get("index", -1)),
    }

    try:
        for step in range(1, MAX_STEPS + 1):
            print(f"\n--- Step {step} ---")
            raw_response = call_qwen(messages)
            print(f"[Qwen raw]: {raw_response[:300]}")

            try:
                action = extract_json(raw_response)
            except (ValueError, json.JSONDecodeError) as e:
                print(f"[!] JSON parse fail: {e}")
                messages.append({"role": "assistant", "content": raw_response})
                messages.append({
                    "role": "user",
                    "content": "ERROR: tumhara response valid JSON nahi tha. Sirf JSON object do, kuch aur nahi.",
                })
                continue

            tool_name = action.get("tool")
            args = action.get("args", {})

            messages.append({"role": "assistant", "content": json.dumps(action)})

            if tool_name == "done":
                final_answer = args.get("answer", "(no answer given)")
                print("\n" + "=" * 50)
                print("FINAL ANSWER")
                print("=" * 50)
                print(final_answer)
                print("=" * 50)
                return final_answer

            if tool_name not in tools_map:
                result = f"ERROR: unknown tool '{tool_name}'. Available: {list(tools_map.keys()) + ['done']}"
            else:
                print(f"[Executing]: {tool_name}({args})")
                result = tools_map[tool_name](args)

            print(f"[Result]: {str(result)[:300]}")
            messages.append({"role": "user", "content": f"TOOL RESULT: {result}"})

        print("\n[!] Max steps reach ho gaye bina 'done' call kiye.")
        return None



def main():
    print("=== Research Agent - Step 3 (Agentic Loop) ===\n")
    task = input("Task batao (e.g. 'surat me aaj barish hogi kya pata karo'): ").strip()
    run_agent(task)


if __name__ == "__main__":
    main()