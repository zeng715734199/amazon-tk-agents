"""TikTok 内容与直播带货智能体。"""

import random
import time
from datetime import datetime, timedelta

from llm import llm_chat
from src.mock.content_mock import HASHTAG_DB, LIVE_TEMPLATE, TRENDING_TOPICS, VIDEO_TEMPLATES


def _template_script(product_name: str, features: list[str], template: dict) -> str:
    lines = []
    for section in template["structure"]:
        lines.append(f"**{section['section']}**")
        name = section["section"].lower()
        if "hook" in name:
            lines.append(f'[Camera on package] "Wait until you see the {product_name}!"')
        elif "feature" in name or "look" in name:
            lines.extend(f'[Close-up] "{feature} — and it actually works."' for feature in features[:3])
        elif "test" in name or "pro" in name:
            feature = features[0] if features else "the headline feature"
            lines.append(f'[Demo] "See? {feature} — exactly as advertised."')
        elif "cta" in name:
            lines.append('"Tap the shop button to check it out!"')
        else:
            lines.append(f"[{section['content']}]")
        lines.append("")
    return "\n".join(lines)


async def _llm_script(product_name: str, features: list[str], template: dict, language: str) -> str:
    sections = "\n".join(f"- {item['section']}: {item['content']}" for item in template["structure"])
    prompt = f"""Write a TikTok video script for {product_name}.
Features: {', '.join(features[:4])}
Format: {template['name']} ({template['duration']})
Language: {language}

Follow this structure:
{sections}

Include spoken lines and visual directions in brackets."""
    return await llm_chat([
        {"role": "system", "content": "You create authentic TikTok product videos that drive sales."},
        {"role": "user", "content": prompt},
    ])


async def generate_video_script(
    product_name: str,
    product_features: list[str],
    format_type: str = "unboxing",
    language: str = "en",
) -> dict:
    started_at = time.perf_counter()
    template = VIDEO_TEMPLATES.get(format_type, VIDEO_TEMPLATES["unboxing"])
    steps = [{"type": "analyze", "detail": f"Format: {template['name']}, Duration: {template['duration']}"}]
    script = await _llm_script(product_name, product_features, template, language)
    if "[Demo Mode" in script or "[LLM Error" in script:
        script = _template_script(product_name, product_features, template)
        steps.append({"type": "template", "detail": "Generated from template"})
    else:
        steps.append({"type": "llm", "detail": "Generated via LLM"})

    hashtags = _select_hashtags(product_name, product_features)
    steps.append({"type": "hashtags", "detail": f"Selected {len(hashtags)} optimized hashtags"})
    trends = [item for item in TRENDING_TOPICS if item["format"] == format_type or item["relevance"] == "high"][:4]
    return {
        "script": script,
        "template": template,
        "hashtags": hashtags,
        "trending": trends,
        "format": format_type,
        "steps": steps,
        "elapsed_ms": round((time.perf_counter() - started_at) * 1000, 2),
    }


async def generate_live_script(
    product_name: str,
    product_features: list[str],
    price: float,
    promo_price: float | None = None,
) -> dict:
    started_at = time.perf_counter()
    discount = round((1 - promo_price / price) * 100) if promo_price else 0
    offer = f"today only USD {promo_price}, {discount}% off!" if promo_price else "we have a special deal!"
    sections = {
        "opening": random.choice(LIVE_TEMPLATE["opening"]),
        "product_intro": [
            random.choice(LIVE_TEMPLATE["product_intro"]),
            f"This is the {product_name}. Let me show you why I love it.",
            f"Features: {', '.join(product_features[:3])}",
            f"Normally USD {price}, but {offer}",
        ],
        "engagement_hooks": LIVE_TEMPLATE["engagement"],
        "closing": random.choice(LIVE_TEMPLATE["closing"]),
        "key_numbers": {
            "original_price": price,
            "promo_price": promo_price,
            "discount_pct": discount,
            "suggested_duration": "45-60 min",
            "products_to_show": 5,
        },
    }
    return {"sections": sections, "elapsed_ms": round((time.perf_counter() - started_at) * 1000, 2)}


async def generate_content_calendar(products: list[dict], days: int = 7) -> dict:
    calendar = []
    formats = list(VIDEO_TEMPLATES)
    base_date = datetime.now()
    for index in range(days):
        date = base_date + timedelta(days=index)
        product = products[index % len(products)] if products else {"name": "Featured Product"}
        format_key = formats[index % len(formats)]
        template = VIDEO_TEMPLATES[format_key]
        calendar.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": date.strftime("%A"),
            "product": product.get("name", "TBD"),
            "format": format_key,
            "format_name": template["name"],
            "duration": template["duration"],
            "post_time": random.choice(["10:00 AM EST", "2:00 PM EST", "6:00 PM EST", "8:00 PM EST"]),
            "hashtag_set": _select_hashtags(product.get("name", ""), product.get("features", []))[:5],
            "notes": f"Focus on {random.choice(['hook optimization', 'engagement CTA', 'product close-ups', 'lifestyle angle', 'trending sound'])}",
        })
    return {
        "calendar": calendar,
        "total_days": days,
        "formats_used": list({item["format"] for item in calendar}),
    }


def _select_hashtags(product_name: str, features: list[str]) -> list[str]:
    tags = HASHTAG_DB["general"][:3] + HASHTAG_DB["shopping"][:3]
    searchable = f"{product_name} {' '.join(features)}".lower()
    category_terms = {
        "electronics": ["earbud", "audio", "bluetooth", "lamp", "usb"],
        "fitness": ["yoga", "fitness", "workout", "exercise"],
        "home": ["home", "desk", "lamp", "decor"],
    }
    for category, terms in category_terms.items():
        if any(term in searchable for term in terms):
            tags.extend(HASHTAG_DB[category][:3])
    tags.append(f"#{product_name.replace(' ', '')}")
    return list(dict.fromkeys(tags))[:12]


def get_format_list() -> list[dict]:
    return [
        {"key": key, "name": value["name"], "duration": value["duration"], "steps": len(value["structure"])}
        for key, value in VIDEO_TEMPLATES.items()
    ]
