import platform
import time
from playwright.sync_api import sync_playwright

class UnofficialChatGPTAPI:
    def __init__(self):
        # Playwright ko class ke andar hi start karna
        self.p = sync_playwright().start()
        self.brave_path = self._get_brave_path()
        
        print("\n🚀 System Start: Brave browser Private/Incognito mode me launch ho raha hai...")
        
        # Har baar ek fresh, temporary browser instance (No saved data)
        self.browser = self.p.chromium.launch(
            executable_path=self.brave_path,
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--incognito" # Forcefully private window
            ],
            ignore_default_args=["--enable-automation"]
        )
        
        # Naya context aur tab banana
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
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
            
    def start_chat(self):
        print("🌐 ChatGPT server se connect kar rahe hain...")
        self.page.goto("https://chatgpt.com/", timeout=60000)
        self.page.wait_for_selector("#prompt-textarea", state="visible", timeout=60000)
        
    def ask(self, prompt_text):
        try:
            prompt_box = self.page.locator("#prompt-textarea").first
            
            # 1. Type instantly (Zero delay as requested)
            prompt_box.press_sequentially(prompt_text, delay=0)
            
            # 2. Send message
            send_button = self.page.locator('button[data-testid="send-button"]').first
            send_button.wait_for(state="visible", timeout=5000)
            send_button.click()
            
            # 3. Wait for response element to appear
            response_selector = 'div[data-message-author-role="assistant"]'
            self.page.wait_for_selector(response_selector, state="visible", timeout=30000)
            
            # Hamesha latest response ko target karna
            assistant_msg = self.page.locator(response_selector).last
            
            # 4. Stream Detection Logic (Wait until text stops changing)
            previous_text = ""
            stable_count = 0
            
            while True:
                current_text = assistant_msg.inner_text()
                
                # Agar text update nahi ho raha aur khali nahi hai
                if current_text == previous_text and len(current_text) > 0:
                    stable_count += 1
                    # Agar lagatar 1 second (2 * 0.5s) tak text same rahe, toh iska matlab stream puri ho gayi
                    if stable_count >= 2: 
                        break
                else:
                    stable_count = 0 # Agar text badla, toh count reset
                    
                previous_text = current_text
                time.sleep(0.5)
                
            return current_text
            
        except Exception as e:
            # Error aane par script band nahi hogi, fresh chat start hogi
            print(f"\n⚠️ Error Limit/Block Detect Hua: {e}")
            print("🔄 Naya fresh session start kar rahe hain...")
            self.start_chat()
            return "Server error ya limit ki wajah se chat refresh ki gayi hai. Kripya apna sawal dobara puchein."
            
    def close(self):
        print("\n🛑 System close ho raha hai... Saare tabs aur background process band kiye ja rahe hain.")
        self.context.close()
        self.browser.close()
        self.p.stop() # Playwright instance ko properly close karna

# --- MAIN EXECUTION BLOCK ---
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
                
            print("⏳ AI generate kar raha hai...")
            response = chat_api.ask(user_msg)
            
            print("\n🤖 ChatGPT:")
            print(response)
            print("-" * 50)
            
    finally:
        # User jab bhi exit karega, sab kuch properly band hoga
        chat_api.close()
        print("✅ Exit Successful.")

if __name__ == "__main__":
    main()