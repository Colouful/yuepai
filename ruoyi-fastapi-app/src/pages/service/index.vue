<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50 flex flex-col">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">在线客服</text>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 py-4 space-y-4" :show-scrollbar="false">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm text-center">
        <view class="i-lucide-headphones text-4xl text-rose-400 mb-3"></view>
        <text class="text-sm font-bold text-slate-800 block">智能客服</text>
        <text class="text-xs text-slate-400 block mt-1">常见问题快速解答</text>
      </view>
      <view class="space-y-2">
        <view v-for="q in questions" :key="q" class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 flex items-center justify-between shadow-sm active:scale-[0.98] transition-transform">
          <text class="text-xs text-slate-700">{{ q }}</text>
          <view class="i-lucide-chevron-right text-rose-300 text-sm"></view>
        </view>
      </view>
    </scroll-view>
    <view class="bg-white/80 backdrop-blur-sm px-5 py-3 border-t border-rose-100">
      <view class="flex items-center space-x-2">
        <input placeholder="输入您的问题..." placeholder-class="text-slate-300"
          class="flex-1 h-10 rounded-xl bg-rose-50/50 px-4 text-sm text-slate-700" />
        <view class="size-10 rounded-xl bg-gradient-to-r from-rose-400 to-violet-400 flex items-center justify-center">
          <view class="i-lucide-send text-white text-sm"></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
const questions = ["如何发布约拍？","如何申请退款？","如何认证摄影师？","如何上传作品？","如何提现？"];
</script>
