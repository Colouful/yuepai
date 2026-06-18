<template>
  <div class="after-sale-container">
    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stat-row">
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-pending">
          <div class="stat-value">23</div>
          <div class="stat-label">待处理</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-processing">
          <div class="stat-value">15</div>
          <div class="stat-label">处理中</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-completed">
          <div class="stat-value">1,256</div>
          <div class="stat-label">已完成</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-total">
          <div class="stat-value">¥12,580</div>
          <div class="stat-label">退款总额</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 主要内容区 -->
    <el-card shadow="never">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <!-- 退款申请 -->
        <el-tab-pane label="退款申请" name="refund">
          <el-form :model="searchForm" inline class="search-form">
            <el-form-item label="订单号">
              <el-input v-model="searchForm.orderNo" placeholder="请输入订单号" clearable style="width: 200px" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="全部" clearable style="width: 150px">
                <el-option label="待处理" value="pending" />
                <el-option label="处理中" value="processing" />
                <el-option label="已完成" value="completed" />
                <el-option label="已驳回" value="rejected" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
              <el-button :icon="Refresh" @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>

          <el-table v-loading="loading" :data="refundData" border stripe>
            <el-table-column prop="orderNo" label="订单号" width="180" />
            <el-table-column label="买家" width="140">
              <template #default="{ row }">
                <div class="user-cell">
                  <el-avatar :size="28" :src="row.buyerAvatar" />
                  <span>{{ row.buyerName }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="卖家" width="140">
              <template #default="{ row }">
                <div class="user-cell">
                  <el-avatar :size="28" :src="row.sellerAvatar" />
                  <span>{{ row.sellerName }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" width="120" align="center">
              <template #default="{ row }">
                <span class="amount">¥{{ row.amount }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="reason" label="退款原因" min-width="160" show-overflow-tooltip />
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="refundStatusMap[row.status].type" effect="dark" round>
                  {{ refundStatusMap[row.status].label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="submitTime" label="提交时间" width="180" align="center" />
            <el-table-column label="操作" width="240" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleViewDetail(row)">详情</el-button>
                <template v-if="row.status === 'pending'">
                  <el-button type="success" link size="small" @click="handleAction(row, 'full')">同意退款</el-button>
                  <el-button type="warning" link size="small" @click="handleAction(row, 'partial')">部分退款</el-button>
                  <el-button type="danger" link size="small" @click="handleAction(row, 'reject')">驳回</el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 投诉工单 -->
        <el-tab-pane label="投诉工单" name="complaint">
          <el-table v-loading="loading" :data="complaintData" border stripe>
            <el-table-column prop="orderNo" label="关联订单" width="180" />
            <el-table-column label="投诉人" width="120">
              <template #default="{ row }">{{ row.complainant }}</template>
            </el-table-column>
            <el-table-column label="被投诉人" width="120">
              <template #default="{ row }">{{ row.respondent }}</template>
            </el-table-column>
            <el-table-column prop="type" label="投诉类型" width="120" align="center">
              <template #default="{ row }">
                <el-tag effect="plain">{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="投诉描述" min-width="200" show-overflow-tooltip />
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="complaintStatusMap[row.status].type" effect="dark" round>
                  {{ complaintStatusMap[row.status].label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="180" align="center" />
            <el-table-column label="操作" width="180" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleViewComplaint(row)">详情</el-button>
                <el-button v-if="row.status !== 'closed'" type="warning" link size="small" @click="handleIntervene(row)">平台介入</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 争议处理 -->
        <el-tab-pane label="争议处理" name="dispute">
          <el-table v-loading="loading" :data="disputeData" border stripe>
            <el-table-column prop="disputeNo" label="争议编号" width="180" />
            <el-table-column prop="orderNo" label="关联订单" width="180" />
            <el-table-column label="申请人" width="120">
              <template #default="{ row }">{{ row.applicant }}</template>
            </el-table-column>
            <el-table-column prop="type" label="争议类型" width="140" align="center">
              <template #default="{ row }">
                <el-tag type="warning" effect="plain">{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="争议金额" width="120" align="center">
              <template #default="{ row }">
                <span class="amount">¥{{ row.amount }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="disputeStatusMap[row.status].type" effect="dark" round>
                  {{ disputeStatusMap[row.status].label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="deadline" label="处理期限" width="180" align="center" />
            <el-table-column label="操作" width="200" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleViewDispute(row)">详情</el-button>
                <el-button v-if="row.status === 'pending'" type="warning" link size="small" @click="handleArbitrate(row)">仲裁</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          background
        />
      </div>
    </el-card>

    <!-- 退款详情弹窗 -->
    <el-dialog v-model="refundDetailVisible" title="退款详情" width="800px" destroy-on-close>
      <div v-if="currentRefund" class="refund-detail">
        <!-- 订单信息 -->
        <el-descriptions title="订单信息" :column="2" border>
          <el-descriptions-item label="订单号">{{ currentRefund.orderNo }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">¥{{ currentRefund.amount }}</el-descriptions-item>
          <el-descriptions-item label="买家">{{ currentRefund.buyerName }}</el-descriptions-item>
          <el-descriptions-item label="卖家">{{ currentRefund.sellerName }}</el-descriptions-item>
          <el-descriptions-item label="退款原因" :span="2">{{ currentRefund.reason }}</el-descriptions-item>
        </el-descriptions>

        <!-- 证据材料 -->
        <div class="evidence-section">
          <h4>双方证据</h4>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="evidence-card buyer">
                <div class="evidence-title">买家举证</div>
                <div class="evidence-images">
                  <el-image
                    v-for="(img, idx) in currentRefund.buyerEvidence"
                    :key="idx"
                    :src="img"
                    :preview-src-list="currentRefund.buyerEvidence"
                    fit="cover"
                    class="evidence-img"
                  />
                </div>
                <p class="evidence-desc">{{ currentRefund.buyerDescription }}</p>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="evidence-card seller">
                <div class="evidence-title">卖家举证</div>
                <div class="evidence-images">
                  <el-image
                    v-for="(img, idx) in currentRefund.sellerEvidence"
                    :key="idx"
                    :src="img"
                    :preview-src-list="currentRefund.sellerEvidence"
                    fit="cover"
                    class="evidence-img"
                  />
                </div>
                <p class="evidence-desc">{{ currentRefund.sellerDescription }}</p>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 聊天记录 -->
        <div class="chat-section">
          <h4>协商记录</h4>
          <div class="chat-list">
            <div
              v-for="(msg, idx) in currentRefund.chatRecords"
              :key="idx"
              class="chat-item"
              :class="msg.sender === 'buyer' ? 'buyer' : 'seller'"
            >
              <div class="chat-sender">{{ msg.sender === 'buyer' ? '买家' : '卖家' }}</div>
              <div class="chat-content">{{ msg.content }}</div>
              <div class="chat-time">{{ msg.time }}</div>
            </div>
          </div>
        </div>

        <!-- 处理时间线 -->
        <div class="timeline-section">
          <h4>处理进度</h4>
          <el-timeline>
            <el-timeline-item
              v-for="(item, idx) in currentRefund.timeline"
              :key="idx"
              :timestamp="item.time"
              :type="item.type"
              placement="top"
            >
              {{ item.content }}
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
      <template #footer>
        <el-button @click="refundDetailVisible = false">关闭</el-button>
        <template v-if="currentRefund?.status === 'pending'">
          <el-button type="success" @click="handleAction(currentRefund, 'full')">同意退款</el-button>
          <el-button type="warning" @click="handleAction(currentRefund, 'partial')">部分退款</el-button>
          <el-button type="info" @click="handleAction(currentRefund, 'intervene')">平台介入</el-button>
          <el-button type="danger" @click="handleAction(currentRefund, 'reject')">驳回</el-button>
        </template>
      </template>
    </el-dialog>

    <!-- 部分退款弹窗 -->
    <el-dialog v-model="partialRefundVisible" title="部分退款" width="500px" destroy-on-close>
      <el-form :model="partialRefundForm" label-width="100px">
        <el-form-item label="订单金额">
          <span>¥{{ partialRefundForm.totalAmount }}</span>
        </el-form-item>
        <el-form-item label="退款金额">
          <el-input-number
            v-model="partialRefundForm.refundAmount"
            :min="0.01"
            :max="partialRefundForm.totalAmount"
            :precision="2"
            :step="10"
          />
        </el-form-item>
        <el-form-item label="处理说明">
          <el-input
            v-model="partialRefundForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入处理说明"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="partialRefundVisible = false">取消</el-button>
        <el-button type="primary" :loading="actionLoading" @click="confirmPartialRefund">确认退款</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 当前标签页
const activeTab = ref('refund')
const loading = ref(false)
const actionLoading = ref(false)

// 搜索表单
const searchForm = reactive({
  orderNo: '',
  status: ''
})

// 分页
const pagination = reactive({
  page: 1,
  size: 10,
  total: 50
})

// 弹窗控制
const refundDetailVisible = ref(false)
const partialRefundVisible = ref(false)
const currentRefund = ref<any>(null)

// 部分退款表单
const partialRefundForm = reactive({
  totalAmount: 0,
  refundAmount: 0,
  remark: ''
})

// 状态映射
const refundStatusMap: Record<string, { label: string; type: string }> = {
  pending: { label: '待处理', type: 'warning' },
  processing: { label: '处理中', type: 'primary' },
  completed: { label: '已完成', type: 'success' },
  rejected: { label: '已驳回', type: 'danger' }
}

const complaintStatusMap: Record<string, { label: string; type: string }> = {
  pending: { label: '待处理', type: 'warning' },
  processing: { label: '处理中', type: 'primary' },
  resolved: { label: '已解决', type: 'success' },
  closed: { label: '已关闭', type: 'info' }
}

const disputeStatusMap: Record<string, { label: string; type: string }> = {
  pending: { label: '待仲裁', type: 'warning' },
  processing: { label: '仲裁中', type: 'primary' },
  resolved: { label: '已裁决', type: 'success' },
  closed: { label: '已关闭', type: 'info' }
}

// 退款数据
const refundData = ref([
  {
    id: 1,
    orderNo: 'YP20260615001',
    buyerName: '张小花',
    buyerAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    sellerName: '李摄影',
    sellerAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 299,
    reason: '拍摄效果与预期不符，照片质量差',
    status: 'pending',
    submitTime: '2026-06-15 14:30:00',
    buyerEvidence: [
      'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
    ],
    buyerDescription: '照片模糊、构图差，与样片差距很大',
    sellerEvidence: [
      'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
    ],
    sellerDescription: '已按照约定完成拍摄，照片质量符合标准',
    chatRecords: [
      { sender: 'buyer', content: '照片质量太差了，要求退款', time: '2026-06-15 15:00' },
      { sender: 'seller', content: '可以重新修图，但不支持退款', time: '2026-06-15 15:10' },
      { sender: 'buyer', content: '不接受重修，要求全额退款', time: '2026-06-15 15:20' }
    ],
    timeline: [
      { time: '2026-06-15 14:30', content: '买家发起退款申请', type: 'primary' },
      { time: '2026-06-15 14:35', content: '系统通知卖家', type: '' },
      { time: '2026-06-15 15:20', content: '双方协商未达成一致', type: 'warning' }
    ]
  },
  {
    id: 2,
    orderNo: 'YP20260614002',
    buyerName: '王美美',
    buyerAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    sellerName: '陈摄影',
    sellerAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 599,
    reason: '摄影师未按约定时间到场',
    status: 'processing',
    submitTime: '2026-06-14 10:20:00',
    buyerEvidence: ['https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'],
    buyerDescription: '约定下午2点，摄影师3点才到',
    sellerEvidence: ['https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'],
    sellerDescription: '因交通拥堵迟到，已提前通知',
    chatRecords: [
      { sender: 'buyer', content: '迟到1小时，严重影响拍摄计划', time: '2026-06-14 16:00' },
      { sender: 'seller', content: '非常抱歉，愿意补偿部分费用', time: '2026-06-14 16:10' }
    ],
    timeline: [
      { time: '2026-06-14 10:20', content: '买家发起退款申请', type: 'primary' },
      { time: '2026-06-14 10:25', content: '系统通知卖家', type: '' },
      { time: '2026-06-14 16:10', content: '卖家同意部分退款', type: 'success' }
    ]
  },
  {
    id: 3,
    orderNo: 'YP20260613003',
    buyerName: '刘先生',
    buyerAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    sellerName: '赵摄影',
    sellerAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 199,
    reason: '重复扣款',
    status: 'completed',
    submitTime: '2026-06-13 09:15:00',
    buyerEvidence: [],
    buyerDescription: '',
    sellerEvidence: [],
    sellerDescription: '',
    chatRecords: [],
    timeline: [
      { time: '2026-06-13 09:15', content: '买家发起退款申请', type: 'primary' },
      { time: '2026-06-13 09:30', content: '系统确认重复扣款', type: '' },
      { time: '2026-06-13 10:00', content: '退款已到账', type: 'success' }
    ]
  }
])

// 投诉数据
const complaintData = ref([
  {
    id: 1,
    orderNo: 'YP20260615005',
    complainant: '小红',
    respondent: '大伟摄影',
    type: '服务态度',
    description: '摄影师态度恶劣，拍摄过程中多次催促，影响拍摄体验',
    status: 'pending',
    createTime: '2026-06-15 16:30:00'
  },
  {
    id: 2,
    orderNo: 'YP20260614008',
    complainant: '阿杰',
    respondent: '美美模特',
    type: '虚假信息',
    description: '模特照片与本人差距过大，涉嫌使用过度修图照片',
    status: 'processing',
    createTime: '2026-06-14 11:20:00'
  },
  {
    id: 3,
    orderNo: 'YP20260613012',
    complainant: '小芳',
    respondent: '光影工作室',
    type: '价格欺诈',
    description: '实际收费与平台标价不一致，加收额外费用',
    status: 'resolved',
    createTime: '2026-06-13 14:45:00'
  }
])

// 争议数据
const disputeData = ref([
  {
    id: 1,
    disputeNo: 'DZ20260615001',
    orderNo: 'YP20260615001',
    applicant: '张小花',
    type: '退款争议',
    amount: 299,
    status: 'pending',
    deadline: '2026-06-18 14:30:00'
  },
  {
    id: 2,
    disputeNo: 'DZ20260614002',
    orderNo: 'YP20260614008',
    applicant: '阿杰',
    type: '服务争议',
    amount: 599,
    status: 'processing',
    deadline: '2026-06-17 11:20:00'
  }
])

// 标签页切换
const handleTabChange = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

// 搜索
const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

const handleReset = () => {
  searchForm.orderNo = ''
  searchForm.status = ''
  handleSearch()
}

// 查看退款详情
const handleViewDetail = (row: any) => {
  currentRefund.value = row
  refundDetailVisible.value = true
}

// 查看投诉详情
const handleViewComplaint = (row: any) => {
  ElMessage.info(`查看投诉详情: ${row.orderNo}`)
}

// 查看争议详情
const handleViewDispute = (row: any) => {
  ElMessage.info(`查看争议详情: ${row.disputeNo}`)
}

// 处理退款操作
const handleAction = (row: any, action: string) => {
  if (action === 'full') {
    ElMessageBox.confirm('确认同意全额退款？', '确认操作', {
      type: 'warning'
    }).then(() => {
      row.status = 'completed'
      refundDetailVisible.value = false
      ElMessage.success('退款成功')
    }).catch(() => {})
  } else if (action === 'partial') {
    partialRefundForm.totalAmount = row.amount
    partialRefundForm.refundAmount = row.amount / 2
    partialRefundForm.remark = ''
    partialRefundVisible.value = true
  } else if (action === 'reject') {
    ElMessageBox.prompt('请输入驳回原因', '驳回退款', {
      inputType: 'textarea',
      inputValidator: (val) => val && val.trim() ? true : '请输入驳回原因'
    }).then(({ value }) => {
      row.status = 'rejected'
      refundDetailVisible.value = false
      ElMessage.success('已驳回')
    }).catch(() => {})
  } else if (action === 'intervene') {
    ElMessageBox.confirm('确认提交平台介入处理？', '平台介入', {
      type: 'warning'
    }).then(() => {
      row.status = 'processing'
      refundDetailVisible.value = false
      ElMessage.success('已提交平台介入')
    }).catch(() => {})
  }
}

// 确认部分退款
const confirmPartialRefund = () => {
  actionLoading.value = true
  setTimeout(() => {
    actionLoading.value = false
    partialRefundVisible.value = false
    refundDetailVisible.value = false
    ElMessage.success('部分退款成功')
  }, 800)
}

// 平台介入
const handleIntervene = (row: any) => {
  ElMessageBox.confirm('确认提交平台介入处理？', '平台介入', {
    type: 'warning'
  }).then(() => {
    row.status = 'processing'
    ElMessage.success('已提交平台介入')
  }).catch(() => {})
}

// 仲裁
const handleArbitrate = (row: any) => {
  ElMessageBox.confirm('确认开始仲裁处理？', '开始仲裁', {
    type: 'warning'
  }).then(() => {
    row.status = 'processing'
    ElMessage.success('已开始仲裁')
  }).catch(() => {})
}
</script>

<style scoped>
.after-sale-container {
  padding: 20px;
}

.stat-row {
  margin-bottom: 16px;
}

.stat-card {
  text-align: center;
  padding: 10px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-pending .stat-value { color: #E6A23C; }
.stat-processing .stat-value { color: #6734E8; }
.stat-completed .stat-value { color: #67C23A; }
.stat-total .stat-value { color: #F56C6C; }

.search-form {
  margin-bottom: 16px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.amount {
  color: #F56C6C;
  font-weight: 600;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.refund-detail {
  max-height: 600px;
  overflow-y: auto;
}

.evidence-section,
.chat-section,
.timeline-section {
  margin-top: 20px;
}

.evidence-section h4,
.chat-section h4,
.timeline-section h4 {
  margin-bottom: 12px;
  color: #303133;
  font-size: 15px;
}

.evidence-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 12px;
}

.evidence-card.buyer {
  border-color: #67C23A;
}

.evidence-card.seller {
  border-color: #E6A23C;
}

.evidence-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.evidence-card.buyer .evidence-title { color: #67C23A; }
.evidence-card.seller .evidence-title { color: #E6A23C; }

.evidence-images {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.evidence-img {
  width: 80px;
  height: 80px;
  border-radius: 4px;
}

.evidence-desc {
  font-size: 13px;
  color: #606266;
  margin: 0;
}

.chat-list {
  max-height: 300px;
  overflow-y: auto;
}

.chat-item {
  margin-bottom: 12px;
  padding: 10px;
  border-radius: 8px;
}

.chat-item.buyer {
  background: #f0f9eb;
  margin-right: 40px;
}

.chat-item.seller {
  background: #fdf6ec;
  margin-left: 40px;
}

.chat-sender {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 4px;
}

.chat-content {
  font-size: 14px;
  color: #303133;
}

.chat-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

:deep(.el-button--primary) {
  --el-button-bg-color: #6734E8;
  --el-button-border-color: #6734E8;
  --el-button-hover-bg-color: #7c4ddb;
  --el-button-hover-border-color: #7c4ddb;
}

:deep(.el-tabs__item.is-active) {
  color: #6734E8;
}

:deep(.el-tabs__active-bar) {
  background-color: #6734E8;
}
</style>
