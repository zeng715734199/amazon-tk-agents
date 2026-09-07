"""Product-listing generation agent."""

import random
import re
import time

from llm import llm_chat

DEMO_PRODUCTS = {
    "earbuds": {
        "name": "ProSound X1 Wireless Earbuds",
        "category": "Electronics > Audio > Earbuds",
        "features": ["Active Noise Cancellation", "40h battery life", "IPX5 waterproof", "Bluetooth 5.3", "Touch controls", "Fast charging (10min = 2h)"],
        "price": 39.99,
        "images": 8,
        "variants": ["Black", "White", "Navy Blue"],
    },
    "yoga_mat": {
        "name": "ZenFlex Premium Yoga Mat",
        "category": "Sports > Yoga > Mats",
        "features": ["6mm thick TPE material", "Non-slip dual texture", "72x24 inch", "Eco-friendly", "Carrying strap included", "Alignment lines"],
        "price": 29.99,
        "images": 6,
        "variants": ["Purple", "Teal", "Grey", "Pink"],
    },
    "desk_lamp": {
        "name": "LumiPro Smart Desk Lamp",
        "category": "Home > Lighting > Desk Lamps",
        "features": ["5 color temperatures", "10 brightness levels", "USB-C charging port", "Memory function", "Eye-care LED", "Touch control", "Timer 30/60min"],
        "price": 34.99,
        "images": 7,
        "variants": ["White", "Black", "Silver"],
    },
}

CATEGORY_KEYWORDS = {
    "Electronics > Audio > Earbuds": {
        "primary": ["wireless earbuds", "bluetooth earbuds", "noise cancelling earbuds", "earbuds with microphone"],
        "secondary": ["workout earbuds", "waterproof earbuds", "long battery earbuds", "earbuds for iphone", "earbuds for android"],
        "backend": ["wireless headphones", "TWS earphones", "in-ear headphones", "sport earbuds", "gym earbuds"],
    },
    "Sports > Yoga > Mats": {
        "primary": ["yoga mat", "exercise mat", "non slip yoga mat", "thick yoga mat"],
        "secondary": ["yoga mat for women", "pilates mat", "workout mat", "gym mat", "eco friendly yoga mat"],
        "backend": ["fitness mat", "stretching mat", "floor exercise mat", "TPE yoga mat"],
    },
    "Home > Lighting > Desk Lamps": {
        "primary": ["desk lamp", "LED desk lamp", "desk lamp for office", "study lamp"],
        "secondary": ["desk lamp with USB port", "eye care desk lamp", "touch desk lamp", "dimmable desk lamp"],
        "backend": ["table lamp", "reading lamp", "task lamp", "computer desk lamp"],
    },
}


def _template_listing(product: dict, keywords: dict, platform: str, language: str) -> dict:
    name = product["name"]
    features = product["features"]
    primary = keywords["primary"]
    if platform == "amazon":
        title = f"{name} — {features[0]}, {features[1]}, {primary[0].title()} for {primary[-1].split()[-1].title()}"
        bullets = [f"【{feature.split()[0].upper()}】{feature} — Designed for performance and comfort." for feature in features[:5]]
        description = (
            f"{name} combines modern technology with premium build quality. "
            f"Featuring {features[0].lower()} and {features[1].lower()}, it delivers "
            "exceptional value for everyday use, travel, and work."
        )
    else:
        title = f"✨ {name} | {features[0]} | Must-Have!"
        bullets = [f"✅ {feature}" for feature in features[:5]]
        hashtags = " | ".join(f"#{keyword.replace(' ', '')}" for keyword in primary[:5])
        description = f"Meet the {name}! {features[0]} + {features[1]} = your new favorite.\n\n{hashtags}"

    listing = {
        "from_llm": False,
        "title": title,
        "description": description,
        "backend_keywords": ", ".join(keywords["backend"]),
    }
    listing.update({f"bullet{index}": bullets[index - 1] if index <= len(bullets) else "" for index in range(1, 6)})
    return listing
