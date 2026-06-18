<template>
  <view class="min-h-screen bg-gradient-to-b from-rose-50 via-white to-violet-50">
    <!-- 顶部状态栏占位 -->
    <view :style="{ height: statusBarHeight + 'px' }"></view>

    <!-- Header -->
    <view class="px-5 pt-2 pb-4">
      <view class="flex items-center justify-between mb-4">
        <view>
          <text class="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-rose-500 to-violet-500 bg-clip-text text-transparent">约拍</text>
          <text class="text-[10px] text-slate-400 block -mt-0.5">记录每一个美好瞬间</text>
        </view>
        <view class="flex items-center space-x-2">
          <view class="relative size-10 rounded-2xl bg-white/80 backdrop-blur-sm flex items-center justify-center shadow-sm shadow-rose-100/50 active:scale-95 transition-transform">
            <view class="i-lucide-bell text-slate-500 text-lg"></view>
            <view class="absolute -top-0.5 -right-0.5 size-2.5 rounded-full bg-rose-400 border-2 border-white"></view>
          </view>
          <view class="size-10 rounded-2xl bg-gradient-to-br from-rose-400 to-violet-400 flex items-center justify-center shadow-sm shadow-rose-200/50 active:scale-95 transition-transform" @click="handleSearch">
            <view class="i-lucide-search text-white text-lg"></view>
          </view>
        </view>
      </view>

      <!-- 搜索框 -->
      <view class="relative mb-4" @click="handleSearch">
        <view class="absolute left-4 top-0 bottom-0 flex items-center text-rose-300">
          <view class="i-lucide-search text-sm"></view>
        </view>
        <view class="h-11 rounded-2xl bg-white/80 backdrop-blur-sm pl-10 pr-4 flex items-center shadow-sm shadow-rose-100/30">
          <text class="text-sm text-slate-300">搜索摄影师、模特、作品...</text>
        </view>
      </view>

      <!-- 城市定位 -->
      <view class="flex items-center space-x-1 mb-2">
        <view class="i-lucide-map-pin text-rose-400 text-xs"></view>
        <text class="text-xs text-slate-500 font-medium">北京</text>
        <view class="i-lucide-chevron-down text-slate-400 text-[10px]"></view>
      </view>
    </view>

    <scroll-view scroll-y class="flex-1" :show-scrollbar="false" :style="{ height: scrollHeight + 'px' }">
      <view class="px-5 pb-8 space-y-6">

        <!-- Banner 轮播 -->
        <view class="relative h-44 rounded-3xl overflow-hidden shadow-lg shadow-rose-200/30">
          <swiper class="h-44" autoplay interval="4000" circular>
            <swiper-item>
              <view class="h-full w-full bg-gradient-to-br from-rose-400 via-pink-400 to-violet-400 flex items-center justify-between px-6">
                <view>
                  <text class="text-white text-xl font-extrabold block">新人专享</text>
                  <text class="text-white/80 text-sm block mt-1">首单立减50元</text>
                  <view class="mt-3 rounded-full bg-white/20 backdrop-blur-sm px-4 py-1.5 text-xs font-semibold text-white inline-block">立即领取</view>
                </view>
                <view class="i-lucide-camera text-white/30 text-7xl"></view>
              </view>
            </swiper-item>
            <swiper-item>
              <view class="h-full w-full bg-gradient-to-br from-sky-400 via-cyan-400 to-emerald-400 flex items-center justify-between px-6">
                <view>
                  <text class="text-white text-xl font-extrabold block">互勉约拍</text>
                  <text class="text-white/80 text-sm block mt-1">免费创作机会</text>
                  <view class="mt-3 rounded-full bg-white/20 backdrop-blur-sm px-4 py-1.5 text-xs font-semibold text-white inline-block">去看看</view>
                </view>
                <view class="i-lucide-heart text-white/30 text-7xl"></view>
              </view>
            </swiper-item>
          </swiper>
        </view>

        <!-- 快捷入口 - 4个圆形图标 -->
        <view class="flex justify-between px-2">
          <view v-for="entry in entries" :key="entry.label" class="flex flex-col items-center active:scale-95 transition-transform" @click="entry.action">
            <view class="size-14 rounded-2xl flex items-center justify-center mb-2 shadow-sm" :class="entry.bg">
              <view :class="entry.icon" class="text-2xl text-white"></view>
            </view>
            <text class="text-[11px] font-medium text-slate-600">{{ entry.label }}</text>
          </view>
        </view>

        <!-- 频道标签 -->
        <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
          <view class="inline-flex space-x-2">
            <view v-for="(tab, i) in channels" :key="tab"
              class="inline-block rounded-full px-4 py-2 text-xs font-semibold transition-all duration-300"
              :class="activeChannel === i ? 'bg-gradient-to-r from-rose-400 to-violet-400 text-white shadow-md shadow-rose-200/50' : 'bg-white/80 text-slate-500 shadow-sm'"
              @click="activeChannel = i">{{ tab }}</view>
          </view>
        </scroll-view>

        <!-- 附近摄影师 -->
        <view>
          <view class="flex items-center justify-between mb-3">
            <view class="flex items-center space-x-2">
              <view class="h-5 w-1 rounded-full bg-gradient-to-b from-rose-400 to-violet-400"></view>
              <text class="text-base font-bold text-slate-800">附近摄影师</text>
            </view>
            <text class="text-xs text-rose-400 font-medium" @click="goPhotographers">查看全部</text>
          </view>
          <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
            <view class="inline-flex space-x-3">
              <view v-for="p in photographers" :key="p.name"
                class="inline-block w-36 rounded-2xl bg-white/80 backdrop-blur-sm p-3 shadow-sm shadow-rose-100/30 active:scale-[0.97] transition-transform"
                @click="goPhotographerDetail">
                <view class="flex items-center space-x-2.5 mb-2.5">
                  <view class="size-11 rounded-xl bg-gradient-to-br flex items-center justify-center text-white font-bold text-sm" :class="p.color">
                    {{ p.name[0] }}
                  </view>
                  <view class="flex-1 min-w-0">
                    <text class="text-sm font-bold text-slate-800 block truncate">{{ p.name }}</text>
                    <text class="text-[10px] text-slate-400 block">{{ p.style }}</text>
                  </view>
                </view>
                <view class="flex items-center justify-between">
                  <text class="text-[10px] text-slate-400">{{ p.city }}</text>
                  <view class="flex items-center space-x-0.5">
                    <view class="i-lucide-star text-amber-400 text-[10px]"></view>
                    <text class="text-[10px] font-semibold text-slate-600">{{ p.rating }}</text>
                  </view>
                </view>
              </view>
            </view>
          </scroll-view>
        </view>

        <!-- 热门需求 -->
        <view>
          <view class="flex items-center justify-between mb-3">
            <view class="flex items-center space-x-2">
              <view class="h-5 w-1 rounded-full bg-gradient-to-b from-sky-400 to-emerald-400"></view>
              <text class="text-base font-bold text-slate-800">热门需求</text>
            </view>
            <text class="text-xs text-rose-400 font-medium" @click="goDemand">更多需求</text>
          </view>
          <view class="space-y-3">
            <view v-for="d in demands" :key="d.title"
              class="rounded-2xl bg-white/80 backdrop-blur-sm p-4 shadow-sm shadow-rose-100/30 active:scale-[0.98] transition-transform">
              <view class="flex items-start justify-between mb-2">
                <view class="flex-1">
                  <view class="flex items-center space-x-2 mb-1">
                    <view class="rounded-lg px-2 py-0.5 text-[10px] font-bold"
                      :class="d.mutual ? 'bg-emerald-50 text-emerald-500' : 'bg-rose-50 text-rose-500'">
                      {{ d.mutual ? '互勉' : '¥' + d.price }}</view>
                    <text class="text-sm font-bold text-slate-800">{{ d.title }}</text>
                  </view>
                  <text class="text-[11px] text-slate-400">{{ d.type }} · {{ d.city }} · {{ d.date }}</text>
                </view>
              </view>
              <view class="flex items-center justify-between">
                <view class="flex items-center space-x-1.5">
                  <view class="size-6 rounded-full bg-gradient-to-br flex items-center justify-center text-white text-[8px] font-bold" :class="d.color">{{ d.user[0] }}</view>
                  <text class="text-[10px] text-slate-400">{{ d.user }}</text>
                </view>
                <text class="text-[10px] text-slate-300">{{ d.apply }}人报名</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 精选作品 -->
        <view>
          <view class="flex items-center justify-between mb-3">
            <view class="flex items-center space-x-2">
              <view class="h-5 w-1 rounded-full bg-gradient-to-b from-amber-400 to-orange-400"></view>
              <text class="text-base font-bold text-slate-800">精选作品</text>
            </view>
            <text class="text-xs text-rose-400 font-medium" @click="goWorks">更多作品</text>
          </view>
          <view class="flex flex-wrap gap-2.5">
            <view v-for="w in works" :key="w.title"
              class="w-[48%] rounded-2xl bg-white/80 backdrop-blur-sm overflow-hidden shadow-sm shadow-rose-100/30 active:scale-[0.97] transition-transform">
              <view class="h-36 bg-gradient-to-br" :class="w.gradient"></view>
              <view class="p-3">
                <text class="text-xs font-bold text-slate-800 block truncate">{{ w.title }}</text>
                <view class="mt-1.5 flex items-center justify-between">
                  <view class="flex items-center space-x-1">
                    <view class="size-4 rounded-full bg-gradient-to-br flex items-center justify-center text-white text-[6px] font-bold" :class="w.color">{{ w.author[0] }}</view>
                    <text class="text-[10px] text-slate-400">{{ w.author }}</text>
                  </view>
                  <view class="flex items-center space-x-0.5">
                    <view class="i-lucide-heart text-rose-300 text-[10px]"></view>
                    <text class="text-[10px] text-slate-400">{{ w.likes }}</text>
                  </view>
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
import { ref, getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance();
const statusBarHeight = ref(44);
const scrollHeight = ref(600);
const activeChannel = ref(0);

try {
  const sys = uni.getSystemInfoSync();
  statusBarHeight.value = sys.statusBarHeight || 44;
  scrollHeight.value = sys.windowHeight - statusBarHeight.value - 50;
} catch(e) {}

const channels = ["推荐", "附近", "摄影师", "模特", "互勉", "旅拍", "婚纱", "古风"];

const entries = [
  { label: "找摄影师", icon: "i-lucide-camera", bg: "bg-gradient-to-br from-rose-400 to-pink-400", action: () => proxy.$tab.navigateTo('/pages/photographer/index') },
  { label: "找模特", icon: "i-lucide-user", bg: "bg-gradient-to-br from-violet-400 to-purple-400", action: () => proxy.$tab.navigateTo('/pages/model/index') },
  { label: "需求大厅", icon: "i-lucide-megaphone", bg: "bg-gradient-to-br from-sky-400 to-cyan-400", action: () => proxy.$tab.navigateTo('/pages/demand/index') },
  { label: "拍摄场地", icon: "i-lucide-map-pin", bg: "bg-gradient-to-br from-emerald-400 to-teal-400", action: () => proxy.$tab.navigateTo('/pages/venue/index') },
];

const photographers = [
  { name: "林默", style: "人像写真", city: "北京", rating: "4.9", color: "from-rose-400 to-pink-400" },
  { name: "苏晴", style: "婚纱摄影", city: "上海", rating: "4.8", color: "from-violet-400 to-purple-400" },
  { name: "陈风", style: "商业摄影", city: "广州", rating: "4.7", color: "from-sky-400 to-cyan-400" },
  { name: "叶知秋", style: "写真摄影", city: "成都", rating: "4.9", color: "from-emerald-400 to-teal-400" },
  { name: "白鹭", style: "古风摄影", city: "杭州", rating: "4.8", color: "from-amber-400 to-orange-400" },
];

const demands = [
  { title: "周末人像写真", type: "人像", city: "北京", date: "6月20日", price: 500, user: "小雨", apply: 12, mutual: false, color: "from-rose-400 to-pink-400" },
  { title: "古风汉服互勉", type: "古风", city: "杭州", date: "6月22日", price: 0, user: "苏晴", apply: 8, mutual: true, color: "from-violet-400 to-purple-400" },
  { title: "婚纱照拍摄", type: "婚纱", city: "上海", date: "6月25日", price: 2000, user: "陈先生", apply: 5, mutual: false, color: "from-sky-400 to-cyan-400" },
];

const works = [
  { title: "夏日清新人像", author: "林默", likes: 326, gradient: "from-rose-200 to-pink-200", color: "from-rose-400 to-pink-400" },
  { title: "汉服古风写真", author: "苏晴", likes: 218, gradient: "from-violet-200 to-purple-200", color: "from-violet-400 to-purple-400" },
  { title: "城市夜景街拍", author: "陈风", likes: 156, gradient: "from-sky-200 to-cyan-200", color: "from-sky-400 to-cyan-400" },
  { title: "日系胶片风格", author: "叶知秋", likes: 412, gradient: "from-emerald-200 to-teal-200", color: "from-emerald-400 to-teal-400" },
];

function handleSearch() { proxy.$tab.navigateTo('/pages/search/index'); }
function goPhotographers() { proxy.$tab.navigateTo('/pages/photographer/index'); }
function goPhotographerDetail() { proxy.$tab.navigateTo('/pages/photographer/detail'); }
function goDemand() { proxy.$tab.navigateTo('/pages/demand/index'); }
function goWorks() { proxy.$tab.navigateTo('/pages/works/index'); }
</script>
