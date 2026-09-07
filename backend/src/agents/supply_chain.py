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


def get_inventory_overview() -> dict:
    overview = []
    total_value = 0
    alerts = []
    for product_key, product in INVENTORY.items():
        velocity = SALES_VELOCITY.get(product_key, {})
        product_data = {
            "key": product_key,
            "sku": product["sku"],
            "name": product["name"],
            "unit_cost": product["unit_cost"],
            "variants": [],
            "totals": {"amazon_fba": 0, "tiktok_warehouse": 0, "in_transit": 0, "total": 0},
        }
        for variant, stock in product["variants"].items():
            speeds = velocity.get(variant, {"amazon": 0, "tiktok": 0})
            daily = speeds["amazon"] + speeds["tiktok"]
            total_stock = stock["amazon_fba"] + stock["tiktok_warehouse"]
            days = round(total_stock / max(daily, 0.1))
            variant_data = {
                "variant": variant, **stock,
                "daily_velocity": daily,
                "amazon_velocity": speeds["amazon"],
                "tiktok_velocity": speeds["tiktok"],
                "days_of_stock": days,
                "amazon_days": round(stock["amazon_fba"] / max(speeds["amazon"], 0.1)),
                "tiktok_days": round(stock["tiktok_warehouse"] / max(speeds["tiktok"], 0.1)),
                "status": "critical" if days < 14 else "warning" if days < 30 else "healthy",
            }
            product_data["variants"].append(variant_data)
            for key in ["amazon_fba", "tiktok_warehouse", "in_transit"]:
                product_data["totals"][key] += stock[key]
            product_data["totals"]["total"] += total_stock + stock["in_transit"]
            total_value += (total_stock + stock["in_transit"]) * product["unit_cost"]
            if days < 14:
                alerts.append({"severity": "critical", "product": product["name"], "variant": variant, "message": f"Only {days} days of stock remaining ({total_stock} units). Immediate restock needed!"})
            elif days < 30:
                alerts.append({"severity": "warning", "product": product["name"], "variant": variant, "message": f"{days} days of stock remaining. Plan restock soon."})
            if variant_data["amazon_days"] < 10 and stock["in_transit"] == 0:
                alerts.append({"severity": "critical", "product": product["name"], "variant": variant, "message": "Amazon FBA stock critically low and no inbound shipment found."})
        overview.append(product_data)
    return {
        "products": overview,
        "total_inventory_value": round(total_value, 2),
        "alerts": sorted(alerts, key=lambda item: 0 if item["severity"] == "critical" else 1),
    }
