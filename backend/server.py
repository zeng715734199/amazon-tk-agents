"""AgentHub FastAPI 应用入口。"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import FRONTEND_DIST_DIR
from src.routers.registry import register_routers


def create_app(frontend_dir: str | Path | None = None) -> FastAPI:
    """创建并配置 FastAPI 应用实例。"""
    application = FastAPI(title="E-Commerce Agent Platform", version="1.0.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 演示环境允许跨域，生产环境应配置白名单。
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routers(application)

    static_dir = Path(frontend_dir).resolve() if frontend_dir else FRONTEND_DIST_DIR
    if static_dir.is_dir() and (static_dir / "index.html").is_file():
        application.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="warning")
