<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <view class="px-5 pt-3 pb-3">
      <view class="flex items-end justify-between">
        <view>
          <text class="yp-eyebrow block">INBOX</text>
          <text class="yp-title block mt-1">消息</text>
        </view>
        <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="markAllRead">
          <view class="i-lucide-check-check text-zinc-700 text-lg"></view>
        </view>
      </view>

      <view class="mt-4 rounded-2xl bg-zinc-100 p-1 flex">
        <view
          v-for="(item, index) in tabs"
          :key="item"
          class="relative flex-1 h-10 rounded-xl flex items-center justify-center text-xs font-bold"
          :class="tabIndex === index ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-400'"
          @click="tabIndex = index"
        >
          {{ item }}
          <view v-if="index === 0 && unreadCount" class="absolute right-3 top-2 min-w-4 h-4 rounded-full bg-rose-500 px-1 flex items-center justify-center text-[9px] text-white">{{ unreadCount }}</view>
        </view>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28">
        <template v-if="tabIndex === 0">
          <view class="grid grid-cols-3 gap-3 mb-5">
            <view v-for="item in shortcuts" :key="item.label" class="yp-card py-4 flex flex-col items-center" @click="openShortcut(item)">
              <view class="relative size-11 rounded-2xl flex items-center justify-center" :style="{ background: item.background }">
                <view :class="item.icon" class="text-lg" :style="{ color: item.color }"></view>
                <view v-if="item.unread" class="absolute -right-1 -top-1 min-w-4 h-4 rounded-full bg-rose-500 px-1 text-[9px] text-white flex items-center justify-center">{{ item.unread }}</view>
              </view>
              <text class="text-[10px] text-zinc-600 mt-2">{{ item.label }}</text>
            </view>
          </view>

          <view class="flex items-center justify-between mb-3">
            <text class="yp-section-title">最近联系</text>
            <text class="text-xs text-zinc-400">{{ conversations.length }} 个会话</text>
          </view>

          <view class="yp-card overflow-hidden">
            <view
              v-for="(item, index) in conversations"
              :key="item.id"
              class="flex items-center px-4 py-4"
              :class="index < conversations.length - 1 ? 'border-b border-black/5' : ''"
              @click="openChat(item)"
            >
              <view class="relative shrink-0">
                <view class="size-12 rounded-2xl flex items-center justify-center text-white font-black" :style="{ background: item.avatar }">{{ item.name[0] }}</view>
                <view v-if="item.online" class="absolute -right-0.5 -bottom-0.5 size-3 rounded-full bg-emerald-500 border-2 border-white"></view>
              </view>

              <view class="flex-1 min-w-0 ml-3">
                <view class="flex items-center justify-between">
                  <view class="flex items-center min-w-0">
                    <text class="text-sm font-black text-zinc-900 truncate">{{ item.name }}</text>
                    <view v-if="item.verified" class="i-lucide-badge-check text-rose-500 text-xs ml-1"></view>
                  </view>
                  <text class="text-[10px]" :class="item.unread ? 'text-zinc-900 font-bold' : 'text-zinc-300'">{{ item.time }}</text>
                </view>
                <view class="flex items-center mt-1">
                  <view v-if="item.type" class="rounded-md bg-zinc-100 px-1.5 py-0.5 text-[9px] text-zinc-500 mr-1.5">{{ item.type }}</view>
                  <text class="flex-1 text-xs truncate" :class="item.unread ? 'text-zinc-700 font-semibold' : 'text-zinc-400'">{{ item.lastMessage }}</text>
                  <view v-if="item.unread" class="min-w-5 h-5 rounded-full bg-rose-500 px-1.5 flex items-center justify-center text-[10px] text-white ml-2">{{ item.unread }}</view>
                </view>
              </view>
            </view>
          </view>
        </template>

        <template v-else-if="tabIndex === 1">
          <view class="space-y-3">
            <view v-for="item in interactions" :key="item.id" class="yp-card p-4 flex items-center">
              <view class="size-11 rounded-2xl flex items-center justify-center" :style="{ background: item.avatar }">
                <text class="text-white font-black">{{ item.name[0] }}</text>
              </view>
              <view class="flex-1 min-w-0 ml-3">
                <text class="text-sm text-zinc-800 block"><text class="font-black">{{ item.name }}</text> {{ item.action }}</text>
                <text class="text-[10px] text-zinc-400 block mt-1">{{ item.time }}</text>
              </view>
              <view class="size-11 rounded-xl flex items-center justify-center" :style="{ background: item.preview }">
                <view :class="item.icon" class="text-white text-base"></view>
              </view>
            </view>
          </view>
        </template>

        <template v-else>
          <view class="space-y-3">
            <view v-for="item in notifications" :key="item.id" class="yp-card p-4" @click="openNotification(item)">
              <view class="flex items-start">
                <view class="size-10 rounded-2xl flex items-center justify-center" :style="{ background: item.background }">
                  <view :class="item.icon" class="text-base" :style="{ color: item.color }"></view>
                </view>
                <view class="flex-1 ml-3">
                  <view class="flex items-center justify-between">
                    <text class="text-sm font-black text-zinc-900">{{ item.title }}</text>
                    <view v-if="!item.read" class="size-2 rounded-full bg-rose-500"></view>
                  </view>
                  <text class="text-xs text-zinc-500 leading-relaxed block mt-1.5">{{ item.content }}</text>
                  <text class="text-[10px] text-zinc-300 block mt-2">{{ item.time }}</text>
                </view>
              </view>
            </view>
          </view>
        </template>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const scrollH = ref(600);
