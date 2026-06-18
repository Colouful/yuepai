<template>
  <view class="min-h-screen" style="background: linear-gradient(180deg, #FDF2F8 0%, #FFFFFF 40%, #F5F3FF 100%)">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <!-- Header -->
    <view class="px-5 pt-3 pb-2">
      <view class="flex items-center justify-between">
        <view>
          <text class="text-[22px] font-black tracking-tight" style="background:linear-gradient(135deg,#EC4899,#A78BFA);-webkit-background-clip:text;-webkit-text-fill-color:transparent">约拍</text>
          <text class="text-[10px] text-slate-400 block ml-0.5">记录美好瞬间</text>
        </view>
        <view class="flex items-center space-x-2.5">
          <view class="relative size-10 rounded-2xl bg-white flex items-center justify-center" style="box-shadow:0 2px 12px rgba(244,114,182,0.1)">
            <view class="i-lucide-bell text-slate-500 text-lg"></view>
            <view class="absolute -top-0.5 -right-0.5 size-2.5 rounded-full bg-rose-400 border-2 border-white"></view>
          </view>
          <view class="size-10 rounded-2xl flex items-center justify-center" style="background:linear-gradient(135deg,#F472B6,#A78BFA);box-shadow:0 4px 15px rgba(244,114,182,0.25)" @click="$tab.navigateTo('/pages/search/index')">
            <view class="i-lucide-search text-white text-lg"></view>
          </view>
        </view>
      </view>

      <!-- 定位 + 搜索 -->
      <view class="mt-3 flex items-center space-x-1.5 mb-3">
        <view class="i-lucide-map-pin text-rose-400 text-xs"></view>
        <text class="text-xs text-slate-500 font-semibold">北京</text>
        <view class="i-lucide-chevron-down text-slate-400 text-[10px]"></view>
      </view>
      <view class="h-11 rounded-2xl bg-white flex items-center px-4" style="box-shadow:0 2px 12px rgba(244,114,182,0.08)" @click="$tab.navigateTo('/pages/search/index')">
        <view class="i-lucide-search text-rose-300 text-sm mr-2"></view>
        <text class="text-sm text-slate-300">搜索摄影师、模特、作品...</text>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-24 space-y-5">

        <!-- Banner -->
        <swiper class="h-44 rounded-3xl overflow-hidden" autoplay interval="4000" circular indicator-dots indicator-color="rgba(255,255,255,0.4)" indicator-active-color="#FFFFFF">
          <swiper-item>
            <view class="h-full w-full flex items-center px-6" style="background:linear-gradient(135deg,#EC4899 0%,#A78BFA 50%,#8B5CF6 100%)">
              <view class="flex-1">
                <text class="text-white text-xl font-black block">新人专享</text>
                <text class="text-white/80 text-xs block mt-1">首单立减50元</text>
                <view class="mt-3 rounded-full bg-white/25 px-5 py-2 text-xs font-bold text-white inline-block backdrop-blur-sm">立即领取</view>
              </view>
              <view class="i-lucide-camera text-white/20 text-[80px]"></view>
            </view>
          </swiper-item>
          <swiper-item>
            <view class="h-full w-full flex items-center px-6" style="background:linear-gradient(135deg,#38BDF8 0%,#34D399 100%)">
              <view class="flex-1">
                <text class="text-white text-xl font-black block">互勉创作</text>
                <text class="text-white/80 text-xs block mt-1">免费约拍机会</text>
                <view class="mt-3 rounded-full bg-white/25 px-5 py-2 text-xs font-bold text-white inline-block backdrop-blur-sm">去看看</view>
              </view>
              <view class="i-lucide-heart text-white/20 text-[80px]"></view>
            </view>
          </swiper-item>
        </swiper>

        <!-- 快捷入口 -->
        <view class="flex justify-between px-1">
          <view v-for="e in entries" :key="e.label" class="flex flex-col items-center" @click="e.fn()">
            <view class="size-14 rounded-2xl flex items-center justify-center mb-2 active:scale-90 transition-transform duration-200" :style="{background:e.bg, boxShadow:e.shadow}">
              <view :class="e.icon" class="text-2xl text-white"></view>
            </view>
            <text class="text-[11px] font-semibold text-slate-600">{{ e.label }}</text>
          </view>
        </view>

        <!-- 频道标签 -->
        <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
          <view class="inline-flex space-x-2">
            <view v-for="(ch, i) in channels" :key="ch" class="inline-block rounded-full px-4 py-2 text-xs font-bold transition-all duration-300"
              :style="chIdx===i ? 'background:linear-gradient(135deg,#F472B6,#A78BFA);color:#fff;box-shadow:0 4px 15px rgba(244,114,182,0.3)' : 'background:rgba(255,255,255,0.9);color:#64748B;box-shadow:0 2px 8px rgba(244,114,182,0.06)'"
              @click="chIdx=i">{{ ch }}</view>
          </view>
        </scroll-view>

        <!-- 附近摄影师 -->
        <view>
          <view class="flex items-center justify-between mb-3">
            <view class="flex items-center space-x-2">
              <view class="h-5 w-1 rounded-full" style="background:linear-gradient(180deg,#F472B6,#A78BFA)"></view>
              <text class="text-[15px] font-black text-slate-800">附近摄影师</text>
            </view>
            <text class="text-xs font-semibold text-rose-400" @click="$tab.navigateTo('/pages/photographer/index')">全部</text>
          </view>
          <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
            <view class="inline-flex space-x-3">
              <view v-for="p in photographers" :key="p.name" class="inline-block w-36 rounded-2xl bg-white p-3 active:scale-95 transition-transform duration-200" style="box-shadow:0 2px 12px rgba(244,114,182,0.08)" @click="$tab.navigateTo('/pages/photographer/detail')">
                <view class="flex items-center space-x-2.5 mb-2">
                  <view class="size-11 rounded-xl flex items-center justify-center text-white font-bold text-sm" :style="{background:p.bg}">{{ p.name[0] }}</view>
                  <view class="flex-1 min-w-0">
                    <text class="text-sm font-bold text-slate-800 block truncate">{{ p.name }}</text>
                    <text class="text-[10px] text-slate-400 block">{{ p.style }}</text>
                  </view>
                </view>
                <view class="flex items-center justify-between">
                  <text class="text-[10px] text-slate-400">{{ p.city }}</text>
                  <view class="flex items-center space-x-0.5">
                    <view class="i-lucide-star text-amber-400 text-[10px]"></view>
                    <text class="text-[10px] font-bold text-slate-600">{{ p.rating }}</text>
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
              <view class="h-5 w-1 rounded-full" style="background:linear-gradient(180deg,#38BDF8,#34D399)"></view>
              <text class="text-[15px] font-black text-slate-800">热门需求</text>
            </view>
            <text class="text-xs font-semibold text-rose-400" @click="$tab.navigateTo('/pages/demand/index')">更多</text>
          </view>
          <view class="space-y-3">
            <view v-for="d in demands" :key="d.title" class="rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform duration-200" style="box-shadow:0 2px 12px rgba(244,114,182,0.06)">
              <view class="flex items-start justify-between mb-2">
                <view class="flex-1">
                  <view class="flex items-center space-x-2 mb-1">
                    <view class="rounded-lg px-2 py-0.5 text-[10px] font-black" :style="d.mutual ? 'background:#ECFDF5;color:#059669' : 'background:#FDF2F8;color:#EC4899'">{{ d.tag }}</view>
                    <text class="text-sm font-bold text-slate-800">{{ d.title }}</text>
                  </view>
                  <text class="text-[11px] text-slate-400">{{ d.info }}</text>
                </view>
                <text class="text-base font-black text-rose-500">{{ d.price }}</text>
              </view>
              <view class="flex items-center justify-between">
                <view class="flex items-center space-x-1.5">
                  <view class="size-6 rounded-full flex items-center justify-center text-white text-[8px] font-bold" :style="{background:d.avatarBg}">{{ d.user[0] }}</view>
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
              <view class="h-5 w-1 rounded-full" style="background:linear-gradient(180deg,#FBBF24,#FB923C)"></view>
              <text class="text-[15px] font-black text-slate-800">精选作品</text>
            </view>
            <text class="text-xs font-semibold text-rose-400" @click="$tab.navigateTo('/pages/works/index')">更多</text>
          </view>
          <view class="flex flex-wrap gap-2.5">
            <view v-for="w in works" :key="w.title" class="w-[48%] rounded-2xl bg-white overflow-hidden active:scale-95 transition-transform duration-200" style="box-shadow:0 2px 12px rgba(244,114,182,0.06)">
              <view class="h-36" :style="{background:w.bg}"></view>
              <view class="p-3">
                <text class="text-xs font-bold text-slate-800 block truncate">{{ w.title }}</text>
                <view class="mt-1.5 flex items-center justify-between">
                  <view class="flex items-center space-x-1">
                    <view class="size-4 rounded-full flex items-center justify-center text-white text-[6px] font-bold" :style="{background:w.avatarBg}">{{ w.author[0] }}</view>
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
const statusBarH = ref(44);
const scrollH = ref(600);
const chIdx = ref(0);
try { const s = uni.getSystemInfoSync(); statusBarH.value = s.statusBarHeight||44; scrollH.value = s.windowHeight - statusBarH.value - 60; } catch(e){}

