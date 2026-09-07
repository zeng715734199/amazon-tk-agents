"""库存、补货与需求预测链路。"""

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


def generate_restock_plan(product_key: str) -> dict:
    product = INVENTORY.get(product_key)
    if not product:
        return {"error": f"Product '{product_key}' not found"}
    velocity = SALES_VELOCITY.get(product_key, {})
    plan = {
        "product": product["name"], "sku": product["sku"], "unit_cost": product["unit_cost"],
        "moq": product["moq"], "lead_time_days": product["lead_time_days"], "orders": [],
        "total_units": 0, "total_cost": 0,
    }
    for variant, stock in product["variants"].items():
        speeds = velocity.get(variant, {"amazon": 0, "tiktok": 0})
        daily = speeds["amazon"] + speeds["tiktok"]
        current = stock["amazon_fba"] + stock["tiktok_warehouse"] + stock["in_transit"]
        target = math.ceil(daily * 60)
        gap = max(0, target - current)
        if not gap:
            continue
        quantity = math.ceil(max(gap, product["moq"]) / 50) * 50
        amazon_share = speeds["amazon"] / max(daily, 0.1)
        days = current / max(daily, 0.1)
        air = days < 20
        order = {
            "variant": variant, "current_stock": current, "in_transit": stock["in_transit"],
            "target_stock": target, "gap": gap, "order_quantity": quantity,
            "allocation": {"amazon_fba": round(quantity * amazon_share), "tiktok_warehouse": quantity - round(quantity * amazon_share)},
            "cost": round(quantity * product["unit_cost"], 2),
            "urgency": "urgent" if days < 14 else "normal",
            "ship_method": "air" if air else "sea",
            "estimated_arrival": (datetime.now() + timedelta(days=product["lead_time_days"] + (product["shipping_time_air"] if air else product["shipping_time_sea"]))).strftime("%Y-%m-%d"),
        }
        plan["orders"].append(order)
        plan["total_units"] += quantity
        plan["total_cost"] += order["cost"]
    plan["total_cost"] = round(plan["total_cost"], 2)
    return plan


def forecast_demand(product_key: str, days: int = 30) -> dict:
    velocity = SALES_VELOCITY.get(product_key, {})
    product = INVENTORY.get(product_key, {})
    if not velocity:
        return {"error": f"No velocity data for '{product_key}'"}
    base_date = datetime.now()
    forecast = []
    for variant, speeds in velocity.items():
        stock = product["variants"].get(variant, {})
        daily = speeds["amazon"] + speeds["tiktok"]
        running = stock.get("amazon_fba", 0) + stock.get("tiktok_warehouse", 0)
        stockout_date = None
        daily_forecast = []
        for offset in range(days):
            date = base_date + timedelta(days=offset)
            multiplier = 1.2 if date.weekday() in (5, 6) else 0.9 if date.weekday() == 1 else 1.0
            projected_sales = round(daily * multiplier * random.uniform(0.85, 1.15))
            running = max(0, running - projected_sales)
            if running == 0 and stockout_date is None:
                stockout_date = date.strftime("%Y-%m-%d")
            daily_forecast.append({"date": date.strftime("%Y-%m-%d"), "projected_sales": projected_sales, "projected_stock": running})
        forecast.append({
            "variant": variant, "avg_daily_velocity": daily, "current_stock": stock.get("amazon_fba", 0) + stock.get("tiktok_warehouse", 0),
            "projected_30d_sales": sum(item["projected_sales"] for item in daily_forecast),
            "stockout_date": stockout_date, "daily_forecast": daily_forecast,
        })
    return {"product": product.get("name", product_key), "forecast_days": days, "variants": forecast}


def get_supply_chain_stats() -> dict:
    overview = get_inventory_overview()
    total_units = sum(item["totals"]["total"] for item in overview["products"])
    return {
        "total_skus": sum(len(item["variants"]) for item in overview["products"]),
        "total_units": total_units,
        "total_value": overview["total_inventory_value"],
        "critical_alerts": sum(alert["severity"] == "critical" for alert in overview["alerts"]),
        "warning_alerts": sum(alert["severity"] == "warning" for alert in overview["alerts"]),
        "warehouses": {
            "amazon_fba": sum(item["totals"]["amazon_fba"] for item in overview["products"]),
            "tiktok": sum(item["totals"]["tiktok_warehouse"] for item in overview["products"]),
            "in_transit": sum(item["totals"]["in_transit"] for item in overview["products"]),
        },
    }
