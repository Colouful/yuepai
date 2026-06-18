<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-gradient-to-br from-slate-800 to-slate-900 px-5 pt-14 pb-8 text-white">
      <text class="text-sm text-slate-400">总资产 (元)</text>
      <text class="text-3xl font-bold tracking-tight mt-1">¥ 3,680.00</text>
      <view class="mt-4 flex space-x-4">
        <view class="flex-1 rounded-xl bg-white/10 p-3">
          <text class="text-[10px] text-slate-400">可用余额</text>
          <text class="text-base font-bold block mt-0.5">¥ 2,180.00</text>
        </view>
        <view class="flex-1 rounded-xl bg-white/10 p-3">
          <text class="text-[10px] text-slate-400">待结算</text>
          <text class="text-base font-bold block mt-0.5">¥ 1,500.00</text>
        </view>
      </view>
    </view>
    <view class="px-5 pt-5 space-y-3">
      <view class="flex space-x-3">
        <view class="flex-1 h-11 rounded-xl bg-amber-500 flex items-center justify-center text-sm font-semibold text-white active:scale-95 transition-transform">提现</view>
        <view class="flex-1 h-11 rounded-xl bg-white flex items-center justify-center text-sm font-semibold text-slate-700 ring-1 ring-slate-200 active:scale-95 transition-transform">充值</view>
      </view>
      <view class="rounded-2xl bg-white">
        <view class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
          <text class="text-sm font-semibold text-slate-800">收支明细</text>
          <text class="text-xs text-slate-400">查看全部</text>
        </view>
        <view v-for="record in records" :key="record.title" class="px-4 py-3 border-b border-slate-50 flex items-center justify-between">
          <view>
            <text class="text-sm text-slate-700">{{ record.title }}</text>
            <text class="text-[10px] text-slate-400 block">{{ record.time }}</text>
          </view>
          <text class="text-sm font-semibold" :class="record.income ? 'text-emerald-600' : 'text-slate-800'">
            {{ record.income ? '+' : '-' }}¥{{ record.amount }}
          </text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const records = ref([
  { title: "人像写真订单结算", time: "2026-06-15", amount: "500.00", income: true },
  { title: "提现到银行卡", time: "2026-06-14", amount: "1,000.00", income: false },
  { title: "婚纱照订单定金", time: "2026-06-13", amount: "2,000.00", income: true },
]);
</script>