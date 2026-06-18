<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">我的订单</text>
      <view class="mt-3 flex space-x-1">
        <view v-for="tab in tabs" :key="tab" class="flex-1 text-center py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'text-amber-600 border-b-2 border-amber-500' : 'text-slate-400'"
          @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="order in orders" :key="order.no"
          class="rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform">
          <view class="flex items-center justify-between mb-3">
            <text class="text-xs text-slate-400">订单号: {{ order.no }}</text>
            <view class="rounded-md px-2 py-0.5 text-[10px] font-semibold"
              :class="order.statusClass">{{ order.status }}</view>
          </view>
          <view class="flex items-center space-x-3">
            <view class="size-14 rounded-xl bg-slate-200 shrink-0"></view>
            <view class="flex-1">
              <text class="text-sm font-semibold text-slate-800">{{ order.title }}</text>
              <text class="text-xs text-slate-400 block mt-0.5">{{ order.photographer }} · {{ order.date }}</text>
            </view>
            <text class="text-base font-bold text-slate-800">¥{{ order.amount }}</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const tabs = ["全部", "待付款", "进行中", "待评价", "售后"];
const activeTab = ref("全部");
const orders = ref([
  { no: "YP20260617001", title: "人像写真拍摄", photographer: "林默", date: "6月20日", amount: 500, status: "待服务", statusClass: "bg-amber-50 text-amber-600" },
  { no: "YP20260615002", title: "婚纱照拍摄", photographer: "苏晴", date: "6月18日", amount: 2000, status: "已完成", statusClass: "bg-emerald-50 text-emerald-600" },
  { no: "YP20260610003", title: "证件照拍摄", photographer: "陈风", date: "6月12日", amount: 100, status: "待评价", statusClass: "bg-sky-50 text-sky-600" },
]);
</script>