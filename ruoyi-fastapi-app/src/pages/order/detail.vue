<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">订单详情</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <!-- Status -->
      <view class="rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 p-5 text-white shadow-lg shadow-rose-200/30">
        <text class="text-lg font-bold">待服务</text>
        <text class="text-sm opacity-80 block mt-1">摄影师将在约定时间到达拍摄地点</text>
      </view>
      <!-- Info -->
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">服务信息</text>
        <view class="space-y-3">
          <view class="flex justify-between"><text class="text-xs text-slate-400">订单编号</text><text class="text-xs text-slate-700">YP20260617001</text></view>
          <view class="flex justify-between"><text class="text-xs text-slate-400">服务类型</text><text class="text-xs text-slate-700">人像写真拍摄</text></view>
          <view class="flex justify-between"><text class="text-xs text-slate-400">摄影师</text><text class="text-xs text-slate-700">林默</text></view>
          <view class="flex justify-between"><text class="text-xs text-slate-400">拍摄时间</text><text class="text-xs text-slate-700">6月20日 14:00</text></view>
          <view class="flex justify-between"><text class="text-xs text-slate-400">拍摄地点</text><text class="text-xs text-slate-700">北京朝阳三里屯</text></view>
        </view>
      </view>
      <!-- Fee -->
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">费用明细</text>
        <view class="space-y-2">
          <view class="flex justify-between"><text class="text-xs text-slate-400">服务费用</text><text class="text-xs text-slate-700">¥500.00</text></view>
          <view class="flex justify-between"><text class="text-xs text-slate-400">平台服务费</text><text class="text-xs text-slate-700">¥25.00</text></view>
          <view class="h-px bg-rose-100 my-1"></view>
          <view class="flex justify-between"><text class="text-sm font-bold text-slate-700">合计</text><text class="text-lg font-bold text-rose-400">¥525.00</text></view>
        </view>
      </view>
      <view class="flex space-x-3">
        <view class="flex-1 h-11 rounded-xl bg-white text-slate-700 flex items-center justify-center text-sm font-semibold ring-1 ring-rose-200 active:scale-95 transition-transform">联系摄影师</view>
        <view class="flex-1 h-11 rounded-xl bg-gradient-to-r from-rose-400 to-violet-400 text-white flex items-center justify-center text-sm font-semibold active:scale-95 transition-transform">确认完成</view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
