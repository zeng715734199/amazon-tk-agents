"""利润分析业务路由。"""

from typing import Literal

from fastapi import APIRouter

from src.services import profit_service

router = APIRouter(prefix="/api/profit", tags=["利润"])


@router.get("")
def profit_report(period: Literal["30d", "90d", "year"] = "30d") -> dict:
    """返回指定周期的利润分析数据。"""
    return profit_service.get_profit_report(period)
