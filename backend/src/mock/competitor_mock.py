"""竞品跟踪与自有商品演示数据。"""

TRACKED_COMPETITORS = {
    "earbuds": [
        {"asin": "B09JNK4YPF", "name": "SoundCore A40 Earbuds", "brand": "Anker", "platform": "amazon", "price_history": [39.99, 39.99, 35.99, 35.99, 33.99, 33.99, 36.99], "current_price": 36.99, "rating": 4.5, "reviews": 42350, "bsr": 156, "bsr_history": [180, 165, 156, 148, 160, 155, 156]},
        {"asin": "B0C8DL3HSR", "name": "JBL Tune Buds", "brand": "JBL", "platform": "amazon", "price_history": [49.99, 49.99, 44.99, 44.99, 44.99, 42.99, 44.99], "current_price": 44.99, "rating": 4.3, "reviews": 18920, "bsr": 289, "bsr_history": [310, 295, 289, 280, 275, 290, 289]},
        {"asin": "B0D123FAKE", "name": "BassKing Pro ANC", "brand": "BassKing", "platform": "tiktok", "price_history": [29.99, 29.99, 24.99, 22.99, 22.99, 25.99, 27.99], "current_price": 27.99, "rating": 4.1, "reviews": 3250, "bsr": None, "tiktok_sales_30d": 8500},
    ],
    "yoga_mat": [
        {"asin": "B01LP0U5X0", "name": "BalanceFrom GoYoga Mat", "brand": "BalanceFrom", "platform": "amazon", "price_history": [19.99, 19.99, 18.49, 17.99, 18.49, 19.99, 19.99], "current_price": 19.99, "rating": 4.5, "reviews": 98200, "bsr": 42, "bsr_history": [45, 43, 42, 40, 38, 42, 42]},
        {"asin": "B074DZ1YQZ", "name": "Manduka PRO Yoga Mat", "brand": "Manduka", "platform": "amazon", "price_history": [92.00, 92.00, 88.00, 85.00, 85.00, 88.00, 92.00], "current_price": 92.00, "rating": 4.7, "reviews": 12400, "bsr": 180, "bsr_history": [190, 185, 180, 175, 180, 185, 180]},
    ],
    "desk_lamp": [
        {"asin": "B08DKQ1ZSP", "name": "BenQ ScreenBar", "brand": "BenQ", "platform": "amazon", "price_history": [109.00, 109.00, 99.00, 99.00, 109.00, 109.00, 109.00], "current_price": 109.00, "rating": 4.6, "reviews": 15600, "bsr": 320, "bsr_history": [340, 330, 320, 315, 325, 330, 320]},
        {"asin": "B08FXJDK6L", "name": "TaoTronics LED Desk Lamp", "brand": "TaoTronics", "platform": "amazon", "price_history": [29.99, 27.99, 25.99, 25.99, 27.99, 29.99, 29.99], "current_price": 29.99, "rating": 4.4, "reviews": 28900, "bsr": 210, "bsr_history": [220, 215, 210, 208, 212, 215, 210]},
    ],
}

OUR_PRODUCTS = {
    "earbuds": {"name": "ProSound X1", "price": 39.99, "cost": 12.50, "min_price": 28.99, "rating": 4.4, "reviews": 1250, "bsr": 420, "monthly_sales": 1800},
    "yoga_mat": {"name": "ZenFlex Premium", "price": 29.99, "cost": 8.20, "min_price": 19.99, "rating": 4.3, "reviews": 680, "bsr": 380, "monthly_sales": 950},
    "desk_lamp": {"name": "LumiPro Smart", "price": 34.99, "cost": 11.80, "min_price": 24.99, "rating": 4.5, "reviews": 420, "bsr": 550, "monthly_sales": 620},
}
