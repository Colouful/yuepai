<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="风险交易" name="transaction" />
      <el-tab-pane label="封禁管理" name="blocked" />
      <el-tab-pane label="风控规则" name="rule" />
      <el-tab-pane label="操作日志" name="log" />
    </el-tabs>

    <el-form :inline="true" :model="queryParams" class="search-form">
      <el-form-item label="状态">
        <el-select v-model="queryParams.status" clearable placeholder="全部" style="width: 130px">
          <el-option label="待处理" value="pending" /><el-option label="处理中" value="processing" />
          <el-option label="已解决" value="resolved" /><el-option label="已忽略" value="ignored" />
        </el-select>
      </el-form-item>
      <el-form-item label="风险等级" v-if="activeTab==='transaction'">
        <el-select v-model="queryParams.risk_level" clearable placeholder="全部" style="width: 120px">
          <el-option label="高" value="high" /><el-option label="中" value="medium" /><el-option label="低" value="low" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 统计 -->
    <el-row :gutter="16" style="margin-bottom: 16px" v-if="activeTab==='transaction'">
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#F56C6C">{{ riskStats.high }}</div><div style="color:#999;font-size:13px">高风险</div>
      </el-card></el-col>
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#E6A23C">{{ riskStats.medium }}</div><div style="color:#999;font-size:13px">中风险</div>
      </el-card></el-col>
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#909399">{{ riskStats.low }}</div><div style="color:#999;font-size:13px">低风险</div>
      </el-card></el-col>
      <el-col :span="6"><el-card shadow="hover" body-style="padding:16px;text-align:center">
        <div style="font-size:28px;font-weight:700;color:#409EFF">{{ riskStats.pending }}</div><div style="color:#999;font-size:13px">待处理</div>
      </el-card></el-col>
    </el-row>

    <el-button v-if="activeTab!=='log'" type="primary" icon="Plus" style="margin-bottom:16px" @click="handleAdd">新增</el-button>

    <el-table v-loading="loading" :data="list" border stripe>
      <el-table-column label="ID" prop="id" width="70" align="center" />
      <el-table-column label="类型" width="100" align="center"><template #default="{ row }"><el-tag>{{ typeLabels[row.type] || row.type }}</el-tag></template></el-table-column>
      <el-table-column label="目标" prop="target_name" width="130" />
      <el-table-column v-if="activeTab==='transaction'" label="风险等级" width="100" align="center">
        <template #default="{ row }"><el-tag :type="levelMap[row.risk_level]?.type" effect="dark" round>{{ levelMap[row.risk_level]?.label }}</el-tag></template>
      </el-table-column>
      <el-table-column v-if="activeTab==='transaction'" label="金额" width="100" align="right"><template #default="{ row }"><span style="color:#F56C6C">¥{{ row.amount || 0 }}</span></template></el-table-column>
      <el-table-column label="原因" prop="reason" min-width="200" show-overflow-tooltip />
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }"><el-tag :type="statusMap[row.status]?.type" effect="dark" round>{{ statusMap[row.status]?.label }}</el-tag></template>
      </el-table-column>
      <el-table-column label="操作人" prop="operator" width="100" />
      <el-table-column label="创建时间" prop="create_time" width="170" />
      <el-table-column label="操作" width="200" fixed="right" align="center">
        <template #default="{ row }">
          <el-button size="small" @click="handleDetail(row)">详情</el-button>
          <template v-if="row.status==='pending'">
            <el-button size="small" type="success" @click="handleStatus(row, 'resolved')">确认</el-button>
            <el-button size="small" type="danger" @click="handleStatus(row, 'ignored')">忽略</el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.page_num" v-model:limit="queryParams.page_size" @pagination="getList" />

    <el-dialog v-model="detailVisible" title="详情" width="600px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="ID">{{ currentRow.id }}</el-descriptions-item>
        <el-descriptions-item label="类型">{{ typeLabels[currentRow.type] }}</el-descriptions-item>
        <el-descriptions-item label="目标">{{ currentRow.target_name }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">{{ levelMap[currentRow.risk_level]?.label }}</el-descriptions-item>
        <el-descriptions-item label="原因" :span="2">{{ currentRow.reason }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ currentRow.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">{{ statusMap[currentRow.status]?.label }}</el-descriptions-item>
        <el-descriptions-item label="操作人">{{ currentRow.operator || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="addVisible" title="新增风控记录" width="500px">
      <el-form :model="addForm" label-width="90px">
        <el-form-item label="类型"><el-select v-model="addForm.type"><el-option label="风险交易" value="transaction" /><el-option label="封禁" value="blocked" /><el-option label="规则" value="rule" /></el-select></el-form-item>
        <el-form-item label="目标名称"><el-input v-model="addForm.target_name" /></el-form-item>
        <el-form-item label="风险等级"><el-select v-model="addForm.risk_level"><el-option label="高" value="high" /><el-option label="中" value="medium" /><el-option label="低" value="low" /></el-select></el-form-item>
        <el-form-item label="原因"><el-input v-model="addForm.reason" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAdd">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { getRiskList, saveRisk, updateRiskStatus } from '@/api/yuepai/admin'
import { ElMessage } from 'element-plus'

const activeTab = ref('transaction'); const loading = ref(false); const list = ref([]); const total = ref(0)
const queryParams = reactive({ type: 'transaction', status: '', risk_level: '', page_num: 1, page_size: 20 })
const detailVisible = ref(false); const addVisible = ref(false); const currentRow = ref(null)
const addForm = reactive({ type: 'transaction', target_name: '', risk_level: 'medium', reason: '' })

const typeLabels = { transaction: '风险交易', blocked: '封禁', rule: '规则', log: '日志' }
const levelMap = { high: { label: '高风险', type: 'danger' }, medium: { label: '中风险', type: 'warning' }, low: { label: '低风险', type: 'info' } }
const statusMap = { pending: { label: '待处理', type: 'warning' }, processing: { label: '处理中', type: '' }, resolved: { label: '已解决', type: 'success' }, ignored: { label: '已忽略', type: 'info' } }

const riskStats = computed(() => {
  const s = { high: 0, medium: 0, low: 0, pending: 0 }
  list.value.forEach(r => { if (s[r.risk_level] !== undefined) s[r.risk_level]++; if (r.status === 'pending') s.pending++ })
  return s
})

async function getList() {
  loading.value = true
  try { const res = await getRiskList(queryParams); list.value = res.data?.rows || []; total.value = res.data?.total || 0 } finally { loading.value = false }
}
function handleTabChange(tab) { queryParams.type = tab; queryParams.page_num = 1; getList() }
function handleQuery() { queryParams.page_num = 1; getList() }
function resetQuery() { Object.assign(queryParams, { status: '', risk_level: '', page_num: 1 }); getList() }
function handleDetail(row) { currentRow.value = row; detailVisible.value = true }
function handleAdd() { Object.assign(addForm, { type: activeTab.value, target_name: '', risk_level: 'medium', reason: '' }); addVisible.value = true }
async function handleStatus(row, status) { await updateRiskStatus({ id: row.id, status }); ElMessage.success('操作成功'); getList() }
async function confirmAdd() { await saveRisk(addForm); ElMessage.success('保存成功'); addVisible.value = false; getList() }
getList()
</script>
