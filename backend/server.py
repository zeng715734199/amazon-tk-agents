"""AgentHub FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

from config import LLM_MODEL, LLM_PROVIDER, get_connection_status
from src.agents import competitor_agent
from src.services import customer_service
from src.chains import supply_chain
from src.models import ChatRequest


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用实例。"""
    application = FastAPI(title="跨境电商 Agent 平台", version="1.0.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 演示环境允许跨域，生产环境应配置白名单。
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = create_app()


@app.get("/api/status")
def status() -> dict:
    """返回平台连接、客服、库存和商品数量。"""
    service_stats = customer_service.get_service_stats()
    supply_stats = supply_chain.get_supply_chain_stats()
    return {
        "connections": get_connection_status(),
        "llm": {"provider": LLM_PROVIDER, "model": LLM_MODEL},
        "customer_service": service_stats["today"],
        "inventory": supply_stats,
        "products": len(supply_chain.INVENTORY),
    }


@app.get("/api/dashboard")
async def dashboard() -> dict:
    """聚合首页看板需要的业务摘要。"""
    service_stats = customer_service.get_service_stats()
    supply_stats = supply_chain.get_supply_chain_stats()
    inventory = supply_chain.get_inventory_overview()
    briefing = await competitor_agent.generate_daily_briefing()
    return {
        "customer_service": service_stats,
        "supply_chain": supply_stats,
        "inventory_alerts": inventory["alerts"][:5],
        "competitor_briefing": briefing,
        "connections": get_connection_status(),
    }


@app.post("/api/cs/chat")
async def customer_chat(request: ChatRequest) -> dict:
    """处理客服消息并返回可解释的处理结果。"""
    return await customer_service.handle_customer_message(
        request.message,
        platform=request.platform,
        conversation_history=[],
    )


@app.get("/api/cs/stats")
def customer_stats() -> dict:
    """返回客服运营统计。"""
    return customer_service.get_service_stats()


@app.get("/api/cs/orders/{order_id}")
def customer_order(order_id: str) -> dict:
    """查询演示订单。"""
    result = customer_service.lookup_order(order_id)
    if not result["found"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="warning")
