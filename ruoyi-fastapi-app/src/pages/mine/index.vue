<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <view class="flex items-center justify-between px-5 pt-3 pb-4">
      <view>
        <text class="yp-eyebrow block">PERSONAL</text>
        <text class="yp-title block mt-1">我的</text>
      </view>
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="open('/pages/mine/setting/index')">
        <view class="i-lucide-settings text-lg text-zinc-700"></view>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-5">
        <view class="yp-card-strong relative overflow-hidden p-5" @click="goProfile">
          <view class="absolute -right-12 -top-12 size-40 rounded-full" style="background:rgba(244,63,94,.28);filter:blur(24px)"></view>
          <view class="absolute right-4 bottom-3 text-white/5 text-[96px] font-black leading-none">91</view>

          <view class="relative z-10 flex items-center">
            <view class="size-16 rounded-2xl bg-white/10 border border-white/15 flex items-center justify-center text-2xl font-black">
              {{ name ? name[0] : '游' }}
            </view>
            <view class="flex-1 ml-4 min-w-0">
              <view class="flex items-center space-x-2">
                <text class="text-lg font-black text-white truncate">{{ name || '登录 / 注册' }}</text>
                <view v-if="name" class="i-lucide-badge-check text-rose-400 text-base"></view>
              </view>
              <text class="text-xs text-white/55 block mt-1">{{ name ? '摄影爱好者 · 北京' : '登录后管理订单、收藏与作品' }}</text>
              <view class="mt-2 flex items-center space-x-2">
                <view class="rounded-full bg-white/10 px-2.5 py-1 text-[10px] text-white/80">信用 100</view>
                <view class="rounded-full bg-rose-500/20 px-2.5 py-1 text-[10px] text-rose-200">实名认证</view>
              </view>
            </view>
            <view class="i-lucide-chevron-right text-white/45 text-lg"></view>
          </view>

          <view class="relative z-10 mt-5 pt-4 border-t border-white/10 grid grid-cols-4">
            <view v-for="item in stats" :key="item.label" class="text-center">
              <text class="text-lg font-black text-white block">{{ item.value }}</text>
              <text class="text-[10px] text-white/45 block mt-0.5">{{ item.label }}</text>
            </view>
          </view>
        </view>

        <view class="yp-card p-4">
          <view class="flex items-center justify-between mb-4">
            <text class="yp-section-title">订单中心</text>
            <view class="flex items-center" @click="open('/pages/order/index')">
              <text class="text-xs text-zinc-400">全部订单</text>
              <view class="i-lucide-chevron-right text-zinc-300 text-sm ml-1"></view>
            </view>
          </view>
          <view class="grid grid-cols-5 gap-1">
            <view v-for="item in orders" :key="item.label" class="flex flex-col items-center py-1" @click="open('/pages/order/index')">
              <view class="relative size-10 rounded-2xl bg-zinc-50 flex items-center justify-center">
                <view :class="item.icon" class="text-lg text-zinc-700"></view>
                <view v-if="item.badge" class="absolute -right-1 -top-1 min-w-4 h-4 px-1 rounded-full bg-rose-500 text-white text-[9px] flex items-center justify-center">{{ item.badge }}</view>
              </view>
              <text class="text-[10px] text-zinc-600 mt-2">{{ item.label }}</text>
            </view>
          </view>
        </view>

        <view class="relative overflow-hidden rounded-3xl p-5" style="background:linear-gradient(135deg,#fff1f2 0%,#ffffff 58%,#f4f4f5 100%);border:1px solid rgba(244,63,94,.12)" @click="open('/pages/creator/index')">
          <view class="absolute -right-6 -bottom-8 size-28 rounded-full bg-rose-200/45"></view>
          <view class="relative z-10 flex items-center">
            <view class="size-12 rounded-2xl bg-zinc-900 flex items-center justify-center">
              <view class="i-lucide-aperture text-white text-xl"></view>
            </view>
            <view class="flex-1 ml-3">
              <text class="text-base font-black text-zinc-900 block">创作者中心</text>
              <text class="text-[11px] text-zinc-500 block mt-1">管理作品、服务、档期与收入</text>
            </view>
            <view class="rounded-full bg-rose-500 px-3 py-1.5 text-[10px] font-bold text-white">进入</view>
          </view>
        </view>

        <view>
          <view class="flex items-center justify-between mb-3">
            <text class="yp-section-title">常用服务</text>
            <text class="text-xs text-zinc-400">为你的每次创作提供保障</text>
          </view>
          <view class="grid grid-cols-4 gap-3">
            <view v-for="item in services" :key="item.label" class="yp-card py-4 flex flex-col items-center" @click="open(item.path)">
              <view class="size-10 rounded-2xl flex items-center justify-center" :style="{ background: item.background }">
                <view :class="item.icon" class="text-lg" :style="{ color: item.color }"></view>
              </view>
              <text class="text-[10px] text-zinc-600 mt-2">{{ item.label }}</text>
            </view>
          </view>
        </view>

        <view class="yp-card overflow-hidden">
          <view v-for="(item, index) in menus" :key="item.label" class="flex items-center px-4 py-4" :class="index < menus.length - 1 ? 'border-b border-black/5' : ''" @click="open(item.path)">
            <view class="size-9 rounded-xl bg-zinc-50 flex items-center justify-center">
              <view :class="item.icon" class="text-base text-zinc-700"></view>
            </view>
            <text class="flex-1 text-sm text-zinc-700 ml-3">{{ item.label }}</text>
            <text v-if="item.extra" class="text-[10px] text-rose-500 mr-1">{{ item.extra }}</text>
            <view class="i-lucide-chevron-right text-zinc-300 text-sm"></view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { useUserStore } from "@/store";

