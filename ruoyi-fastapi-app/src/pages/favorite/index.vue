<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">我的收藏</text>
      <view class="mt-3 flex space-x-1">
        <view v-for="tab in tabs" :key="tab" class="flex-1 text-center py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'text-amber-600 border-b-2 border-amber-500' : 'text-slate-400'"
          @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="item in favorites" :key="item.title"
          class="flex items-center space-x-3 rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform">
          <view class="size-14 rounded-xl bg-slate-200 shrink-0"></view>
          <view class="flex-1 min-w-0">
            <text class="text-sm font-semibold text-slate-800 block truncate">{{ item.title }}</text>
            <text class="text-xs text-slate-400 block mt-0.5">{{ item.desc }}</text>
          </view>
          <view class="i-lucide-heart text-rose-400 text-sm"></view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const tabs = ["摄影师", "作品", "场地", "活动"];
const activeTab = ref("摄影师");
const favorites = ref([
  { title: "林默 · 人像摄影", desc: "北京 · 4.9分 · 326单" },
  { title: "苏晴 · 婚纱摄影", desc: "上海 · 4.8分 · 218单" },
  { title: "光圈摄影棚", desc: "北京朝阳 · 4.9分 · ¥200/小时" },
]);
</script>