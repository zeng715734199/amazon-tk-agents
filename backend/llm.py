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


async def _chat_openai(
    client: httpx.AsyncClient,
    messages: Sequence[Message],
    temperature: float,
    max_tokens: int,
) -> str:
    response = await client.post(
        f"{LLM_BASE_URL.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "messages": list(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _demo_response(messages: Sequence[Message]) -> str:
    user_message = str(messages[-1].get("content", "")) if messages else ""
    return (
        "[Demo Mode — Connect LLM API for real generation]\n\n"
        f'Based on your input: "{user_message[:100]}..."\n\n'
        "This is a placeholder response. Configure LLM_API_KEY to enable generation."
    )


async def llm_chat(
    messages: Sequence[Message], temperature: float = 0.7, max_tokens: int = 2000
) -> str:
    """Route a chat request and degrade gracefully when a provider is unavailable."""
    if not _uses_ollama() and not LLM_API_KEY:
        return _demo_response(messages)

    try:
        async with httpx.AsyncClient() as client:
            if _uses_ollama():
                return await _chat_ollama(client, messages, temperature, max_tokens)
            return await _chat_openai(client, messages, temperature, max_tokens)
    except Exception as exc:
        return f"[LLM Error: {exc}] — Please check your LLM API configuration."
