<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-800">约拍管理</text>
      <view class="mt-3 flex space-x-1">
        <view v-for="tab in ['我发布的','我报名的','收到的报名']" :key="tab"
          class="flex-1 text-center py-1.5 text-[11px] font-medium transition-colors"
          :class="activeTab === tab ? 'text-rose-500 border-b-2 border-rose-400' : 'text-slate-400'"
          @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="d in demands" :key="d.title" class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 shadow-sm">
          <view class="flex items-center space-x-2 mb-2">
            <view class="rounded-md px-1.5 py-0.5 text-[10px] font-semibold bg-rose-100 text-rose-500">{{ d.status }}</view>
            <text class="text-sm font-bold text-slate-800">{{ d.title }}</text>
          </view>
          <text class="text-[10px] text-slate-400 block">{{ d.date }} · {{ d.apply }}人报名</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const activeTab = ref("我发布的");
const demands = ref([
  { title: "周末人像写真", date: "6月20日", apply: 12, status: "进行中" },
  { title: "古风汉服创作", date: "6月22日", apply: 8, status: "已截止" },
]);
</script>
