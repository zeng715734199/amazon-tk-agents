"""后端接口请求模型。"""

from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """客服消息请求。"""

    message: str
    platform: str = "tiktok"
    conversation_id: Optional[str] = None


class ListingRequest(BaseModel):
    """商品 Listing 请求。"""

    product_key: str
    platform: str = "amazon"
    language: str = "en"


class ScriptRequest(BaseModel):
    """短视频脚本请求。"""

    product_name: str
    features: list[str] = Field(default_factory=list)
    format_type: str = "unboxing"
    language: str = "en"


class LiveRequest(BaseModel):
    """直播话术请求。"""

    product_name: str
    features: list[str] = Field(default_factory=list)
    price: float
    promo_price: Optional[float] = None


class CompetitorRequest(BaseModel):
    """竞品概览请求。"""

    product_key: str


class RestockRequest(BaseModel):
    """补货计划请求。"""

    product_key: str


class ForecastRequest(BaseModel):
    """需求预测请求。"""

    product_key: str
    days: int = 30


class SearchRequest(BaseModel):
    """竞品搜索请求。"""

    query: str
