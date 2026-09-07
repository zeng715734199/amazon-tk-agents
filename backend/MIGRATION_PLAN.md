# AgentHub 后端迁移计划

## 目标与约束

- 将 `F:\repo\AgentHub-main\AgentHub-main\app` 的后端能力迁移到当前后端仓库。
- 保留当前仓库的分层结构：根目录承载应用入口与基础配置，`src/agents` 承载领域 Agent，预留 `src/routers`、`src/services`、`src/models`、`src/utils` 作为可扩展边界。
- 迁移后支持演示模式（未配置外部密钥时不阻断 API），并保持源项目既有 API 契约。
- 每个功能点独立提交；目标为 48 个规范化 commit。代码只保留必要的模块说明和关键业务注释。

## 目录映射

| 源路径 | 目标路径 | 说明 |
| --- | --- | --- |
| `app/config.py` | `config.py` | 保留环境变量配置与连接状态检查 |
| `app/llm.py` | `llm.py` | 保留 Ollama/OpenAI 兼容调用与演示回退 |
| `app/server.py` | `server.py` + `src/models` | 入口、请求模型和 API 路由；按功能拆分提交 |
| `app/agents/*.py` | `src/agents/*.py` | 五个领域 Agent，调整为当前仓库的包导入路径 |
| `app/__init__.py`、`app/agents/__init__.py` | `src/__init__.py`、`src/agents/__init__.py` | 包初始化与公共导出 |

## 48 个迁移 commit

提交均采用 Conventional Commits 风格，完成一个功能点并通过对应检查后立即提交。

1. `docs: add backend migration plan`：建立本计划书。
2. `chore: prepare source package layout`：补齐 `src`/Agent 包入口和迁移约定。
3. `feat(config): migrate model provider settings`：迁移 LLM、Ollama 配置。
4. `feat(config): migrate marketplace credentials`：迁移 Amazon/TikTok 配置。
5. `feat(config): migrate integration status helper`：迁移外部服务状态检查。
6. `feat(llm): add provider routing`：加入统一异步 LLM 路由。
7. `feat(llm): add ollama chat transport`：加入 Ollama 原生协议。
8. `feat(llm): add openai compatible transport`：加入 OpenAI 兼容协议。
9. `feat(llm): add demo fallback`：加入离线演示回退和异常文本。
10. `feat(agent): migrate shared agent package`：建立 Agent 公共包导出。
11. `feat(customer-service): add language detection`：迁移语言识别。
12. `feat(customer-service): add intent classification`：迁移意图分类。
13. `feat(customer-service): add escalation rules`：迁移升级判断。
14. `feat(customer-service): add knowledge base search`：迁移 TF-IDF 知识库检索。
15. `feat(customer-service): add order lookup`：迁移订单查询和订单号提取。
16. `feat(customer-service): add response orchestration`：迁移客服主流程与多语言回退。
17. `feat(customer-service): add service statistics`：迁移客服统计。
18. `feat(listing): add product catalog`：迁移演示商品和关键词数据。
19. `feat(listing): add template generation`：迁移模板 Listing 生成。
20. `feat(listing): add llm generation`：迁移 LLM Listing 生成。
21. `feat(listing): add seo scoring`：迁移 SEO 评分与问题列表。
22. `feat(listing): add competitor mock analysis`：迁移竞品分析演示数据。
23. `feat(listing): add product listing helper`：迁移商品列表接口数据。
24. `feat(content): add video templates`：迁移短视频模板和格式定义。
25. `feat(content): add template script generation`：迁移模板脚本生成。
26. `feat(content): add llm script generation`：迁移 LLM 脚本生成。
27. `feat(content): add live commerce scripts`：迁移直播话术生成。
28. `feat(content): add content calendar`：迁移内容日历。
29. `feat(content): add hashtag selection`：迁移标签选择与格式列表。
30. `feat(competitor): add tracked products`：迁移竞品和自有商品数据。
31. `feat(competitor): add market overview`：迁移市场概览。
32. `feat(competitor): add live search`：迁移 Serper 搜索和演示回退。
33. `feat(competitor): add pricing recommendations`：迁移动态定价建议。
34. `feat(competitor): add daily briefing`：迁移每日简报和商品列表。
35. `feat(supply): add inventory dataset`：迁移库存与销量数据。
36. `feat(supply): add inventory overview`：迁移库存概览和告警。
37. `feat(supply): add restock planning`：迁移补货计划。
38. `feat(supply): add demand forecasting`：迁移需求预测。
39. `feat(supply): add supply statistics`：迁移供应链 KPI。
40. `feat(models): add request schemas`：迁移并集中请求模型。
41. `feat(api): add application shell`：迁移 FastAPI 应用、CORS 和运行入口。
42. `feat(api): add status and dashboard routes`：迁移状态与仪表盘接口。
43. `feat(api): add customer service routes`：迁移客服接口。
44. `feat(api): add listing and content routes`：迁移 Listing 与内容接口。
45. `feat(api): add competitor routes`：迁移竞品接口。
46. `feat(api): add supply chain routes`：迁移供应链接口。
47. `test: verify migrated api workflows`：增加迁移后的冒烟验证与导入检查。
48. `docs: document migrated backend usage`：补充 README、运行方式和 API 说明。

## 验证策略

每个 Agent 完成后执行模块导入和核心函数的最小调用；API 路由完成后使用 FastAPI `TestClient` 验证状态码、关键字段和未知资源的错误响应。最终执行 `python -m compileall`、完整冒烟测试和 `git log` 检查，确认 48 个提交均存在且工作树干净。

