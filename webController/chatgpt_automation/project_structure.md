# Final Project Structure

```text
chatgpt_automation/
├── __init__.py
├── __main__.py
├── client.py
├── cli.py
├── config.py
├── demo.py
├── exceptions.py
├── prompt_flow.py
├── README.md
├── requirements.txt
├── session.py
└── USAGE.md
```

## File Purpose

- `__init__.py` - public imports for easy usage
- `client.py` - main facade class; import this first
- `cli.py` - terminal entrypoint
- `config.py` - change waiting time, retry counts, selectors, and fallbacks here
- `demo.py` - simple demo prompt runner
- `exceptions.py` - custom error types
- `prompt_flow.py` - write prompt and wait for response logic
- `session.py` - open, close, and restart browser session
- `README.md` - short project overview
- `USAGE.md` - detailed how-to-use guide
- `requirements.txt` - Python dependency list
- `__main__.py` - lets you run the package with `python -m chatgpt_automation`

## Public API

After importing, these are the main callable parts:

- `ChatGPTClient.open()`
- `ChatGPTClient.execute(prompt)`
- `ChatGPTClient.ask(prompt)`
- `ChatGPTClient.send(prompt)`
- `ChatGPTClient.restart()`
- `ChatGPTClient.close()`
- `ChatGPTClient.status()`

## Demo File

The demo file shows a fixed sample prompt and prints the response:

- `demo.py`

Use it when you want a quick one-command test of the package flow.

## Typical Flow

1. Create `ChatGPTClient`
2. Call `open()`
3. Call `execute(prompt)` as many times as needed
4. Call `close()` when done

## Configuration Flow

Change only `config.py` when you want to adjust:

- prompt wait time
- composer wait time
- typing speed and timeout
- response start wait
- response completion wait
- retry counts
- selectors
```
