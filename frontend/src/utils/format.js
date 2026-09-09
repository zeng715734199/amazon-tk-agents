export const formatNumber = value => value == null ? '--' : Number(value).toLocaleString('zh-CN')

export const formatCurrency = value => value == null
  ? '--'
  : new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(Number(value))

export const formatPercent = value => value == null ? '--' : `${Number(value).toFixed(1)}%`

export const statusColor = status => ({
  healthy: 'success', warning: 'warning', critical: 'error', urgent: 'error',
  normal: 'processing', reduce: 'warning', increase: 'processing', hold: 'success',
}[status] || 'default')

export const statusText = status => ({
  healthy: '健康', warning: '预警', critical: '紧急', urgent: '紧急', normal: '正常',
  reduce: '建议降价', increase: '建议提价', hold: '保持价格', air: '空运', sea: '海运',
}[status] || status || '--')
