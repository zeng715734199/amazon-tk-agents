"""Competitor monitoring and dynamic-pricing agent."""

import time
from datetime import datetime

import httpx

from config import SERPER_API_KEY
from src.mock.competitor_mock import OUR_PRODUCTS, TRACKED_COMPETITORS


async def get_market_overview(product_key: str) -> dict:
    started_at = time.perf_counter()
    competitors = TRACKED_COMPETITORS.get(product_key, [])
    product = OUR_PRODUCTS.get(product_key, {})
    if not competitors:
        return {"error": f"No tracked competitors for '{product_key}'"}

    prices = [item["current_price"] for item in competitors]
    raw_score = 100 - (product["price"] - min(prices)) / (max(prices) - min(prices) + 0.01) * 100
    analysis = {
        "our_price": product["price"],
        "market_avg": round(sum(prices) / len(prices), 2),
        "market_min": min(prices),
        "market_max": max(prices),
        "our_position": "above_avg" if product["price"] > sum(prices) / len(prices) else "below_avg",
        "price_competitiveness": round(max(0, min(100, raw_score))),
    }

    alerts = []
    for competitor in competitors:
        history = competitor["price_history"]
        if len(history) >= 2 and history[-1] != history[-2]:
            change = history[-1] - history[-2]
            percent = round(change / history[-2] * 100, 1)
            alerts.append({
                "type": "price_change",
                "severity": "high" if abs(percent) > 10 else "medium",
                "competitor": competitor["name"],
                "detail": f"Price {'dropped' if change < 0 else 'increased'} by USD {abs(change):.2f} ({percent:+.1f}%)",
                "old_price": history[-2],
                "new_price": history[-1],
            })
        bsr_history = competitor.get("bsr_history")
        if bsr_history and len(bsr_history) >= 3:
            trend = bsr_history[-1] - bsr_history[-3]
            if abs(trend) > 20:
                alerts.append({
                    "type": "bsr_change",
                    "severity": "medium",
                    "competitor": competitor["name"],
                    "detail": f"BSR {'improved' if trend < 0 else 'declined'} by {abs(trend)} positions (7d)",
                })

    return {
        "product": product,
        "competitors": competitors,
        "price_analysis": analysis,
        "alerts": alerts,
        "recommendation": _pricing_recommendation(product, competitors, analysis),
        "elapsed_ms": round((time.perf_counter() - started_at) * 1000, 2),
    }


async def search_competitor_live(query: str) -> dict:
    if not SERPER_API_KEY:
        return {"results": [], "note": "Configure SERPER_API_KEY for live search"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
                json={"q": query, "num": 5},
                timeout=10,
            )
            response.raise_for_status()
            results = [
                {"title": item.get("title", ""), "url": item.get("link", ""), "snippet": item.get("snippet", "")}
                for item in response.json().get("organic", [])[:5]
            ]
            return {"results": results}
    except Exception as exc:
        return {"results": [], "error": str(exc)}


def _pricing_recommendation(product: dict, competitors: list[dict], analysis: dict) -> dict:
    cheapest = min(competitors, key=lambda item: item["current_price"])
    current_margin = round((product["price"] - product["cost"]) / product["price"] * 100, 1)
    minimum_margin = round((product["min_price"] - product["cost"]) / product["min_price"] * 100, 1)
    recommendation = {
        "current_margin": current_margin,
        "min_margin": minimum_margin,
        "action": "hold",
        "suggested_price": product["price"],
        "reasoning": "Current pricing is competitive.",
    }
    if product["price"] > cheapest["current_price"] * 1.3:
        suggested = round(cheapest["current_price"] * 1.15, 2)
        if suggested >= product["min_price"]:
            recommendation.update(action="reduce", suggested_price=suggested, reasoning="Reduce the market price gap while preserving margin.")
        else:
            recommendation.update(action="differentiate", reasoning="The margin floor prevents a competitive price reduction.")
    elif product["price"] < cheapest["current_price"] * 0.9:
        recommendation.update(
            action="increase",
            suggested_price=round(cheapest["current_price"] * 0.95, 2),
            reasoning="Increase price while remaining below the cheapest competitor.",
        )
    suggested = recommendation["suggested_price"]
    recommendation["projected_margin"] = round((suggested - product["cost"]) / suggested * 100, 1)
    return recommendation


async def generate_daily_briefing() -> dict:
    started_at = time.perf_counter()
    briefing = {"date": datetime.now().strftime("%Y-%m-%d"), "sections": []}
    for product_key in OUR_PRODUCTS:
        overview = await get_market_overview(product_key)
        if "error" in overview:
            continue
        briefing["sections"].append({
            "product": overview["product"]["name"],
            "our_price": overview["product"]["price"],
            "market_avg": overview["price_analysis"]["market_avg"],
            "alerts": overview["alerts"],
            "recommendation": overview["recommendation"],
            "competitors_count": len(overview["competitors"]),
        })
    briefing["elapsed_ms"] = round((time.perf_counter() - started_at) * 1000, 2)
    briefing["summary"] = f"Monitoring {sum(len(items) for items in TRACKED_COMPETITORS.values())} competitors across {len(OUR_PRODUCTS)} categories."
    return briefing


def get_tracked_products() -> list[dict]:
    return [{"key": key, **product} for key, product in OUR_PRODUCTS.items()]
