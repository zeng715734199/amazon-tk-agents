import http from './http'
import { mockApi } from './mock'

const useMock = import.meta.env.VITE_DATA_MODE !== 'api'
const service = (mock, live) => useMock ? mock : live

export const systemApi = {
  status: () => service(mockApi.system.status, () => http.get('/status'))(),
  dashboard: () => service(mockApi.system.dashboard, () => http.get('/dashboard'))(),
  nextNotification: () => service(mockApi.system.nextNotification, () => http.get('/notifications/next'))(),
}

export const customerServiceApi = {
  config: () => service(mockApi.customer.config, () => http.get('/cs/config'))(),
  stats: () => service(mockApi.customer.stats, () => http.get('/cs/stats'))(),
  chat: payload => service(mockApi.customer.chat, () => http.post('/cs/chat', payload))(payload),
}

export const listingApi = {
  products: () => service(mockApi.listing.products, () => http.get('/listing/products'))(),
  generate: payload => service(mockApi.listing.generate, () => http.post('/listing/generate', payload))(payload),
}

export const contentApi = {
  config: () => service(mockApi.content.config, () => http.get('/content/config'))(),
  calendar: () => service(mockApi.content.calendar, () => http.get('/content/calendar'))(),
  formats: () => service(mockApi.content.formats, () => http.get('/content/formats'))(),
  script: payload => service(mockApi.content.script, () => http.post('/content/script', payload))(payload),
  live: payload => service(mockApi.content.live, () => http.post('/content/live', payload))(payload),
}

export const profitApi = {
  report: period => service(() => mockApi.profit.report(period), () => http.get('/profit', { params: { period } }))(),
}

export const competitorApi = {
  products: () => service(mockApi.competitor.products, () => http.get('/competitor/products'))(),
  overview: productKey => service(() => mockApi.competitor.overview(productKey), () => http.post('/competitor/overview', { product_key: productKey }))(),
  search: query => service(() => mockApi.competitor.search(query), () => http.post('/competitor/search', { query }))(),
}

export const supplyChainApi = {
  overview: () => service(mockApi.supply.overview, () => http.get('/supply/overview'))(),
  stats: () => service(mockApi.supply.stats, () => http.get('/supply/stats'))(),
  restock: productKey => service(() => mockApi.supply.restock(productKey), () => http.post('/supply/restock', { product_key: productKey }))(),
  forecast: (productKey, days) => service(() => mockApi.supply.forecast(productKey, days), () => http.post('/supply/forecast', { product_key: productKey, days }))(),
}
