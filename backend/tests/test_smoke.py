"""后端核心流程冒烟测试。"""

import asyncio
import unittest

from fastapi.testclient import TestClient

from server import app
from src.agents import competitor_agent, content_agent, listing_agent
from src.chains import supply_chain
from src.services import customer_service


class BackendSmokeTest(unittest.TestCase):
    """验证领域模块和接口能够完成最小闭环。"""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_domain_functions(self):
        """验证各领域核心函数返回预期结构。"""
        self.assertEqual(customer_service.detect_language("你好"), "zh")
        self.assertEqual(customer_service.classify_intent("where is my order"), "logistics")
        self.assertTrue(customer_service.lookup_order("ORD-20250301-001")["found"])
        self.assertEqual(len(listing_agent.get_product_list()), 3)
        self.assertEqual(len(content_agent.get_format_list()), 4)
        self.assertEqual(len(competitor_agent.get_tracked_products()), 3)
        self.assertEqual(len(supply_chain.get_inventory_overview()["products"]), 3)

    def test_async_domain_functions(self):
        """验证异步生成流程能够运行。"""
        listing = asyncio.run(listing_agent.generate_listing("earbuds"))
        script = asyncio.run(content_agent.generate_video_script("Demo", ["Fast"]))
        overview = asyncio.run(competitor_agent.get_market_overview("earbuds"))
        self.assertIn("listing", listing)
        self.assertIn("script", script)
        self.assertIn("price_analysis", overview)

    def test_api_routes(self):
        """验证主要接口的状态码和关键字段。"""
        checks = [
            ("get", "/api/status", None, 200),
            ("get", "/api/dashboard", None, 200),
            ("get", "/api/cs/stats", None, 200),
            ("post", "/api/cs/chat", {"message": "where is my order?"}, 200),
            ("get", "/api/listing/products", None, 200),
            ("post", "/api/listing/generate", {"product_key": "earbuds"}, 200),
            ("get", "/api/content/formats", None, 200),
            ("post", "/api/content/script", {"product_name": "Demo", "features": ["Fast"]}, 200),
            ("post", "/api/content/live", {"product_name": "Demo", "features": ["Fast"], "price": 10}, 200),
            ("get", "/api/content/calendar", None, 200),
            ("get", "/api/competitor/products", None, 200),
            ("post", "/api/competitor/overview", {"product_key": "earbuds"}, 200),
            ("get", "/api/competitor/briefing", None, 200),
            ("post", "/api/competitor/search", {"query": "wireless earbuds"}, 200),
            ("get", "/api/supply/overview", None, 200),
            ("post", "/api/supply/restock", {"product_key": "earbuds"}, 200),
            ("post", "/api/supply/forecast", {"product_key": "earbuds", "days": 3}, 200),
            ("get", "/api/supply/stats", None, 200),
        ]
        for method, path, payload, expected_status in checks:
            response = getattr(self.client, method)(path, json=payload) if payload else getattr(self.client, method)(path)
            self.assertEqual(response.status_code, expected_status, path)

        missing = self.client.get("/api/cs/orders/UNKNOWN")
        self.assertEqual(missing.status_code, 404)

    def test_request_validation(self):
        """验证无效请求会返回清晰的校验错误。"""
        invalid_listing = self.client.post("/api/listing/generate", json={})
        invalid_chat = self.client.post("/api/cs/chat", json={"platform": "amazon"})
        invalid_forecast = self.client.post("/api/supply/forecast", json={"product_key": "earbuds", "days": 0})
        empty_search = self.client.post("/api/competitor/search", json={"query": ""})
        self.assertEqual(invalid_listing.status_code, 422)
        self.assertEqual(invalid_chat.status_code, 422)
        self.assertEqual(invalid_forecast.status_code, 422)
        self.assertEqual(empty_search.status_code, 422)

    def test_unknown_resources(self):
        """验证未知商品返回可读错误而不会抛出服务器异常。"""
        listing = self.client.post("/api/listing/generate", json={"product_key": "missing"})
        competitor = self.client.post("/api/competitor/overview", json={"product_key": "missing"})
        restock = self.client.post("/api/supply/restock", json={"product_key": "missing"})
        self.assertEqual(listing.status_code, 200)
        self.assertIn("error", listing.json())
        self.assertEqual(competitor.status_code, 200)
        self.assertIn("error", competitor.json())
        self.assertEqual(restock.status_code, 200)
        self.assertIn("error", restock.json())


if __name__ == "__main__":
    unittest.main()
