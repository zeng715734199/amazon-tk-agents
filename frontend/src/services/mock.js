const products = [
  { key: 'earbuds', name: 'ProSound X1 Wireless Earbuds', price: 39.99, sku: 'PS-X1-BLK', unit_cost: 12.5 },
  { key: 'yoga_mat', name: 'ZenFlex Premium Yoga Mat', price: 29.99, sku: 'ZF-PM-PRP', unit_cost: 8.2 },
  { key: 'desk_lamp', name: 'LumiPro Smart Desk Lamp', price: 34.99, sku: 'LP-SM-WHT', unit_cost: 11.8 },
]

const inventory = products.map((product, index) => ({
  ...product,
  variants: (index === 0 ? [['Black', 450, 180], ['White', 280, 120], ['Navy', 180, 60]]
    : index === 1 ? [['Purple', 320, 150], ['Teal', 180, 80], ['Grey', 95, 40], ['Pink', 210, 110]]
      : [['White', 150, 80], ['Black', 120, 60], ['Silver', 45, 25]])
    .map(([variant, amazon_fba, tiktok_warehouse]) => ({
      variant,
      amazon_fba,
      tiktok_warehouse,
      in_transit: variant === 'Black' ? 300 : 0,
      daily_velocity: index + 5,
      days_of_stock: Math.round((amazon_fba + tiktok_warehouse) / (index + 5)),
      status: amazon_fba < 100 ? 'critical' : amazon_fba < 220 ? 'warning' : 'healthy',
    })),
}))

const clone = value => JSON.parse(JSON.stringify(value))
const resolve = value => Promise.resolve(clone(value))
const dateAfter = offset => {
  const date = new Date('2026-09-18T00:00:00Z')
  date.setUTCDate(date.getUTCDate() + offset)
  return date.toISOString().slice(0, 10)
}
const connectionState = { llm: false, amazon: false, tiktok: false, serper: false, erp: false, webhook: false }
const notificationEvents = [
  { type: 'order', icon: '🛒', title: '新订单', message: 'ProSound X1 Wireless Earbuds - Amazon' },
  { type: 'inventory', icon: '📦', title: '库存预警', message: 'LumiPro Smart Desk Lamp Silver 款 FBA 库存低于安全线' },
  { type: 'competitor', icon: '💰', title: '竞品价格变动', message: 'SoundCore A40 Earbuds 当前价格 $33.99' },
  { type: 'review', icon: '⭐', title: '新评论', message: 'ZenFlex Premium Yoga Mat 收到 5 星评价' },
]
let notificationIndex = 0

const customerConfig = {
  welcome_message: '您好，我是 AgentHub 智能客服。请选择快捷问题或直接输入消息。',
  quick_replies: ['我的订单 ORD-20250305-002 到哪了？', '收到的商品有损坏，我想退货', '有哪些尺码可选？', '你们支持批发价格吗？'],
}

const listingProducts = products.map(item => ({ ...item, feature_count: 6 }))
const contentConfig = {
  defaults: {
    product_name: 'ProSound X1 Earbuds',
    features: ['主动降噪', '40 小时续航', 'IPX5 防水'],
    format_type: 'unboxing',
    language: 'zh',
    price: 39.99,
    promo_price: 29.99,
  },
  trending_hashtags: ['#TikTokMadeMeBuyIt', '#Unboxing', '#ProductReview', '#LifeHack', '#TikTokShop'],
}
const contentFormats = [
  { key: 'unboxing', name: 'Unboxing / First Impressions', duration: '30-60s', steps: 5 },
  { key: 'review', name: 'Honest Review', duration: '45-90s', steps: 6 },
  { key: 'comparison', name: 'Side-by-Side Comparison', duration: '45-60s', steps: 5 },
  { key: 'lifestyle', name: 'Lifestyle Integration', duration: '30-45s', steps: 5 },
]

