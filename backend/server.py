"""AgentHub FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import competitor_router, content_router, customer_router, listing_router, platform_router, supply_router


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用实例。"""
    application = FastAPI(title="跨境电商 Agent 平台", version="1.0.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 演示环境允许跨域，生产环境应配置白名单。
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = create_app()
app.include_router(listing_router.router)
app.include_router(content_router.router)
app.include_router(competitor_router.router)
app.include_router(supply_router.router)
app.include_router(customer_router.router)
app.include_router(platform_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="warning")
