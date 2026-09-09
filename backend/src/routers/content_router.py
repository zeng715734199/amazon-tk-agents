"""TikTok 内容业务路由。"""

from fastapi import APIRouter

from src.agents import content_agent
from src.mock.content_mock import CALENDAR_PRODUCTS
from src.models import LiveRequest, ScriptRequest

router = APIRouter(prefix="/api/content", tags=["内容"])


@router.post("/script")
async def generate_script(request: ScriptRequest) -> dict:
    """生成短视频脚本。"""
    return await content_agent.generate_video_script(
        request.product_name,
        request.features,
        request.format_type,
        request.language,
    )


@router.post("/live")
async def generate_live_script(request: LiveRequest) -> dict:
    """生成直播带货话术。"""
    return await content_agent.generate_live_script(
        request.product_name,
        request.features,
        request.price,
        request.promo_price,
    )


@router.get("/calendar")
async def content_calendar() -> dict:
    """生成七天内容排期。"""
    return await content_agent.generate_content_calendar(CALENDAR_PRODUCTS, 7)


@router.get("/formats")
def content_formats() -> list[dict]:
    """返回可用的视频格式。"""
    return content_agent.get_format_list()