const tabIndex = ref(0);
const tabs = ["私信", "互动", "通知"];

try {
  const systemInfo = uni.getSystemInfoSync();
  statusBarH.value = systemInfo.statusBarHeight || 44;
  scrollH.value = systemInfo.windowHeight - statusBarH.value - 132;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

const shortcuts = reactive([
  { label: "订单消息", icon: "i-lucide-clipboard-list", unread: 2, background: "#fff1f2", color: "#f43f5e", path: "/pages/order/index" },
  { label: "报价通知", icon: "i-lucide-badge-dollar-sign", unread: 1, background: "#fffbeb", color: "#d97706", path: "/pages/quote/index" },
  { label: "系统通知", icon: "i-lucide-bell", unread: 3, background: "#f4f4f5", color: "#3f3f46", tab: 2 },
]);

const conversations = reactive([
  { id: 1, name: "林默", verified: true, online: true, type: "约拍", lastMessage: "好的，周六下午 2 点在三里屯见", time: "刚刚", unread: 2, avatar: "linear-gradient(135deg,#fb7185,#be123c)" },
  { id: 2, name: "苏晴", verified: true, online: true, type: "交付", lastMessage: "作品已经修好，发你预览一下", time: "10:24", unread: 1, avatar: "linear-gradient(135deg,#a78bfa,#5b21b6)" },
  { id: 3, name: "小雨", verified: false, online: false, type: "咨询", lastMessage: "套餐里包含化妆和服装吗？", time: "昨天", unread: 0, avatar: "linear-gradient(135deg,#38bdf8,#0369a1)" },
  { id: 4, name: "陈风", verified: true, online: false, type: "评价", lastMessage: "感谢你的认可，期待下次合作", time: "昨天", unread: 0, avatar: "linear-gradient(135deg,#34d399,#047857)" },
  { id: 5, name: "白鹭", verified: true, online: false, type: "约拍", lastMessage: "古风服装和头饰我来准备", time: "周二", unread: 0, avatar: "linear-gradient(135deg,#fbbf24,#b45309)" },
]);

const interactions = [
  { id: 1, name: "叶知秋", action: "赞了你的作品《雨后的日系小巷》", time: "5 分钟前", avatar: "linear-gradient(135deg,#a78bfa,#5b21b6)", preview: "linear-gradient(135deg,#c4b5fd,#6d28d9)", icon: "i-lucide-heart" },
  { id: 2, name: "南山影像", action: "关注了你", time: "1 小时前", avatar: "linear-gradient(135deg,#38bdf8,#0369a1)", preview: "linear-gradient(135deg,#e0f2fe,#0284c7)", icon: "i-lucide-user-plus" },
  { id: 3, name: "木子", action: "评论了你的作品：氛围感太好了", time: "昨天", avatar: "linear-gradient(135deg,#fbbf24,#b45309)", preview: "linear-gradient(135deg,#fef3c7,#d97706)", icon: "i-lucide-message-circle" },
];

const notifications = reactive([
  { id: 1, title: "认证审核通过", content: "你的摄影师身份认证已通过，现在可以发布服务和管理档期。", time: "今天 09:30", read: false, icon: "i-lucide-shield-check", background: "#f0fdf4", color: "#059669", path: "/pages/certify/index" },
  { id: 2, title: "订单状态更新", content: "订单 YP20260618001 已进入待拍摄状态，请提前与合作方确认地点。", time: "昨天 18:20", read: false, icon: "i-lucide-camera", background: "#fff1f2", color: "#f43f5e", path: "/pages/order/detail" },
  { id: 3, title: "平台安全提醒", content: "请始终通过平台订单进行交易，谨防私下转账和虚假链接。", time: "6 月 16 日", read: true, icon: "i-lucide-triangle-alert", background: "#fffbeb", color: "#d97706", path: "/pages/mine/help/index" },
]);

const unreadCount = computed(() => conversations.reduce((total, item) => total + item.unread, 0));

function openShortcut(item) {
  if (typeof item.tab === "number") {
    tabIndex.value = item.tab;
    return;
  }
  proxy.$tab.navigateTo(item.path);
}

function openChat(item) {
  item.unread = 0;
  proxy.$tab.navigateTo(`/pages/chat/index?id=${item.id}&name=${encodeURIComponent(item.name)}`);
}

function openNotification(item) {
  item.read = true;
  proxy.$tab.navigateTo(item.path);
}

function markAllRead() {
  conversations.forEach((item) => {
    item.unread = 0;
  });
  notifications.forEach((item) => {
    item.read = true;
  });
  shortcuts.forEach((item) => {
    item.unread = 0;
  });
  uni.showToast({ title: "已全部标记为已读", icon: "none" });
}
</script>
