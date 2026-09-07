"""Environment-driven backend configuration."""

import os


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").strip().lower()
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
LLM_MODEL = os.getenv(
    "LLM_MODEL",
    OLLAMA_MODEL if LLM_PROVIDER in {"ollama", "local"} else "gpt-4o-mini",
)
