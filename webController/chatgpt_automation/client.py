"""Public client facade for ChatGPT browser automation."""

from __future__ import annotations

from dataclasses import asdict

from .config import ChatGPTSettings
from .exceptions import ChatGPTAutomationError, BrowserSessionError, ComposerNotReadyError, PromptTypingError, ResponseTimeoutError
from .prompt_flow import PromptFlow
from .session import ChatGPTBrowserSession


class ChatGPTClient:
    def __init__(self, settings: ChatGPTSettings | None = None):
        self.settings = settings or ChatGPTSettings()
        self.session = ChatGPTBrowserSession(self.settings)
        self.flow = PromptFlow(self.session, self.settings)
        self._opened = False

    def open(self) -> None:
        self.session.open()
        self._opened = True

    def start(self) -> None:
        self.open()

    def connect(self) -> None:
        self.open()

    def open_chat(self) -> None:
        self.open()

    def execute(self, prompt_text: str) -> str:
        if not self._opened:
            self.open()
        return self.flow.execute(prompt_text)

    def ask(self, prompt_text: str) -> str:
        return self.execute(prompt_text)

    def send(self, prompt_text: str) -> str:
        return self.execute(prompt_text)

    def restart(self) -> None:
        self.session.close()
        self.session.open()
        self._opened = True

    def close(self) -> None:
        self.session.close()
        self._opened = False

    def status(self) -> dict:
        try:
            return {
                "opened": self._opened,
                "page_alive": self.session._page_alive(),
                "url": self.session.page.url if self.session._page_alive() else None,
                "settings": asdict(self.settings),
            }
        except Exception:
            return {
                "opened": False,
                "page_alive": False,
                "url": None,
                "settings": asdict(self.settings),
            }

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


__all__ = [
    "ChatGPTClient",
    "ChatGPTAutomationError",
    "BrowserSessionError",
    "ComposerNotReadyError",
    "PromptTypingError",
    "ResponseTimeoutError",
]
