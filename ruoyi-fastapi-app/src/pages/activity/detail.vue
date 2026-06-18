<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="relative h-48 bg-gradient-to-br from-rose-300 to-violet-300">
      <view class="absolute top-12 left-5 z-10 size-8 rounded-full bg-white/80 flex items-center justify-center" @click="goBack">
        <view class="i-lucide-arrow-left text-slate-700 text-sm"></view>
      </view>
      <view class="absolute bottom-3 left-5 rounded-lg bg-amber-400 px-2 py-1 text-[10px] font-bold text-white">外拍</view>
    </view>
    <view class="px-5 -mt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-lg font-bold text-slate-800 block">城市夜景人像外拍</text>
        <view class="mt-3 space-y-2">
          <view class="flex items-center space-x-2"><view class="i-lucide-map-pin text-rose-400 text-sm"></view><text class="text-xs text-slate-500">北京 · 国贸CBD</text></view>
          <view class="flex items-center space-x-2"><view class="i-lucide-calendar text-rose-400 text-sm"></view><text class="text-xs text-slate-500">6月22日 19:00 - 22:00</text></view>
          <view class="flex items-center space-x-2"><view class="i-lucide-users text-rose-400 text-sm"></view><text class="text-xs text-slate-500">12/20人已报名</text></view>
        </view>
        <text class="text-2xl font-bold text-rose-400 block mt-3">免费</text>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">活动介绍</text>
        <text class="text-xs text-slate-500 leading-relaxed">一起拍摄城市夜景人像，学习夜景拍摄技巧。自带相机和三脚架，模特由组织方提供。限20人，先到先得。</text>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">立即报名</button>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
