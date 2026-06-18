<template>
  <div class="app-container">
    <el-row :gutter="16">
      <el-col :span="6" v-for="card in cards" :key="card.label"><el-card shadow="hover"><el-statistic :title="card.label" :value="card.value" :suffix="card.suffix" /></el-card></el-col>
    </el-row>
    <el-card class="mt-4" header="数据趋势（待接入ECharts）">
      <el-empty description="图表功能开发中..." />
    </el-card>
  </div>
</template>
<script setup>
import { ref } from "vue";
const cards = ref([
  { label: "总用户", value: 0, suffix: "人" },
  { label: "总需求", value: 0, suffix: "条" },
  { label: "总订单", value: 0, suffix: "单" },
  { label: "总GMV", value: 0, suffix: "元" },
]);
</script>
