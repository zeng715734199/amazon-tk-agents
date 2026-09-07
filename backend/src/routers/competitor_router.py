"""竞品监控业务路由。"""

from fastapi import APIRouter

from src.agents import competitor_agent
from src.models import CompetitorRequest, SearchRequest

router = APIRouter(prefix="/api/competitor", tags=["竞品"])


@router.post("/overview")
async def competitor_overview(request: CompetitorRequest) -> dict:
    """返回指定商品的竞品市场概览。"""
    return await competitor_agent.get_market_overview(request.product_key)


@router.get("/briefing")
async def competitor_briefing() -> dict:
    """返回每日竞品简报。"""
    return await competitor_agent.generate_daily_briefing()


@router.post("/search")
async def competitor_search(request: SearchRequest) -> dict:
    """搜索实时竞品信息。"""
    return await competitor_agent.search_competitor_live(request.query)


@router.get("/products")
def tracked_products() -> list[dict]:
    """返回已跟踪的自有商品。"""
    return competitor_agent.get_tracked_products()
