"""Browser session management for ChatGPT automation."""

from __future__ import annotations

import os
import platform
import time

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from .config import ChatGPTSettings
from .exceptions import BrowserSessionError, ComposerNotReadyError


class ChatGPTBrowserSession:
    def __init__(self, settings: ChatGPTSettings | None = None):
        self.settings = settings or ChatGPTSettings()
        self.p = None
        self.brave_path = self._get_brave_path()
        self.browser = None
        self.context = None
        self.page = None

    def open(self) -> None:
        if self.p is None:
            self.p = sync_playwright().start()
        self._init_browser()
        self.open_chatgpt()

    def _get_brave_path(self) -> str:
        system = platform.system()
        if system == "Linux":
            candidates = [
                "/opt/brave.com/brave/brave",
                "/usr/bin/brave-browser",
                "/usr/bin/brave",
                "/snap/bin/brave",
            ]
        elif system == "Windows":
            candidates = [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            ]
        elif system == "Darwin":
            candidates = [
                "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            ]
        else:
            raise BrowserSessionError("Unsupported OS")

        for path in candidates:
            if os.path.exists(path):
                return path
        return candidates[0]

    def _init_browser(self) -> None:
        self.browser = self.p.chromium.launch(
            executable_path=self.brave_path,
            headless=self.settings.headless,
            args=self.settings.user_agent_args,
            ignore_default_args=["--enable-automation"],
        )
        self.context = self.browser.new_context(viewport=None)
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.settings.browser_timeout_ms)
        self.page.set_default_navigation_timeout(self.settings.navigation_timeout_ms)
        self.page.on("crash", lambda: print("⚠️ Page crash detect hua."))
        self.page.on("close", lambda: print("⚠️ Page close detect hua."))
        self.page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def _page_alive(self) -> bool:
        try:
            return self.page is not None and not self.page.is_closed()
        except Exception:
            return False

    def ensure_page_ready(self) -> None:
        if not self._page_alive():
            self._init_browser()

    def _prompt_locator(self):
        locator = self.page.locator(", ".join(self.settings.prompt_selectors))
        try:
            count = locator.count()
        except Exception:
            return locator.first

        for index in range(count):
            candidate = locator.nth(index)
            try:
                if candidate.is_visible() and candidate.is_enabled():
                    return candidate
            except Exception:
                continue

        return locator.first

    def open_chatgpt(self) -> None:
        last_error = None
        for _ in range(3):
            self.ensure_page_ready()
            try:
                self.page.bring_to_front()
            except Exception:
                pass

            try:
                self.page.goto(
                    self.settings.open_url,
                    wait_until="domcontentloaded",
                    timeout=self.settings.browser_timeout_ms,
                )
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=15000)
                except Exception:
                    pass

                if self.page.url == "about:blank":
                    raise BrowserSessionError("browser remained on about:blank")

                self.wait_for_prompt()
                return
            except Exception as error:
                last_error = error
                time.sleep(self.settings.startup_wait_s)

        raise BrowserSessionError(f"ChatGPT open nahi hua: {last_error}")

    def wait_for_prompt(self) -> None:
        start = time.time()
        while True:
            self.ensure_page_ready()
            try:
                locator = self._prompt_locator()
                if locator.count() > 0:
                    locator.wait_for(state="visible", timeout=1000)
                    return
            except Exception:
                pass

            if time.time() - start > self.settings.prompt_ready_timeout_s:
                raise ComposerNotReadyError("Prompt box ready nahi hua.")

            time.sleep(self.settings.prompt_poll_interval_s)

    def wait_for_composer_ready(self) -> None:
        start = time.time()
        while True:
            self.ensure_page_ready()
            try:
                locator = self._prompt_locator()
                if locator.count() > 0 and locator.is_visible() and locator.is_enabled():
                    return
            except Exception:
                pass

            if time.time() - start > self.settings.composer_ready_timeout_s:
                raise ComposerNotReadyError("Composer ready nahi hua.")

            time.sleep(self.settings.prompt_poll_interval_s)

    def close(self) -> None:
        try:
            if self.context:
                self.context.close()
        except Exception:
            pass

        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass

        self.context = None
        self.browser = None
        self.page = None

        try:
            if self.p:
                self.p.stop()
        except Exception:
            pass
        self.p = None
