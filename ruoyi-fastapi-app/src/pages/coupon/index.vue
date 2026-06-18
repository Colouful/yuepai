<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-800">我的优惠券</text>
      <view class="mt-3 flex space-x-1">
        <view v-for="tab in ['可使用','已使用','已过期']" :key="tab" class="flex-1 text-center py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'text-rose-500 border-b-2 border-rose-400' : 'text-slate-400'" @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="c in coupons" :key="c.title" class="rounded-2xl overflow-hidden shadow-sm">
          <view class="bg-gradient-to-r from-rose-400 to-violet-400 p-4 text-white flex items-center">
            <view class="mr-4"><text class="text-3xl font-bold">¥{{ c.amount }}</text><text class="text-[10px] opacity-80 block">满{{ c.min }}可用</text></view>
            <view class="flex-1"><text class="text-sm font-semibold">{{ c.title }}</text><text class="text-[10px] opacity-80 block mt-0.5">{{ c.desc }}</text><text class="text-[10px] opacity-60 block mt-0.5">{{ c.expire }}</text></view>
            <view class="rounded-full bg-white/20 px-4 py-1.5 text-xs font-semibold">使用</view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const activeTab = ref("可使用");
const coupons = ref([
  { amount: 50, min: 200, title: "新人专享券", desc: "全品类可用", expire: "2026-07-31过期" },
  { amount: 100, min: 500, title: "写真满减券", desc: "人像写真可用", expire: "2026-06-30过期" },
  { amount: 200, min: 1000, title: "婚纱专享券", desc: "婚纱摄影可用", expire: "2026-08-31过期" },
]);
</script>
