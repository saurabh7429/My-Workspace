# ChatGPT Automation Package

This folder contains an importable Playwright-based package for browser automation with ChatGPT.
It is organized so a new user can quickly understand what to import, what to edit, and what to run.

## What You Get

- A single public client class: `ChatGPTClient`
- Clean methods for open, execute, ask, send, restart, close, and status
- A central config file for timings, retries, and selectors
- A demo file for one prompt and one response
- A self-test file for end-to-end validation
- A terminal CLI and a module entrypoint

## Folder Layout

```text
chatgpt_automation/
├── __init__.py
├── __main__.py
├── cli.py
├── client.py
├── config.py
├── demo.py
├── exceptions.py
├── prompt_flow.py
├── self_test.py
├── session.py
├── README.md
└── USAGE.md
```

## Install

```bash
pip install playwright
playwright install
```

## Quick Start

```python
from chatgpt_automation import ChatGPTClient

client = ChatGPTClient()
client.open()
response = client.execute("Hello, write a short intro about browser automation.")
print(response)
client.close()
```

## Public API

- `open()` - start the browser and open ChatGPT
- `execute(prompt)` - type the prompt, send it, wait for the final answer
- `ask(prompt)` - alias of `execute(prompt)`
- `send(prompt)` - alias of `execute(prompt)`
- `restart()` - close the session and open a fresh one
- `close()` - shut down browser and Playwright safely
- `status()` - inspect session state and current settings

## What To Edit When You Need Tuning

Open [config.py](config.py) and change:

- `prompt_ready_timeout_s`
- `composer_ready_timeout_s`
- `typing_timeout_floor_ms`
- `typing_timeout_per_char_ms`
- `typing_timeout_base_ms`
- `typing_settle_delay_s`
- `send_click_delay_s`
- `response_start_timeout_s`
- `response_complete_timeout_s`
- `typing_retries`
- `prompt_selectors`
- `send_selectors`
- `assistant_selector`

## How To Test

Use the self-test script when you want to verify the main public methods end to end:

```bash
python -m chatgpt_automation.self_test
```

The self-test runs a short prompt, alias methods, restart, close/reopen, and a longer prompt.
It also retries failed steps and restarts the browser when needed.

## Demo

Run the simple demo if you only want a single prompt and response:

```bash
python -m chatgpt_automation.demo
```

## Notes

- The package depends on ChatGPT DOM selectors, so UI changes may require config updates.
- If prompts are long, increase the typing-related timeout values in `config.py`.
- If responses are slow, increase response timeouts in `config.py`.
- Always call `close()` at the end of your script.
