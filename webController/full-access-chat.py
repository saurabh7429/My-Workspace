import os
import time
from playwright.sync_api import sync_playwright

def terminal_chatgpt():
    with sync_playwright() as p:
        brave_path = "/opt/brave.com/brave/brave" 
        safe_profile_dir = os.path.expanduser("~/brave_automation_profile")
        
        print("\n🚀 System Start: Brave browser launch ho raha hai...")
        
        context = p.chromium.launch_persistent_context(
            user_data_dir=safe_profile_dir,
            executable_path=brave_path,
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled" 
            ],
            ignore_default_args=["--enable-automation"], 
            no_viewport=True,
            permissions=["clipboard-read", "clipboard-write"]
        )
        
        page = context.pages[0] if len(context.pages) > 0 else context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("🌐 ChatGPT se connect kar rahe hain... Kripya thoda wait karein.")
        
        try:
            page.goto("https://chatgpt.com/", timeout=60000)
            
            prompt_selector = "#prompt-textarea"
            send_button_selector = 'button[data-testid="send-button"]'
            response_selector = 'div[data-message-author-role="assistant"]'
            
            # Pehli baar prompt box load hone ka wait
            page.wait_for_selector(prompt_selector, state="visible", timeout=60000)
            
            print("\n" + "="*50)
            print("✅ CHAT SESSION READY!")
            print("Ab aap terminal se hi continuously chat kar sakte hain.")
            print("Chat band karne ke liye 'exit' ya 'quit' type karein.")
            print("="*50 + "\n")
            
            # --- INFINITE LOOP SHURU ---
            while True:
                # Terminal se user input lena
                user_message = input("Saurabh (You): ")
                
                # Agar user ko exit karna ho
                if user_message.strip().lower() in ['exit', 'quit', 'close']:
                    print("\n🛑 Chat session close kiya ja raha hai...")
                    break
                
                # Agar galti se khali enter dab gaya ho toh ignore karna
                if not user_message.strip():
                    continue
                
                # Pata lagana ki abhi kitne AI messages screen par hain
                # Isse hum naye message ke aane ka wait kar payenge
                ai_msg_count_before = page.locator(response_selector).count()
                
                print("⏳ AI type kar raha hai...")
                
                # 1. Message Type karna (Bot detection se bachne ke liye 50ms ka gap)
                page.locator(prompt_selector).press_sequentially(user_message, delay=0)
                time.sleep(0.5) # Thoda wait taaki send button active ho jaye
                
                # 2. Send karna
                page.wait_for_selector(send_button_selector, state="visible")
                page.click(send_button_selector)
                
                # 3. Naye AI message ke aane ka wait karna
                # Jab tak response generate na ho jaye (Copy button tabhi aata hai jab stream puri hoti hai)
                time.sleep(5) # Initial DOM shift ka buffer
                copy_button_selector = 'button[aria-label*="Copy"]'
                page.locator(copy_button_selector).last.wait_for(state="visible", timeout=120000)
                
                # Text properly load hone ke liye 1 second ka extra time
                time.sleep(1)
                
                # 4. Text nikalna
                responses = page.locator(response_selector).all_inner_texts()
                
                if responses:
                    print("\n🤖 ChatGPT:")
                    print(responses[-1]) # Hamesha aakhri (latest) response hi print hoga
                    print("-" * 50)
                else:
                    print("\n⚠️ Naya response capture nahi ho paya.")
                    print("-" * 50)
                    
        except Exception as e:
            print("\n❌ Error aagaya!")
            print(f"Technical Error Details: {e}\n")
            
        finally:
            print("Browser properly close ho raha hai...")
            context.close() 
            print("✅ System Exit Successful.")

if __name__ == "__main__":
    terminal_chatgpt()