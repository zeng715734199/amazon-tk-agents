"""平台状态与看板路由。"""

from fastapi import APIRouter

from config import LLM_MODEL, LLM_PROVIDER, get_connection_status
from src.agents import competitor_agent
from src.chains import supply_chain
from src.services import customer_service

router = APIRouter(prefix="/api", tags=["平台"])


@router.get("/status")
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


@router.get("/dashboard")
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
