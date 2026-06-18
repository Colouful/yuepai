<template>
  <div class="app-container">
    <el-row :gutter="16" class="mb-4">
      <el-col :span="8"><el-card shadow="hover"><el-statistic title="总订单数" :value="stats.total_orders||0" /></el-card></el-col>
      <el-col :span="8"><el-card shadow="hover"><el-statistic title="总交易额" :value="stats.total_amount||0" prefix="¥" /></el-card></el-col>
      <el-col :span="8"><el-card shadow="hover"><el-statistic title="平台佣金" :value="stats.total_fee||0" prefix="¥" /></el-card></el-col>
    </el-row>
    <el-card header="订单流水"><yp-order /></el-card>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { getYuepaiFinanceStats } from "@/api/yuepai/order";
import YpOrder from "../order/index.vue";
const stats = ref({});
onMounted(async () => { stats.value = await getYuepaiFinanceStats() || {}; });
</script>
