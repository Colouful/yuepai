<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="relative h-48 bg-gradient-to-br from-rose-400 to-violet-400">
      <view class="absolute top-12 left-5 z-10 size-8 rounded-full bg-white/80 flex items-center justify-center" @click="goBack">
        <view class="i-lucide-arrow-left text-slate-700 text-sm"></view>
      </view>
      <view class="absolute bottom-0 left-0 right-0 px-5 pb-4 flex items-end space-x-4">
        <view class="size-16 rounded-2xl bg-white shadow-xl flex items-center justify-center text-2xl font-bold text-rose-400 border-4 border-white/50">雨</view>
        <view class="flex-1 pb-1">
          <text class="text-lg font-bold text-white">小雨</text>
          <text class="text-xs text-white/70 block">北京 · 普通用户 · 3次约拍</text>
        </view>
      </view>
    </view>
    <view class="px-5 py-4 flex space-x-3">
      <view class="flex-1 h-10 rounded-xl bg-gradient-to-r from-rose-400 to-violet-400 text-white flex items-center justify-center text-sm font-semibold active:scale-95 transition-transform">关注</view>
      <view class="h-10 w-10 rounded-xl bg-white flex items-center justify-center text-rose-400 ring-1 ring-rose-200 active:scale-95 transition-transform">
        <view class="i-lucide-message-circle text-lg"></view>
      </view>
    </view>
    <view class="px-5 pb-24 space-y-4">
      <view class="flex space-x-6 text-center">
        <view class="flex-1"><text class="text-lg font-bold text-slate-800 block">128</text><text class="text-[10px] text-slate-400">关注</text></view>
        <view class="flex-1"><text class="text-lg font-bold text-slate-800 block">56</text><text class="text-[10px] text-slate-400">粉丝</text></view>
        <view class="flex-1"><text class="text-lg font-bold text-slate-800 block">3</text><text class="text-[10px] text-slate-400">约拍</text></view>
      </view>
      <view>
        <text class="text-sm font-bold text-slate-700 block mb-3">收藏的作品</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="i in 6" :key="i" class="h-28 w-[31%] rounded-xl bg-gradient-to-br from-rose-100 to-violet-100"></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
