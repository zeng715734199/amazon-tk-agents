# AgentHub 后端

跨境电商智能运营后端，基于 FastAPI 提供客服、商品 Listing、TikTok 内容、竞品监控和供应链能力。

## 目录结构

```text
backend/
├── config.py                 # 环境变量配置
├── llm.py                    # 统一模型调用
├── server.py                # FastAPI 应用入口
├── src/
│   ├── agents/              # Listing、内容、竞品智能体
│   ├── services/            # 客服服务
│   ├── chains/              # 供应链计算链路
│   ├── models/              # Pydantic 请求模型
│   ├── mock/                # 演示数据
│   └── routers/             # 业务 API 路由
└── tests/                   # 冒烟测试
```

## 启动

```powershell
pip install -r requirements.txt
$env:PYTHONPATH = "."
python -m uvicorn server:app --host 0.0.0.0 --port 8081
```

打开 `http://localhost:8081/docs` 查看接口文档。

未配置模型密钥时，Listing 和内容接口自动使用本地模板；竞品实时搜索在未配置 `SERPER_API_KEY` 时返回空结果说明。

内容日历使用三条预置商品生成七天排期。查询不存在的订单时，接口仍返回 `200`，响应中的 `found` 为 `false` 并包含说明信息，便于前端直接展示查询结果。

## 主要接口

| 模块 | 接口 |
| --- | --- |
| 平台 | `GET /api/status`、`GET /api/dashboard` |
| 客服 | `POST /api/cs/chat`、`GET /api/cs/stats`、`GET /api/cs/orders/{order_id}` |
| Listing | `POST /api/listing/generate`、`GET /api/listing/products` |
| 内容 | `POST /api/content/script`、`POST /api/content/live`、`GET /api/content/calendar`、`GET /api/content/formats` |
| 竞品 | `POST /api/competitor/overview`、`GET /api/competitor/briefing`、`POST /api/competitor/search`、`GET /api/competitor/products` |
| 供应链 | `GET /api/supply/overview`、`POST /api/supply/restock`、`POST /api/supply/forecast`、`GET /api/supply/stats` |

## 验证

```powershell
python -m unittest tests.test_smoke -v
python -m compileall -q .
```
