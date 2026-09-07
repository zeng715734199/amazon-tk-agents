"""商品 Listing 与关键词演示数据。"""

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
