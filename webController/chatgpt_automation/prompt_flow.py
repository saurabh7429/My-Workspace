"""Prompt typing and response waiting helpers."""

from __future__ import annotations

import time

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .config import ChatGPTSettings
from .exceptions import PromptTypingError, ResponseTimeoutError
from .session import ChatGPTBrowserSession


class PromptFlow:
    def __init__(self, session: ChatGPTBrowserSession, settings: ChatGPTSettings | None = None):
        self.session = session
        self.settings = settings or session.settings

    def _prompt_locator(self):
        locator = self.session.page.locator(", ".join(self.settings.prompt_selectors))
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

    def _send_button_locator(self):
        for selector in self.settings.send_selectors:
            locator = self.session.page.locator(selector)
            try:
                count = locator.count()
            except Exception:
                continue

            for index in range(count):
                candidate = locator.nth(index)
                try:
                    if candidate.is_visible() and candidate.is_enabled():
                        return candidate
                except Exception:
                    continue

        return None

    def _assistant_locator(self):
        return self.session.page.locator(self.settings.assistant_selector)

    def _type_prompt(self, locator, prompt_text: str) -> None:
        try:
            locator.wait_for(state="visible", timeout=5000)
        except Exception:
            pass

        try:
            locator.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass

        locator.click()
        try:
            locator.press("Control+A")
            locator.press("Backspace")
        except Exception:
            try:
                locator.fill("")
            except Exception:
                pass

        typing_timeout = max(
            self.settings.typing_timeout_floor_ms,
            len(prompt_text) * self.settings.typing_timeout_per_char_ms + self.settings.typing_timeout_base_ms,
        )

        try:
            locator.press_sequentially(prompt_text, delay=self.settings.typing_delay_ms, timeout=typing_timeout)
        except TypeError:
            locator.press_sequentially(prompt_text, delay=self.settings.typing_delay_ms)
        except PlaywrightError as error:
            raise PromptTypingError(f"Typing fail hua: {error}")

        time.sleep(self.settings.typing_settle_delay_s)

        try:
            current_value = locator.input_value(timeout=2000)
            if current_value == prompt_text:
                return
        except Exception:
            pass

        try:
            current_text = locator.inner_text(timeout=2000)
            if prompt_text in current_text:
                return
        except Exception:
            pass

        raise PromptTypingError("Prompt text complete set nahi hua.")

    def _submit_prompt(self, locator) -> None:
        send_button = self._send_button_locator()
        if send_button is not None:
            try:
                send_button.click(timeout=5000)
                return
            except Exception:
                pass

        try:
            locator.press("Enter", timeout=10000)
        except TypeError:
            locator.press("Enter")
        except Exception:
            self.session.page.keyboard.press("Enter")

    def wait_for_response_start(self, old_count: int) -> int:
        start = time.time()
        while True:
            self.session.ensure_page_ready()
            try:
                current_count = self._assistant_locator().count()
                if current_count > old_count:
                    return current_count
            except Exception:
                pass

            if time.time() - start > self.settings.response_start_timeout_s:
                try:
                    assistant_locator = self._assistant_locator()
                    assistant_count = assistant_locator.count()
                    if assistant_count > 0:
                        assistant_locator.last.wait_for(state="visible", timeout=5000)
                        return assistant_count
                except Exception:
                    pass

                raise ResponseTimeoutError("AI ne response start nahi kiya.")

            time.sleep(self.settings.response_poll_interval_s)

    def wait_for_response_complete(self, latest_message_block) -> str:
        previous_text = ""
        stable_count = 0
        start = time.time()

        while True:
            self.session.ensure_page_ready()

            if time.time() - start > self.settings.response_complete_timeout_s:
                raise ResponseTimeoutError("Response timeout.")

            try:
                current_text = latest_message_block.inner_text().strip()
            except Exception:
                time.sleep(self.settings.response_poll_interval_s)
                continue

            if not current_text:
                time.sleep(self.settings.response_poll_interval_s)
                continue

            if current_text == previous_text:
                stable_count += 1
                if stable_count >= self.settings.response_stable_checks:
                    return current_text
            else:
                stable_count = 0

            previous_text = current_text
            time.sleep(self.settings.response_stable_interval_s)

    def execute(self, prompt_text: str) -> str:
        prompt_text = (prompt_text or "").strip()
        if not prompt_text:
            return "❌ Empty prompt."

        self.session.wait_for_composer_ready()
        prompt_box = self._prompt_locator()
        response_selector = self.settings.assistant_selector
        old_msg_count = self._assistant_locator().count()

        typing_done = False
        last_typing_error = None
        for typing_attempt in range(self.settings.typing_retries):
            try:
                self._type_prompt(prompt_box, prompt_text)
                typing_done = True
                break
            except PromptTypingError as error:
                last_typing_error = error
                if typing_attempt < self.settings.typing_retries - 1:
                    time.sleep(0.75)
                    self.session.wait_for_composer_ready()
                    prompt_box = self._prompt_locator()

        if not typing_done:
            raise PromptTypingError(f"Prompt typing failed after retry: {last_typing_error}")

        time.sleep(self.settings.send_click_delay_s)
        self._submit_prompt(prompt_box)

        try:
            current_msg_count = self.wait_for_response_start(old_msg_count)
        except ResponseTimeoutError:
            time.sleep(1)
            self._submit_prompt(prompt_box)
            current_msg_count = self.wait_for_response_start(old_msg_count)

        latest_message_block = self.session.page.locator(response_selector).nth(current_msg_count - 1)
        final_text = self.wait_for_response_complete(latest_message_block)
        try:
            self.session.wait_for_composer_ready()
        except Exception:
            pass
        return final_text
