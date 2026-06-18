<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">报价详情</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 p-5 text-white shadow-lg shadow-rose-200/30">
        <text class="text-xs opacity-80">摄影师报价</text>
        <text class="text-3xl font-bold block mt-1">¥1,200</text>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm space-y-3">
        <view class="flex justify-between"><text class="text-xs text-slate-400">拍摄费用</text><text class="text-xs text-slate-700">¥800</text></view>
        <view class="flex justify-between"><text class="text-xs text-slate-400">化妆费用</text><text class="text-xs text-slate-700">¥200</text></view>
        <view class="flex justify-between"><text class="text-xs text-slate-400">服装租赁</text><text class="text-xs text-slate-700">¥200</text></view>
        <view class="h-px bg-rose-100"></view>
        <view class="flex justify-between"><text class="text-xs text-slate-400">交付内容</text><text class="text-xs text-slate-700">30张精修 + 全部原片</text></view>
        <view class="flex justify-between"><text class="text-xs text-slate-400">交付周期</text><text class="text-xs text-slate-700">3个工作日</text></view>
      </view>
      <view class="flex space-x-3">
        <view class="flex-1 h-11 rounded-xl bg-white text-slate-700 flex items-center justify-center text-sm font-semibold ring-1 ring-rose-200 active:scale-95 transition-transform">议价</view>
        <view class="flex-1 h-11 rounded-xl bg-gradient-to-r from-rose-400 to-violet-400 text-white flex items-center justify-center text-sm font-semibold active:scale-95 transition-transform">接受报价</view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
