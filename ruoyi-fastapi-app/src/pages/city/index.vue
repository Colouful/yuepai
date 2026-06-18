<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3">
      <view class="flex items-center mb-3">
        <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
        <text class="text-lg font-bold text-slate-800">选择城市</text>
      </view>
      <view class="relative">
        <view class="absolute left-3 top-0 bottom-0 flex items-center text-rose-300"><view class="i-lucide-search text-base"></view></view>
        <input placeholder="搜索城市" placeholder-class="text-slate-300" class="w-full h-9 rounded-xl bg-rose-50/50 pl-9 pr-4 text-sm text-slate-700" />
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="mb-5">
        <text class="text-xs font-bold text-rose-400 block mb-2">当前定位</text>
        <view class="inline-block rounded-xl bg-white/80 px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-rose-100">北京</view>
      </view>
      <view class="mb-5">
        <text class="text-xs font-bold text-rose-400 block mb-2">热门城市</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="c in ['北京','上海','广州','深圳','杭州','成都','重庆','武汉','南京','西安']" :key="c"
            class="rounded-xl bg-white/80 px-4 py-2 text-xs font-medium text-slate-600 shadow-sm active:scale-95 transition-transform">{{ c }}</view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
