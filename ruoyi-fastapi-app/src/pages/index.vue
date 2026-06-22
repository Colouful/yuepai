<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <view class="px-5 pt-3 pb-3">
      <view class="flex items-center justify-between">
        <view class="flex items-center" @click="open('/pages/city/index')">
          <view>
            <text class="yp-eyebrow block">YUEPAI</text>
            <view class="flex items-center mt-1">
              <text class="text-xl font-black text-zinc-900">北京</text>
              <view class="i-lucide-chevron-down text-zinc-400 text-sm ml-1"></view>
            </view>
          </view>
        </view>
        <view class="flex items-center space-x-2">
          <view class="relative size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="open('/pages/message/index')">
            <view class="i-lucide-bell text-zinc-700 text-lg"></view>
            <view class="absolute right-1 top-1 size-2 rounded-full bg-rose-500 border border-white"></view>
          </view>
          <view class="size-10 rounded-full bg-zinc-900 flex items-center justify-center" @click="open('/pages/search/index')">
            <view class="i-lucide-search text-white text-lg"></view>
          </view>
        </view>
      </view>

      <view class="mt-4 h-11 rounded-2xl bg-white border border-black/5 px-4 flex items-center" @click="open('/pages/search/index')">
        <view class="i-lucide-search text-zinc-400 text-sm mr-2"></view>
        <text class="text-sm text-zinc-400">搜索摄影师、模特、作品和约拍</text>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-6">
        <view class="relative h-52 rounded-[28px] overflow-hidden bg-zinc-900" @click="open('/pages/demand/index')">
          <view class="absolute -right-8 -top-12 size-48 rounded-full" style="background:rgba(244,63,94,.4);filter:blur(28px)"></view>
          <view class="absolute right-8 bottom-4 size-28 rounded-full border border-white/10"></view>
          <view class="absolute right-14 bottom-10 size-16 rounded-full border border-white/10"></view>
          <view class="absolute inset-0 p-6 flex flex-col justify-between">
            <view class="flex items-center justify-between">
              <view class="rounded-full bg-white/10 border border-white/10 px-3 py-1.5 text-[10px] font-bold text-white">同城灵感计划</view>
              <text class="text-[10px] text-white/45">VOL. 06</text>
            </view>
            <view>
              <text class="text-[11px] tracking-[4px] text-rose-300 block">CREATE TOGETHER</text>
              <text class="text-[25px] leading-tight font-black text-white block mt-2">这个周末，去拍一组<br />真正属于你的照片</text>
              <view class="mt-4 flex items-center">
                <view class="rounded-full bg-white px-4 py-2 text-[11px] font-black text-zinc-900">寻找搭档</view>
                <text class="text-[10px] text-white/55 ml-3">已有 286 人加入</text>
              </view>
            </view>
          </view>
        </view>

        <view class="grid grid-cols-4 gap-3">
          <view v-for="item in entries" :key="item.label" class="flex flex-col items-center" @click="open(item.path)">
            <view class="size-13 rounded-2xl bg-white border border-black/5 flex items-center justify-center">
              <view :class="item.icon" class="text-xl" :style="{ color: item.color }"></view>
            </view>
            <text class="text-[10px] font-semibold text-zinc-600 mt-2">{{ item.label }}</text>
          </view>
        </view>

        <view>
          <view class="flex items-end justify-between mb-3">
            <view>
              <text class="yp-section-title block">同城创作者</text>
              <text class="text-[10px] text-zinc-400 block mt-1">距离近，也懂你的审美</text>
            </view>
            <text class="text-xs font-bold text-rose-500" @click="open('/pages/photographer/index')">查看全部</text>
          </view>

          <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
            <view class="inline-flex space-x-3 pr-5">
              <view v-for="item in creators" :key="item.id" class="inline-block w-40 yp-card overflow-hidden" @click="open('/pages/photographer/detail')">
                <view class="relative h-28" :style="{ background: item.cover }">
                  <view class="absolute right-2 top-2 rounded-full bg-black/35 px-2 py-1 text-[9px] text-white">{{ item.distance }}</view>
                  <view class="absolute left-3 bottom-3 size-10 rounded-2xl bg-white/20 border border-white/25 flex items-center justify-center text-white font-black">{{ item.name[0] }}</view>
                </view>
                <view class="p-3">
                  <view class="flex items-center">
                    <text class="text-sm font-black text-zinc-900 truncate">{{ item.name }}</text>
                    <view class="i-lucide-badge-check text-rose-500 text-xs ml-1"></view>
                  </view>
                  <text class="text-[10px] text-zinc-400 block mt-1">{{ item.style }}</text>
                  <view class="mt-2 flex items-center justify-between">
                    <text class="text-[11px] font-black text-zinc-900">{{ item.price }}</text>
                    <view class="flex items-center">
                      <view class="i-lucide-star text-amber-400 text-[10px]"></view>
                      <text class="text-[10px] text-zinc-500 ml-0.5">{{ item.rating }}</text>
                    </view>
                  </view>
                </view>
              </view>
            </view>
          </scroll-view>
        </view>

        <view>
          <view class="flex items-end justify-between mb-3">
            <view>
              <text class="yp-section-title block">正在招募</text>
              <text class="text-[10px] text-zinc-400 block mt-1">找到合适的人，一起完成创作</text>
            </view>
            <text class="text-xs font-bold text-rose-500" @click="open('/pages/demand/index')">更多需求</text>
          </view>

          <view class="space-y-3">
            <view v-for="item in demands" :key="item.id" class="yp-card p-4" @click="open('/pages/demand/detail')">
              <view class="flex items-start">
                <view class="size-11 rounded-2xl flex items-center justify-center" :style="{ background: item.iconBackground }">
                  <view :class="item.icon" class="text-lg" :style="{ color: item.iconColor }"></view>
                </view>
                <view class="flex-1 ml-3 min-w-0">
                  <view class="flex items-center justify-between">
                    <text class="text-sm font-black text-zinc-900 truncate">{{ item.title }}</text>
                    <text class="text-sm font-black" :class="item.mutual ? 'text-emerald-600' : 'text-rose-500'">{{ item.price }}</text>
                  </view>
                  <text class="text-[10px] text-zinc-400 block mt-1.5">{{ item.meta }}</text>
                  <view class="mt-3 flex items-center justify-between">
                    <view class="flex items-center space-x-1.5">
                      <view v-for="role in item.roles" :key="role" class="rounded-full bg-zinc-100 px-2 py-1 text-[9px] text-zinc-500">{{ role }}</view>
                    </view>
                    <text class="text-[10px] text-zinc-300">{{ item.applicants }} 人报名</text>
                  </view>
                </view>
              </view>
            </view>
          </view>
        </view>

        <view>
          <view class="flex items-end justify-between mb-3">
            <view>
              <text class="yp-section-title block">灵感专题</text>
              <text class="text-[10px] text-zinc-400 block mt-1">从风格开始，找到你的表达</text>
            </view>
            <text class="text-xs font-bold text-rose-500" @click="open('/pages/works/index')">发现更多</text>
          </view>

          <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
            <view class="inline-flex space-x-3 pr-5">
              <view v-for="item in topics" :key="item.title" class="relative inline-block w-64 h-36 rounded-3xl overflow-hidden" :style="{ background: item.cover }" @click="open('/pages/works/index')">
                <view class="absolute inset-0" style="background:linear-gradient(180deg,transparent,rgba(0,0,0,.68))"></view>
                <view class="absolute left-4 right-4 bottom-4">
                  <text class="text-base font-black text-white block">{{ item.title }}</text>
                  <text class="text-[10px] text-white/60 block mt-1">{{ item.subtitle }}</text>
                </view>
              </view>
            </view>
          </scroll-view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { getCurrentInstance, ref } from "vue";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const scrollH = ref(600);

