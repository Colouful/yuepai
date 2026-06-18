<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center justify-between">
      <view class="i-lucide-arrow-left text-slate-700 text-xl" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">发布动态</text>
      <view class="rounded-full bg-gradient-to-r from-rose-400 to-violet-400 px-4 py-1.5 text-xs font-semibold text-white">发布</view>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <textarea placeholder="分享你的拍摄故事..." placeholder-class="text-slate-300"
        class="h-32 w-full rounded-2xl bg-white/80 backdrop-blur-sm p-4 text-sm text-slate-700 shadow-sm"></textarea>
      <view class="flex flex-wrap gap-2">
        <view class="h-24 w-24 rounded-xl bg-gradient-to-br from-rose-100 to-violet-100 flex items-center justify-center">
          <view class="i-lucide-plus text-rose-300 text-2xl"></view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 shadow-sm space-y-3">
        <view class="flex items-center justify-between">
          <view class="flex items-center space-x-2"><view class="i-lucide-map-pin text-rose-400 text-sm"></view><text class="text-xs text-slate-500">添加位置</text></view>
          <view class="i-lucide-chevron-right text-slate-300 text-sm"></view>
        </view>
        <view class="flex items-center justify-between">
          <view class="flex items-center space-x-2"><view class="i-lucide-tag text-rose-400 text-sm"></view><text class="text-xs text-slate-500">添加话题</text></view>
          <view class="i-lucide-chevron-right text-slate-300 text-sm"></view>
        </view>
        <view class="flex items-center justify-between">
          <view class="flex items-center space-x-2"><view class="i-lucide-users text-rose-400 text-sm"></view><text class="text-xs text-slate-500">@提及的人</text></view>
          <view class="i-lucide-chevron-right text-slate-300 text-sm"></view>
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
