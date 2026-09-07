"""Inventory, replenishment, and demand-forecasting agent."""

import math
import random
from datetime import datetime, timedelta

INVENTORY = {
    "earbuds": {
        "sku": "PS-X1-BLK", "name": "ProSound X1 Wireless Earbuds",
        "variants": {
            "Black": {"amazon_fba": 450, "amazon_fbm": 0, "tiktok_warehouse": 180, "in_transit": 500, "supplier_stock": 5000},
            "White": {"amazon_fba": 280, "amazon_fbm": 0, "tiktok_warehouse": 120, "in_transit": 300, "supplier_stock": 5000},
            "Navy": {"amazon_fba": 180, "amazon_fbm": 0, "tiktok_warehouse": 60, "in_transit": 0, "supplier_stock": 5000},
        },
        "unit_cost": 12.50, "moq": 500, "lead_time_days": 21, "shipping_time_sea": 25, "shipping_time_air": 7,
    },
    "yoga_mat": {
        "sku": "ZF-PM-PRP", "name": "ZenFlex Premium Yoga Mat",
        "variants": {
            "Purple": {"amazon_fba": 320, "amazon_fbm": 50, "tiktok_warehouse": 150, "in_transit": 200, "supplier_stock": 3000},
            "Teal": {"amazon_fba": 180, "amazon_fbm": 30, "tiktok_warehouse": 80, "in_transit": 0, "supplier_stock": 3000},
            "Grey": {"amazon_fba": 95, "amazon_fbm": 20, "tiktok_warehouse": 40, "in_transit": 0, "supplier_stock": 3000},
            "Pink": {"amazon_fba": 210, "amazon_fbm": 0, "tiktok_warehouse": 110, "in_transit": 150, "supplier_stock": 3000},
        },
        "unit_cost": 8.20, "moq": 300, "lead_time_days": 18, "shipping_time_sea": 25, "shipping_time_air": 7,
    },
    "desk_lamp": {
        "sku": "LP-SM-WHT", "name": "LumiPro Smart Desk Lamp",
        "variants": {
            "White": {"amazon_fba": 150, "amazon_fbm": 0, "tiktok_warehouse": 80, "in_transit": 0, "supplier_stock": 2000},
            "Black": {"amazon_fba": 120, "amazon_fbm": 0, "tiktok_warehouse": 60, "in_transit": 0, "supplier_stock": 2000},
            "Silver": {"amazon_fba": 45, "amazon_fbm": 0, "tiktok_warehouse": 25, "in_transit": 0, "supplier_stock": 2000},
        },
        "unit_cost": 11.80, "moq": 200, "lead_time_days": 25, "shipping_time_sea": 28, "shipping_time_air": 8,
    },
}

SALES_VELOCITY = {
    "earbuds": {"Black": {"amazon": 18, "tiktok": 12}, "White": {"amazon": 12, "tiktok": 8}, "Navy": {"amazon": 6, "tiktok": 3}},
    "yoga_mat": {"Purple": {"amazon": 8, "tiktok": 6}, "Teal": {"amazon": 5, "tiktok": 3}, "Grey": {"amazon": 3, "tiktok": 2}, "Pink": {"amazon": 7, "tiktok": 5}},
    "desk_lamp": {"White": {"amazon": 5, "tiktok": 3}, "Black": {"amazon": 4, "tiktok": 2}, "Silver": {"amazon": 2, "tiktok": 1}},
}
