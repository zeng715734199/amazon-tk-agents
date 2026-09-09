"""基于环境变量的后端配置。"""

import os
from pathlib import Path


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").strip().lower()
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
LLM_MODEL = os.getenv(
    "LLM_MODEL",
    OLLAMA_MODEL if LLM_PROVIDER in {"ollama", "local"} else "gpt-4o-mini",
)

AMAZON_SELLER_ID = os.getenv("AMAZON_SELLER_ID", "")
AMAZON_ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY", "")
AMAZON_SECRET_KEY = os.getenv("AMAZON_SECRET_KEY", "")
AMAZON_REFRESH_TOKEN = os.getenv("AMAZON_REFRESH_TOKEN", "")
AMAZON_MARKETPLACE = os.getenv("AMAZON_MARKETPLACE", "ATVPDKIKX0DER")

TIKTOK_APP_KEY = os.getenv("TIKTOK_APP_KEY", "")
TIKTOK_APP_SECRET = os.getenv("TIKTOK_APP_SECRET", "")
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")
TIKTOK_SHOP_ID = os.getenv("TIKTOK_SHOP_ID", "")

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
ERP_API_URL = os.getenv("ERP_API_URL", "")
ERP_API_KEY = os.getenv("ERP_API_KEY", "")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
FRONTEND_DIST_DIR = Path(
    os.getenv("FRONTEND_DIST_DIR", Path(__file__).resolve().parent / "output")
).resolve()


def get_connection_status() -> dict[str, bool]:
    """检查各外部服务是否填写必要配置。"""
    return {
        "llm": LLM_PROVIDER in {"ollama", "local"} or bool(LLM_API_KEY),
        "amazon": bool(AMAZON_ACCESS_KEY and AMAZON_SECRET_KEY),
        "tiktok": bool(TIKTOK_APP_KEY and TIKTOK_ACCESS_TOKEN),
        "serper": bool(SERPER_API_KEY),
        "erp": bool(ERP_API_URL and ERP_API_KEY),
        "webhook": bool(WEBHOOK_URL),
    }
