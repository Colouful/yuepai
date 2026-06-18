<template>
  <view class="min-h-screen bg-gradient-to-b from-sky-50 via-white to-violet-50">
    <view :style="{ height: statusBarHeight + 'px' }"></view>

    <view class="px-5 pt-2 pb-3">
      <text class="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-sky-500 to-violet-500 bg-clip-text text-transparent">消息</text>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollHeight + 'px' }">
      <view class="px-5 pb-8 space-y-2.5">
        <!-- 系统消息入口 -->
        <view class="rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 p-4 text-white flex items-center shadow-lg shadow-rose-200/30 active:scale-[0.98] transition-transform">
          <view class="size-12 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center mr-3">
            <view class="i-lucide-bell text-2xl text-white"></view>
          </view>
          <view class="flex-1">
            <text class="text-sm font-bold block">系统通知</text>
            <text class="text-xs opacity-80 block mt-0.5">您的摄影师认证已通过</text>
          </view>
          <view class="size-5 rounded-full bg-white/30 flex items-center justify-center text-[10px] font-bold">3</view>
        </view>

        <!-- 消息列表 -->
        <view v-for="msg in messages" :key="msg.name"
          class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 flex items-center space-x-3 shadow-sm shadow-sky-100/30 active:scale-[0.98] transition-transform">
          <view class="relative shrink-0">
            <view class="size-12 rounded-2xl bg-gradient-to-br flex items-center justify-center text-white font-bold" :class="msg.color">
              {{ msg.name[0] }}
            </view>
            <view v-if="msg.unread" class="absolute -top-0.5 -right-0.5 size-3 rounded-full bg-rose-400 border-2 border-white"></view>
          </view>
          <view class="flex-1 min-w-0">
            <view class="flex items-center justify-between">
              <text class="text-sm font-bold text-slate-800">{{ msg.name }}</text>
              <text class="text-[10px] text-slate-300">{{ msg.time }}</text>
            </view>
            <text class="text-xs text-slate-400 block mt-0.5 truncate">{{ msg.last }}</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref } from "vue";

const statusBarHeight = ref(44);
const scrollHeight = ref(600);
try {
  const sys = uni.getSystemInfoSync();
  statusBarHeight.value = sys.statusBarHeight || 44;
  scrollHeight.value = sys.windowHeight - statusBarHeight.value - 50;
} catch(e) {}

const messages = ref([
  { name: "林默", last: "好的，那我们周六下午2点见！", time: "刚刚", unread: true, color: "from-rose-400 to-pink-400" },
  { name: "苏晴", last: "作品已经修好了，你看看效果", time: "10分钟前", unread: true, color: "from-violet-400 to-purple-400" },
  { name: "小雨", last: "请问这个套餐包含化妆吗？", time: "1小时前", unread: false, color: "from-sky-400 to-cyan-400" },
  { name: "陈风", last: "感谢好评！期待下次合作", time: "昨天", unread: false, color: "from-emerald-400 to-teal-400" },
  { name: "白鹭", last: "古风写真的服装我这边准备", time: "昨天", unread: false, color: "from-amber-400 to-orange-400" },
  { name: "叶知秋", last: "已收到定金，档期已为您保留", time: "2天前", unread: false, color: "from-pink-400 to-rose-400" },
]);
</script>
