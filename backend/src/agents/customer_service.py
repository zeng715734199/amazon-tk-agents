"""Multi-platform customer-service agent."""

import random
import re
import time

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

INTENT_KEYWORDS = {
    "pre_sale": ["price", "size", "color", "available", "stock", "discount", "coupon", "how much", "difference", "recommend", "material", "什么", "多少", "颜色", "尺码", "有货"],
    "after_sale": ["return", "refund", "exchange", "cancel", "warranty", "repair", "退货", "退款", "换货", "取消"],
    "logistics": ["shipping", "delivery", "track", "where", "when arrive", "customs", "物流", "发货", "到了", "快递"],
    "complaint": ["damaged", "broken", "wrong", "bad", "terrible", "never", "scam", "fake", "差", "坏了", "投诉", "骗"],
}
ESCALATION_KEYWORDS = [
    "lawyer", "legal", "sue", "report", "bbb", "fraud", "scam",
    "fda", "government", "律师", "投诉", "举报", "消协",
]
KB_ENTRIES = [
    {"q": "shipping time delivery how long", "a": "Standard shipping takes 7-15 business days. Express shipping takes 3-7 business days. You can track your order using the tracking number in your order confirmation email.", "category": "logistics"},
    {"q": "return refund policy exchange", "a": "We offer a 30-day return policy. Items must be unused and in original packaging. To initiate a return, go to your order page and click 'Request Return'. Refunds are processed within 5-7 business days after we receive the item.", "category": "after_sale"},
    {"q": "order status where track package", "a": "You can track your order from My Orders, with the tracking number in your email, or by contacting us with your order number.", "category": "logistics"},
    {"q": "size chart measurement guide fit", "a": "Please refer to the size chart on each product page. If you're between sizes, we suggest sizing up.", "category": "pre_sale"},
    {"q": "payment method credit card paypal", "a": "We accept Visa, MasterCard, AmEx, PayPal, Apple Pay, and Google Pay.", "category": "pre_sale"},
    {"q": "discount coupon code promotion sale", "a": "Check our store page for promotions and apply coupon codes at checkout.", "category": "pre_sale"},
    {"q": "damaged broken defective quality", "a": "Please send photos of the damage and your order number. We'll arrange a replacement or refund.", "category": "complaint"},
    {"q": "cancel order change modify", "a": "Orders can be cancelled within two hours of placement. Shipped orders must use the return process.", "category": "after_sale"},
    {"q": "customs tax duty import", "a": "Import duties and taxes may apply according to your country's regulations.", "category": "logistics"},
    {"q": "bulk wholesale order business", "a": "We offer wholesale pricing for orders of 50 units or more.", "category": "pre_sale"},
    {"q": "warranty guarantee repair", "a": "All products include a one-year manufacturer warranty for defects.", "category": "after_sale"},
    {"q": "not received missing lost package", "a": "Check tracking and nearby delivery locations first. Confirmed lost packages qualify for replacement or refund.", "category": "complaint"},
]

_kb_texts = [f"{entry['q']} {entry['a']}" for entry in KB_ENTRIES]
_kb_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
_kb_matrix = _kb_vectorizer.fit_transform(_kb_texts)


def detect_language(text: str) -> str:
    """Detect Chinese with a lightweight character-ratio rule."""
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
