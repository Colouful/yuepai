<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">评价服务</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <view class="flex items-center space-x-3 mb-4">
          <view class="size-12 rounded-xl bg-gradient-to-br from-rose-200 to-violet-200"></view>
          <view><text class="text-sm font-bold text-slate-800">人像写真拍摄</text><text class="text-xs text-slate-400 block">摄影师: 林默</text></view>
        </view>
        <view v-for="dim in dimensions" :key="dim.name" class="flex items-center justify-between mb-3">
          <text class="text-xs text-slate-500 w-20">{{ dim.name }}</text>
          <view class="flex space-x-1">
            <view v-for="i in 5" :key="i" class="i-lucide-star text-lg transition-colors"
              :class="i <= dim.score ? 'text-amber-400' : 'text-slate-200'" @click="dim.score = i"></view>
          </view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">评价内容</text>
        <textarea placeholder="分享你的拍摄体验..." placeholder-class="text-slate-300"
          class="h-28 w-full rounded-xl bg-rose-50/50 p-4 text-sm text-slate-700 ring-1 ring-rose-100"></textarea>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">
        提交评价
      </button>
    </view>
  </view>
</template>
<script setup>
import { ref, reactive } from "vue";
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
const dimensions = reactive([
  { name: "服务态度", score: 5 },
  { name: "专业能力", score: 5 },
  { name: "成片质量", score: 5 },
  { name: "准时程度", score: 5 },
  { name: "性价比", score: 4 },
]);
</script>
