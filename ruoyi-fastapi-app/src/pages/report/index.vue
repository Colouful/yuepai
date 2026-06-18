<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">举报投诉</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">举报类型</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="t in types" :key="t" class="rounded-xl px-4 py-2 text-xs font-medium transition-colors"
            :class="selected === t ? 'bg-gradient-to-r from-rose-400 to-violet-400 text-white' : 'bg-rose-50 text-slate-600'"
            @click="selected = t">{{ t }}</view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">详细说明</text>
        <textarea placeholder="请描述具体情况..." placeholder-class="text-slate-300"
          class="h-28 w-full rounded-xl bg-rose-50/50 p-4 text-sm text-slate-700 ring-1 ring-rose-100"></textarea>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold active:scale-[0.98] transition-transform">提交举报</button>
    </view>
  </view>
</template>
<script setup>
import { ref } from "vue";
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
const types = ["色情低俗","诈骗","骚扰","虚假资料","作品盗用","私下交易","服务态度","爽约"];
const selected = ref("");
</script>
