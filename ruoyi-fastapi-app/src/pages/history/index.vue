<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3 flex items-center justify-between">
      <text class="text-xl font-bold tracking-tight text-slate-800">浏览记录</text>
      <text class="text-xs text-rose-400">清空</text>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-2">
        <view v-for="item in records" :key="item.title" class="flex items-center space-x-3 rounded-2xl bg-white/80 backdrop-blur-sm p-3.5 shadow-sm">
          <view class="size-14 rounded-xl bg-gradient-to-br from-rose-100 to-violet-100 shrink-0"></view>
          <view class="flex-1 min-w-0"><text class="text-sm font-semibold text-slate-800 block truncate">{{ item.title }}</text><text class="text-[10px] text-slate-400 block mt-0.5">{{ item.time }}</text></view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const records = ref([
  { title: "林默 · 人像写真作品集", time: "2小时前" },
  { title: "光圈摄影棚 · 场地详情", time: "昨天" },
  { title: "古风汉服互勉创作 · 需求详情", time: "2天前" },
]);
</script>
