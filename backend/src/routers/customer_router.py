"""客服业务路由。"""

from fastapi import APIRouter

from src.models import ChatRequest
from src.services import customer_service

router = APIRouter(prefix="/api/cs", tags=["客服"])


@router.post("/chat")
async def customer_chat(request: ChatRequest) -> dict:
    """处理客服消息并返回可解释结果。"""
    return await customer_service.handle_customer_message(
        request.message,
        platform=request.platform,
        conversation_history=[],
    )


@router.get("/stats")
def customer_stats() -> dict:
    """返回客服运营统计。"""
    return customer_service.get_service_stats()


@router.get("/orders/{order_id}")
def customer_order(order_id: str) -> dict:
    """查询演示订单。"""
    return customer_service.lookup_order(order_id)
