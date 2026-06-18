<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="relative h-48 bg-gradient-to-br from-rose-300 to-violet-300">
      <view class="absolute top-12 left-5 z-10 size-8 rounded-full bg-white/80 flex items-center justify-center" @click="goBack">
        <view class="i-lucide-arrow-left text-slate-700 text-sm"></view>
      </view>
    </view>
    <view class="px-5 -mt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-lg font-bold text-slate-800 block">光圈摄影棚</text>
        <text class="text-xs text-slate-400 block mt-1">摄影棚 · 北京朝阳区 · 4.9分 · 128条评价</text>
        <view class="flex items-center space-x-4 mt-3">
          <text class="text-2xl font-bold text-rose-400">¥200<text class="text-xs text-slate-400">/小时</text></text>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">场地设施</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="f in ['灯光设备','空调','化妆间','更衣室','停车场','WiFi']" :key="f"
            class="rounded-full bg-rose-50 px-3 py-1 text-[10px] text-rose-500">{{ f }}</view>
        </view>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">立即预约</button>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
