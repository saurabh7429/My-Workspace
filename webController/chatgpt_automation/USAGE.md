# How To Use

This file explains the package in a way that is easy to follow for someone new.

## 1. Main Entry Point

### `ChatGPTClient`

This is the class you should import first.

```python
from chatgpt_automation import ChatGPTClient
```

### What the methods do

- `open()` - starts the browser, opens ChatGPT, and waits for the prompt box
- `execute(prompt)` - writes the prompt, sends it, waits for the answer, and returns the final text
- `ask(prompt)` - same as `execute(prompt)`
- `send(prompt)` - same as `execute(prompt)`
- `restart()` - closes the current browser session and starts a fresh one
- `close()` - safely shuts down browser and Playwright
- `status()` - returns current session data like page health, URL, and settings

### Example

```python
from chatgpt_automation import ChatGPTClient

client = ChatGPTClient()
client.open()
response = client.execute("Explain the difference between a class and an object.")
print(response)
client.close()
```

## 2. Configuration File

### `ChatGPTSettings`

Use this when you want to change waiting time, retries, or selectors.

Important fields:

- `prompt_ready_timeout_s` - how long to wait for the prompt box
- `composer_ready_timeout_s` - how long to wait for a usable composer before typing
- `typing_timeout_floor_ms` - minimum typing timeout
- `typing_timeout_per_char_ms` - extra typing time added per character
- `typing_timeout_base_ms` - base typing time added to every prompt
- `send_click_delay_s` - wait time after typing before clicking send
- `response_start_timeout_s` - how long to wait for the first assistant reply block
- `response_complete_timeout_s` - how long to wait for the response to finish streaming
- `typing_retries` - number of retries while typing the prompt
- `retry_attempts` - overall retry count used by the higher-level flow

### Good rule

If your prompt is large, increase the typing time values first. If ChatGPT is slow to respond, increase the response timeouts next.

## 3. Browser Session Layer

### `ChatGPTBrowserSession`

Use this when you want browser open/close behavior only.

Helpful methods:

- `open()` - creates the browser and opens ChatGPT
- `open_chatgpt()` - reloads/open ChatGPT with retry handling
- `wait_for_prompt()` - waits until the prompt box exists
- `wait_for_composer_ready()` - waits until the prompt area is actually usable
- `close()` - closes browser, context, and Playwright safely

## 4. Prompt Flow Layer

### `PromptFlow`

Use this if you want to work with just the write/send/wait logic.

Helpful methods:

- `execute(prompt)` - complete prompt to response flow
- `wait_for_response_start(old_count)` - waits for the first assistant message block
- `wait_for_response_complete(latest_message_block)` - waits until response stops changing

## 5. Demo vs CLI

- `cli.py` - interactive terminal mode
- `demo.py` - short demonstration file for testing prompt and response flow
- `self_test.py` - complete end-to-end runner that checks open, ask, send, restart, close, and reopen

## 6. How To Test Everything

Run the self-test when you want to validate the main public methods:

```bash
python -m chatgpt_automation.self_test
```

This script is meant to exercise the package like a real user would use it.
It sends short prompts, long prompts, restarts the browser, closes it, reopens it, and sends again.

## 7. What To Edit When Something Needs Tuning

If the browser closes too early, edit `config.py`.

If typing is too fast or too slow, edit `typing_delay_ms`, `typing_timeout_floor_ms`, and `typing_timeout_per_char_ms`.

If ChatGPT is slow to answer, edit `response_start_timeout_s` and `response_complete_timeout_s`.

If the prompt selector changes, edit `prompt_selectors` and `send_selectors`.

## 8. Minimal Working Pattern

```python
from chatgpt_automation import ChatGPTClient

client = ChatGPTClient()
client.open()
print(client.ask("Write 5 lines about teamwork in college projects."))
client.close()
```

## 9. Important Notes

- This package still depends on ChatGPT UI selectors.
- If the UI changes, update selectors in `config.py`.
- For very large prompts, keep the typing timeout high.
- Always call `close()` at the end of your script.
