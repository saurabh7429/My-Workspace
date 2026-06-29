import platform
import time
from playwright.sync_api import sync_playwright


class PromptTypingError(Exception):
    pass

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
            return "/opt/brave.com/brave/brave"
        elif system == "Windows":
            return r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        elif system == "Darwin":
            return "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        else:
            raise Exception("Unsupported OS")

    def _init_browser(self):
        print("\n🚀 Browser session initialize ho raha hai...")
        self.browser = self.p.chromium.launch(
            executable_path=self.brave_path,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"]
        )
        self.context = self.browser.new_context(viewport=None)
        self.page = self.context.new_page()
        self.page.set_default_timeout(120000)
        self.page.set_default_navigation_timeout(60000)
        self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _prompt_locator(self):
        locator = self.page.locator("#prompt-textarea, textarea")
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
        selectors = [
            'button[data-testid*="send" i]',
            'button[aria-label*="Send message" i]',
            'button[aria-label*="Send" i]',
            'button[title*="Send message" i]',
            'button[title*="Send" i]',
        ]

        for selector in selectors:
            locator = self.page.locator(selector)
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

    def start_chat(self):
        print("🌐 ChatGPT server se connect kar rahe hain...")
        self.page.goto("https://chatgpt.com/", timeout=60000)
        self.page.wait_for_selector("#prompt-textarea, textarea", state="visible", timeout=60000)

    def restart_browser(self):
        print("🔄 Browser/Renderer puri tarah rebuild kiya ja raha hai...")
        self._safe_close_context()
        self._init_browser()
        self.start_chat()

    def _wait_for_composer_ready(self, timeout_s=30):
        start = time.time()
        while True:
            try:
                prompt_box = self._prompt_locator()
                if prompt_box.count() > 0 and prompt_box.is_visible() and prompt_box.is_enabled():
                    return prompt_box
            except Exception:
                pass

            if time.time() - start > timeout_s:
                raise Exception("Composer ready nahi hua.")

            time.sleep(0.35)

    def _type_prompt(self, prompt_box, prompt_text):
        try:
            prompt_box.wait_for(state="visible", timeout=10000)
        except Exception:
            pass

        try:
            prompt_box.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass

        prompt_box.click()

        try:
            prompt_box.press("Control+A")
            prompt_box.press("Backspace")
        except Exception:
            try:
                prompt_box.fill("")
            except Exception:
                pass

        typing_timeout = max(120000, len(prompt_text) * 25 + 30000)

        try:
            prompt_box.press_sequentially(prompt_text, delay=3, timeout=typing_timeout)
        except TypeError:
            prompt_box.press_sequentially(prompt_text, delay=3)
        except Exception as e:
            raise PromptTypingError(f"Typing fail hua: {e}")

        time.sleep(0.5)

        try:
            current_value = prompt_box.input_value(timeout=2000)
            if current_value == prompt_text:
                return
        except Exception:
            pass

        try:
            current_text = prompt_box.inner_text(timeout=2000)
            if prompt_text in current_text:
                return
        except Exception:
            pass

        raise PromptTypingError("Prompt text complete set nahi hua.")

    def _submit_prompt(self, prompt_box):
        send_button = self._send_button_locator()
        if send_button is not None:
            try:
                send_button.click(timeout=5000)
                return
            except Exception:
                pass

        try:
            prompt_box.press("Enter", timeout=10000)
        except TypeError:
            prompt_box.press("Enter")
        except Exception:
            self.page.keyboard.press("Enter")

    def ask(self, prompt_text):
        prompt_text = (prompt_text or "").strip()
        if not prompt_text:
            return "❌ Empty prompt."

        for attempt in range(3):
            try:
                prompt_box = self._prompt_locator()
                response_selector = 'div[data-message-author-role="assistant"]'
                
                prompt_box = self._wait_for_composer_ready(timeout_s=60)

                old_msg_count = self.page.locator(response_selector).count()
                
                typing_done = False
                for typing_attempt in range(2):
                    try:
                        self._type_prompt(prompt_box, prompt_text)
                        typing_done = True
                        break
                    except PromptTypingError as typing_err:
                        print(f"\n⚠️ Typing attempt {typing_attempt + 1} Failed: (Error: {typing_err})")
                        if typing_attempt < 1:
                            time.sleep(0.75)
                            prompt_box = self._prompt_locator()

                if not typing_done:
                    raise PromptTypingError("Prompt typing failed after retry.")

                self._submit_prompt(prompt_box)
                
                print("⏳ ChatGPT answer generate kar raha hai...")
                
                # FIX 3: Naya message aane ka wait 'Timer' ke sath
                wait_start_time = time.time()
                while True:
                    current_msg_count = self.page.locator(response_selector).count()
                    if current_msg_count > old_msg_count:
                        break
                    
                    # Agar 45 seconds tak naya message aana shuru nahi hua, toh loop tod do
                    if time.time() - wait_start_time > 45:
                        raise Exception("45 seconds tak naya message aana shuru nahi hua. (Net slow ya Server error)")
                    
                    time.sleep(0.5)
                    
                latest_message_block = self.page.locator(response_selector).nth(current_msg_count - 1)
                
                copy_btn = latest_message_block.locator('button[aria-label*="Copy"]')
                
                # FIX 4: Maximum 3 Minutes (180000 ms) ka wait response ke liye. 
                # Agar ChatGPT hang ho gaya, toh yeh 3 min baad automatically retry karega.
                copy_btn.wait_for(state="visible", timeout=180000)
                
                time.sleep(1)
                
                final_text = latest_message_block.inner_text()
                self._wait_for_composer_ready(timeout_s=30)
                return final_text
                
            except Exception as e:
                print(f"\n⚠️ Attempt {attempt + 1} Failed: (Error: {e})")
                if isinstance(e, PromptTypingError):
                    if attempt < 2:
                        time.sleep(1)
                        continue
                    return "❌ Prompt likhne me problem aa rahi hai. Kripya prompt aur prompt box check karein."
                if attempt < 2:
                    self.restart_browser()
                else:
                    return "❌ 3 attempts ke baad bhi chat fail ho gayi. Kripya system check karein."    
                
    def _safe_close_context(self):
        try:
            if self.context: self.context.close()
            if self.browser: self.browser.close()
        except Exception:
            pass

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
        print("\n" + "="*50)
        print("✅ TERMINAL CHATGPT READY!")
        print("Chat band karne ke liye 'exit' ya 'quit' type karein.")
        print("="*50 + "\n")
        
        while True:
            user_msg = input("Saurabh (You): ")
            
            if user_msg.strip().lower() in ['exit', 'quit', 'close']:
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