<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">发布约拍</text>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-5">
        <!-- 约拍类型 -->
        <view>
          <text class="text-sm font-semibold text-slate-700 block mb-3">约拍类型</text>
          <view class="flex flex-wrap gap-2">
            <view v-for="t in types" :key="t" class="rounded-xl px-4 py-2 text-xs font-medium transition-colors"
              :class="selectedType === t ? 'bg-amber-500 text-white' : 'bg-white text-slate-600'"
              @click="selectedType = t">{{ t }}</view>
          </view>
        </view>
        <!-- 标题 -->
        <view>
          <text class="text-sm font-semibold text-slate-700 block mb-2">需求标题</text>
          <input placeholder="例：周末人像写真拍摄" placeholder-class="text-slate-400"
            class="h-11 w-full rounded-xl bg-white px-4 text-sm text-slate-800 ring-1 ring-slate-200" />
        </view>
        <!-- 描述 -->
        <view>
          <text class="text-sm font-semibold text-slate-700 block mb-2">详细描述</text>
          <textarea placeholder="描述你的拍摄需求、风格偏好、参考图片等..." placeholder-class="text-slate-400"
            class="h-28 w-full rounded-xl bg-white p-4 text-sm text-slate-800 ring-1 ring-slate-200" />
        </view>
        <!-- 日期城市 -->
        <view class="flex space-x-3">
          <view class="flex-1">
            <text class="text-sm font-semibold text-slate-700 block mb-2">拍摄日期</text>
            <input type="date" class="h-11 w-full rounded-xl bg-white px-4 text-sm text-slate-800 ring-1 ring-slate-200" />
          </view>
          <view class="flex-1">
            <text class="text-sm font-semibold text-slate-700 block mb-2">拍摄城市</text>
            <input placeholder="选择城市" placeholder-class="text-slate-400"
              class="h-11 w-full rounded-xl bg-white px-4 text-sm text-slate-800 ring-1 ring-slate-200" />
          </view>
        </view>
        <!-- 预算 -->
        <view>
          <text class="text-sm font-semibold text-slate-700 block mb-2">预算设置</text>
          <view class="flex space-x-2">
            <view v-for="b in budgets" :key="b" class="rounded-xl px-4 py-2 text-xs font-medium transition-colors"
              :class="selectedBudget === b ? 'bg-amber-500 text-white' : 'bg-white text-slate-600'"
              @click="selectedBudget = b">{{ b }}</view>
          </view>
        </view>
        <!-- 发布按钮 -->
        <button class="h-12 w-full rounded-xl bg-gradient-to-r from-slate-800 to-slate-900 text-base font-semibold text-white active:scale-[0.98] transition-transform">
          发布需求
        </button>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const types = ["个人写真", "情侣写真", "婚纱摄影", "旅拍", "商业拍摄", "互勉创作", "同城陪拍", "证件照"];
const selectedType = ref("个人写真");
const budgets = ["¥200以下", "¥200-500", "¥500-1000", "¥1000-2000", "¥2000以上", "互勉"];
const selectedBudget = ref("¥500-1000");
</script>