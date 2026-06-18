<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">消息中心</text>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-1">
        <view v-for="msg in messages" :key="msg.title"
          class="flex items-center space-x-3.5 rounded-2xl bg-white p-4 active:bg-slate-50 transition-colors">
          <view class="relative shrink-0">
            <view class="size-11 rounded-2xl flex items-center justify-center text-white"
              :class="msg.bgClass">
              <view :class="msg.icon" class="text-lg"></view>
            </view>
            <view v-if="msg.unread" class="absolute -top-1 -right-1 size-3 rounded-full bg-rose-500 border-2 border-white"></view>
          </view>
          <view class="flex-1 min-w-0">
            <view class="flex items-center justify-between">
              <text class="text-sm font-semibold text-slate-800">{{ msg.title }}</text>
              <text class="text-[10px] text-slate-300">{{ msg.time }}</text>
            </view>
            <text class="text-xs text-slate-400 block mt-0.5 truncate">{{ msg.desc }}</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const messages = ref([
  { title: "订单通知", desc: "您的预约拍摄订单已确认", time: "刚刚", icon: "i-lucide-clipboard-list", bgClass: "bg-amber-500", unread: true },
  { title: "互动消息", desc: "林默 赞了您的作品", time: "5分钟前", icon: "i-lucide-heart", bgClass: "bg-rose-500", unread: true },
  { title: "系统通知", desc: "平台将于6月20日进行维护", time: "1小时前", icon: "i-lucide-bell", bgClass: "bg-sky-500", unread: false },
  { title: "审核通知", desc: "您的摄影师认证已通过", time: "昨天", icon: "i-lucide-shield-check", bgClass: "bg-emerald-500", unread: false },
  { title: "资金通知", desc: "订单结算 ¥500 已到账", time: "2天前", icon: "i-lucide-wallet", bgClass: "bg-violet-500", unread: false },
]);
</script>