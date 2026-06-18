<template>
  <view class="min-h-screen" style="background:linear-gradient(180deg,#FDF2F8 0%,#FFFFFF 40%,#F5F3FF 100%)">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <!-- 个人卡片 -->
    <view class="px-5 pt-3 pb-5">
      <view class="rounded-3xl p-5 text-white relative overflow-hidden" style="background:linear-gradient(135deg,#EC4899 0%,#A78BFA 50%,#8B5CF6 100%);box-shadow:0 12px 40px rgba(236,72,153,0.25)">
        <view class="absolute -right-10 -top-10 size-40 rounded-full bg-white/10 blur-3xl"></view>
        <view class="absolute -left-10 -bottom-10 size-32 rounded-full bg-white/10 blur-3xl"></view>
        <view class="relative z-10 flex items-center space-x-4">
          <view class="size-16 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center text-3xl font-black border-2 border-white/30">{{ name ? name[0] : '?' }}</view>
          <view class="flex-1">
            <text class="text-lg font-black block">{{ name || '点击登录' }}</text>
            <text class="text-xs opacity-80 block mt-0.5">{{ name ? '摄影师 · 北京' : '登录享受更多服务' }}</text>
            <view class="mt-2 flex space-x-2">
              <view class="rounded-full bg-white/20 px-3 py-1 text-[10px] font-bold">已认证</view>
              <view class="rounded-full bg-white/20 px-3 py-1 text-[10px] font-bold">信用100</view>
            </view>
          </view>
        </view>
        <view class="relative z-10 mt-5 grid grid-cols-4 gap-2">
          <view v-for="s in stats" :key="s.l" class="text-center">
            <text class="text-lg font-black block">{{ s.v }}</text>
            <text class="text-[10px] opacity-70 block">{{ s.l }}</text>
          </view>
        </view>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-24 space-y-4">
        <!-- 快捷操作 -->
        <view class="grid grid-cols-4 gap-3">
          <view v-for="a in actions" :key="a.label" class="flex flex-col items-center" @click="a.fn()">
            <view class="size-12 rounded-2xl flex items-center justify-center mb-1.5 active:scale-90 transition-transform duration-200" :style="{background:a.bg, boxShadow:a.shadow}">
              <view :class="a.icon" class="text-xl text-white"></view>
            </view>
            <text class="text-[10px] text-slate-600 font-semibold">{{ a.label }}</text>
          </view>
        </view>

        <!-- 菜单 -->
        <view class="rounded-2xl bg-white overflow-hidden" style="box-shadow:0 2px 12px rgba(244,114,182,0.06)">
          <view v-for="(m,i) in menu" :key="m.label" class="flex items-center justify-between px-4 py-3.5 active:bg-rose-50/50 transition-colors" :class="i<menu.length-1?'border-b border-rose-50':''" @click="m.fn()">
            <view class="flex items-center space-x-3">
              <view class="size-9 rounded-xl flex items-center justify-center" :style="{background:m.bg}"><view :class="m.icon" class="text-sm text-white"></view></view>
              <text class="text-sm text-slate-700">{{ m.label }}</text>
            </view>
            <view class="flex items-center space-x-2">
              <text v-if="m.badge" class="text-[10px] text-rose-400 font-bold">{{ m.badge }}</text>
              <view class="i-lucide-chevron-right text-rose-200 text-sm"></view>
            </view>
          </view>
        </view>

        <!-- 设置 -->
        <view class="rounded-2xl bg-white overflow-hidden" style="box-shadow:0 2px 12px rgba(244,114,182,0.06)">
          <view class="flex items-center justify-between px-4 py-3.5 active:bg-rose-50/50 transition-colors" @click="$tab.navigateTo('/pages/mine/setting/index')">
            <view class="flex items-center space-x-3">
              <view class="size-9 rounded-xl flex items-center justify-center" style="background:linear-gradient(135deg,#94A3B8,#64748B)"><view class="i-lucide-settings text-sm text-white"></view></view>
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
const statusBarH = ref(44); const scrollH = ref(600);
try { const s=uni.getSystemInfoSync(); statusBarH.value=s.statusBarHeight||44; scrollH.value=s.windowHeight-statusBar.value-300; } catch(e){}

const stats = [{v:"128",l:"关注"},{v:"56",l:"粉丝"},{v:"12",l:"约拍"},{v:"¥3.6k",l:"收入"}];
const actions = [
  { label:"我的订单", icon:"i-lucide-clipboard-list", bg:"linear-gradient(135deg,#F472B6,#EC4899)", shadow:"0 4px 12px rgba(244,114,182,0.2)", fn:()=>proxy.$tab.navigateTo('/pages/order/index') },
  { label:"我的钱包", icon:"i-lucide-wallet", bg:"linear-gradient(135deg,#A78BFA,#8B5CF6)", shadow:"0 4px 12px rgba(167,139,250,0.2)", fn:()=>proxy.$tab.navigateTo('/pages/wallet/index') },
  { label:"我的收藏", icon:"i-lucide-heart", bg:"linear-gradient(135deg,#38BDF8,#0EA5E9)", shadow:"0 4px 12px rgba(56,189,248,0.2)", fn:()=>proxy.$tab.navigateTo('/pages/favorite/index') },
  { label:"优惠券", icon:"i-lucide-ticket", bg:"linear-gradient(135deg,#34D399,#10B981)", shadow:"0 4px 12px rgba(52,211,153,0.2)", fn:()=>proxy.$tab.navigateTo('/pages/coupon/index') },
];
const menu = [
  { label:"约拍管理", icon:"i-lucide-calendar", bg:"linear-gradient(135deg,#F472B6,#EC4899)", badge:"3", fn:()=>proxy.$tab.navigateTo('/pages/demand-manage/index') },
  { label:"创作者工作台", icon:"i-lucide-layout-dashboard", bg:"linear-gradient(135deg,#A78BFA,#8B5CF6)", badge:"", fn:()=>proxy.$tab.navigateTo('/pages/creator/index') },
  { label:"会员中心", icon:"i-lucide-crown", bg:"linear-gradient(135deg,#FBBF24,#F59E0B)", badge:"", fn:()=>proxy.$tab.navigateTo('/pages/member/index') },
  { label:"实名认证", icon:"i-lucide-shield-check", bg:"linear-gradient(135deg,#38BDF8,#0EA5E9)", badge:"已认证", fn:()=>proxy.$tab.navigateTo('/pages/certify/index') },
  { label:"浏览记录", icon:"i-lucide-clock", bg:"linear-gradient(135deg,#34D399,#10B981)", badge:"", fn:()=>proxy.$tab.navigateTo('/pages/history/index') },
  { label:"我的关注", icon:"i-lucide-users", bg:"linear-gradient(135deg,#FB923C,#F97316)", badge:"", fn:()=>proxy.$tab.navigateTo('/pages/follow/index') },
  { label:"在线客服", icon:"i-lucide-headphones", bg:"linear-gradient(135deg,#94A3B8,#64748B)", badge:"", fn:()=>proxy.$tab.navigateTo('/pages/service/index') },
];
</script>
