import request from '@/utils/request'

export function getYuepaiPostList(params) {
  return request({ url: '/yuepai/post/list', method: 'get', params })
}
export function auditYuepaiPost(id, audit_status) {
  return request({ url: '/yuepai/post/audit', method: 'put', params: { post_id: id, audit_status } })
}
