<template>
  <div class="app-container">
    <el-form :inline="true" :model="queryParams">
      <el-form-item label="订单号"><el-input v-model="queryParams.order_no" clearable /></el-form-item>
      <el-form-item label="状态"><el-select v-model="queryParams.status" clearable><el-option v-for="s in statusList" :key="s.value" :label="s.label" :value="s.value" /></el-select></el-form-item>
      <el-form-item><el-button type="primary" @click="handleQuery">搜索</el-button></el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="订单号" prop="order_no" width="170" />
      <el-table-column label="总金额" width="100" align="right"><template #default="{row}">¥{{ row.total_amount }}</template></el-table-column>
      <el-table-column label="定金" width="90" align="right"><template #default="{row}">¥{{ row.deposit_amount }}</template></el-table-column>
      <el-table-column label="平台佣金" width="100" align="right"><template #default="{row}">¥{{ row.platform_fee }}</template></el-table-column>
      <el-table-column label="摄影师收入" width="110" align="right"><template #default="{row}">¥{{ row.photographer_income }}</template></el-table-column>
      <el-table-column label="拍摄日期" width="120"><template #default="{row}">{{ row.shooting_date?.slice(0,10) }}</template></el-table-column>
      <el-table-column label="状态" width="100" align="center"><template #default="{row}"><el-tag :type="statusTag(row.status)">{{ statusText(row.status) }}</el-tag></template></el-table-column>
      <el-table-column label="创建时间" prop="create_time" width="160" />
    </el-table>
    <el-pagination v-model:current-page="queryParams.page_num" :total="total" :page-size="20" layout="total, prev, pager, next" @current-change="handleQuery" />
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { getYuepaiOrderList } from "@/api/yuepai/order";
const statusList = [{label:"待付定金",value:"0"},{label:"已付定金",value:"1"},{label:"拍摄中",value:"2"},{label:"已完成",value:"4"},{label:"已取消",value:"5"},{label:"退款中",value:"6"}];
const statusText = (s) => ({0:"待付定金",1:"已付定金",2:"拍摄中",3:"待付尾款",4:"已完成",5:"已取消",6:"退款中"}[s]||"未知");
const statusTag = (s) => ({0:"warning",1:"primary",2:"",4:"success",5:"info",6:"danger"}[s]);
const loading=ref(false);const list=ref([]);const total=ref(0);
const queryParams=ref({order_no:"",status:"",page_num:1,page_size:20});
async function handleQuery(){loading.value=true;try{const res=await getYuepaiOrderList(queryParams.value);list.value=res.rows||[];total.value=res.total||0;}finally{loading.value=false;}}
onMounted(()=>handleQuery());
</script>
