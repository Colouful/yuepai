<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50 flex flex-col">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-3 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <view class="size-8 rounded-full bg-gradient-to-br from-rose-300 to-violet-300 flex items-center justify-center text-white text-xs font-bold mr-2">林</view>
      <text class="text-base font-bold text-slate-800">林默</text>
      <view class="ml-auto i-lucide-more-horizontal text-slate-400"></view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 py-4 space-y-4" :show-scrollbar="false">
      <view v-for="msg in messages" :key="msg.id" class="flex" :class="msg.mine ? 'justify-end' : 'justify-start'">
        <view v-if="!msg.mine" class="size-8 rounded-full bg-gradient-to-br from-rose-300 to-violet-300 flex items-center justify-center text-white text-xs font-bold mr-2 shrink-0">林</view>
        <view class="max-w-[70%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed"
          :class="msg.mine ? 'bg-gradient-to-r from-rose-400 to-violet-400 text-white rounded-tr-md' : 'bg-white text-slate-700 rounded-tl-md shadow-sm'">
          {{ msg.text }}
        </view>
      </view>
    </scroll-view>
    <view class="bg-white/80 backdrop-blur-sm px-5 py-3 flex items-center space-x-2 border-t border-rose-100">
      <view class="i-lucide-plus text-rose-300 text-xl"></view>
      <input placeholder="输入消息..." placeholder-class="text-slate-300"
        class="flex-1 h-10 rounded-xl bg-rose-50/50 px-4 text-sm text-slate-700" />
      <view class="size-10 rounded-xl bg-gradient-to-r from-rose-400 to-violet-400 flex items-center justify-center">
        <view class="i-lucide-send text-white text-sm"></view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref } from "vue";
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
const messages = ref([
  { id: 1, text: "你好，我想咨询一下人像写真的拍摄", mine: true },
  { id: 2, text: "你好呀！请问你想要什么风格的呢？", mine: false },
  { id: 3, text: "日系清新风格，大概1小时左右", mine: true },
  { id: 4, text: "可以的！基础写真套餐是500元，包含1小时拍摄和10张精修。你方便的时间是？", mine: false },
  { id: 5, text: "这周六下午可以吗？", mine: true },
]);
</script>
