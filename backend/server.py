import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn



# 创建应用对象，标题和版本会出现在 OpenAPI 文档中。
app = FastAPI(title="跨境电商Agent平台", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 对所有来源开放，生产环境应改成白名单域名。
    allow_methods=["*"],  # 允许 GET、POST 等所有方法。
    allow_headers=["*"],  # 接受所有请求头，例如 Content-Type。
)

# 平台状态接口。
@app.get("/api/status")
def status():
    return True


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8081, log_level="warning")
