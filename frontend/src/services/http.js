import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 90_000,
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail
      || error.response?.data?.message
      || (error.code === 'ECONNABORTED' ? '请求超时，请稍后重试' : '服务暂时不可用，请检查后端连接')
    return Promise.reject(new Error(message))
  },
)

export default http
