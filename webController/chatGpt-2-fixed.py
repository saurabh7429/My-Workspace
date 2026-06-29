import os
import platform
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError


class UnofficialChatGPTAPI:
    def __init__(self):
        self.p = sync_playwright().start()
        self.brave_path = self._get_brave_path()
        self.browser = None
        self.context = None
        self.page = None
        self._init_browser()

    def _get_brave_path(self):
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
            raise Exception("Unsupported OS")

        for path in candidates:
            if os.path.exists(path):
                return path
        return candidates[0]

    def _init_browser(self):
        print("\n🚀 Browser session initialize ho raha hai...")
        self.browser = self.p.chromium.launch(
            executable_path=self.brave_path,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-client-side-phishing-detection",
                "--disable-component-update",
                "--disable-default-apps",
                "--disable-popup-blocking",
                "--disable-renderer-backgrounding",
                "--disable-sync",
                "--metrics-recording-only",
                "--mute-audio",
            ],
            ignore_default_args=["--enable-automation"],
        )
        self.context = self.browser.new_context(viewport=None)
        self.page = self.context.new_page()
        self.page.set_default_timeout(60000)
        self.page.set_default_navigation_timeout(60000)
        self.page.on("crash", lambda: print("⚠️ Page crash detect hua."))
        self.page.on("close", lambda: print("⚠️ Page close detect hua."))
        self.page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def _page_alive(self):
        try:
            return self.page is not None and not self.page.is_closed()
        except Exception:
            return False

    def _ensure_page_ready(self):
        if not self._page_alive():
            self._init_browser()

    def _prompt_locator(self):
        return self.page.locator("#prompt-textarea, textarea").first

    def _assistant_locator(self):
        return self.page.locator('div[data-message-author-role="assistant"]')

    def _wait_for_prompt(self, timeout_s=90):
        start = time.time()
        while True:
            self._ensure_page_ready()
            try:
                prompt = self._prompt_locator()
                if prompt.count() > 0:
                    prompt.wait_for(state="visible", timeout=1000)
                    return prompt
            except Exception:
                pass

            if time.time() - start > timeout_s:
                raise PlaywrightTimeoutError("Prompt box ready nahi hua.")

            time.sleep(0.35)

    def _open_chatgpt(self, timeout_s=60):
        last_error = None

        for attempt in range(3):
            self._ensure_page_ready()
            try:
                self.page.bring_to_front()
            except Exception:
                pass

            try:
                self.page.goto(
                    "https://chatgpt.com/",
                    wait_until="domcontentloaded",
                    timeout=timeout_s * 1000,
                )
                try:
                    self.page.wait_for_load_state("domcontentloaded", timeout=15000)
                except Exception:
                    pass

                if self.page.url == "about:blank":
                    raise Exception("browser remained on about:blank")

                self._wait_for_prompt(timeout_s=90)
                return
            except Exception as e:
                last_error = e
                time.sleep(1)

        raise Exception(f"ChatGPT open nahi hua: {last_error}")

    def start_chat(self):
        print("🌐 ChatGPT server se connect kar rahe hain...")
        self._open_chatgpt(timeout_s=60)

    def restart_browser(self):
        print("🔄 Browser/Renderer puri tarah rebuild kiya ja raha hai...")
        self._safe_close_context()
        time.sleep(1)
        self._init_browser()
        self._open_chatgpt(timeout_s=60)

    def _type_prompt(self, locator, prompt_text):
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

        typing_timeout = max(120000, len(prompt_text) * 20 + 30000)

        try:
            locator.fill(prompt_text, timeout=typing_timeout)
            return
        except Exception:
            pass

        try:
            locator.press_sequentially(prompt_text, delay=3, timeout=typing_timeout)
        except TypeError:
            locator.press_sequentially(prompt_text, delay=3)
        except PlaywrightError as e:
            raise Exception(f"Typing fail hua: {e}")

        time.sleep(0.25)

        current_value = None
        current_text = None

        try:
            current_value = locator.input_value(timeout=2000)
        except Exception:
            pass

        if current_value == prompt_text:
            return

        try:
            current_text = locator.inner_text(timeout=2000)
        except Exception:
            pass

        if current_text is not None and prompt_text in current_text:
            return

        raise Exception("Prompt text complete set nahi hua.")

    def _submit_prompt(self, locator):
        try:
            locator.press("Enter", timeout=10000)
        except TypeError:
            locator.press("Enter")
        except Exception:
            self.page.keyboard.press("Enter")

    def _wait_for_response_start(self, old_count):
        start = time.time()
        while True:
            self._ensure_page_ready()
            try:
                current_count = self._assistant_locator().count()
                if current_count > old_count:
                    return current_count
            except Exception:
                pass

            if time.time() - start > 90:
                raise PlaywrightTimeoutError("AI ne response start nahi kiya.")

            time.sleep(0.35)

    def _wait_for_response_stable(self, latest_message_block):
        previous_text = ""
        stable_count = 0
        start = time.time()

        while True:
            self._ensure_page_ready()

            if time.time() - start > 240:
                raise PlaywrightTimeoutError("Response timeout.")

            try:
                current_text = latest_message_block.inner_text().strip()
            except Exception:
                time.sleep(0.35)
                continue

            if not current_text:
                time.sleep(0.35)
                continue

            if current_text == previous_text:
                stable_count += 1
                if stable_count >= 6:
                    return current_text
            else:
                stable_count = 0

            previous_text = current_text
            time.sleep(0.5)

    def ask(self, prompt_text):
        prompt_text = (prompt_text or "").strip()
        if not prompt_text:
            return "❌ Empty prompt."

        for attempt in range(3):
            try:
                self._ensure_page_ready()
                prompt_box = self._wait_for_prompt(timeout_s=90)
                response_selector = 'div[data-message-author-role="assistant"]'
                old_msg_count = self._assistant_locator().count()

                print("✍️ Prompt likh rahe hain...")
                self._type_prompt(prompt_box, prompt_text)

                print("📨 Send kar rahe hain...")
                self._submit_prompt(prompt_box)

                print("⏳ ChatGPT answer generate kar raha hai...")
                current_msg_count = self._wait_for_response_start(old_msg_count)

                latest_message_block = self.page.locator(response_selector).nth(current_msg_count - 1)

                print("⏳ AI likh raha hai. Stream complete hone ka wait kar rahe hain...")
                current_text = self._wait_for_response_stable(latest_message_block)

                print("✅ Response complete.")
                return current_text

            except Exception as e:
                print(f"\n⚠️ Attempt {attempt + 1} Failed: (Error: {e})")
                if attempt < 2:
                    try:
                        self.restart_browser()
                    except Exception as restart_err:
                        print(f"⚠️ Restart error: {restart_err}")
                else:
                    return "❌ 3 attempts ke baad bhi chat fail ho gayi. Kripya system check karein."

    def _safe_close_context(self):
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

    def close(self):
        print("\n🛑 System close ho raha hai...")
        self._safe_close_context()
        try:
            self.p.stop()
        except Exception:
            pass


# --- MAIN LOOP ---
def main():
    chat_api = UnofficialChatGPTAPI()

    try:
        chat_api.start_chat()
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
            response = chat_api.ask(user_msg)

            print("\n🤖 ChatGPT:")
            print(response)
            print("-" * 50)

    finally:
        chat_api.close()
        print("✅ Exit Successful.")


if __name__ == "__main__":
    main()
