<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">作品广场</text>
      <view class="mt-3 flex space-x-2">
        <view v-for="tab in tabs" :key="tab" class="rounded-full px-4 py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-500'"
          @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 pb-24" :show-scrollbar="false">
      <view class="px-5 pt-4">
        <view class="flex flex-wrap justify-between gap-y-3">
          <view v-for="work in works" :key="work.title" class="w-[48%] rounded-2xl bg-white overflow-hidden active:scale-[0.97] transition-transform">
            <view class="h-44 bg-gradient-to-br from-slate-200 to-slate-300"></view>
            <view class="p-3">
              <text class="text-sm font-semibold text-slate-800 block truncate">{{ work.title }}</text>
              <view class="mt-2 flex items-center justify-between">
                <view class="flex items-center space-x-1.5">
                  <view class="size-5 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white text-[8px] font-bold">{{ work.author[0] }}</view>
                  <text class="text-[10px] text-slate-400">{{ work.author }}</text>
                </view>
                <view class="flex items-center space-x-0.5">
                  <view class="i-lucide-heart text-rose-400 text-[10px]"></view>
                  <text class="text-[10px] text-slate-400">{{ work.likes }}</text>
                </view>
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
const tabs = ["推荐", "人像", "古风", "婚纱", "JK", "街拍"];
const activeTab = ref("推荐");
const works = ref([
  { title: "夏日清新人像", author: "林默", likes: 326 },
  { title: "汉服古风写真", author: "苏晴", likes: 218 },
  { title: "城市夜景街拍", author: "陈风", likes: 156 },
  { title: "日系胶片风格", author: "叶知秋", likes: 412 },
  { title: "婚纱客片精选", author: "白鹭", likes: 89 },
  { title: "JK制服日常", author: "林默", likes: 267 },
]);
</script>