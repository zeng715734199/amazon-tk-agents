"""Unified asynchronous chat interface for local and remote models."""

from collections.abc import Sequence
from typing import Any

import httpx

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_PROVIDER, OLLAMA_BASE_URL

Message = dict[str, Any]


def _uses_ollama() -> bool:
    return LLM_PROVIDER in {"ollama", "local"}


async def _chat_ollama(
    client: httpx.AsyncClient,
    messages: Sequence[Message],
    temperature: float,
    max_tokens: int,
) -> str:
    response = await client.post(
        f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat",
        headers={"Content-Type": "application/json"},
        json={
            "model": LLM_MODEL,
            "messages": list(messages),
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]
