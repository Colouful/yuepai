<template>
  <div class="app-container">
    <el-form :inline="true" :model="queryParams" class="search-form">
      <el-form-item label="用户UID"><el-input v-model="queryParams.uid" placeholder="UID" clearable /></el-form-item>
      <el-form-item label="角色">
        <el-select v-model="queryParams.role" clearable placeholder="全部">
          <el-option label="摄影师" value="photographer" /><el-option label="模特" value="model" />
          <el-option label="化妆师" value="makeup" /><el-option label="普通用户" value="user" />
        </el-select>
      </el-form-item>
      <el-form-item label="城市"><el-input v-model="queryParams.city" placeholder="城市" clearable /></el-form-item>
      <el-form-item label="认证">
        <el-select v-model="queryParams.is_verified" clearable placeholder="全部">
          <el-option label="已认证" value="1" /><el-option label="未认证" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item><el-button type="primary" @click="handleQuery"><i class="el-icon-search" /> 搜索</el-button><el-button @click="resetQuery">重置</el-button></el-form-item>
    </el-form>

    <el-table v-loading="loading" :data="userList" border stripe>
      <el-table-column label="UID" prop="uid" width="130" />
      <el-table-column label="角色" prop="role" width="100">
        <template #default="{ row }"><el-tag :type="roleTag(row.role)">{{ roleName(row.role) }}</el-tag></template>
      </el-table-column>
      <el-table-column label="城市" prop="city" width="100" />
      <el-table-column label="实名认证" width="90" align="center">
        <template #default="{ row }"><el-tag :type="row.is_verified==='1'?'success':'info'" size="small">{{ row.is_verified==='1'?'已认证':'未认证' }}</el-tag></template>
      </el-table-column>
      <el-table-column label="信用分" prop="credit_score" width="80" align="center" />
      <el-table-column label="余额" prop="balance" width="90" align="right" />
      <el-table-column label="积分" prop="point_balance" width="80" align="center" />
      <el-table-column label="约拍次数" prop="yuepai_count" width="90" align="center" />
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }"><el-tag :type="row.status==='0'?'success':'danger'">{{ row.status==='0'?'正常':'禁用' }}</el-tag></template>
      </el-table-column>
      <el-table-column label="注册时间" prop="create_time" width="160" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleDetail(row)">详情</el-button>
          <el-button size="small" :type="row.status==='0'?'warning':'success'" @click="handleToggleStatus(row)">{{ row.status==='0'?'禁用':'启用' }}</el-button>
          <el-button v-if="row.is_verified==='0'" size="small" type="primary" @click="handleVerify(row)">认证</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="queryParams.page_num" :total="total" :page-size="queryParams.page_size" layout="total, sizes, prev, pager, next" @current-change="handleQuery" @size-change="handleSizeChange" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getYuepaiUserList, updateYuepaiUserStatus, auditYuepaiVerify } from "@/api/yuepai/user";
import { ElMessage, ElMessageBox } from "element-plus";

const loading = ref(false);
const userList = ref([]);
const total = ref(0);
const queryParams = ref({ uid: "", role: "", city: "", status: "", is_verified: "", page_num: 1, page_size: 20 });

const roleName = (r) => ({ photographer: "摄影师", model: "模特", makeup: "化妆师", merchant: "商家", user: "用户" }[r] || r);
const roleTag = (r) => ({ photographer: "danger", model: "", makeup: "warning", merchant: "success" }[r] || "info");

async function handleQuery() {
  loading.value = true;
  try {
    const res = await getYuepaiUserList(queryParams.value);
    userList.value = res.rows || []; total.value = res.total || 0;
  } finally { loading.value = false; }
}
function resetQuery() { queryParams.value = { uid: "", role: "", city: "", status: "", is_verified: "", page_num: 1, page_size: 20 }; handleQuery(); }
function handleSizeChange(size) { queryParams.value.page_size = size; handleQuery(); }
function handleDetail(row) { ElMessage.info("用户详情: " + row.uid); }
async function handleToggleStatus(row) {
  const newStatus = row.status === "0" ? "1" : "0";
  await ElMessageBox.confirm(`确定${newStatus === "1" ? "禁用" : "启用"}该用户？`, "提示");
  await updateYuepaiUserStatus(row.id, newStatus);
  ElMessage.success("操作成功"); handleQuery();
}
async function handleVerify(row) {
  await ElMessageBox.confirm("确定通过该用户的实名认证？", "认证审核");
  await auditYuepaiVerify(row.id, "1");
  ElMessage.success("认证通过"); handleQuery();
}
onMounted(() => handleQuery());
</script>
