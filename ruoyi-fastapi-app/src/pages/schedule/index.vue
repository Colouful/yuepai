<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">档期管理</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <!-- Month -->
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <view class="flex items-center justify-between mb-4">
          <view class="i-lucide-chevron-left text-rose-400"></view>
          <text class="text-base font-bold text-slate-800">2026年6月</text>
          <view class="i-lucide-chevron-right text-rose-400"></view>
        </view>
        <view class="grid grid-cols-7 gap-1 text-center">
          <view v-for="d in ['一','二','三','四','五','六','日']" :key="d" class="text-[10px] text-slate-400 py-1">{{ d }}</view>
          <view v-for="day in 30" :key="day" class="py-2 rounded-lg text-xs"
            :class="day === 20 ? 'bg-gradient-to-r from-rose-400 to-violet-400 text-white font-bold' : day < 18 ? 'text-slate-300' : 'text-slate-600'">
            {{ day }}
          </view>
        </view>
      </view>
      <!-- Legend -->
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">图例</text>
        <view class="flex flex-wrap gap-4">
          <view class="flex items-center space-x-1.5"><view class="size-3 rounded-full bg-gradient-to-r from-rose-400 to-violet-400"></view><text class="text-[10px] text-slate-500">已预约</text></view>
          <view class="flex items-center space-x-1.5"><view class="size-3 rounded-full bg-emerald-400"></view><text class="text-[10px] text-slate-500">可预约</text></view>
          <view class="flex items-center space-x-1.5"><view class="size-3 rounded-full bg-slate-200"></view><text class="text-[10px] text-slate-500">不可约</text></view>
        </view>
      </view>
      <!-- Today -->
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">6月20日 安排</text>
        <view class="rounded-xl bg-rose-50 p-3 flex items-center space-x-3">
          <view class="size-10 rounded-xl bg-gradient-to-r from-rose-400 to-violet-400 flex items-center justify-center text-white text-xs font-bold">14:00</view>
          <view class="flex-1"><text class="text-sm font-semibold text-slate-700">人像写真拍摄</text><text class="text-[10px] text-slate-400 block">客户: 小雨 · 三里屯</text></view>
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
