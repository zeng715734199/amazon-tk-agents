import http from './http'

export const systemApi = {
  status: () => http.get('/status'),
  dashboard: () => http.get('/dashboard'),
}

export const customerServiceApi = {
  stats: () => http.get('/cs/stats'),
  chat: payload => http.post('/cs/chat', payload),
}

export const listingApi = {
  products: () => http.get('/listing/products'),
  generate: payload => http.post('/listing/generate', payload),
}

export const contentApi = {
  calendar: () => http.get('/content/calendar'),
  formats: () => http.get('/content/formats'),
  script: payload => http.post('/content/script', payload),
  live: payload => http.post('/content/live', payload),
}

export const competitorApi = {
  products: () => http.get('/competitor/products'),
  overview: productKey => http.post('/competitor/overview', { product_key: productKey }),
  search: query => http.post('/competitor/search', { query }),
}

export const supplyChainApi = {
  overview: () => http.get('/supply/overview'),
  stats: () => http.get('/supply/stats'),
  restock: productKey => http.post('/supply/restock', { product_key: productKey }),
  forecast: (productKey, days) => http.post('/supply/forecast', { product_key: productKey, days }),
}
