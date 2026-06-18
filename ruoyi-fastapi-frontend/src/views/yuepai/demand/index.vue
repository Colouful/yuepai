<template>
  <div class="app-container">
    <el-form :inline="true" :model="queryParams">
      <el-form-item label="编号"><el-input v-model="queryParams.demand_no" clearable /></el-form-item>
      <el-form-item label="类型"><el-select v-model="queryParams.type" clearable><el-option label="找摄影师" value="seek_photographer" /><el-option label="找模特" value="seek_model" /><el-option label="互勉" value="mutual" /></el-select></el-form-item>
      <el-form-item label="审核"><el-select v-model="queryParams.audit_status" clearable><el-option label="待审核" value="0" /><el-option label="已通过" value="1" /><el-option label="已拒绝" value="2" /></el-select></el-form-item>
      <el-form-item><el-button type="primary" @click="handleQuery">搜索</el-button></el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="编号" prop="demand_no" width="150" />
      <el-table-column label="类型" prop="type" width="100"><template #default="{row}"><el-tag>{{ typeMap[row.type] }}</el-tag></template></el-table-column>
      <el-table-column label="标题" prop="title" show-overflow-tooltip />
      <el-table-column label="城市" prop="city" width="80" />
      <el-table-column label="预算" width="140"><template #default="{row}">¥{{ row.budget_min }}-{{ row.budget_max }}</template></el-table-column>
      <el-table-column label="浏览" prop="view_count" width="70" align="center" />
      <el-table-column label="申请" prop="apply_count" width="70" align="center" />
      <el-table-column label="审核" width="90" align="center"><template #default="{row}"><el-tag :type="auditTag(row.audit_status)">{{ auditMap[row.audit_status] }}</el-tag></template></el-table-column>
      <el-table-column label="时间" prop="create_time" width="160" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{row}">
          <el-button v-if="row.audit_status==='0'" size="small" type="success" @click="handleAudit(row.id,'1')">通过</el-button>
          <el-button v-if="row.audit_status==='0'" size="small" type="danger" @click="handleAudit(row.id,'2')">拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="queryParams.page_num" :total="total" :page-size="20" layout="total, prev, pager, next" @current-change="handleQuery" />
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { getYuepaiDemandList, auditYuepaiDemand } from "@/api/yuepai/demand";
import { ElMessage } from "element-plus";
const typeMap = { seek_photographer: "找摄影", seek_model: "找模特", seek_makeup: "找化妆", mutual: "互勉" };
const auditMap = { "0": "待审核", "1": "已通过", "2": "已拒绝" };
const auditTag = (s) => ({ "0": "warning", "1": "success", "2": "danger" }[s]);
const loading = ref(false); const list = ref([]); const total = ref(0);
const queryParams = ref({ demand_no: "", type: "", audit_status: "", page_num: 1, page_size: 20 });
async function handleQuery() { loading.value = true; try { const res = await getYuepaiDemandList(queryParams.value); list.value = res.rows||[]; total.value = res.total||0; } finally { loading.value = false; } }
async function handleAudit(id, status) { await auditYuepaiDemand(id, status); ElMessage.success("审核成功"); handleQuery(); }
onMounted(() => handleQuery());
</script>
