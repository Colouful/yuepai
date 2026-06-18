<template>
  <view class="min-h-screen bg-gradient-to-b from-rose-50 via-white to-violet-50">
    <view :style="{ height: statusBarHeight + 'px' }"></view>

    <!-- Profile Header -->
    <view class="px-5 pt-4 pb-6">
      <view class="rounded-3xl bg-gradient-to-br from-rose-400 via-pink-400 to-violet-400 p-5 text-white shadow-xl shadow-rose-200/40 relative overflow-hidden">
        <!-- 装饰 -->
        <view class="absolute -right-8 -top-8 size-32 rounded-full bg-white/10 blur-2xl"></view>
        <view class="absolute -left-8 -bottom-8 size-24 rounded-full bg-white/10 blur-2xl"></view>

        <view class="relative z-10 flex items-center space-x-4">
          <view class="size-16 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center text-3xl font-bold border-2 border-white/30 shadow-lg">
            {{ name ? name[0] : '?' }}
          </view>
          <view class="flex-1">
            <text class="text-lg font-extrabold block">{{ name || '点击登录' }}</text>
            <text class="text-xs opacity-80 block mt-0.5">{{ name ? '摄影师 · 北京' : '登录后享受更多服务' }}</text>
            <view class="mt-2 flex items-center space-x-3">
              <view class="rounded-full bg-white/20 px-3 py-1 text-[10px] font-semibold">已认证</view>
              <view class="rounded-full bg-white/20 px-3 py-1 text-[10px] font-semibold">信用分 100</view>
            </view>
          </view>
        </view>

        <!-- 数据统计 -->
        <view class="relative z-10 mt-5 grid grid-cols-4 gap-2">
          <view v-for="stat in profileStats" :key="stat.label" class="text-center">
            <text class="text-lg font-extrabold block">{{ stat.value }}</text>
            <text class="text-[10px] opacity-70 block">{{ stat.label }}</text>
          </view>
        </view>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollHeight + 'px' }">
      <view class="px-5 pb-8 space-y-4">

        <!-- 快捷操作 -->
        <view class="grid grid-cols-4 gap-3">
          <view v-for="action in quickActions" :key="action.label"
            class="flex flex-col items-center active:scale-95 transition-transform" @click="action.action">
            <view class="size-12 rounded-2xl flex items-center justify-center mb-1.5 shadow-sm" :class="action.bg">
              <view :class="action.icon" class="text-xl text-white"></view>
            </view>
            <text class="text-[10px] text-slate-600 font-medium">{{ action.label }}</text>
          </view>
        </view>

        <!-- 功能菜单 -->
        <view class="rounded-2xl bg-white/80 backdrop-blur-sm overflow-hidden shadow-sm shadow-rose-100/30">
          <view v-for="(item, i) in menuItems" :key="item.label"
            class="flex items-center justify-between px-4 py-3.5 active:bg-rose-50/50 transition-colors"
            :class="i < menuItems.length - 1 ? 'border-b border-rose-50' : ''"
            @click="item.action">
            <view class="flex items-center space-x-3">
              <view class="size-9 rounded-xl flex items-center justify-center" :class="item.bg">
                <view :class="item.icon" class="text-sm text-white"></view>
              </view>
              <text class="text-sm text-slate-700">{{ item.label }}</text>
            </view>
            <view class="flex items-center space-x-2">
              <text v-if="item.badge" class="text-[10px] text-rose-400 font-semibold">{{ item.badge }}</text>
              <view class="i-lucide-chevron-right text-rose-200 text-sm"></view>
            </view>
          </view>
        </view>

        <!-- 设置入口 -->
        <view class="rounded-2xl bg-white/80 backdrop-blur-sm overflow-hidden shadow-sm shadow-rose-100/30">
          <view class="flex items-center justify-between px-4 py-3.5 active:bg-rose-50/50 transition-colors" @click="goSetting">
            <view class="flex items-center space-x-3">
              <view class="size-9 rounded-xl bg-gradient-to-br from-slate-400 to-zinc-400 flex items-center justify-center">
                <view class="i-lucide-settings text-sm text-white"></view>
              </view>
              <text class="text-sm text-slate-700">设置</text>
            </view>
            <view class="i-lucide-chevron-right text-rose-200 text-sm"></view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, computed, getCurrentInstance } from "vue";
import { useUserStore } from "@/store";

const { proxy } = getCurrentInstance();
const userStore = useUserStore();
const name = computed(() => userStore.name);

const statusBarHeight = ref(44);
const scrollHeight = ref(600);
try {
  const sys = uni.getSystemInfoSync();
  statusBarHeight.value = sys.statusBarHeight || 44;
  scrollHeight.value = sys.windowHeight - statusBarHeight.value - 280;
} catch(e) {}

const profileStats = [
  { value: "128", label: "关注" },
  { value: "56", label: "粉丝" },
  { value: "12", label: "约拍" },
  { value: "¥3.6k", label: "收入" },
];

const quickActions = [
  { label: "我的订单", icon: "i-lucide-clipboard-list", bg: "bg-gradient-to-br from-rose-400 to-pink-400", action: () => proxy.$tab.navigateTo('/pages/order/index') },
  { label: "我的钱包", icon: "i-lucide-wallet", bg: "bg-gradient-to-br from-violet-400 to-purple-400", action: () => proxy.$tab.navigateTo('/pages/wallet/index') },
  { label: "我的收藏", icon: "i-lucide-heart", bg: "bg-gradient-to-br from-sky-400 to-cyan-400", action: () => proxy.$tab.navigateTo('/pages/favorite/index') },
  { label: "优惠券", icon: "i-lucide-ticket", bg: "bg-gradient-to-br from-emerald-400 to-teal-400", action: () => proxy.$tab.navigateTo('/pages/coupon/index') },
];

const menuItems = [
  { label: "约拍管理", icon: "i-lucide-calendar", bg: "bg-gradient-to-br from-rose-400 to-pink-400", badge: "3", action: () => proxy.$tab.navigateTo('/pages/demand-manage/index') },
  { label: "创作者工作台", icon: "i-lucide-layout-dashboard", bg: "bg-gradient-to-br from-violet-400 to-purple-400", badge: "", action: () => proxy.$tab.navigateTo('/pages/creator/index') },
  { label: "会员中心", icon: "i-lucide-crown", bg: "bg-gradient-to-br from-amber-400 to-orange-400", badge: "", action: () => proxy.$tab.navigateTo('/pages/member/index') },
  { label: "实名认证", icon: "i-lucide-shield-check", bg: "bg-gradient-to-br from-sky-400 to-cyan-400", badge: "已认证", action: () => proxy.$tab.navigateTo('/pages/certify/index') },
  { label: "浏览记录", icon: "i-lucide-clock", bg: "bg-gradient-to-br from-emerald-400 to-teal-400", badge: "", action: () => proxy.$tab.navigateTo('/pages/history/index') },
  { label: "我的关注", icon: "i-lucide-users", bg: "bg-gradient-to-br from-pink-400 to-rose-400", badge: "", action: () => proxy.$tab.navigateTo('/pages/follow/index') },
  { label: "在线客服", icon: "i-lucide-headphones", bg: "bg-gradient-to-br from-slate-400 to-zinc-400", badge: "", action: () => proxy.$tab.navigateTo('/pages/service/index') },
];

function goSetting() { proxy.$tab.navigateTo('/pages/mine/setting/index'); }
</script>
