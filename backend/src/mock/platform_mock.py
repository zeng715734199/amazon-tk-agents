"""平台总览与利润分析演示数据。"""

DASHBOARD_SALES_TREND = [
    {"label": "周一", "amazon": 142, "tiktok": 96},
    {"label": "周二", "amazon": 158, "tiktok": 108},
    {"label": "周三", "amazon": 151, "tiktok": 121},
    {"label": "周四", "amazon": 176, "tiktok": 118},
    {"label": "周五", "amazon": 183, "tiktok": 143},
    {"label": "周六", "amazon": 214, "tiktok": 177},
    {"label": "周日", "amazon": 226, "tiktok": 189},
]

PROFIT_BASE_ROWS = [
    {"item": "销售收入", "amazon": 84260, "tiktok": 51740, "highlight": True},
    {"item": "商品成本", "amazon": -26780, "tiktok": -15820},
    {"item": "平台佣金", "amazon": -12639, "tiktok": -4140},
    {"item": "广告费用", "amazon": -8940, "tiktok": -7230},
    {"item": "仓储与物流", "amazon": -6740, "tiktok": -4850},
    {"item": "退款与售后", "amazon": -2180, "tiktok": -1640},
    {"item": "净利润", "amazon": 26981, "tiktok": 18060, "highlight": True},
]

PROFIT_PERIOD_FACTORS = {"30d": 1, "90d": 2.82, "year": 10.6}

PROFIT_TREND = [
    {"label": f"第 {index + 1} 周", "revenue": revenue, "net_profit": net_profit}
    for index, (revenue, net_profit) in enumerate(zip(
        [25100, 26800, 27400, 29100, 28600, 31200, 32900, 34100, 35800, 37600, 39100, 41800],
        [7200, 7900, 8100, 8400, 8200, 9100, 9800, 10200, 10800, 11400, 11900, 12600],
    ))
]
