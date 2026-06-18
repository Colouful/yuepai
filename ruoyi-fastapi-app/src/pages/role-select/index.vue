<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50 flex flex-col items-center justify-center px-6 pb-20">
    <view class="mb-8 text-center">
      <view class="size-20 rounded-3xl bg-gradient-to-br from-rose-400 to-violet-400 mx-auto flex items-center justify-center shadow-lg shadow-rose-200/50 mb-4">
        <view class="i-lucide-camera text-white text-4xl"></view>
      </view>
      <text class="text-2xl font-bold tracking-tight text-slate-800">欢迎加入约拍</text>
      <text class="text-sm text-slate-400 mt-1 block">选择你的身份，开始创作之旅</text>
    </view>
    <view class="w-full space-y-3">
      <view v-for="role in roles" :key="role.name"
        class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 flex items-center space-x-4 active:scale-[0.97] transition-all duration-200 shadow-sm"
        :class="selected === role.name ? 'ring-2 ring-rose-400 shadow-rose-100' : ''"
        @click="selected = role.name">
        <view class="size-12 rounded-2xl flex items-center justify-center text-white" :class="role.bg">
          <view :class="role.icon" class="text-xl"></view>
        </view>
        <view class="flex-1">
          <text class="text-sm font-bold text-slate-800 block">{{ role.name }}</text>
          <text class="text-[11px] text-slate-400 block mt-0.5">{{ role.desc }}</text>
        </view>
        <view v-if="selected === role.name" class="i-lucide-check-circle text-rose-400 text-xl"></view>
      </view>
    </view>
    <button class="mt-8 w-full h-12 rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">
      开始探索
    </button>
  </view>
</template>
<script setup>
import { ref } from "vue";
const selected = ref("找摄影师");
const roles = [
  { name: "找摄影师", desc: "寻找专业摄影师记录美好瞬间", icon: "i-lucide-search", bg: "bg-gradient-to-br from-rose-400 to-pink-400" },
  { name: "摄影师", desc: "展示作品，接单约拍", icon: "i-lucide-camera", bg: "bg-gradient-to-br from-violet-400 to-purple-400" },
  { name: "模特", desc: "发布模卡，接受拍摄邀请", icon: "i-lucide-user", bg: "bg-gradient-to-br from-sky-400 to-cyan-400" },
  { name: "化妆师", desc: "展示妆造案例，提供妆造服务", icon: "i-lucide-palette", bg: "bg-gradient-to-br from-emerald-400 to-teal-400" },
  { name: "商家", desc: "摄影工作室/场地/婚纱馆", icon: "i-lucide-store", bg: "bg-gradient-to-br from-amber-400 to-orange-400" },
  { name: "普通用户", desc: "浏览作品，发现灵感", icon: "i-lucide-heart", bg: "bg-gradient-to-br from-pink-400 to-rose-400" },
];
</script>