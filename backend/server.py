"""AgentHub FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import LLM_MODEL, LLM_PROVIDER, get_connection_status
from src.agents import competitor_agent
from src.services import customer_service
from src.chains import supply_chain
from src.routers import competitor_router, content_router, customer_router, listing_router, supply_router


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
app.include_router(listing_router.router)
app.include_router(content_router.router)
app.include_router(competitor_router.router)
app.include_router(supply_router.router)
app.include_router(customer_router.router)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="warning")
