<template>
  <div class="cert-review-container">
    <!-- 搜索区域 -->
    <el-card shadow="never" class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="用户姓名">
          <el-input v-model="searchForm.name" placeholder="请输入用户姓名" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="searchForm.phone" placeholder="请输入手机号" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="认证类型">
          <el-select v-model="searchForm.certType" placeholder="全部" clearable style="width: 150px">
            <el-option label="实名认证" value="realname" />
            <el-option label="摄影师认证" value="photographer" />
            <el-option label="模特认证" value="model" />
            <el-option label="商家认证" value="merchant" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="searchForm.status" placeholder="全部" clearable style="width: 150px">
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已驳回" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 表格区域 -->
    <el-card shadow="never" class="table-card">
      <template #header>
        <div class="card-header">
          <span>认证审核列表</span>
          <div class="header-actions">
            <el-button type="primary" plain size="small" @click="handleBatchApprove">批量通过</el-button>
            <el-button type="danger" plain size="small" @click="handleBatchReject">批量驳回</el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="tableData"
        border
        stripe
        @selection-change="handleSelectionChange"
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="用户信息" min-width="200">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="40" :src="row.avatar" />
              <div class="user-detail">
                <div class="user-name">{{ row.name }}</div>
                <div class="user-phone">{{ row.phone }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="认证类型" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="certTypeMap[row.certType].type" effect="plain">
              {{ certTypeMap[row.certType].label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="submitTime" label="提交时间" width="180" align="center" sortable />
        <el-table-column label="审核状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="statusMap[row.status].type" effect="dark" round>
              {{ statusMap[row.status].label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reviewer" label="审核人" width="120" align="center" />
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">查看</el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              link
              size="small"
              @click="handleApprove(row)"
            >通过</el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              link
              size="small"
              @click="handleReject(row)"
            >驳回</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          background
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="认证详情" width="700px" destroy-on-close>
      <div v-if="currentRecord" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户姓名">{{ currentRecord.name }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ currentRecord.phone }}</el-descriptions-item>
          <el-descriptions-item label="认证类型">
            <el-tag :type="certTypeMap[currentRecord.certType].type">
              {{ certTypeMap[currentRecord.certType].label }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ currentRecord.submitTime }}</el-descriptions-item>
          <el-descriptions-item label="审核状态">
            <el-tag :type="statusMap[currentRecord.status].type">
              {{ statusMap[currentRecord.status].label }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="审核人">{{ currentRecord.reviewer || '-' }}</el-descriptions-item>
        </el-descriptions>

        <div class="materials-section">
          <h4>提交材料</h4>
          <div class="materials-list">
            <div v-for="(material, index) in currentRecord.materials" :key="index" class="material-item">
              <div class="material-label">{{ material.label }}</div>
              <el-image
                :src="material.url"
                :preview-src-list="currentRecord.materials.map(m => m.url)"
                :initial-index="index"
                fit="cover"
                class="material-image"
              />
            </div>
          </div>
        </div>

        <div v-if="currentRecord.remark" class="remark-section">
          <h4>审核备注</h4>
          <p>{{ currentRecord.remark }}</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <template v-if="currentRecord?.status === 'pending'">
          <el-button type="success" @click="handleApprove(currentRecord)">通过</el-button>
          <el-button type="danger" @click="handleReject(currentRecord)">驳回</el-button>
        </template>
      </template>
    </el-dialog>

    <!-- 审核弹窗 -->
    <el-dialog
      v-model="reviewDialogVisible"
      :title="reviewAction === 'approve' ? '审核通过' : '审核驳回'"
      width="500px"
      destroy-on-close
    >
      <el-form :model="reviewForm" label-width="80px">
        <el-form-item label="用户">
          <span>{{ reviewForm.name }} ({{ reviewForm.phone }})</span>
        </el-form-item>
        <el-form-item label="认证类型">
          <el-tag :type="certTypeMap[reviewForm.certType]?.type">
            {{ certTypeMap[reviewForm.certType]?.label }}
          </el-tag>
        </el-form-item>
        <el-form-item label="审核备注">
          <el-input
            v-model="reviewForm.remark"
            type="textarea"
            :rows="4"
            :placeholder="reviewAction === 'approve' ? '通过备注（选填）' : '请填写驳回原因（必填）'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button
          :type="reviewAction === 'approve' ? 'success' : 'danger'"
          :loading="reviewLoading"
          @click="confirmReview"
        >
          {{ reviewAction === 'approve' ? '确认通过' : '确认驳回' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 类型定义
interface Material {
  label: string
  url: string
}

interface CertRecord {
  id: number
  name: string
  phone: string
  avatar: string
  certType: string
  submitTime: string
  status: string
  reviewer: string
  materials: Material[]
  remark: string
}

// 搜索表单
const searchForm = reactive({
  name: '',
  phone: '',
  certType: '',
  status: ''
})

// 分页
const pagination = reactive({
  page: 1,
  size: 10,
  total: 50
})

// 加载状态
const loading = ref(false)
const reviewLoading = ref(false)

// 弹窗控制
const detailVisible = ref(false)
const reviewDialogVisible = ref(false)
const reviewAction = ref<'approve' | 'reject'>('approve')

// 当前记录
const currentRecord = ref<CertRecord | null>(null)
const selectedRows = ref<CertRecord[]>([])

// 审核表单
const reviewForm = reactive({
  id: 0,
  name: '',
  phone: '',
  certType: '',
  remark: ''
})

// 认证类型映射
const certTypeMap: Record<string, { label: string; type: string }> = {
  realname: { label: '实名认证', type: 'info' },
  photographer: { label: '摄影师认证', type: 'primary' },
  model: { label: '模特认证', type: 'warning' },
  merchant: { label: '商家认证', type: 'success' }
}

// 状态映射
const statusMap: Record<string, { label: string; type: string }> = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已通过', type: 'success' },
  rejected: { label: '已驳回', type: 'danger' }
}

// 模拟数据
const tableData = ref<CertRecord[]>([
  {
    id: 1,
    name: '张小花',
    phone: '138****8001',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    certType: 'photographer',
    submitTime: '2026-06-15 14:30:00',
    status: 'pending',
    reviewer: '',
    materials: [
      { label: '身份证正面', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '身份证反面', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '摄影作品1', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '摄影作品2', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' }
    ],
    remark: ''
  },
  {
    id: 2,
    name: '李模特',
    phone: '139****8002',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    certType: 'model',
    submitTime: '2026-06-15 10:20:00',
    status: 'pending',
    reviewer: '',
    materials: [
      { label: '身份证正面', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '个人写真1', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '个人写真2', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' }
    ],
    remark: ''
  },
  {
    id: 3,
    name: '王老板',
    phone: '137****8003',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    certType: 'merchant',
    submitTime: '2026-06-14 16:45:00',
    status: 'approved',
    reviewer: '管理员A',
    materials: [
      { label: '营业执照', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '法人身份证', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '门店照片', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' }
    ],
    remark: '材料齐全，审核通过'
  },
  {
    id: 4,
    name: '赵实名',
    phone: '136****8004',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    certType: 'realname',
    submitTime: '2026-06-14 09:10:00',
    status: 'rejected',
    reviewer: '管理员B',
    materials: [
      { label: '身份证正面', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '身份证反面', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' }
    ],
    remark: '身份证照片模糊，请重新上传清晰照片'
  },
  {
    id: 5,
    name: '孙摄影',
    phone: '135****8005',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    certType: 'photographer',
    submitTime: '2026-06-13 20:30:00',
    status: 'pending',
    reviewer: '',
    materials: [
      { label: '身份证正面', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '摄影作品1', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '摄影作品2', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' },
      { label: '摄影作品3', url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' }
    ],
    remark: ''
  }
])

// 搜索
const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('搜索完成')
  }, 500)
}

// 重置
const handleReset = () => {
  searchForm.name = ''
  searchForm.phone = ''
  searchForm.certType = ''
  searchForm.status = ''
  handleSearch()
}

// 选择变化
const handleSelectionChange = (rows: CertRecord[]) => {
  selectedRows.value = rows
}

// 查看详情
const handleView = (row: CertRecord) => {
  currentRecord.value = row
  detailVisible.value = true
}

// 审核通过
const handleApprove = (row: CertRecord) => {
  reviewAction.value = 'approve'
  reviewForm.id = row.id
  reviewForm.name = row.name
  reviewForm.phone = row.phone
  reviewForm.certType = row.certType
  reviewForm.remark = ''
  reviewDialogVisible.value = true
}

// 审核驳回
const handleReject = (row: CertRecord) => {
  reviewAction.value = 'reject'
  reviewForm.id = row.id
  reviewForm.name = row.name
  reviewForm.phone = row.phone
  reviewForm.certType = row.certType
  reviewForm.remark = ''
  reviewDialogVisible.value = true
}

// 确认审核
const confirmReview = () => {
  if (reviewAction.value === 'reject' && !reviewForm.remark.trim()) {
    ElMessage.warning('请填写驳回原因')
    return
  }
  reviewLoading.value = true
  setTimeout(() => {
    reviewLoading.value = false
    reviewDialogVisible.value = false
    detailVisible.value = false
    ElMessage.success(reviewAction.value === 'approve' ? '审核通过成功' : '驳回成功')
    // 更新状态
    const index = tableData.value.findIndex(item => item.id === reviewForm.id)
    if (index !== -1) {
      tableData.value[index].status = reviewAction.value === 'approve' ? 'approved' : 'rejected'
      tableData.value[index].reviewer = '当前管理员'
      tableData.value[index].remark = reviewForm.remark
    }
  }, 800)
}

// 批量通过
const handleBatchApprove = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要通过的记录')
    return
  }
  ElMessageBox.confirm(`确认通过选中的 ${selectedRows.value.length} 条记录？`, '批量通过', {
    type: 'warning'
  }).then(() => {
    selectedRows.value.forEach(row => {
      const index = tableData.value.findIndex(item => item.id === row.id)
      if (index !== -1) {
        tableData.value[index].status = 'approved'
        tableData.value[index].reviewer = '当前管理员'
      }
    })
    ElMessage.success('批量通过成功')
  }).catch(() => {})
}

// 批量驳回
const handleBatchReject = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要驳回的记录')
    return
  }
  ElMessageBox.prompt('请输入驳回原因', '批量驳回', {
    inputType: 'textarea',
    inputValidator: (val) => val && val.trim() ? true : '请输入驳回原因'
  }).then(({ value }) => {
    selectedRows.value.forEach(row => {
      const index = tableData.value.findIndex(item => item.id === row.id)
      if (index !== -1) {
        tableData.value[index].status = 'rejected'
        tableData.value[index].reviewer = '当前管理员'
        tableData.value[index].remark = value
      }
    })
    ElMessage.success('批量驳回成功')
  }).catch(() => {})
}

// 分页
const handleSizeChange = () => {
  handleSearch()
}
const handlePageChange = () => {
  handleSearch()
}
</script>

<style scoped>
.cert-review-container {
  padding: 20px;
}

.search-card {
  margin-bottom: 16px;
}

.search-card :deep(.el-card__body) {
  padding-bottom: 2px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-detail {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #303133;
}

.user-phone {
  font-size: 12px;
  color: #909399;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.detail-content {
  max-height: 600px;
  overflow-y: auto;
}

.materials-section {
  margin-top: 20px;
}

.materials-section h4 {
  margin-bottom: 12px;
  color: #303133;
}

.materials-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.material-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}

.material-label {
  margin-bottom: 8px;
  font-size: 13px;
  color: #606266;
}

.material-image {
  width: 100%;
  height: 150px;
  border-radius: 4px;
}

.remark-section {
  margin-top: 20px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.remark-section h4 {
  margin-bottom: 8px;
  color: #303133;
}

.remark-section p {
  color: #606266;
  margin: 0;
}

:deep(.el-button--primary) {
  --el-button-bg-color: #6734E8;
  --el-button-border-color: #6734E8;
  --el-button-hover-bg-color: #7c4ddb;
  --el-button-hover-border-color: #7c4ddb;
}
</style>
