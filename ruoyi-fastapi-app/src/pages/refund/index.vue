<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">退款售后</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">退款原因</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="r in reasons" :key="r" class="rounded-xl px-4 py-2 text-xs font-medium"
            :class="selected === r ? 'bg-gradient-to-r from-rose-400 to-violet-400 text-white' : 'bg-rose-50 text-slate-600'"
            @click="selected = r">{{ r }}</view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">补充说明</text>
        <textarea placeholder="请详细描述退款原因..." placeholder-class="text-slate-300"
          class="h-24 w-full rounded-xl bg-rose-50/50 p-4 text-sm text-slate-700 ring-1 ring-rose-100"></textarea>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <view class="flex justify-between"><text class="text-xs text-slate-400">退款金额</text><text class="text-lg font-bold text-rose-400">¥500.00</text></view>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold active:scale-[0.98] transition-transform">提交退款申请</button>
    </view>
  </view>
</template>
<script setup>
import { ref } from "vue";
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
const reasons = ["服务者无法履约","临时取消","服务与描述不符","作品质量不满意","双方协商取消","天气原因"];
const selected = ref("");
</script>
