<template>
  <div class="app-container">
    <el-form :inline="true" :model="queryParams" class="search-form">
      <el-form-item label="类型">
        <el-select v-model="queryParams.type" clearable placeholder="全部" style="width: 130px">
          <el-option label="退款" value="refund" /><el-option label="投诉" value="complaint" /><el-option label="争议" value="dispute" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="queryParams.status" clearable placeholder="全部" style="width: 130px">
          <el-option label="待处理" value="pending" /><el-option label="处理中" value="processing" />
          <el-option label="已解决" value="resolved" /><el-option label="已驳回" value="rejected" /><el-option label="已关闭" value="closed" />
        </el-select>
      </el-form-item>
      <el-form-item label="工单号"><el-input v-model="queryParams.ticket_no" placeholder="请输入" clearable style="width: 180px" /></el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 统计卡片 -->
    <el-row :gutter="16" style="margin-bottom: 16px">
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#E6A23C">{{ stats.pending }}</div><div style="color:#999;font-size:13px">待处理</div>
      </el-card></el-col>
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#409EFF">{{ stats.processing }}</div><div style="color:#999;font-size:13px">处理中</div>
      </el-card></el-col>
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#67C23A">{{ stats.resolved }}</div><div style="color:#999;font-size:13px">已解决</div>
      </el-card></el-col>
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#F56C6C">{{ stats.rejected }}</div><div style="color:#999;font-size:13px">已驳回</div>
      </el-card></el-col>
    </el-row>

    <el-table v-loading="loading" :data="list" border stripe>
      <el-table-column label="工单号" prop="ticket_no" width="170" />
      <el-table-column label="类型" width="90" align="center">
        <template #default="{ row }"><el-tag :type="typeMap[row.type]?.type">{{ typeMap[row.type]?.label }}</el-tag></template>
      </el-table-column>
      <el-table-column label="关联订单" prop="order_no" width="160" />
      <el-table-column label="金额" width="100" align="right"><template #default="{ row }"><span style="color:#F56C6C">¥{{ row.amount || 0 }}</span></template></el-table-column>
      <el-table-column label="原因" prop="reason" min-width="180" show-overflow-tooltip />
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }"><el-tag :type="statusMap[row.status]?.type" effect="dark" round>{{ statusMap[row.status]?.label }}</el-tag></template>
      </el-table-column>
      <el-table-column label="处理人" prop="handler" width="100" />
      <el-table-column label="创建时间" prop="create_time" width="170" />
      <el-table-column label="操作" width="180" fixed="right" align="center">
        <template #default="{ row }">
          <el-button size="small" @click="handleDetail(row)">详情</el-button>
          <template v-if="row.status === 'pending' || row.status === 'processing'">
            <el-button size="small" type="success" @click="handleAction(row, 'resolved')">解决</el-button>
            <el-button size="small" type="danger" @click="handleAction(row, 'rejected')">驳回</el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.page_num" v-model:limit="queryParams.page_size" @pagination="getList" />

    <el-dialog v-model="detailVisible" title="工单详情" width="600px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="工单号">{{ currentRow.ticket_no }}</el-descriptions-item>
        <el-descriptions-item label="类型">{{ typeMap[currentRow.type]?.label }}</el-descriptions-item>
        <el-descriptions-item label="关联订单">{{ currentRow.order_no || '-' }}</el-descriptions-item>
        <el-descriptions-item label="金额">¥{{ currentRow.amount || 0 }}</el-descriptions-item>
        <el-descriptions-item label="原因" :span="2">{{ currentRow.reason }}</el-descriptions-item>
        <el-descriptions-item label="详细描述" :span="2">{{ currentRow.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">{{ statusMap[currentRow.status]?.label }}</el-descriptions-item>
        <el-descriptions-item label="处理人">{{ currentRow.handler || '-' }}</el-descriptions-item>
        <el-descriptions-item label="处理结果" :span="2">{{ currentRow.handle_result || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="handleVisible" :title="handleForm.status==='resolved'?'确认解决':'确认驳回'" width="500px">
      <el-form label-width="80px">
        <el-form-item label="工单号">{{ currentRow?.ticket_no }}</el-form-item>
        <el-form-item label="处理结果"><el-input v-model="handleForm.handle_result" type="textarea" :rows="3" placeholder="请输入处理结果" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleVisible = false">取消</el-button>
        <el-button :type="handleForm.status==='resolved'?'success':'danger'" @click="confirmHandle">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { getAftersaleList, handleAftersale } from '@/api/yuepai/admin'
import { ElMessage } from 'element-plus'

const loading = ref(false); const list = ref([]); const total = ref(0)
const queryParams = reactive({ type: '', status: '', ticket_no: '', page_num: 1, page_size: 20 })
const detailVisible = ref(false); const handleVisible = ref(false); const currentRow = ref(null)
const handleForm = reactive({ id: 0, status: '', handle_result: '' })

const typeMap = { refund: { label: '退款', type: 'danger' }, complaint: { label: '投诉', type: 'warning' }, dispute: { label: '争议', type: 'primary' } }
const statusMap = { pending: { label: '待处理', type: 'warning' }, processing: { label: '处理中', type: '' }, resolved: { label: '已解决', type: 'success' }, rejected: { label: '已驳回', type: 'danger' }, closed: { label: '已关闭', type: 'info' } }

const stats = computed(() => {
  const s = { pending: 0, processing: 0, resolved: 0, rejected: 0 }
  list.value.forEach(r => { if (s[r.status] !== undefined) s[r.status]++ })
  return s
})

async function getList() {
  loading.value = true
  try { const res = await getAftersaleList(queryParams); list.value = res.data?.rows || []; total.value = res.data?.total || 0 } finally { loading.value = false }
}
function handleQuery() { queryParams.page_num = 1; getList() }
function resetQuery() { Object.assign(queryParams, { type: '', status: '', ticket_no: '', page_num: 1 }); getList() }
function handleDetail(row) { currentRow.value = row; detailVisible.value = true }
function handleAction(row, status) { currentRow.value = row; Object.assign(handleForm, { id: row.id, status, handle_result: '' }); handleVisible.value = true }
async function confirmHandle() {
  await handleAftersale(handleForm); ElMessage.success('操作成功'); handleVisible.value = false; getList()
}
getList()
</script>
