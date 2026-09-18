# TK & Amazon 智能运营系统

跨境电商智能运营平台，包含 FastAPI 后端和 Vue 3 前端，提供客服、商品 Listing、TikTok 内容、竞品监控、供应链和利润分析能力。

前端支持两种数据模式：GitHub Pages 默认使用内置 Mock 数据，无需启动后端即可体验完整界面；本地联调时可以切换到 FastAPI 接口。

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

```text
frontend/
├── src/services/api.js      # 统一数据访问入口与模式切换
├── src/services/mock.js     # GitHub Pages 使用的 Mock 数据与交互
├── src/views/               # 业务页面
├── vite.config.js           # base、构建目录和 API 代理
└── .env.example             # 前端环境变量示例
.github/workflows/
└── deploy-frontend.yml      # GitHub Pages 自动部署
```

## 启动

```powershell
cd backend
uv sync --frozen
$env:PYTHONPATH = "."
uv run uvicorn server:app --host 0.0.0.0 --port 8081
```

后端直接依赖在 `pyproject.toml` 中固定版本，`uv.lock` 同时锁定全部传递依赖。仍可使用 `pip install -r requirements.txt` 安装相同版本的直接依赖。

打开 `http://localhost:8081/docs` 查看接口文档。

未配置模型密钥时，Listing 和内容接口自动使用本地模板；竞品实时搜索在未配置 `SERPER_API_KEY` 时返回空结果说明。

内容日历使用三条预置商品生成七天排期。查询不存在的订单时，接口仍返回 `200`，响应中的 `found` 为 `false` 并包含说明信息，便于前端直接展示查询结果。

若需要由后端托管前端构建产物，请将包含 `index.html` 的目录配置到 `FRONTEND_DIST_DIR`。默认读取后端目录下的 `output`；目录不存在时应用仅提供 API，不会创建额外目录。

## 前端开发

```powershell
cd frontend
npm ci

# 默认使用 Mock 数据，访问 http://127.0.0.1:5173/
npm run dev

# 显式使用 Mock 数据
npm run dev:mock

# 连接运行在 127.0.0.1:8081 的 FastAPI
npm run dev:api
```

数据模式由 `VITE_DATA_MODE` 控制：

| 模式 | 行为 | 使用场景 |
| --- | --- | --- |
| `mock` | 使用 `frontend/src/services/mock.js`，不请求后端 | GitHub Pages、产品演示、无后端开发 |
| `api` | 请求 FastAPI 接口 | 本地联调、真实后端环境 |

API 模式的默认接口地址是 `/api`，开发服务器会代理到 `http://127.0.0.1:8081`。部署到独立后端时，可以设置 `VITE_API_BASE_URL`，例如 `https://api.example.com/api`。页面组件不直接区分两种模式，切换模式无需修改页面代码。

## GitHub Pages 部署

当前 Git 远程仓库是 `zeng715734199/amazon-tk-agents`，项目站点地址预期为：

```text
https://zeng715734199.github.io/amazon-tk-agents/
```

`.github/workflows/deploy-frontend.yml` 会在代码推送到 `master` 后自动完成以下步骤：

1. 使用 Node.js 20 和 `frontend/package-lock.json` 安装依赖。
2. 执行 `npm run build:mock`，构建无需后端的静态演示版本。
3. 根据 `${{ github.event.repository.name }}` 自动生成静态资源基础路径，当前为 `/amazon-tk-agents/`。
4. 复制 `dist/index.html` 为 `dist/404.html`，兼容 GitHub Pages 单页应用访问。
5. 将 `frontend/dist` 发布到 GitHub Pages。

首次部署前，需要在 GitHub 仓库的 **Settings → Pages → Build and deployment** 中将 Source 设置为 **GitHub Actions**。工作流所需的 `pages: write` 和 `id-token: write` 权限已经配置。

在本地生成同等静态包：

```powershell
cd frontend
npm run build:mock
Copy-Item dist/index.html dist/404.html
npm run preview
```

预览地址为 `http://localhost:4173/amazon-tk-agents/`。

构建产物位于 `frontend/dist/`，不应手工提交到源码仓库。

若要构建连接独立后端的版本：

```powershell
$env:VITE_DATA_MODE = "api"
$env:VITE_API_BASE_URL = "https://api.example.com/api"
$env:VITE_BASE_PATH = "/amazon-tk-agents/"
npm run build:api
```

GitHub Pages 只能托管静态资源，不能运行 FastAPI。部署 API 模式时必须将后端部署到其他服务，并正确配置 HTTPS 和 CORS。

## 主要接口

| 模块 | 接口 |
| --- | --- |
| 平台 | `GET /api/status`、`GET /api/dashboard`、`GET /api/notifications/next` |
| 客服 | `GET /api/cs/config`、`POST /api/cs/chat`、`GET /api/cs/stats`、`GET /api/cs/orders/{order_id}` |
| Listing | `POST /api/listing/generate`、`GET /api/listing/products` |
| 内容 | `GET /api/content/config`、`POST /api/content/script`、`POST /api/content/live`、`GET /api/content/calendar`、`GET /api/content/formats` |
| 竞品 | `POST /api/competitor/overview`、`GET /api/competitor/briefing`、`POST /api/competitor/search`、`GET /api/competitor/products` |
| 供应链 | `GET /api/supply/overview`、`POST /api/supply/restock`、`POST /api/supply/forecast`、`GET /api/supply/stats` |
| 利润 | `GET /api/profit?period=30d` |

## 验证

```powershell
python -m unittest tests.test_smoke -v
python -m compileall -q .

cd ..\frontend
npm run build:mock
Copy-Item dist/index.html dist/404.html
Test-Path dist\index.html
Test-Path dist\404.html
```

当前冒烟测试覆盖 17 条领域、接口和静态资源验证用例。
