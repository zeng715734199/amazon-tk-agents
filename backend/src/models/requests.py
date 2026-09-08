"""后端接口请求模型。"""

from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ChatRequest(BaseModel):
    """客服消息请求。"""

    message: str = Field(min_length=1)
    platform: str = "tiktok"
    conversation_id: Optional[str] = None


class ListingRequest(BaseModel):
    """商品 Listing 请求。"""

    product_key: str = Field(min_length=1)
    platform: str = "amazon"
    language: str = "en"


class ScriptRequest(BaseModel):
    """短视频脚本请求。"""

    product_name: str = Field(min_length=1)
    features: list[str] = Field(default_factory=list)
    format_type: str = "unboxing"
    language: str = "en"


class LiveRequest(BaseModel):
    """直播话术请求。"""

    product_name: str = Field(min_length=1)
    features: list[str] = Field(default_factory=list)
    price: float = Field(gt=0)
    promo_price: Optional[float] = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_promotion_price(self):
        """确保促销价不高于原价。"""
        if self.promo_price is not None and self.promo_price > self.price:
            raise ValueError("促销价不能高于原价")
        return self


class CompetitorRequest(BaseModel):
    """竞品概览请求。"""

    product_key: str = Field(min_length=1)


class RestockRequest(BaseModel):
    """补货计划请求。"""

    product_key: str = Field(min_length=1)


class ForecastRequest(BaseModel):
    """需求预测请求。"""

    product_key: str
    days: int = Field(default=30, gt=0, le=365)


class SearchRequest(BaseModel):
    """竞品搜索请求。"""

    query: str = Field(min_length=1)
