/**
 * 约拍平台管理后台 API 封装
 * 基于 RuoYi 框架的 request 工具
 */
import request from '@/utils/request'

// ============================================================
// 用户管理
// ============================================================

/** 获取用户列表 */
export function getUserList(params) {
  return request({
    url: '/yuepai-api/user/list',
    method: 'get',
    params
  })
}

/** 获取用户详情 */
export function getUserDetail(userId) {
  return request({
    url: '/yuepai-api/user/' + userId,
    method: 'get'
  })
}

/** 更新用户状态（启用/禁用） */
export function updateUserStatus(userId, status) {
  return request({
    url: '/yuepai-api/user/' + userId + '/status',
    method: 'put',
    data: { status }
  })
}

/** 审核用户认证 */
export function reviewCertification(data) {
  return request({
    url: '/yuepai-api/user/certify/review',
    method: 'post',
    data
  })
}

/** 导出用户数据 */
export function exportUser(params) {
  return request({
    url: '/yuepai-api/user/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// ============================================================
// 订单管理
// ============================================================

/** 获取订单列表 */
export function getOrderList(params) {
  return request({
    url: '/yuepai-api/order/list',
    method: 'get',
    params
  })
}

/** 获取订单详情 */
export function getOrderDetail(orderId) {
  return request({
    url: '/yuepai-api/order/' + orderId,
    method: 'get'
  })
}

/** 退款审核 */
export function reviewRefund(data) {
  return request({
    url: '/yuepai-api/order/refund/review',
    method: 'post',
    data
  })
}

/** 获取订单统计 */
export function getOrderStats() {
  return request({
    url: '/yuepai-api/order/stats',
    method: 'get'
  })
}

/** 导出订单数据 */
export function exportOrder(params) {
  return request({
    url: '/yuepai-api/order/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// ============================================================
// 内容审核
// ============================================================

/** 获取内容列表 */
export function getContentList(params) {
  return request({
    url: '/yuepai-api/content/list',
    method: 'get',
    params
  })
}

/** 获取内容详情 */
export function getContentDetail(contentId) {
  return request({
    url: '/yuepai-api/content/' + contentId,
    method: 'get'
  })
}

/** 审核通过 */
export function approveContent(contentId, data) {
  return request({
    url: '/yuepai-api/content/' + contentId + '/approve',
    method: 'post',
    data
  })
}

/** 审核拒绝 */
export function rejectContent(contentId, data) {
  return request({
    url: '/yuepai-api/content/' + contentId + '/reject',
    method: 'post',
    data
  })
}

/** 批量审核通过 */
export function batchApproveContent(ids) {
  return request({
    url: '/yuepai-api/content/batch/approve',
    method: 'post',
    data: { ids }
  })
}

/** 批量审核拒绝 */
export function batchRejectContent(ids, data) {
  return request({
    url: '/yuepai-api/content/batch/reject',
    method: 'post',
    data: { ids, ...data }
  })
}

/** 删除内容 */
export function deleteContent(contentId) {
  return request({
    url: '/yuepai-api/content/' + contentId,
    method: 'delete'
  })
}

/** 获取审核统计 */
export function getContentStats() {
  return request({
    url: '/yuepai-api/content/stats',
    method: 'get'
  })
}

// ============================================================
// 财务管理
// ============================================================

/** 获取财务指标 */
export function getFinanceMetrics(params) {
  return request({
    url: '/yuepai-api/finance/metrics',
    method: 'get',
    params
  })
}

/** 获取趋势数据 */
export function getTrendData(params) {
  return request({
    url: '/yuepai-api/finance/trend',
    method: 'get',
    params
  })
}

/** 获取饼图数据 */
export function getPieData(params) {
  return request({
    url: '/yuepai-api/finance/pie',
    method: 'get',
    params
  })
}

/** 获取提现列表 */
export function getWithdrawList(params) {
  return request({
    url: '/yuepai-api/finance/withdraw/list',
    method: 'get',
    params
  })
}

/** 审核通过提现 */
export function approveWithdraw(withdrawId) {
  return request({
    url: '/yuepai-api/finance/withdraw/' + withdrawId + '/approve',
    method: 'post'
  })
}

/** 审核拒绝提现 */
export function rejectWithdraw(withdrawId, data) {
  return request({
    url: '/yuepai-api/finance/withdraw/' + withdrawId + '/reject',
    method: 'post',
    data
  })
}

/** 获取交易记录 */
export function getTransactions(params) {
  return request({
    url: '/yuepai-api/finance/transactions',
    method: 'get',
    params
  })
}

/** 导出财务数据 */
export function exportFinance(params) {
  return request({
    url: '/yuepai-api/finance/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// ============================================================
// 数据统计
// ============================================================

/** 获取核心指标 */
export function getCoreMetrics(params) {
  return request({
    url: '/yuepai-api/stats/core',
    method: 'get',
    params
  })
}

/** 获取DAU趋势 */
export function getDauTrend(params) {
  return request({
    url: '/yuepai-api/stats/dau',
    method: 'get',
    params
  })
}

/** 获取新增用户趋势 */
export function getNewUserTrend(params) {
  return request({
    url: '/yuepai-api/stats/new-users',
    method: 'get',
    params
  })
}

/** 获取约拍数趋势 */
export function getAppointmentTrend(params) {
  return request({
    url: '/yuepai-api/stats/appointments',
    method: 'get',
    params
  })
}

/** 获取GMV趋势 */
export function getGmvTrend(params) {
  return request({
    url: '/yuepai-api/stats/gmv',
    method: 'get',
    params
  })
}

/** 获取留存数据 */
export function getRetentionData(params) {
  return request({
    url: '/yuepai-api/stats/retention',
    method: 'get',
    params
  })
}

/** 获取漏斗数据 */
export function getFunnelData(params) {
  return request({
    url: '/yuepai-api/stats/funnel',
    method: 'get',
    params
  })
}

/** 导出统计数据 */
export function exportStats(params) {
  return request({
    url: '/yuepai-api/stats/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// ============================================================
// 积分管理
// ============================================================

/** 获取积分规则列表 */
export function getPointRules() {
  return request({
    url: '/yuepai-api/point/rules',
    method: 'get'
  })
}

/** 新增积分规则 */
export function addPointRule(data) {
  return request({
    url: '/yuepai-api/point/rules',
    method: 'post',
    data
  })
}

/** 更新积分规则 */
export function updatePointRule(ruleId, data) {
  return request({
    url: '/yuepai-api/point/rules/' + ruleId,
    method: 'put',
    data
  })
}

/** 删除积分规则 */
export function deletePointRule(ruleId) {
  return request({
    url: '/yuepai-api/point/rules/' + ruleId,
    method: 'delete'
  })
}

/** 获取用户积分列表 */
export function getUserPoints(params) {
  return request({
    url: '/yuepai-api/point/users',
    method: 'get',
    params
  })
}

/** 获取积分明细 */
export function getPointDetail(params) {
  return request({
    url: '/yuepai-api/point/detail',
    method: 'get',
    params
  })
}

/** 发放积分 */
export function grantPoints(userId, data) {
  return request({
    url: '/yuepai-api/point/' + userId + '/grant',
    method: 'post',
    data
  })
}

/** 批量发放积分 */
export function batchGrantPoints(userIds, data) {
  return request({
    url: '/yuepai-api/point/batch/grant',
    method: 'post',
    data: { userIds, ...data }
  })
}

/** 扣减积分 */
export function deductPoints(userId, data) {
  return request({
    url: '/yuepai-api/point/' + userId + '/deduct',
    method: 'post',
    data
  })
}

// ============================================================
// 会员管理
// ============================================================

/** 获取会员列表 */
export function getMemberList(params) {
  return request({
    url: '/yuepai-api/member/list',
    method: 'get',
    params
  })
}

/** 更新会员信息 */
export function updateMember(userId, data) {
  return request({
    url: '/yuepai-api/member/' + userId,
    method: 'put',
    data
  })
}

/** 冻结/解冻会员 */
export function freezeMember(userId, data) {
  return request({
    url: '/yuepai-api/member/' + userId + '/freeze',
    method: 'post',
    data
  })
}

/** 会员续期 */
export function renewMember(userId, data) {
  return request({
    url: '/yuepai-api/member/' + userId + '/renew',
    method: 'post',
    data
  })
}

/** 获取等级列表 */
export function getLevelList() {
  return request({
    url: '/yuepai-api/member/levels',
    method: 'get'
  })
}

/** 新增等级 */
export function addLevel(data) {
  return request({
    url: '/yuepai-api/member/levels',
    method: 'post',
    data
  })
}

/** 更新等级 */
export function updateLevel(levelId, data) {
  return request({
    url: '/yuepai-api/member/levels/' + levelId,
    method: 'put',
    data
  })
}

/** 更新等级状态 */
export function updateLevelStatus(levelId, data) {
  return request({
    url: '/yuepai-api/member/levels/' + levelId + '/status',
    method: 'put',
    data
  })
}

/** 获取权益列表 */
export function getBenefitList() {
  return request({
    url: '/yuepai-api/member/benefits',
    method: 'get'
  })
}

/** 新增权益 */
export function addBenefit(data) {
  return request({
    url: '/yuepai-api/member/benefits',
    method: 'post',
    data
  })
}

/** 更新权益 */
export function updateBenefit(benefitId, data) {
  return request({
    url: '/yuepai-api/member/benefits/' + benefitId,
    method: 'put',
    data
  })
}

/** 删除权益 */
export function deleteBenefit(benefitId) {
  return request({
    url: '/yuepai-api/member/benefits/' + benefitId,
    method: 'delete'
  })
}
