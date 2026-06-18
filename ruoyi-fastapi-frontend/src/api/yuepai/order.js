import request from '@/utils/request'

export function getYuepaiOrderList(params) {
  return request({ url: '/yuepai/order/list', method: 'get', params })
}
export function getYuepaiFinanceStats() {
  return request({ url: '/yuepai/order/finance/stats', method: 'get' })
}
