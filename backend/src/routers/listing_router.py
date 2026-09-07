"""Listing 业务路由。"""

from fastapi import APIRouter

from src.agents import listing_agent
from src.models import ListingRequest

router = APIRouter(prefix="/api/listing", tags=["Listing"])


@router.post("/generate")
async def generate_listing(request: ListingRequest) -> dict:
    """生成商品 Listing 文案。"""
    return await listing_agent.generate_listing(
        request.product_key,
        request.platform,
        request.language,
    )


@router.get("/products")
def list_products() -> list[dict]:
    """返回可生成 Listing 的商品列表。"""
    return listing_agent.get_product_list()
