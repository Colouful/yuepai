<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-800">我的关注</text>
      <view class="mt-3 flex space-x-1">
        <view v-for="tab in ['关注','粉丝','互关']" :key="tab" class="flex-1 text-center py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'text-rose-500 border-b-2 border-rose-400' : 'text-slate-400'" @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-2">
        <view v-for="u in users" :key="u.name" class="flex items-center space-x-3 rounded-2xl bg-white/80 backdrop-blur-sm p-3.5 shadow-sm">
          <view class="size-11 rounded-full bg-gradient-to-br from-rose-300 to-violet-300 flex items-center justify-center text-white font-bold text-sm">{{ u.name[0] }}</view>
          <view class="flex-1"><text class="text-sm font-semibold text-slate-800">{{ u.name }}</text><text class="text-[10px] text-slate-400 block">{{ u.desc }}</text></view>
          <view class="rounded-full px-3 py-1 text-[10px] font-medium" :class="u.followed ? 'bg-slate-100 text-slate-400' : 'bg-gradient-to-r from-rose-400 to-violet-400 text-white'">
            {{ u.followed ? '已关注' : '+ 关注' }}</view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const activeTab = ref("关注");
const users = ref([
  { name: "林默", desc: "人像摄影 · 北京 · 4.9分", followed: true },
  { name: "苏晴", desc: "婚纱摄影 · 上海 · 4.8分", followed: true },
  { name: "陈风", desc: "商业摄影 · 广州 · 4.7分", followed: false },
]);
</script>
