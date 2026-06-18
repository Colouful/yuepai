<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <!-- Header -->
    <view class="relative h-56 bg-gradient-to-br from-rose-400 to-violet-400">
      <view class="absolute inset-0 bg-black/10"></view>
      <view class="absolute top-12 left-5 z-10" @click="goBack">
        <view class="i-lucide-arrow-left text-white text-xl"></view>
      </view>
      <view class="absolute bottom-0 left-0 right-0 px-5 pb-4 z-10 flex items-end space-x-4">
        <view class="size-20 rounded-3xl bg-white shadow-xl flex items-center justify-center text-3xl font-bold text-rose-400 border-4 border-white/50">林</view>
        <view class="flex-1 pb-1">
          <view class="flex items-center space-x-2">
            <text class="text-xl font-bold text-white">林默</text>
            <view class="i-lucide-badge-check text-amber-300 text-lg"></view>
          </view>
          <text class="text-sm text-white/80 block">人像摄影 · 北京 · 从业5年</text>
          <view class="flex items-center space-x-3 mt-1">
            <text class="text-xs text-white/70">326单</text>
            <view class="flex items-center space-x-0.5">
              <view class="i-lucide-star text-amber-300 text-xs"></view>
              <text class="text-xs text-white/90 font-medium">4.9</text>
            </view>
            <text class="text-xs text-white/70">回复率 98%</text>
          </view>
        </view>
      </view>
    </view>
    <!-- Actions -->
    <view class="px-5 py-4 flex space-x-3 bg-white/80 backdrop-blur-sm">
      <view class="flex-1 h-10 rounded-xl bg-gradient-to-r from-rose-400 to-pink-400 text-white flex items-center justify-center text-sm font-semibold active:scale-95 transition-transform">立即预约</view>
      <view class="h-10 w-10 rounded-xl bg-violet-50 flex items-center justify-center text-violet-400 active:scale-95 transition-transform">
        <view class="i-lucide-message-circle text-lg"></view>
      </view>
      <view class="h-10 w-10 rounded-xl bg-rose-50 flex items-center justify-center text-rose-400 active:scale-95 transition-transform">
        <view class="i-lucide-heart text-lg"></view>
      </view>
    </view>
    <!-- Content -->
    <view class="px-5 pb-24 space-y-4">
      <!-- Tags -->
      <view class="flex flex-wrap gap-2">
        <view v-for="tag in ['人像','写真','婚纱','古风','旅拍']" :key="tag"
          class="rounded-full px-3 py-1 text-[11px] font-medium bg-white/80 text-rose-400 ring-1 ring-rose-100">{{ tag }}</view>
      </view>
      <!-- Intro -->
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">个人简介</text>
        <text class="text-xs text-slate-500 leading-relaxed">专注人像摄影5年，擅长日系清新、情绪写真风格。曾为多家杂志拍摄封面，作品多次获得摄影大赛奖项。用心记录每一个美好瞬间。</text>
      </view>
      <!-- Works -->
      <view>
        <text class="text-sm font-bold text-slate-700 block mb-3">代表作品</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="i in 6" :key="i" class="h-28 w-[31%] rounded-xl bg-gradient-to-br from-rose-100 to-violet-100"></view>
        </view>
      </view>
      <!-- Packages -->
      <view>
        <text class="text-sm font-bold text-slate-700 block mb-3">服务套餐</text>
        <view v-for="pkg in packages" :key="pkg.name" class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 mb-3 shadow-sm">
          <view class="flex items-center justify-between mb-2">
            <text class="text-sm font-bold text-slate-800">{{ pkg.name }}</text>
            <text class="text-base font-bold text-rose-400">¥{{ pkg.price }}</text>
          </view>
          <text class="text-xs text-slate-400">{{ pkg.desc }}</text>
          <view class="mt-3 flex items-center justify-between">
            <text class="text-[10px] text-slate-300">{{ pkg.duration }} · {{ pkg.photos }}</text>
            <view class="rounded-lg bg-gradient-to-r from-rose-400 to-pink-400 px-4 py-1.5 text-[10px] font-semibold text-white">预约</view>
          </view>
        </view>
      </view>
      <!-- Reviews -->
      <view>
        <text class="text-sm font-bold text-slate-700 block mb-3">用户评价 (128)</text>
        <view v-for="r in reviews" :key="r.name" class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 mb-3 shadow-sm">
          <view class="flex items-center space-x-2 mb-2">
            <view class="size-8 rounded-full bg-gradient-to-br from-rose-300 to-violet-300 flex items-center justify-center text-white text-xs font-bold">{{ r.name[0] }}</view>
            <text class="text-xs font-semibold text-slate-700">{{ r.name }}</text>
            <view class="flex space-x-0.5">
              <view v-for="i in 5" :key="i" class="i-lucide-star text-[10px]" :class="i <= r.stars ? 'text-amber-400' : 'text-slate-200'"></view>
            </view>
          </view>
          <text class="text-xs text-slate-500 leading-relaxed">{{ r.content }}</text>
        </view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref } from "vue";
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
const packages = ref([
  { name: "基础写真", price: 500, desc: "1小时拍摄 · 室内/室外", duration: "1小时", photos: "10张精修" },
  { name: "精致人像", price: 1200, desc: "3小时拍摄 · 2套服装 · 含化妆", duration: "3小时", photos: "30张精修" },
  { name: "全天旅拍", price: 3000, desc: "全天跟拍 · 不限服装 · 含化妆", duration: "全天", photos: "80张精修" },
]);
const reviews = ref([
  { name: "小雨", stars: 5, content: "林默老师非常专业，拍出来的照片超出预期！氛围感很好，全程沟通顺畅。" },
  { name: "苏晴", stars: 5, content: "第三次合作了，每次都很满意。推荐给所有想拍写真的朋友！" },
]);
</script>