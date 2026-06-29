"""Terminal entrypoint for ChatGPT browser automation."""

from pathlib import Path
import sys


if __package__ in (None, ""):
    package_root = Path(__file__).resolve().parent.parent
    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))
    from chatgpt_automation.client import ChatGPTClient
else:
    from .client import ChatGPTClient


def main():
    client = ChatGPTClient()

    try:
        client.open()
        print("\n" + "=" * 50)
        print("✅ TERMINAL CHATGPT READY!")
        print("Chat band karne ke liye 'exit' ya 'quit' type karein.")
        print("=" * 50 + "\n")

        while True:
            try:
                user_msg = input("You: ")
            except (EOFError, KeyboardInterrupt):
                break

            if user_msg.strip().lower() in ["exit", "quit", "close"]:
                break
            if not user_msg.strip():
                continue

            print("⏳ Type kar rahe hain...")
            response = client.execute(user_msg)

            print("\n🤖 ChatGPT:")
            print(response)
            print("-" * 50)

    finally:
        client.close()
        print("✅ Exit Successful.")


if __name__ == "__main__":
    main()
