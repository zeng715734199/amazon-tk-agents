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
