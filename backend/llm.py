"""Unified asynchronous chat interface for local and remote models."""

from collections.abc import Sequence
from typing import Any

import httpx

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_PROVIDER, OLLAMA_BASE_URL

Message = dict[str, Any]


def _uses_ollama() -> bool:
    return LLM_PROVIDER in {"ollama", "local"}
