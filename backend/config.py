"""
跨境电商 AI Agent 平台配置中心。

所有配置优先从环境变量读取；未配置时保持空字符串，后端会自动进入演示模式。
"""
import os


LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai").strip().lower()  # 提供方选择：ollama/local 或 openai/remote。
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")  # 远端模型鉴权密钥
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")  # 远端 OpenAI 兼容 API 根地址。


# Ollama 原生接口地址和本地模型名；可用环境变量覆盖默认值。
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")  # Ollama 服务监听地址。
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")  # 本地默认模型名，需已通过 ollama pull 下载。

# 未显式指定模型时，根据提供方选择合理默认值。
LLM_MODEL = os.environ.get("LLM_MODEL", OLLAMA_MODEL if LLM_PROVIDER in {"ollama", "local"} else "gpt-4o-mini")


# Amazon SP-API 配置。
# 官方文档：https://developer-docs.amazon.com/sp-api/
AMAZON_SELLER_ID = os.environ.get("AMAZON_SELLER_ID", "")  # Amazon 卖家账号 ID。
AMAZON_ACCESS_KEY = os.environ.get("AMAZON_ACCESS_KEY", "")  # SP-API 访问密钥。
AMAZON_SECRET_KEY = os.environ.get("AMAZON_SECRET_KEY", "")  # SP-API 秘密密钥。
AMAZON_REFRESH_TOKEN = os.environ.get("AMAZON_REFRESH_TOKEN", "")  # OAuth 刷新令牌。
AMAZON_MARKETPLACE = os.environ.get("AMAZON_MARKETPLACE", "ATVPDKIKX0DER")  # Marketplace ID，默认美国站。



# TikTok Shop 开放平台配置。
# 官方文档：https://partner.tiktokshop.com/docv2
TIKTOK_APP_KEY = os.environ.get("TIKTOK_APP_KEY", "")  # TikTok Shop 应用 Key。
TIKTOK_APP_SECRET = os.environ.get("TIKTOK_APP_SECRET", "")  # TikTok Shop 应用 Secret。
TIKTOK_ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN", "")  # 店铺访问令牌。
TIKTOK_SHOP_ID = os.environ.get("TIKTOK_SHOP_ID", "")  # 店铺标识。


# 网页搜索：供竞品监控 Agent 查询实时搜索结果。
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")  # Serper 搜索 API 密钥。

# ERP / 库存系统：预留给真实库存同步。
ERP_API_URL = os.environ.get("ERP_API_URL", "")  # ERP 服务基础地址。
ERP_API_KEY = os.environ.get("ERP_API_KEY", "")  # ERP 鉴权密钥。


# 通知 Webhook：预留给 Slack、钉钉或飞书告警。
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")  # Slack / DingTalk / Feishu 告警 Webhook 地址。


# 配置检查辅助函数：判断各外部服务是否“已填写配置”。
def get_connection_status():
    """
    返回各外部服务是否已配置。

    布尔值仅代表必要环境变量非空，不会发起健康检查，
    因此 True 不等于远端账号或密钥一定有效。
    """
    return {
        # Ollama 不需要 API Key；远端模型则以 Key 是否存在作为“已配置”标志。
        "llm": LLM_PROVIDER in {"ollama", "local"} or bool(LLM_API_KEY),
        "amazon": bool(AMAZON_ACCESS_KEY and AMAZON_SECRET_KEY),
        "tiktok": bool(TIKTOK_APP_KEY and TIKTOK_ACCESS_TOKEN),
        "serper": bool(SERPER_API_KEY),
        "erp": bool(ERP_API_URL and ERP_API_KEY),
        "webhook": bool(WEBHOOK_URL),
    }