try {
  const systemInfo = uni.getSystemInfoSync();
  statusBarH.value = systemInfo.statusBarHeight || 44;
  scrollH.value = systemInfo.windowHeight - statusBarH.value - 112;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

const entries = [
  { label: "找摄影师", icon: "i-lucide-camera", color: "#f43f5e", path: "/pages/photographer/index" },
  { label: "找模特", icon: "i-lucide-user-round", color: "#7c3aed", path: "/pages/model/index" },
  { label: "需求大厅", icon: "i-lucide-megaphone", color: "#0284c7", path: "/pages/demand/index" },
  { label: "拍摄场地", icon: "i-lucide-map-pinned", color: "#059669", path: "/pages/venue/index" },
];

const creators = [
  { id: 1, name: "林默", style: "情绪人像 · 胶片", distance: "1.2km", price: "¥599 起", rating: "4.9", cover: "linear-gradient(145deg,#fecdd3,#fb7185 52%,#881337)" },
  { id: 2, name: "苏晴", style: "婚纱纪实 · 旅拍", distance: "2.8km", price: "¥899 起", rating: "4.8", cover: "linear-gradient(145deg,#ddd6fe,#8b5cf6 52%,#3b0764)" },
  { id: 3, name: "陈风", style: "商业摄影 · 街拍", distance: "3.6km", price: "¥699 起", rating: "4.7", cover: "linear-gradient(145deg,#bae6fd,#0ea5e9 52%,#082f49)" },
  { id: 4, name: "白鹭", style: "汉服古风 · 棚拍", distance: "4.1km", price: "¥799 起", rating: "4.9", cover: "linear-gradient(145deg,#d1fae5,#10b981 52%,#022c22)" },
];

const demands = [
  { id: 1, title: "周末三里屯情绪人像", price: "¥500", meta: "北京朝阳 · 6 月 20 日 · 约 3 小时", roles: ["摄影师", "化妆师"], applicants: 12, mutual: false, icon: "i-lucide-aperture", iconBackground: "#fff1f2", iconColor: "#f43f5e" },
  { id: 2, title: "西湖宋制汉服互勉创作", price: "互勉", meta: "杭州西湖 · 6 月 22 日 · 下午", roles: ["摄影师", "模特"], applicants: 8, mutual: true, icon: "i-lucide-flower-2", iconBackground: "#f0fdf4", iconColor: "#059669" },
  { id: 3, title: "城市品牌夏季 Lookbook", price: "¥2000", meta: "上海静安 · 6 月 25 日 · 全天", roles: ["模特", "造型师"], applicants: 5, mutual: false, icon: "i-lucide-sparkles", iconBackground: "#fffbeb", iconColor: "#d97706" },
];

const topics = [
  { title: "城市夜色", subtitle: "霓虹、街道与情绪表达", cover: "linear-gradient(135deg,#18181b,#312e81 55%,#f43f5e)" },
  { title: "东方新叙事", subtitle: "汉服与现代审美的碰撞", cover: "linear-gradient(135deg,#064e3b,#10b981 55%,#fef3c7)" },
  { title: "胶片日常", subtitle: "记录真实而松弛的瞬间", cover: "linear-gradient(135deg,#78350f,#f59e0b 55%,#fef3c7)" },
];

function open(path) {
  proxy.$tab.navigateTo(path);
}
</script>
