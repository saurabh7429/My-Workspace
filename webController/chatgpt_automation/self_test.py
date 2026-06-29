"""End-to-end self test for the ChatGPT automation package.

This runner exercises the public API with real prompts and retries so a new user
can see how to use open, execute, ask, send, restart, close, and reopen.
"""

from __future__ import annotations

import os
import time
from textwrap import dedent

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


SHORT_PROMPT = "Write 3 lines about browser automation."
LONG_PROMPT = dedent(
    """
    Explain browser automation in simple terms.
    Mention typing, clicking, waiting, and response handling.
    Keep the answer easy for a college project demo.
    Use 6 to 8 lines.
    """
).strip()


def print_block(title: str, value: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(value)
    print("-" * 60)


def run_step(label: str, action, restart_action=None):
    last_error = None
    for attempt in range(2):
        try:
            print(f"[{label}] attempt {attempt + 1}")
            return action()
        except Exception as error:
            last_error = error
            print(f"[{label}] failed: {error}")
            if attempt == 0 and restart_action is not None:
                try:
                    restart_action()
                except Exception as restart_error:
                    print(f"[{label}] restart failed: {restart_error}")
                time.sleep(1)
    return None


def run_self_test() -> None:
    settings = ChatGPTSettings()
    client = ChatGPTClient(settings=settings)

    try:
        print("[1] Opening browser session")
        run_step("open", client.open)
        print(client.status())

        print_block("[2] Short prompt test", SHORT_PROMPT)
        short_response = run_step("execute-short", lambda: client.execute(SHORT_PROMPT), restart_action=client.restart)
        if short_response:
            print_block("Short response", short_response)

        print_block("[3] ask() alias test", "What is browser automation in one line?")
        ask_response = run_step("ask", lambda: client.ask("What is browser automation in one line?"), restart_action=client.restart)
        if ask_response:
            print_block("Ask response", ask_response)

        print_block("[4] send() alias test", "Give 4 benefits of browser automation.")
        send_response = run_step("send", lambda: client.send("Give 4 benefits of browser automation."), restart_action=client.restart)
        if send_response:
            print_block("Send response", send_response)

        print("[5] Restart test")
        run_step("restart", client.restart)
        print(client.status())

        if os.getenv("CHATGPT_AUTOMATION_FULL_SELF_TEST", "0") == "1":
            print_block("[6] Long prompt test", LONG_PROMPT)
            long_response = run_step("execute-long", lambda: client.execute(LONG_PROMPT), restart_action=client.restart)
            if long_response:
                print_block("Long response", long_response)

        print("[6] Close / reopen test")
        run_step("close", client.close)
        print(client.status())
        run_step("reopen", client.open)
        print(client.status())

        print_block("[7] Final prompt after reopen", "Write a 5-line summary of browser automation testing.")
        final_response = run_step(
            "execute-final",
            lambda: client.execute("Write a 5-line summary of browser automation testing."),
            restart_action=client.restart,
        )
        if final_response:
            print_block("Final response", final_response)

        print("Self test complete.")
    finally:
        client.close()


if __name__ == "__main__":
    run_self_test()
