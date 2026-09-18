"""平台实时通知数据服务。"""

import random

from src.mock.competitor_mock import TRACKED_COMPETITORS
from src.mock.listing_mock import DEMO_PRODUCTS
from src.mock.supply_chain_mock import INVENTORY


NOTIFICATION_DELAY_RANGE_MS = (8_000, 12_000)


def _order_notification() -> dict:
    product = random.choice(list(DEMO_PRODUCTS.values()))
    platform = random.choice(["Amazon", "TikTok Shop"])
    return {
        "type": "order",
        "icon": "🛒",
        "title": "新订单",
        "message": f"{product['name']} - {platform}",
    }


def _inventory_notification() -> dict:
    product = random.choice(list(INVENTORY.values()))
    variant_name, _ = min(
        product["variants"].items(),
        key=lambda item: item[1]["amazon_fba"],
    )
    return {
        "type": "inventory",
        "icon": "📦",
        "title": "库存预警",
        "message": f"{product['name']} {variant_name} 款 FBA 库存低于安全线",
    }


def _competitor_notification() -> dict:
    competitor = random.choice([
        item
        for competitors in TRACKED_COMPETITORS.values()
        for item in competitors
    ])
    return {
        "type": "competitor",
        "icon": "💰",
        "title": "竞品价格变动",
        "message": f"{competitor['name']} 当前价格 ${competitor['current_price']:.2f}",
    }


def _review_notification() -> dict:
    product = random.choice(list(DEMO_PRODUCTS.values()))
    rating = random.choice([4, 5])
    return {
        "type": "review",
        "icon": "⭐",
        "title": "新评论",
        "message": f"{product['name']} 收到 {rating} 星评价",
    }


NOTIFICATION_FACTORIES = (
    _order_notification,
    _inventory_notification,
    _competitor_notification,
    _review_notification,
)


def get_next_notification() -> dict:
    """返回下一条平台通知及前端展示前的等待时间。"""
    notification = random.choice(NOTIFICATION_FACTORIES)()
    return {
        **notification,
        "delay_ms": random.randint(*NOTIFICATION_DELAY_RANGE_MS),
    }
