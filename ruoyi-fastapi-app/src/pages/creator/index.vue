<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-gradient-to-br from-rose-400 to-violet-400 px-5 pt-14 pb-6 text-white">
      <text class="text-lg font-bold">创作者工作台</text>
      <view class="mt-4 grid grid-cols-4 gap-2">
        <view v-for="stat in stats" :key="stat.label" class="text-center">
          <text class="text-xl font-bold block">{{ stat.value }}</text>
          <text class="text-[10px] opacity-70 block">{{ stat.label }}</text>
        </view>
      </view>
    </view>
    <view class="px-5 -mt-3 pb-24 space-y-3">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 shadow-sm">
        <text class="text-sm font-bold text-slate-700 block mb-3">待处理</text>
        <view class="grid grid-cols-3 gap-2">
          <view v-for="item in pending" :key="item.label" class="text-center rounded-xl bg-rose-50 p-3 active:scale-95 transition-transform">
            <text class="text-lg font-bold text-rose-500 block">{{ item.value }}</text>
            <text class="text-[10px] text-slate-500 block mt-0.5">{{ item.label }}</text>
          </view>
        </view>
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm">
        <view v-for="action in actions" :key="action.label" class="flex items-center justify-between px-4 py-3.5 border-b border-rose-50 active:bg-rose-50/50 transition-colors">
          <view class="flex items-center space-x-3">
            <view class="size-9 rounded-xl flex items-center justify-center text-white" :class="action.bg">
              <view :class="action.icon" class="text-sm"></view>
            </view>
            <text class="text-sm text-slate-700">{{ action.label }}</text>
          </view>
          <view class="i-lucide-chevron-right text-rose-300 text-sm"></view>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
const stats = [
  { value: "¥3,680", label: "本月收入" },
  { value: "326", label: "总订单" },
  { value: "4.9", label: "评分" },
  { value: "98%", label: "回复率" },
];
const pending = [
  { value: 3, label: "待接单" },
  { value: 2, label: "待交付" },
  { value: 5, label: "待回复" },
];
const actions = [
  { label: "服务管理", icon: "i-lucide-package", bg: "bg-gradient-to-br from-rose-400 to-pink-400" },
  { label: "作品管理", icon: "i-lucide-images", bg: "bg-gradient-to-br from-violet-400 to-purple-400" },
  { label: "档期管理", icon: "i-lucide-calendar", bg: "bg-gradient-to-br from-sky-400 to-cyan-400" },
  { label: "客户管理", icon: "i-lucide-users", bg: "bg-gradient-to-br from-emerald-400 to-teal-400" },
  { label: "数据分析", icon: "i-lucide-bar-chart-3", bg: "bg-gradient-to-br from-amber-400 to-orange-400" },
  { label: "收入提现", icon: "i-lucide-wallet", bg: "bg-gradient-to-br from-pink-400 to-rose-400" },
];
</script>
