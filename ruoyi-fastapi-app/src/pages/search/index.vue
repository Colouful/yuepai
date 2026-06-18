<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3 flex items-center space-x-2">
      <view class="i-lucide-arrow-left text-slate-700 text-xl" @click="goBack"></view>
      <view class="flex-1 relative">
        <view class="absolute left-3 top-0 bottom-0 flex items-center text-rose-300"><view class="i-lucide-search text-base"></view></view>
        <input placeholder="搜索摄影师、模特、作品..." placeholder-class="text-slate-300" focus
          class="w-full h-9 rounded-xl bg-rose-50/50 pl-9 pr-4 text-sm text-slate-700" />
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="mb-4">
        <view class="flex items-center justify-between mb-2">
          <text class="text-xs font-bold text-rose-400">搜索历史</text>
          <text class="text-[10px] text-slate-300">清空</text>
        </view>
        <view class="flex flex-wrap gap-2">
          <view v-for="h in ['人像写真','婚纱摄影','古风','北京摄影师']" :key="h"
            class="rounded-xl bg-white/80 px-3 py-1.5 text-[11px] text-slate-500 shadow-sm">{{ h }}</view>
        </view>
      </view>
      <view>
        <text class="text-xs font-bold text-rose-400 block mb-2">热门搜索</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="(h,i) in ['写真','婚纱','旅拍','证件照','互勉','汉服','情侣','闺蜜']" :key="h"
            class="rounded-xl px-3 py-1.5 text-[11px] font-medium shadow-sm"
            :class="i < 3 ? 'bg-gradient-to-r from-rose-400 to-violet-400 text-white' : 'bg-white/80 text-slate-500'">{{ h }}</view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
