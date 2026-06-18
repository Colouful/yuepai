import request from '@/utils/request'

export function getYuepaiUserList(params) {
  return request({ url: '/yuepai/user/list', method: 'get', params })
}
export function getYuepaiUserDetail(id) {
  return request({ url: `/yuepai/user/${id}`, method: 'get' })
}
export function updateYuepaiUserStatus(id, status) {
  return request({ url: '/yuepai/user/status', method: 'put', params: { user_id: id, status } })
}
export function auditYuepaiVerify(id, is_verified) {
  return request({ url: '/yuepai/user/verify', method: 'put', params: { user_id: id, is_verified } })
}
