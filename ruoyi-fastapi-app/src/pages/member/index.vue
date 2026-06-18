<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-gradient-to-br from-rose-400 to-violet-400 px-5 pt-14 pb-8 text-white relative overflow-hidden">
      <view class="absolute -right-10 -top-10 size-40 rounded-full bg-white/10 blur-3xl"></view>
      <text class="text-sm opacity-80">当前会员</text>
      <text class="text-2xl font-bold block mt-1">银卡会员</text>
      <text class="text-xs opacity-60 block mt-1">有效期至 2026-12-31</text>
    </view>
    <view class="px-5 -mt-4 space-y-3">
      <view v-for="plan in plans" :key="plan.name" class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 shadow-sm flex items-center active:scale-[0.97] transition-transform"
        :class="selected === plan.name ? 'ring-2 ring-rose-400' : ''" @click="selected = plan.name">
        <view class="flex-1">
          <text class="text-sm font-bold text-slate-800">{{ plan.name }}</text>
          <text class="text-[10px] text-slate-400 block mt-0.5">{{ plan.desc }}</text>
        </view>
        <text class="text-lg font-bold text-rose-400">¥{{ plan.price }}<text class="text-[10px] text-slate-400">/{{ plan.period }}</text></text>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">
        立即开通
      </button>
    </view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const selected = ref("季卡");
const plans = [
  { name: "月卡", desc: "专属折扣 + 优先客服", price: 29, period: "月" },
  { name: "季卡", desc: "月卡权益 + 每月优惠券", price: 69, period: "季" },
  { name: "年卡", desc: "全部权益 + 专属客服 + 免费曝光", price: 199, period: "年" },
];
</script>
