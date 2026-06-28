import platform
import time
from playwright.sync_api import sync_playwright

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
        self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def start_chat(self):
        print("🌐 ChatGPT server se connect kar rahe hain...")
        self.page.goto("https://chatgpt.com/", timeout=60000)
        self.page.wait_for_selector("#prompt-textarea, textarea", state="visible", timeout=60000)

    def restart_browser(self):
        print("🔄 Browser/Renderer puri tarah rebuild kiya ja raha hai...")
        self._safe_close_context()
        self._init_browser()
        self.start_chat()

    def ask(self, prompt_text):
        for attempt in range(3):
            try:
                # ----------------------------------------------------
                # 🔥 SMART DELAY LOGIC (Tumhari equation apply ki hai)
                # ----------------------------------------------------
                typing_delay_ms = 3 # 3 millisecond per character
                # Prompt kitna lamba hai, uske hisaab se typing time calculate karna (milliseconds mein)
                estimated_typing_time_ms = len(prompt_text) * typing_delay_ms
                
                # Chatgpt ka response time (hum normally 2 minute = 120,000ms mante hain)
                base_wait_time_ms = 120000 
                
                # Dynamic Timeout = Type karne ka time + 2 Minutes Extra
                dynamic_timeout = estimated_typing_time_ms + base_wait_time_ms
                # ----------------------------------------------------
                
                prompt_box = self.page.locator("#prompt-textarea, textarea").first
                
                # Type karte waqt humara calculated timeout allow karna
                prompt_box.press_sequentially(prompt_text, delay=typing_delay_ms)
                
                # Send dabane se pehle thoda sa buffer (taaki system command catch kar le)
                time.sleep(0.5) 
                
                prompt_box.press("Enter")
                
                response_selector = 'div[data-message-author-role="assistant"]'
                
                # Ab timeout static 120000 nahi, balki "dynamic_timeout" hai
                self.page.wait_for_selector(response_selector, state="visible", timeout=dynamic_timeout)
                
                assistant_msg = self.page.locator(response_selector).last
                
                previous_text = ""
                stable_count = 0
                
                while True:
                    current_text = assistant_msg.inner_text()
                    
                    if current_text == previous_text and len(current_text) > 10:
                        stable_count += 1
                        if stable_count >= 3: 
                            break
                    else:
                        stable_count = 0 
                        
                    previous_text = current_text
                    time.sleep(0.5)
                    
                return current_text
                
            except Exception as e:
                print(f"\n⚠️ Attempt {attempt + 1} Failed: Bada Prompt tha ya net slow tha. (Error: {e})")
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
            # Agar tum multi-line lamba prompt copy-paste karna chahte ho, toh terminal usko theek se handle kare, 
            # isliye input ka nature thoda smark rakhna padta hai, par abhi simple rakhte hain.
            user_msg = input("Saurabh (You): ")
            
            if user_msg.strip().lower() in ['exit', 'quit', 'close']:
                break
            if not user_msg.strip():
                continue
                
            print("⏳ AI generate kar raha hai (Lamba prompt hoga toh typing mein extra time lagega)...")
            response = chat_api.ask(user_msg)
            
            print("\n🤖 ChatGPT:")
            print(response)
            print("-" * 50)
            
    finally:
        chat_api.close()
        print("✅ Exit Successful.")

if __name__ == "__main__":
    main()