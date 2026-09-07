"""Multi-platform customer-service agent."""

import random
import re
import time

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def detect_language(text: str) -> str:
    """Detect Chinese with a lightweight character-ratio rule."""
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return "zh" if chinese_chars > len(text) * 0.15 else "en"
