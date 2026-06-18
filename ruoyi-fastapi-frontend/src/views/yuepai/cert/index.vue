<template>
  <div class="app-container">
    <el-form :inline="true" :model="queryParams" class="search-form">
      <el-form-item label="认证类型">
        <el-select v-model="queryParams.cert_type" clearable placeholder="全部" style="width: 140px">
          <el-option label="实名认证" value="realname" />
          <el-option label="摄影师" value="photographer" />
          <el-option label="模特" value="model" />
          <el-option label="商家" value="merchant" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="queryParams.status" clearable placeholder="全部" style="width: 120px">
          <el-option label="待审核" value="0" />
          <el-option label="已通过" value="1" />
          <el-option label="已驳回" value="2" />
        </el-select>
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="queryParams.real_name" placeholder="请输入" clearable style="width: 160px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table v-loading="loading" :data="list" border stripe>
      <el-table-column label="ID" prop="id" width="70" align="center" />
      <el-table-column label="用户ID" prop="user_id" width="100" align="center" />
      <el-table-column label="认证类型" width="110" align="center">
        <template #default="{ row }">
          <el-tag :type="certTypeMap[row.cert_type]?.type">{{ certTypeMap[row.cert_type]?.label }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="真实姓名" prop="real_name" width="110" />
      <el-table-column label="申请说明" prop="description" min-width="180" show-overflow-tooltip />
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="['warning','success','danger'][row.status]">{{ ['待审核','已通过','已驳回'][row.status] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="审核人" prop="reviewer" width="100" />
      <el-table-column label="申请时间" prop="create_time" width="170" />
      <el-table-column label="操作" width="180" fixed="right" align="center">
        <template #default="{ row }">
          <el-button size="small" @click="handleDetail(row)">详情</el-button>
          <template v-if="row.status === '0'">
            <el-button size="small" type="success" @click="handleAudit(row, '1')">通过</el-button>
            <el-button size="small" type="danger" @click="handleAudit(row, '2')">驳回</el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.page_num" v-model:limit="queryParams.page_size" @pagination="getList" />

    <!-- 审核弹窗 -->
    <el-dialog v-model="auditVisible" :title="auditForm.status === '1' ? '审核通过' : '审核驳回'" width="500px">
      <el-form :model="auditForm" label-width="80px">
        <el-form-item label="用户">{{ currentRow?.real_name }}</el-form-item>
        <el-form-item label="类型">{{ certTypeMap[currentRow?.cert_type]?.label }}</el-form-item>
        <el-form-item label="备注">
          <el-input v-model="auditForm.review_remark" type="textarea" :rows="3" :placeholder="auditForm.status==='2'?'请填写驳回原因（必填）':'选填'" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="auditVisible = false">取消</el-button>
        <el-button :type="auditForm.status==='1'?'success':'danger'" @click="confirmAudit">确认</el-button>
      </template>
    </el-dialog>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="认证详情" width="600px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="用户ID">{{ currentRow.user_id }}</el-descriptions-item>
        <el-descriptions-item label="认证类型">{{ certTypeMap[currentRow.cert_type]?.label }}</el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{ currentRow.real_name }}</el-descriptions-item>
        <el-descriptions-item label="身份证">{{ currentRow.id_card }}</el-descriptions-item>
        <el-descriptions-item label="申请说明" :span="2">{{ currentRow.description }}</el-descriptions-item>
        <el-descriptions-item label="状态">{{ ['待审核','已通过','已驳回'][currentRow.status] }}</el-descriptions-item>
        <el-descriptions-item label="审核人">{{ currentRow.reviewer || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核备注" :span="2">{{ currentRow.review_remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { getCertList, auditCert } from '@/api/yuepai/admin'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const list = ref([])
const total = ref(0)
const queryParams = reactive({ cert_type: '', status: '', real_name: '', page_num: 1, page_size: 20 })

const certTypeMap = {
  realname: { label: '实名认证', type: 'info' },
  photographer: { label: '摄影师', type: 'primary' },
  model: { label: '模特', type: 'warning' },
  merchant: { label: '商家', type: 'success' }
}

const auditVisible = ref(false)
const detailVisible = ref(false)
const currentRow = ref(null)
const auditForm = reactive({ id: 0, status: '', review_remark: '' })

async function getList() {
  loading.value = true
  try {
    const res = await getCertList(queryParams)
    list.value = res.data?.rows || res.data?.list || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}

function handleQuery() { queryParams.page_num = 1; getList() }
function resetQuery() { Object.assign(queryParams, { cert_type: '', status: '', real_name: '', page_num: 1 }); getList() }

function handleDetail(row) { currentRow.value = row; detailVisible.value = true }
function handleAudit(row, status) {
  currentRow.value = row
  Object.assign(auditForm, { id: row.id, status, review_remark: '' })
  auditVisible.value = true
}

async function confirmAudit() {
  if (auditForm.status === '2' && !auditForm.review_remark) {
    ElMessage.warning('请填写驳回原因'); return
  }
  await auditCert(auditForm)
  ElMessage.success('审核成功')
  auditVisible.value = false
  getList()
}

getList()
</script>
