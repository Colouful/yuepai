<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">摄影活动</text>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="act in activities" :key="act.title"
          class="rounded-2xl bg-white overflow-hidden active:scale-[0.98] transition-transform">
          <view class="h-40 bg-gradient-to-br from-slate-200 to-slate-300 relative">
            <view class="absolute top-3 left-3 rounded-lg bg-amber-500 px-2 py-1 text-[10px] font-bold text-white">{{ act.tag }}</view>
          </view>
          <view class="p-4">
            <text class="text-sm font-bold text-slate-800">{{ act.title }}</text>
            <view class="mt-2 flex items-center space-x-3">
              <view class="flex items-center space-x-1">
                <view class="i-lucide-map-pin text-slate-400 text-[10px]"></view>
                <text class="text-[10px] text-slate-400">{{ act.city }}</text>
              </view>
              <view class="flex items-center space-x-1">
                <view class="i-lucide-calendar text-slate-400 text-[10px]"></view>
                <text class="text-[10px] text-slate-400">{{ act.date }}</text>
              </view>
              <view class="flex items-center space-x-1">
                <view class="i-lucide-users text-slate-400 text-[10px]"></view>
                <text class="text-[10px] text-slate-400">{{ act.joined }}/{{ act.limit }}</text>
              </view>
            </view>
            <view class="mt-3 flex items-center justify-between">
              <text class="text-sm font-bold text-amber-600">{{ act.price }}</text>
              <view class="rounded-lg bg-amber-500 px-4 py-1.5 text-xs font-semibold text-white">立即报名</view>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const activities = ref([
  { title: "城市夜景人像外拍", tag: "外拍", city: "北京", date: "6月22日", joined: 12, limit: 20, price: "免费" },
  { title: "古风汉服摄影采风", tag: "采风", city: "杭州", date: "6月25日", joined: 8, limit: 15, price: "¥50" },
  { title: "摄影构图公开课", tag: "课程", city: "线上", date: "6月28日", joined: 156, limit: 500, price: "免费" },
]);
</script>