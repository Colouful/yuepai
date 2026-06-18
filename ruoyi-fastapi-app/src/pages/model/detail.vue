<template>
  <view class="min-h-screen bg-gradient-to-br from-sky-50 via-cyan-50 to-emerald-50">
    <view class="relative h-56 bg-gradient-to-br from-sky-400 to-emerald-400">
      <view class="absolute inset-0 bg-black/10"></view>
      <view class="absolute top-12 left-5 z-10" @click="goBack">
        <view class="i-lucide-arrow-left text-white text-xl"></view>
      </view>
      <view class="absolute bottom-0 left-0 right-0 px-5 pb-4 z-10 flex items-end space-x-4">
        <view class="size-20 rounded-3xl bg-white shadow-xl flex items-center justify-center text-3xl font-bold text-sky-400 border-4 border-white/50">雨</view>
        <view class="flex-1 pb-1">
          <view class="flex items-center space-x-2">
            <text class="text-xl font-bold text-white">小雨</text>
            <view class="i-lucide-badge-check text-amber-300 text-lg"></view>
          </view>
          <text class="text-sm text-white/80 block">168cm · 人像写真 · 北京</text>
          <text class="text-xs text-white/70 mt-0.5 block">56次合作 · 4.9分 · 接受互勉</text>
        </view>
      </view>
    </view>
    <view class="px-5 py-4 flex space-x-3 bg-white/80 backdrop-blur-sm">
      <view class="flex-1 h-10 rounded-xl bg-gradient-to-r from-sky-400 to-emerald-400 text-white flex items-center justify-center text-sm font-semibold active:scale-95 transition-transform">邀请约拍</view>
      <view class="h-10 w-10 rounded-xl bg-violet-50 flex items-center justify-center text-violet-400 active:scale-95 transition-transform">
        <view class="i-lucide-message-circle text-lg"></view>
      </view>
      <view class="h-10 w-10 rounded-xl bg-rose-50 flex items-center justify-center text-rose-400 active:scale-95 transition-transform">
        <view class="i-lucide-heart text-lg"></view>
      </view>
    </view>
    <view class="px-5 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">基本资料</text>
        <view class="grid grid-cols-3 gap-3">
          <view v-for="info in [{l:'身高',v:'168cm'},{l:'体重',v:'50kg'},{l:'鞋码',v:'37'},{l:'风格',v:'清新日系'},{l:'城市',v:'北京'},{l:'可约',v:'周末'}]" :key="info.l"
            class="text-center rounded-xl bg-sky-50/50 py-2">
            <text class="text-[10px] text-slate-400 block">{{ info.l }}</text>
            <text class="text-xs font-semibold text-slate-700 block mt-0.5">{{ info.v }}</text>
          </view>
        </view>
      </view>
      <view>
        <text class="text-sm font-bold text-slate-700 block mb-3">模卡作品</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="i in 6" :key="i" class="h-28 w-[31%] rounded-xl bg-gradient-to-br from-sky-100 to-emerald-100"></view>
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