"""应用路由注册器。"""

from fastapi import FastAPI

from . import competitor_router, content_router, customer_router, listing_router, platform_router, supply_router


def register_routers(application: FastAPI) -> None:
    """将所有业务路由统一挂载到应用。"""
    for module in (
        platform_router,
        customer_router,
        listing_router,
        content_router,
        competitor_router,
        supply_router,
    ):
        application.include_router(module.router)
