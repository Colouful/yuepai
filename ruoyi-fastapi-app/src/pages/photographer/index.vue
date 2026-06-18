<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">找摄影师</text>
      <view class="mt-3 flex items-center space-x-2">
        <view class="flex-1 relative">
          <view class="absolute left-3 top-0 bottom-0 flex items-center text-slate-400">
            <view class="i-lucide-search text-base"></view>
          </view>
          <input placeholder="搜索摄影师..." placeholder-class="text-slate-400"
            class="w-full h-9 rounded-xl bg-slate-100/80 pl-9 pr-4 text-sm text-slate-800" />
        </view>
        <view class="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-100/80 text-slate-500">
          <view class="i-lucide-sliders-horizontal text-base"></view>
        </view>
      </view>
      <scroll-view scroll-x class="mt-3 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2">
          <view v-for="tag in tags" :key="tag" class="inline-block rounded-full px-3 py-1 text-[11px] font-medium"
            :class="activeTag === tag ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-500'"
            @click="activeTag = tag">{{ tag }}</view>
        </view>
      </scroll-view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="p in photographers" :key="p.name"
          class="rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform" @click="handleDetail(p)">
          <view class="flex items-center space-x-3">
            <view class="size-14 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white font-bold text-lg">{{ p.name[0] }}</view>
            <view class="flex-1 min-w-0">
              <view class="flex items-center space-x-1.5">
                <text class="font-bold text-sm text-slate-800">{{ p.name }}</text>
                <view v-if="p.verified" class="i-lucide-badge-check text-amber-500 text-sm"></view>
              </view>
              <text class="text-xs text-slate-400 block mt-0.5">{{ p.style }} · {{ p.city }}</text>
              <view class="flex items-center space-x-3 mt-1.5">
                <text class="text-[10px] text-slate-400">{{ p.orders }}单</text>
                <view class="flex items-center space-x-0.5">
                  <view class="i-lucide-star text-amber-400 text-[10px]"></view>
                  <text class="text-[10px] font-medium text-slate-600">{{ p.rating }}</text>
                </view>
                <text class="text-[10px] text-slate-400">{{ p.distance }}</text>
              </view>
            </view>
            <view class="text-right">
              <text class="text-base font-bold text-amber-600">¥{{ p.price }}</text>
              <text class="text-[10px] text-slate-400 block">起/次</text>
            </view>
          </view>
          <view class="mt-3 flex space-x-2 overflow-hidden">
            <view v-for="(img, i) in p.works" :key="i" class="h-16 w-16 rounded-xl bg-slate-200 shrink-0"></view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
const tags = ["全部", "人像", "婚纱", "古风", "JK", "商业", "旅拍"];
const activeTag = ref("全部");
const photographers = ref([
  { name: "林默", style: "人像摄影", city: "北京", rating: "4.9", orders: 326, price: 500, distance: "3.2km", verified: true, works: [1,2,3] },
  { name: "苏晴", style: "婚纱摄影", city: "上海", rating: "4.8", orders: 218, price: 2000, distance: "5.1km", verified: true, works: [1,2,3] },
  { name: "陈风", style: "商业摄影", city: "广州", rating: "4.7", orders: 156, price: 800, distance: "2.8km", verified: true, works: [1,2,3] },
  { name: "叶知秋", style: "写真摄影", city: "成都", rating: "4.9", orders: 412, price: 300, distance: "1.5km", verified: false, works: [1,2,3] },
  { name: "白鹭", style: "古风摄影", city: "杭州", rating: "4.8", orders: 89, price: 600, distance: "8.3km", verified: true, works: [1,2,3] },
]);
function handleDetail(p) { proxy.$modal.msg("摄影师详情建设中~"); }
</script>