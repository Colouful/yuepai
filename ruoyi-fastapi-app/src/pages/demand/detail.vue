<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">需求详情</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <view class="flex items-center space-x-2 mb-3">
          <view class="rounded-lg bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-500">付费</view>
          <text class="text-base font-bold text-slate-800">周末人像写真拍摄</text>
        </view>
        <view class="space-y-2">
          <view class="flex items-center space-x-2"><view class="i-lucide-tag text-rose-400 text-sm"></view><text class="text-xs text-slate-500">人像摄影</text></view>
          <view class="flex items-center space-x-2"><view class="i-lucide-map-pin text-rose-400 text-sm"></view><text class="text-xs text-slate-500">北京朝阳区三里屯</text></view>
          <view class="flex items-center space-x-2"><view class="i-lucide-calendar text-rose-400 text-sm"></view><text class="text-xs text-slate-500">6月20日 14:00 - 17:00</text></view>
          <view class="flex items-center space-x-2"><view class="i-lucide-users text-rose-400 text-sm"></view><text class="text-xs text-slate-500">12人已报名 / 限20人</text></view>
        </view>
        <view class="mt-4 flex items-center justify-between">
          <text class="text-2xl font-bold text-rose-400">¥500</text>
          <view class="text-[10px] text-slate-300">6月18日截止</view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">详细描述</text>
        <text class="text-xs text-slate-500 leading-relaxed">寻找一位擅长日系清新风格的摄影师，在三里屯附近拍摄一组个人写真。希望拍摄自然、清新的感觉，参考图片风格。需要提供10张精修照片，3天内交付。</text>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">参考图片</text>
        <view class="flex space-x-2">
          <view v-for="i in 3" :key="i" class="h-20 w-20 rounded-xl bg-gradient-to-br from-rose-100 to-violet-100"></view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">发布者</text>
        <view class="flex items-center space-x-3">
          <view class="size-10 rounded-full bg-gradient-to-br from-rose-300 to-violet-300 flex items-center justify-center text-white font-bold text-sm">雨</view>
          <view class="flex-1"><text class="text-sm font-semibold text-slate-700">小雨</text><text class="text-[10px] text-slate-400 block">已实名认证 · 3次发布</text></view>
        </view>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">
        立即报名
      </button>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
