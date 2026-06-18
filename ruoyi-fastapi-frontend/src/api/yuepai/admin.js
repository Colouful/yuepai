import request from '@/utils/request'

// ========== 认证审核 ==========
export function getCertList(params) {
  return request({ url: '/yuepai/cert/list', method: 'get', params })
}
export function getCertDetail(id) {
  return request({ url: `/yuepai/cert/${id}`, method: 'get' })
}
export function auditCert(data) {
  return request({ url: '/yuepai/cert/audit', method: 'put', data })
}

// ========== 售后管理 ==========
export function getAftersaleList(params) {
  return request({ url: '/yuepai/aftersale/list', method: 'get', params })
}
export function getAftersaleDetail(id) {
  return request({ url: `/yuepai/aftersale/${id}`, method: 'get' })
}
export function handleAftersale(data) {
  return request({ url: '/yuepai/aftersale/handle', method: 'put', data })
}

// ========== 运营管理 ==========
export function getOperationList(params) {
  return request({ url: '/yuepai/operation/list', method: 'get', params })
}
export function getOperationDetail(id) {
  return request({ url: `/yuepai/operation/${id}`, method: 'get' })
}
export function saveOperation(data) {
  return request({ url: '/yuepai/operation/save', method: 'post', data })
}
export function deleteOperation(id) {
  return request({ url: `/yuepai/operation/${id}`, method: 'delete' })
}

// ========== 风控中心 ==========
export function getRiskList(params) {
  return request({ url: '/yuepai/risk/list', method: 'get', params })
}
export function getRiskDetail(id) {
  return request({ url: `/yuepai/risk/${id}`, method: 'get' })
}
export function saveRisk(data) {
  return request({ url: '/yuepai/risk/save', method: 'post', data })
}
export function updateRiskStatus(params) {
  return request({ url: '/yuepai/risk/status', method: 'put', params })
}
