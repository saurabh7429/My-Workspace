"""Custom exceptions for ChatGPT browser automation."""


class ChatGPTAutomationError(Exception):
    """Base exception for all package errors."""


class BrowserSessionError(ChatGPTAutomationError):
    """Browser or page lifecycle failure."""


class ComposerNotReadyError(ChatGPTAutomationError):
    """Prompt composer is not ready for input."""


class PromptTypingError(ChatGPTAutomationError):
    """Prompt text could not be written completely."""


class ResponseTimeoutError(ChatGPTAutomationError):
    """ChatGPT did not start or finish responding in time."""
