<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">确认订单</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <view class="flex items-center space-x-3">
          <view class="size-16 rounded-xl bg-gradient-to-br from-rose-200 to-violet-200"></view>
          <view class="flex-1">
            <text class="text-sm font-bold text-slate-800">精致人像写真</text>
            <text class="text-xs text-slate-400 block mt-0.5">摄影师: 林默 · 3小时拍摄</text>
            <text class="text-xs text-slate-400 block">含化妆 · 30张精修</text>
          </view>
          <text class="text-lg font-bold text-rose-400">¥1200</text>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm space-y-3">
        <view class="flex justify-between"><text class="text-xs text-slate-400">拍摄日期</text><text class="text-xs text-slate-700">6月20日 14:00</text></view>
        <view class="flex justify-between"><text class="text-xs text-slate-400">拍摄地点</text><text class="text-xs text-slate-700">北京朝阳三里屯</text></view>
        <view class="flex justify-between"><text class="text-xs text-slate-400">优惠券</text><text class="text-xs text-rose-400">新人立减50元</text></view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <view class="space-y-2">
          <view class="flex justify-between"><text class="text-xs text-slate-400">服务费用</text><text class="text-xs text-slate-700">¥1200.00</text></view>
          <view class="flex justify-between"><text class="text-xs text-slate-400">优惠金额</text><text class="text-xs text-emerald-500">-¥50.00</text></view>
          <view class="flex justify-between"><text class="text-xs text-slate-400">平台服务费</text><text class="text-xs text-slate-700">¥57.50</text></view>
          <view class="h-px bg-rose-100 my-1"></view>
          <view class="flex justify-between"><text class="text-sm font-bold text-slate-700">需支付</text><text class="text-xl font-bold text-rose-400">¥1207.50</text></view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <view class="flex items-center space-x-2">
          <view class="i-lucide-shield text-emerald-400 text-sm"></view>
          <text class="text-[10px] text-slate-400">平台资金担保 · 服务完成确认后结算</text>
        </view>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">
        立即支付 ¥1207.50
      </button>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