const { proxy } = getCurrentInstance();
const userStore = useUserStore();
const name = computed(() => userStore.name);
const statusBarH = ref(44);
const scrollH = ref(600);

try {
  const systemInfo = uni.getSystemInfoSync();
  statusBarH.value = systemInfo.statusBarHeight || 44;
  scrollH.value = systemInfo.windowHeight - statusBarH.value - 72;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

const stats = [
  { value: "128", label: "关注" },
  { value: "56", label: "粉丝" },
  { value: "12", label: "约拍" },
  { value: "3.6k", label: "获赞" },
];

const orders = [
  { label: "待确认", icon: "i-lucide-message-square-text", badge: 2 },
  { label: "待付款", icon: "i-lucide-wallet-cards", badge: 1 },
  { label: "待拍摄", icon: "i-lucide-camera", badge: 0 },
  { label: "待交付", icon: "i-lucide-images", badge: 1 },
  { label: "待评价", icon: "i-lucide-star", badge: 0 },
];

const services = [
  { label: "收藏", icon: "i-lucide-heart", path: "/pages/favorite/index", background: "#fff1f2", color: "#f43f5e" },
  { label: "关注", icon: "i-lucide-users", path: "/pages/follow/index", background: "#f4f4f5", color: "#3f3f46" },
  { label: "钱包", icon: "i-lucide-wallet", path: "/pages/wallet/index", background: "#fffbeb", color: "#d97706" },
  { label: "优惠券", icon: "i-lucide-ticket", path: "/pages/coupon/index", background: "#f0fdf4", color: "#059669" },
];

const menus = [
  { label: "我的约拍", icon: "i-lucide-calendar-days", path: "/pages/demand-manage/index", extra: "3 个进行中" },
  { label: "浏览记录", icon: "i-lucide-history", path: "/pages/history/index" },
  { label: "身份认证", icon: "i-lucide-shield-check", path: "/pages/certify/index", extra: "已认证" },
  { label: "会员中心", icon: "i-lucide-crown", path: "/pages/member/index" },
  { label: "帮助与客服", icon: "i-lucide-headphones", path: "/pages/service/index" },
];

function open(path) {
  proxy.$tab.navigateTo(path);
}

function goProfile() {
  open(name.value ? "/pages/profile/index" : "/pages/login");
}
</script>
