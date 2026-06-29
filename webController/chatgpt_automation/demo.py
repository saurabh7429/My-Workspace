"""Simple demo for the ChatGPT automation package."""

from pathlib import Path
import sys


if __package__ in (None, ""):
    package_root = Path(__file__).resolve().parent.parent
    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))
    from chatgpt_automation.client import ChatGPTClient
    from chatgpt_automation.config import ChatGPTSettings
else:
    from .client import ChatGPTClient
    from .config import ChatGPTSettings


def main():
    settings = ChatGPTSettings()
    client = ChatGPTClient(settings=settings)

    try:
        client.open()
        prompt = "Write a short 5-line introduction about my college project on browser automation."
        print("PROMPT:")
        print(prompt)
        print()
        print("RESPONSE:")
        response = client.execute(prompt)
        print(response)
    finally:
        client.close()


if __name__ == "__main__":
    main()
