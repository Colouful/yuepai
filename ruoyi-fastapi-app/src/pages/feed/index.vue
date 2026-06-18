<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">动态广场</text>
      <view class="mt-3 flex space-x-2">
        <view v-for="tab in tabs" :key="tab" class="rounded-full px-4 py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-500'"
          @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-4">
        <view v-for="post in posts" :key="post.title" class="rounded-2xl bg-white p-4">
          <view class="flex items-center space-x-3 mb-3">
            <view class="size-10 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white font-bold text-sm">{{ post.author[0] }}</view>
            <view class="flex-1">
              <text class="text-sm font-semibold text-slate-800">{{ post.author }}</text>
              <text class="text-[10px] text-slate-400 block">{{ post.time }}</text>
            </view>
            <view class="i-lucide-more-horizontal text-slate-300"></view>
          </view>
          <text class="text-sm text-slate-700 leading-relaxed">{{ post.content }}</text>
          <view class="mt-3 flex flex-wrap gap-1.5">
            <view v-for="(img, i) in post.images" :key="i" class="h-24 w-[31%] rounded-xl bg-slate-200"></view>
          </view>
          <view class="mt-3 flex items-center justify-between">
            <view class="flex items-center space-x-4">
              <view class="flex items-center space-x-1">
                <view class="i-lucide-heart text-slate-400 text-sm"></view>
                <text class="text-xs text-slate-400">{{ post.likes }}</text>
              </view>
              <view class="flex items-center space-x-1">
                <view class="i-lucide-message-circle text-slate-400 text-sm"></view>
                <text class="text-xs text-slate-400">{{ post.comments }}</text>
              </view>
            </view>
            <view class="i-lucide-share-2 text-slate-400 text-sm"></view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const tabs = ["关注", "推荐", "同城"];
const activeTab = ref("推荐");
const posts = ref([
  { author: "林默", time: "2小时前", content: "今日客片分享，夏日清新人像写真，感谢小姐姐的信任 📷", images: [1,2,3], likes: 128, comments: 23 },
  { author: "苏晴", time: "5小时前", content: "汉服古风拍摄花絮，杭州西湖取景，光影绝美 ✨", images: [1,2], likes: 256, comments: 45 },
  { author: "陈风", time: "昨天", content: "商业产品拍摄，极简风格，客户非常满意", images: [1,2,3], likes: 89, comments: 12 },
]);
</script>