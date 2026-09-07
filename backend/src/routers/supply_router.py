"""供应链业务路由。"""

from fastapi import APIRouter

from src.chains import supply_chain
from src.models import ForecastRequest, RestockRequest

router = APIRouter(prefix="/api/supply", tags=["供应链"])


@router.get("/overview")
def supply_overview() -> dict:
    """返回库存总览和告警。"""
    return supply_chain.get_inventory_overview()


@router.post("/restock")
def supply_restock(request: RestockRequest) -> dict:
    """生成补货计划。"""
    return supply_chain.generate_restock_plan(request.product_key)


@router.post("/forecast")
def supply_forecast(request: ForecastRequest) -> dict:
    """生成需求预测。"""
    return supply_chain.forecast_demand(request.product_key, request.days)


@router.get("/stats")
def supply_stats() -> dict:
    """返回供应链运营指标。"""
    return supply_chain.get_supply_chain_stats()
