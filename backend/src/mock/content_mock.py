"""短视频趋势、标签与脚本模板演示数据。"""

TRENDING_TOPICS = [
    {"topic": "Unboxing Haul", "views": "2.3B", "growth": "+15%", "relevance": "high", "format": "unboxing"},
    {"topic": "TikTok Made Me Buy It", "views": "48B", "growth": "+8%", "relevance": "high", "format": "review"},
    {"topic": "Amazon Finds", "views": "12B", "growth": "+22%", "relevance": "high", "format": "haul"},
    {"topic": "Side-by-Side Comparison", "views": "890M", "growth": "+35%", "relevance": "medium", "format": "comparison"},
    {"topic": "Day in My Life + Product", "views": "5.6B", "growth": "+5%", "relevance": "medium", "format": "lifestyle"},
    {"topic": "POV: When your order arrives", "views": "1.2B", "growth": "+42%", "relevance": "high", "format": "skit"},
]

CALENDAR_PRODUCTS = [
    {"name": "ProSound X1 Earbuds", "features": ["ANC", "40h battery"]},
    {"name": "ZenFlex Yoga Mat", "features": ["Non-slip", "6mm thick"]},
    {"name": "LumiPro Desk Lamp", "features": ["5 color temps", "USB-C"]},
]

HASHTAG_DB = {
    "general": ["#fyp", "#foryou", "#foryoupage", "#viral", "#trending"],
    "shopping": ["#TikTokMadeMeBuyIt", "#TikTokShop", "#TikTokFinds", "#OnlineShopping", "#ShopWithMe"],
    "electronics": ["#TechTok", "#GadgetReview", "#TechFinds", "#WirelessEarbuds", "#SmartHome"],
    "fitness": ["#FitTok", "#WorkoutEssentials", "#YogaLife", "#HomeGym", "#FitnessFinds"],
    "home": ["#HomeTok", "#HomeDecor", "#DeskSetup", "#RoomMakeover", "#AestheticRoom"],
}

VIDEO_TEMPLATES = {
    "unboxing": {
        "name": "Unboxing / First Impressions",
        "duration": "30-60s",
        "structure": [
            {"section": "Hook (0-3s)", "content": "Show package arriving"},
            {"section": "Unboxing (3-15s)", "content": "Open package and show contents"},
            {"section": "First Look (15-35s)", "content": "Highlight key features"},
            {"section": "Quick Test (35-50s)", "content": "Show the product working"},
            {"section": "CTA (50-60s)", "content": "Invite viewers to tap the shop button"},
        ],
    },
    "review": {
        "name": "Honest Review",
        "duration": "45-90s",
        "structure": [
            {"section": "Hook (0-3s)", "content": "Promise an honest verdict"},
            {"section": "Context (3-10s)", "content": "Explain expectations"},
            {"section": "Pros (10-30s)", "content": "Show three benefits"},
            {"section": "Cons (30-40s)", "content": "Mention honest drawbacks"},
            {"section": "Verdict (40-55s)", "content": "Give a clear rating"},
            {"section": "CTA (55-60s)", "content": "Ask viewers to save or follow"},
        ],
    },
    "comparison": {
        "name": "Side-by-Side Comparison",
        "duration": "45-60s",
        "structure": [
            {"section": "Hook (0-3s)", "content": "Ask whether the upgrade is worthwhile"},
            {"section": "Visual Compare (3-20s)", "content": "Show both products"},
            {"section": "Feature Battle (20-40s)", "content": "Test key features"},
            {"section": "Winner (40-50s)", "content": "Give the verdict"},
            {"section": "CTA (50-60s)", "content": "Ask viewers to choose"},
        ],
    },
    "lifestyle": {
        "name": "Lifestyle Integration",
        "duration": "30-45s",
        "structure": [
            {"section": "Scene Set (0-5s)", "content": "Show a daily routine"},
            {"section": "Problem (5-12s)", "content": "Present a relatable need"},
            {"section": "Product Reveal (12-25s)", "content": "Introduce the product"},
            {"section": "Result (25-38s)", "content": "Show the improvement"},
            {"section": "CTA (38-45s)", "content": "Invite viewers to shop"},
        ],
    },
}

LIVE_TEMPLATE = {
    "opening": ["Hey everyone! Welcome to our live! 👋", "We've got amazing deals today! 🎉", "Drop a ❤️ if you can hear me!"],
    "product_intro": ["Let me show you our bestseller.", "This is what everyone has been asking about.", "Let me show you why this is worth it."],
    "engagement": ["Type YES if you want this!", "Tag a friend who'd love this!", "Comment your size or color!", "Flash deal for 60 seconds! ⏰"],
    "closing": ["Thank you for watching!", "Your cart discount expires soon!", "See you next time! 💕"],
}
