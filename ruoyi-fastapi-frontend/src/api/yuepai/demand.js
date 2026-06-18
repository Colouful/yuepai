import request from '@/utils/request'

export function getYuepaiDemandList(params) {
  return request({ url: '/yuepai/demand/list', method: 'get', params })
}
export function auditYuepaiDemand(id, audit_status) {
  return request({ url: '/yuepai/demand/audit', method: 'put', params: { demand_id: id, audit_status } })
}
export function updateYuepaiDemandStatus(id, status) {
  return request({ url: '/yuepai/demand/status', method: 'put', params: { demand_id: id, status } })
}
