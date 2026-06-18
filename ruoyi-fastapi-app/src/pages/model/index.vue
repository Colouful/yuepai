<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">找模特</text>
      <view class="mt-3 flex items-center space-x-2">
        <view class="flex-1 relative">
          <view class="absolute left-3 top-0 bottom-0 flex items-center text-slate-400">
            <view class="i-lucide-search text-base"></view>
          </view>
          <input placeholder="搜索模特..." placeholder-class="text-slate-400"
            class="w-full h-9 rounded-xl bg-slate-100/80 pl-9 pr-4 text-sm text-slate-800" />
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
        <view v-for="m in models" :key="m.name"
          class="rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform">
          <view class="flex items-center space-x-3">
            <view class="size-14 rounded-2xl bg-gradient-to-br from-rose-400 to-rose-600 flex items-center justify-center text-white font-bold text-lg">{{ m.name[0] }}</view>
            <view class="flex-1">
              <view class="flex items-center space-x-1.5">
                <text class="font-bold text-sm text-slate-800">{{ m.name }}</text>
                <view v-if="m.verified" class="i-lucide-badge-check text-amber-500 text-sm"></view>
              </view>
              <text class="text-xs text-slate-400 block mt-0.5">{{ m.height }} · {{ m.style }} · {{ m.city }}</text>
              <view class="flex items-center space-x-3 mt-1.5">
                <text class="text-[10px] text-slate-400">{{ m.coops }}次合作</text>
                <view class="flex items-center space-x-0.5">
                  <view class="i-lucide-star text-amber-400 text-[10px]"></view>
                  <text class="text-[10px] font-medium text-slate-600">{{ m.rating }}</text>
                </view>
                <text class="text-[10px] px-1.5 py-0.5 rounded-md"
                  :class="m.mutual ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'">
                  {{ m.mutual ? '接受互勉' : '¥' + m.price + '/次' }}</text>
              </view>
            </view>
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
const tags = ["全部", "人像", "古风", "JK", "婚纱", "商业", "互勉"];
const activeTag = ref("全部");
const models = ref([
  { name: "小雨", height: "168cm", style: "人像写真", city: "北京", rating: "4.9", coops: 56, price: 300, mutual: false, verified: true },
  { name: "苏晴", height: "172cm", style: "古风汉服", city: "杭州", rating: "4.8", coops: 34, price: 0, mutual: true, verified: true },
  { name: "叶知秋", height: "165cm", style: "JK制服", city: "成都", rating: "4.9", coops: 89, price: 200, mutual: false, verified: false },
  { name: "白鹭", height: "170cm", style: "婚纱礼服", city: "上海", rating: "4.7", coops: 23, price: 500, mutual: false, verified: true },
]);
</script>