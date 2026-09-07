"""多平台智能客服服务。"""

import random
import re
import time

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.mock.customer_service_mock import (
    DEMO_ORDERS,
    ESCALATION_KEYWORDS,
    INTENT_KEYWORDS,
    KB_ENTRIES,
)

_kb_texts = [f"{entry['q']} {entry['a']}" for entry in KB_ENTRIES]
_kb_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
_kb_matrix = _kb_vectorizer.fit_transform(_kb_texts)


def detect_language(text: str) -> str:
    """根据中文字符比例进行轻量级语言识别。"""
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return "zh" if chinese_chars > len(text) * 0.15 else "en"


def classify_intent(text: str) -> str:
    text = text.lower()
    scores = {
        intent: sum(keyword in text for keyword in keywords)
        for intent, keywords in INTENT_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] else "general"


def check_escalation(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in ESCALATION_KEYWORDS)


def search_kb(query: str, top_k: int = 3) -> list[dict]:
    scores = cosine_similarity(_kb_vectorizer.transform([query]), _kb_matrix).flatten()
    results = []
    for index in np.argsort(scores)[::-1][:top_k]:
        if scores[index] > 0.05:
            results.append({
                "answer": KB_ENTRIES[index]["a"],
                "category": KB_ENTRIES[index]["category"],
                "score": round(float(scores[index]), 4),
            })
    return results


def lookup_order(order_id: str) -> dict:
    order = DEMO_ORDERS.get(order_id)
    if order:
        return {"found": True, **order}
    return {"found": False, "message": f"Order {order_id} not found"}


def extract_order_id(text: str) -> str | None:
    match = re.search(r"ORD-\d{8}-\d{3}", text.upper())
    if match:
        return match.group()
    match = re.search(r"#?(\d{6,})", text)
    return f"ORD-{match.group(1)}" if match else None


def _escalation_response(language: str) -> str:
    ticket = random.randint(10000, 99999)
    if language == "zh":
        return f"您的问题已升级至人工客服。专员将在30分钟内与您联系。工单编号：#ESC-{ticket}"
    return f"Your case has been escalated. A specialist will contact you within 30 minutes. Reference: #ESC-{ticket}"


def _order_response(order: dict) -> str:
    messages = {
        "processing": "Your order is being prepared and will ship within 1-2 business days.",
        "in_transit": f"Your order is on the way! Tracking: {order.get('tracking', 'N/A')}. Estimated delivery: {order.get('estimated_delivery', 'N/A')}.",
        "delivered": f"Your order was delivered on {order.get('delivered_date', 'N/A')}.",
        "returned": f"Your return has been processed. Refund status: {order.get('refund_status', 'pending')}.",
    }
    return messages.get(order["status"], f"Order status: {order['status']}")


def _fallback_response(intent: str) -> str:
    messages = {
        "pre_sale": "Which product are you considering? I can help with details, sizing, and availability.",
        "after_sale": "Please provide your order number so I can help with your after-sale request.",
        "logistics": "Please share your order or tracking number and I'll check the latest status.",
        "complaint": "I'm sorry about your experience. Please share your order number and details.",
        "general": "How can I help? I can assist with products, tracking, returns, and other concerns.",
    }
    return messages.get(intent, messages["general"])


async def handle_customer_message(
    message: str,
    conversation_history: list | None = None,
    platform: str = "tiktok",
) -> dict:
    """完成分类、订单查询、知识检索和回复选择。"""
    started_at = time.perf_counter()
    language = detect_language(message)
    intent = classify_intent(message)
    escalated = check_escalation(message)
    steps = [{"type": "detect", "detail": f"Language: {language}, Intent: {intent}, Escalation: {escalated}"}]

    order_id = extract_order_id(message)
    order_info = lookup_order(order_id) if order_id else None
    if order_id:
        steps.append({"type": "tool_call", "tool": "lookup_order", "input": order_id, "output": order_info})

    kb_results = search_kb(message)
    steps.append({"type": "kb_search", "results_count": len(kb_results), "top_score": kb_results[0]["score"] if kb_results else 0})

    if escalated:
        response = _escalation_response(language)
        steps.append({"type": "escalation", "detail": "Routed to human agent"})
    elif order_info and order_info["found"]:
        response = _order_response(order_info)
    elif kb_results:
        response = kb_results[0]["answer"]
        if language == "zh":
            response += "\n\n[Auto-translate to zh when LLM is connected]"
    else:
        response = _fallback_response(intent)

    return {
        "response": response,
        "intent": intent,
        "language": language,
        "escalated": escalated,
        "order_info": order_info,
        "kb_results": kb_results[:2],
        "steps": steps,
        "elapsed_ms": round((time.perf_counter() - started_at) * 1000, 2),
        "platform": platform,
    }


def get_service_stats() -> dict:
    return {
        "today": {"total": 47, "auto_resolved": 38, "escalated": 3, "avg_response_ms": 230},
        "week": {"total": 312, "auto_resolved": 264, "escalated": 18, "satisfaction": 4.6},
        "top_intents": [
            {"intent": "logistics", "count": 128, "pct": 41},
            {"intent": "pre_sale", "count": 84, "pct": 27},
            {"intent": "after_sale", "count": 62, "pct": 20},
            {"intent": "complaint", "count": 38, "pct": 12},
        ],
        "platforms": {"tiktok": 185, "amazon": 127},
    }