function dashboard() {
  return {
    customer_service: {
      today: { total: 47, auto_resolved: 38, escalated: 3, avg_response_ms: 230 },
      top_intents: [
        { intent: 'logistics', count: 128, pct: 41 },
        { intent: 'pre_sale', count: 84, pct: 27 },
        { intent: 'after_sale', count: 62, pct: 20 },
        { intent: 'complaint', count: 38, pct: 12 },
      ],
    },
    supply_chain: { total_skus: 10, total_units: 2240, total_value: 38420, critical_alerts: 1, warning_alerts: 3, warehouses: { amazon_fba: 1580, tiktok: 510, in_transit: 150 } },
    inventory_alerts: [{ severity: 'critical', product: 'LumiPro Smart Desk Lamp', variant: 'Silver', message: '库存不足，建议立即补货' }],
    competitor_briefing: { sections: [{ product: 'ProSound X1', our_price: 39.99, market_avg: 36.99, competitors_count: 3, recommendation: { action: 'hold', suggested_price: 39.99 } }] },
    connections: connectionState,
    sales_trend: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'].map((label, index) => ({ label, amazon: [142, 158, 151, 176, 183, 214, 226][index], tiktok: [96, 108, 121, 118, 143, 177, 189][index] })),
  }
}

function listingResult(payload) {
  const product = listingProducts.find(item => item.key === payload.product_key) || listingProducts[0]
  return {
    product,
    platform: payload.platform,
    language: payload.language,
    listing: {
      title: `${product.name} - Premium Wireless Performance for Everyday Use`,
      description: `Experience reliable performance with the ${product.name}. Designed for comfort, durability, and simple everyday use.`,
      backend_keywords: 'wireless audio premium durable everyday essentials',
      bullet1: 'Premium materials built for daily use', bullet2: 'Comfortable design with dependable performance',
      bullet3: 'Fast setup and intuitive controls', bullet4: 'A practical choice for home, work, and travel', bullet5: 'Backed by responsive customer support',
    },
    keywords: { primary: ['wireless product', 'premium essentials'], secondary: ['everyday product', 'gift idea'], backend: ['durable', 'comfortable', 'portable'] },
    competitors: [{ rank: 1, title: 'Best Seller Alternative', price: 36.99, rating: 4.5, reviews: 42350, bsr: 156 }],
    seo: { score: 88, keyword_coverage: 82, issues: [] },
  }
}

function contentCalendar() {
  return { total_days: 7, calendar: Array.from({ length: 7 }, (_, index) => ({ date: dateAfter(index), day: ['Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'][index], product: products[index % products.length].name, format_name: contentFormats[index % contentFormats.length].name, duration: contentFormats[index % contentFormats.length].duration, post_time: '6:00 PM EST', hashtag_set: contentConfig.trending_hashtags.slice(0, 3), notes: 'Focus on engagement CTA' })) }
}

function competitorOverview(productKey) {
  const product = listingProducts.find(item => item.key === productKey) || listingProducts[0]
  const competitors = [{ asin: 'B09JNK4YPF', name: 'SoundCore A40 Earbuds', brand: 'Anker', platform: 'amazon', current_price: 36.99, price_history: [39.99, 39.99, 35.99, 35.99, 33.99, 33.99, 36.99], rating: 4.5, reviews: 42350, bsr: 156 }]
  return { product: { name: product.name, price: product.price }, competitors, price_analysis: { market_avg: 36.99, price_competitiveness: 82 }, alerts: [], recommendation: { action: 'hold', current_margin: 68.7, projected_margin: 68.7, suggested_price: product.price, reasoning: 'Current pricing is competitive.' } }
}

function forecast(productKey, days) {
  const item = inventory.find(product => product.key === productKey) || inventory[0]
  return { product: item.name, forecast_days: days, variants: item.variants.map(variant => ({ variant: variant.variant, current_stock: variant.amazon_fba + variant.tiktok_warehouse, avg_daily_velocity: variant.daily_velocity, projected_30d_sales: variant.daily_velocity * days, stockout_date: null, daily_forecast: Array.from({ length: days }, (_, index) => ({ date: dateAfter(index), projected_sales: variant.daily_velocity, projected_stock: Math.max(0, variant.amazon_fba + variant.tiktok_warehouse - variant.daily_velocity * (index + 1)) })) })) }
}

