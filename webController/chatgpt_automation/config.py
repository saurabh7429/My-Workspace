"""Central configuration for ChatGPT browser automation."""

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class ChatGPTSettings:
    browser_timeout_ms: int = 60000
    navigation_timeout_ms: int = 60000
    prompt_ready_timeout_s: int = 90
    composer_ready_timeout_s: int = 30
    typing_timeout_floor_ms: int = 120000
    typing_timeout_per_char_ms: int = 25
    typing_timeout_base_ms: int = 30000
    typing_delay_ms: float = 3
    response_start_timeout_s: int = 90
    response_complete_timeout_s: int = 240
    retry_attempts: int = 3
    typing_retries: int = 2
    response_stable_checks: int = 6
    response_stable_interval_s: float = 0.5
    prompt_poll_interval_s: float = 0.35
    response_poll_interval_s: float = 0.35
    typing_settle_delay_s: float = 0.5
    send_click_delay_s: float = 0.5
    after_response_ready_wait_s: int = 30
    startup_wait_s: int = 1
    headless: bool = False
    open_url: str = "https://chatgpt.com/"
    user_agent_args: List[str] = field(
        default_factory=lambda: [
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
        ]
    )
    prompt_selectors: List[str] = field(
        default_factory=lambda: ["#prompt-textarea", "textarea"]
    )
    send_selectors: List[str] = field(
        default_factory=lambda: [
            'button[data-testid*="send" i]',
            'button[aria-label*="Send message" i]',
            'button[aria-label*="Send" i]',
            'button[title*="Send message" i]',
            'button[title*="Send" i]',
        ]
    )
    assistant_selector: str = 'div[data-message-author-role="assistant"]'
    copy_button_selector: str = 'button[aria-label*="Copy"]'
