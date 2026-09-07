"""客服知识库、意图规则与订单演示数据。"""

INTENT_KEYWORDS = {
    "pre_sale": ["price", "size", "color", "available", "stock", "discount", "coupon", "how much", "difference", "recommend", "material", "什么", "多少", "颜色", "尺码", "有货"],
    "after_sale": ["return", "refund", "exchange", "cancel", "warranty", "repair", "退货", "退款", "换货", "取消"],
    "logistics": ["shipping", "delivery", "track", "where", "when arrive", "customs", "物流", "发货", "到了", "快递"],
    "complaint": ["damaged", "broken", "wrong", "bad", "terrible", "never", "scam", "fake", "差", "坏了", "投诉", "骗"],
}

ESCALATION_KEYWORDS = [
    "lawyer", "legal", "sue", "report", "bbb", "fraud", "scam",
    "fda", "government", "律师", "投诉", "举报", "消协",
]

KB_ENTRIES = [
    {"q": "shipping time delivery how long", "a": "Standard shipping takes 7-15 business days. Express shipping takes 3-7 business days. You can track your order using the tracking number in your order confirmation email.", "category": "logistics"},
    {"q": "return refund policy exchange", "a": "We offer a 30-day return policy. Items must be unused and in original packaging. To initiate a return, go to your order page and click 'Request Return'. Refunds are processed within 5-7 business days after we receive the item.", "category": "after_sale"},
    {"q": "order status where track package", "a": "You can track your order from My Orders, with the tracking number in your email, or by contacting us with your order number.", "category": "logistics"},
    {"q": "size chart measurement guide fit", "a": "Please refer to the size chart on each product page. If you're between sizes, we suggest sizing up.", "category": "pre_sale"},
    {"q": "payment method credit card paypal", "a": "We accept Visa, MasterCard, AmEx, PayPal, Apple Pay, and Google Pay.", "category": "pre_sale"},
    {"q": "discount coupon code promotion sale", "a": "Check our store page for promotions and apply coupon codes at checkout.", "category": "pre_sale"},
    {"q": "damaged broken defective quality", "a": "Please send photos of the damage and your order number. We'll arrange a replacement or refund.", "category": "complaint"},
    {"q": "cancel order change modify", "a": "Orders can be cancelled within two hours of placement. Shipped orders must use the return process.", "category": "after_sale"},
    {"q": "customs tax duty import", "a": "Import duties and taxes may apply according to your country's regulations.", "category": "logistics"},
    {"q": "bulk wholesale order business", "a": "We offer wholesale pricing for orders of 50 units or more.", "category": "pre_sale"},
    {"q": "warranty guarantee repair", "a": "All products include a one-year manufacturer warranty for defects.", "category": "after_sale"},
    {"q": "not received missing lost package", "a": "Check tracking and nearby delivery locations first. Confirmed lost packages qualify for replacement or refund.", "category": "complaint"},
]

DEMO_ORDERS = {
    "ORD-20250301-001": {"status": "delivered", "items": ["Wireless Earbuds Pro"], "tracking": "UPS1Z999AA10123456784", "shipped_date": "2025-03-03", "delivered_date": "2025-03-10", "platform": "amazon"},
    "ORD-20250305-002": {"status": "in_transit", "items": ["Phone Case Ultra Slim", "Screen Protector 2-Pack"], "tracking": "USPS9400111899223100001", "shipped_date": "2025-03-07", "estimated_delivery": "2025-03-18", "platform": "tiktok"},
    "ORD-20250310-003": {"status": "processing", "items": ["LED Desk Lamp Smart"], "tracking": None, "estimated_ship": "2025-03-12", "platform": "amazon"},
    "ORD-20250312-004": {"status": "returned", "items": ["Yoga Mat Premium"], "tracking": "UPS1Z999AA10123456799", "return_reason": "Wrong size", "refund_status": "processed", "platform": "tiktok"},
}