function profitReport(period) {
  const factor = { '30d': 1, '90d': 2.82, year: 10.6 }[period] || 1
  const scale = value => Math.round(value * factor)
  return {
    period,
    summary: { revenue: scale(136000), gross_profit: scale(93400), net_profit: scale(45041), net_margin: 33.1 },
    pnl_rows: [
      { item: '销售收入', amazon: scale(84260), tiktok: scale(51740), total: scale(136000), highlight: true },
      { item: '商品成本', amazon: scale(-26780), tiktok: scale(-15820), total: scale(-42600) },
      { item: '平台佣金', amazon: scale(-12639), tiktok: scale(-4140), total: scale(-16779) },
      { item: '净利润', amazon: scale(26981), tiktok: scale(18060), total: scale(45041), highlight: true },
    ],
    platform_comparison: [
      { metric: '销售收入', amazon: scale(84260), tiktok: scale(51740) },
      { metric: '净利润', amazon: scale(26981), tiktok: scale(18060) },
    ],
    trend: Array.from({ length: 12 }, (_, index) => ({ label: `第 ${index + 1} 周`, revenue: 25000 + index * 1200, net_profit: 7000 + index * 450 })),
  }
}

export const mockApi = {
  system: {
    status: () => resolve({ connections: connectionState, llm: { provider: 'mock', model: 'demo' }, customer_service: dashboard().customer_service.today, inventory: dashboard().supply_chain, products: products.length }),
    dashboard: () => resolve(dashboard()),
    nextNotification: () => resolve({ ...notificationEvents[notificationIndex++ % notificationEvents.length], delay_ms: 9000 }),
  },
  customer: {
    config: () => resolve(customerConfig),
    stats: () => resolve({ today: customerConfig ? { total: 47, auto_resolved: 38, escalated: 3, avg_response_ms: 230 } : {}, week: { total: 312, auto_resolved: 264, escalated: 18, satisfaction: 4.6 }, top_intents: [], platforms: {} }),
    chat: payload => resolve({ response: `感谢您的咨询：“${payload.message}”。这是 Mock 演示回复，实际部署可切换到后端服务。`, intent: 'general', language: /[\u4e00-\u9fff]/.test(payload.message) ? 'zh' : 'en', escalated: false, order_info: null, kb_results: [{ category: 'general', score: 0.92 }], elapsed_ms: 86, platform: payload.platform }),
  },
  listing: { products: () => resolve(listingProducts), generate: payload => resolve(listingResult(payload)) },
  content: {
    config: () => resolve(contentConfig), formats: () => resolve(contentFormats), calendar: () => resolve(contentCalendar()),
    script: payload => resolve({ script: `**开场**\n${payload.product_name} 带来更轻松的日常体验。\n\n**产品亮点**\n${payload.features.join('、')}\n\n**行动号召**\n点击商品链接了解更多。`, hashtags: contentConfig.trending_hashtags, format: payload.format_type, elapsed_ms: 72 }),
    live: payload => resolve({ sections: { opening: '欢迎来到今天的直播！', product_intro: [`这是 ${payload.product_name}。`, `核心特点：${payload.features.join('、')}`, `今天直播价 $${payload.promo_price || payload.price}`], engagement_hooks: ['评论区告诉我你的需求', '喜欢的话点击购物车'], closing: '感谢观看，我们下次直播见！' }, elapsed_ms: 64 }),
  },
  profit: { report: period => resolve(profitReport(period)) },
  competitor: { products: () => resolve(listingProducts.map(({ key, name, price }) => ({ key, name, price }))), overview: productKey => resolve(competitorOverview(productKey)), search: query => resolve({ results: [{ title: `Mock search result for ${query}`, link: '#', snippet: 'This result is provided by the static demo mode.', source: 'Mock data' }] }) },
  supply: { overview: () => resolve({ products: inventory, total_inventory_value: 38420, alerts: [{ severity: 'critical', product: 'LumiPro Smart Desk Lamp', variant: 'Silver', message: '库存不足，建议立即补货' }] }), stats: () => resolve(dashboard().supply_chain), restock: productKey => resolve({ product: (inventory.find(item => item.key === productKey) || inventory[0]).name, sku: 'MOCK-SKU', total_units: 500, total_cost: 5900, orders: [{ variant: 'Black', current_stock: 300, order_quantity: 500, cost: 5900, urgency: 'normal', ship_method: 'sea', estimated_arrival: '2026-10-20' }] }), forecast: (productKey, days) => resolve(forecast(productKey, days)) },
}