const channels = ["推荐","附近","摄影师","模特","互勉","旅拍","婚纱","古风"];
const entries = [
  { label:"找摄影师", icon:"i-lucide-camera", bg:"linear-gradient(135deg,#F472B6,#EC4899)", shadow:"0 4px 15px rgba(244,114,182,0.3)", fn:()=>proxy.$tab.navigateTo('/pages/photographer/index') },
  { label:"找模特", icon:"i-lucide-user", bg:"linear-gradient(135deg,#A78BFA,#8B5CF6)", shadow:"0 4px 15px rgba(167,139,250,0.3)", fn:()=>proxy.$tab.navigateTo('/pages/model/index') },
  { label:"需求大厅", icon:"i-lucide-megaphone", bg:"linear-gradient(135deg,#38BDF8,#0EA5E9)", shadow:"0 4px 15px rgba(56,189,248,0.3)", fn:()=>proxy.$tab.navigateTo('/pages/demand/index') },
  { label:"拍场地", icon:"i-lucide-map-pin", bg:"linear-gradient(135deg,#34D399,#10B981)", shadow:"0 4px 15px rgba(52,211,153,0.3)", fn:()=>proxy.$tab.navigateTo('/pages/venue/index') },
];
const photographers = [
  { name:"林默", style:"人像写真", city:"北京", rating:"4.9", bg:"linear-gradient(135deg,#F472B6,#EC4899)" },
  { name:"苏晴", style:"婚纱摄影", city:"上海", rating:"4.8", bg:"linear-gradient(135deg,#A78BFA,#8B5CF6)" },
  { name:"陈风", style:"商业摄影", city:"广州", rating:"4.7", bg:"linear-gradient(135deg,#38BDF8,#0EA5E9)" },
  { name:"叶知秋", style:"写真摄影", city:"成都", rating:"4.9", bg:"linear-gradient(135deg,#34D399,#10B981)" },
  { name:"白鹭", style:"古风摄影", city:"杭州", rating:"4.8", bg:"linear-gradient(135deg,#FBBF24,#F59E0B)" },
];
const demands = [
  { title:"周末人像写真", tag:"¥500", info:"人像 · 北京朝阳 · 6月20日", price:"¥500", user:"小雨", apply:12, mutual:false, avatarBg:"linear-gradient(135deg,#F472B6,#EC4899)" },
  { title:"古风汉服互勉", tag:"互勉", info:"古风 · 杭州西湖 · 6月22日", price:"免费", user:"苏晴", apply:8, mutual:true, avatarBg:"linear-gradient(135deg,#A78BFA,#8B5CF6)" },
  { title:"婚纱照拍摄", tag:"¥2000", info:"婚纱 · 上海外滩 · 6月25日", price:"¥2k", user:"陈先生", apply:5, mutual:false, avatarBg:"linear-gradient(135deg,#38BDF8,#0EA5E9)" },
];
const works = [
  { title:"夏日清新人像", author:"林默", likes:326, bg:"linear-gradient(135deg,#FBCFE8,#F9A8D4)", avatarBg:"linear-gradient(135deg,#F472B6,#EC4899)" },
  { title:"汉服古风写真", author:"苏晴", likes:218, bg:"linear-gradient(135deg,#DDD6FE,#C4B5FD)", avatarBg:"linear-gradient(135deg,#A78BFA,#8B5CF6)" },
  { title:"城市夜景街拍", author:"陈风", likes:156, bg:"linear-gradient(135deg,#BAE6FD,#7DD3FC)", avatarBg:"linear-gradient(135deg,#38BDF8,#0EA5E9)" },
  { title:"日系胶片风格", author:"叶知秋", likes:412, bg:"linear-gradient(135deg,#A7F3D0,#6EE7B7)", avatarBg:"linear-gradient(135deg,#34D399,#10B981)" },
];
</script>
