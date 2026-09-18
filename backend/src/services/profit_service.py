"""跨平台利润分析服务。"""

from src.mock.platform_mock import PROFIT_BASE_ROWS, PROFIT_PERIOD_FACTORS, PROFIT_TREND


def get_profit_report(period: str) -> dict:
    """按周期返回损益、摘要、平台对比和趋势。"""
    factor = PROFIT_PERIOD_FACTORS[period]
    rows = [
        {
            **row,
            "amazon": round(row["amazon"] * factor),
            "tiktok": round(row["tiktok"] * factor),
            "total": round((row["amazon"] + row["tiktok"]) * factor),
        }
        for row in PROFIT_BASE_ROWS
    ]
    revenue = rows[0]["total"]
    net_profit = rows[-1]["total"]
    direct_costs = abs(rows[1]["total"] + rows[2]["total"])
    return {
        "period": period,
        "summary": {
            "revenue": revenue,
            "gross_profit": revenue - direct_costs,
            "net_profit": net_profit,
            "net_margin": round(net_profit / revenue * 100, 1),
        },
        "pnl_rows": rows,
        "platform_comparison": [
            {
                "metric": "销售收入",
                "amazon": rows[0]["amazon"],
                "tiktok": rows[0]["tiktok"],
            },
            {
                "metric": "毛利润",
                "amazon": rows[0]["amazon"] + rows[1]["amazon"] + rows[2]["amazon"],
                "tiktok": rows[0]["tiktok"] + rows[1]["tiktok"] + rows[2]["tiktok"],
            },
            {
                "metric": "净利润",
                "amazon": rows[-1]["amazon"],
                "tiktok": rows[-1]["tiktok"],
            },
        ],
        "trend": PROFIT_TREND,
    }
