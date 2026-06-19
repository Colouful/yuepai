<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <view class="px-5 pt-3 pb-3">
      <view class="flex items-center space-x-3">
        <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack">
          <view class="i-lucide-arrow-left text-zinc-700 text-lg"></view>
        </view>
        <view class="flex-1 h-11 rounded-2xl bg-white border border-black/5 px-4 flex items-center">
          <view class="i-lucide-search text-zinc-400 text-sm mr-2"></view>
          <input
            v-model="keyword"
            focus
            confirm-type="search"
            placeholder="搜索摄影师、模特、作品和约拍"
            placeholder-class="text-zinc-300"
            class="flex-1 text-sm text-zinc-900"
            @confirm="submitSearch"
          />
          <view v-if="keyword" class="i-lucide-circle-x text-zinc-300 text-sm" @click="keyword = ''"></view>
        </view>
        <text class="text-xs font-bold text-rose-500" @click="submitSearch">搜索</text>
      </view>

      <scroll-view v-if="hasSearched" scroll-x class="mt-4 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2 pr-5">
          <view
            v-for="item in tabs"
            :key="item.value"
            class="yp-chip"
            :class="activeTab === item.value ? 'yp-chip-active' : ''"
            @click="activeTab = item.value"
          >
            {{ item.label }} {{ item.count ? `(${item.count})` : '' }}
          </view>
        </view>
      </scroll-view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-24">
        <template v-if="!hasSearched">
          <view v-if="history.length" class="mb-6">
            <view class="flex items-center justify-between mb-3">
              <text class="yp-section-title">最近搜索</text>
              <view class="flex items-center text-zinc-400" @click="clearHistory">
                <view class="i-lucide-trash-2 text-xs mr-1"></view>
                <text class="text-[10px]">清空</text>
              </view>
            </view>
            <view class="flex flex-wrap gap-2">
              <view v-for="item in history" :key="item" class="yp-chip" @click="quickSearch(item)">{{ item }}</view>
            </view>
          </view>

          <view>
            <view class="flex items-center justify-between mb-3">
              <text class="yp-section-title">热门搜索</text>
              <text class="text-[10px] text-zinc-400">大家都在找</text>
            </view>
            <view class="yp-card overflow-hidden">
              <view
                v-for="(item, index) in hotKeywords"
                :key="item.keyword"
                class="flex items-center px-4 py-3.5"
                :class="index < hotKeywords.length - 1 ? 'border-b border-black/5' : ''"
                @click="quickSearch(item.keyword)"
              >
                <text class="w-7 text-sm font-black" :class="index < 3 ? 'text-rose-500' : 'text-zinc-300'">{{ index + 1 }}</text>
                <text class="flex-1 text-sm font-semibold text-zinc-700">{{ item.keyword }}</text>
                <text class="text-[10px] text-zinc-400">{{ item.count }} 次搜索</text>
              </view>
            </view>
          </view>

          <view class="mt-6">
            <text class="yp-section-title block mb-3">风格灵感</text>
            <view class="grid grid-cols-2 gap-3">
              <view v-for="item in inspirations" :key="item.title" class="relative h-28 rounded-3xl overflow-hidden" :style="{ background: item.cover }" @click="quickSearch(item.title)">
                <view class="absolute inset-0" style="background:linear-gradient(180deg,transparent,rgba(0,0,0,.6))"></view>
                <text class="absolute left-4 bottom-4 text-sm font-black text-white">{{ item.title }}</text>
              </view>
            </view>
          </view>
        </template>

        <template v-else>
          <view class="flex items-center justify-between mb-3">
            <text class="yp-section-title">搜索结果</text>
            <text class="text-xs text-zinc-400">共 {{ filteredResults.length }} 条</text>
          </view>

          <view v-if="filteredResults.length" class="space-y-3">
            <view v-for="item in filteredResults" :key="`${item.category}-${item.id}`" class="yp-card p-4" @click="openResult(item)">
              <view class="flex items-center">
                <view class="size-14 rounded-2xl flex items-center justify-center text-white font-black shrink-0" :style="{ background: item.cover }">
                  <view v-if="item.icon" :class="item.icon" class="text-xl"></view>
                  <text v-else>{{ item.title[0] }}</text>
                </view>
                <view class="flex-1 min-w-0 ml-3">
                  <view class="flex items-center">
                    <text class="text-sm font-black text-zinc-900 truncate">{{ item.title }}</text>
                    <view v-if="item.verified" class="i-lucide-badge-check text-rose-500 text-xs ml-1"></view>
                  </view>
                  <text class="text-xs text-zinc-500 block mt-1 truncate">{{ item.subtitle }}</text>
                  <view class="flex items-center mt-2">
                    <view class="rounded-full bg-zinc-100 px-2 py-1 text-[9px] text-zinc-500">{{ categoryLabel(item.category) }}</view>
                    <text class="text-[10px] text-zinc-300 ml-2">{{ item.meta }}</text>
                  </view>
                </view>
                <view class="i-lucide-chevron-right text-zinc-300 text-sm"></view>
              </view>
            </view>
          </view>

          <view v-else class="py-20 flex flex-col items-center">
            <view class="size-16 rounded-full bg-zinc-100 flex items-center justify-center">
              <view class="i-lucide-search-x text-2xl text-zinc-400"></view>
            </view>
            <text class="text-sm font-black text-zinc-700 mt-4">没有找到相关内容</text>
            <text class="text-xs text-zinc-400 mt-2">换个关键词或分类试试</text>
          </view>
        </template>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const scrollH = ref(600);
const keyword = ref("");
const submittedKeyword = ref("");
const activeTab = ref("all");
const history = ref(loadHistory());

try {
  const systemInfo = uni.getSystemInfoSync();
  statusBarH.value = systemInfo.statusBarHeight || 44;
  scrollH.value = systemInfo.windowHeight - statusBarH.value - 86;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

const hotKeywords = [
  { keyword: "北京人像摄影师", count: "2.8k" },
  { keyword: "汉服互勉", count: "2.1k" },
  { keyword: "日系写真", count: "1.9k" },
  { keyword: "同城陪拍", count: "1.6k" },
  { keyword: "婚纱旅拍", count: "1.2k" },
  { keyword: "胶片街拍", count: "980" },
];

const inspirations = [
  { title: "城市夜景", cover: "linear-gradient(135deg,#18181b,#312e81 55%,#f43f5e)" },
  { title: "东方古风", cover: "linear-gradient(135deg,#064e3b,#10b981 55%,#fef3c7)" },
  { title: "自然清新", cover: "linear-gradient(135deg,#d1fae5,#38bdf8 55%,#0369a1)" },
  { title: "胶片情绪", cover: "linear-gradient(135deg,#78350f,#f59e0b 55%,#292524)" },
];

const allResults = [
  { id: 1, category: "creator", title: "林默", subtitle: "人像摄影师 · 日系清新 / 情绪写真", meta: "北京 · 4.9 分 · 326 单", verified: true, cover: "linear-gradient(135deg,#fb7185,#be123c)", path: "/pages/photographer/detail?id=1", keywords: "北京 人像 日系 写真 摄影师 林默" },
  { id: 2, category: "creator", title: "苏晴", subtitle: "婚纱摄影师 · 纪实婚礼 / 旅拍", meta: "上海 · 4.8 分 · 218 单", verified: true, cover: "linear-gradient(135deg,#a78bfa,#5b21b6)", path: "/pages/photographer/detail?id=2", keywords: "上海 婚纱 旅拍 摄影师 苏晴" },
  { id: 3, category: "model", title: "木子", subtitle: "平面模特 · 日系 / JK / 街拍", meta: "北京 · 176cm · 可互勉", verified: true, cover: "linear-gradient(135deg,#38bdf8,#0369a1)", path: "/pages/model/detail?id=3", keywords: "北京 模特 日系 JK 街拍 木子 互勉" },
  { id: 4, category: "work", title: "旧街区的胶片情绪", subtitle: "陈风创作的城市街拍作品", meta: "广州 · 518 赞", icon: "i-lucide-image", cover: "linear-gradient(135deg,#78716c,#292524)", path: "/pages/profile/index?id=4", keywords: "胶片 街拍 城市 情绪 作品 陈风 广州" },
  { id: 5, category: "work", title: "西湖边的一场宋韵", subtitle: "白鹭创作的汉服古风作品", meta: "杭州 · 890 赞", icon: "i-lucide-image", cover: "linear-gradient(135deg,#34d399,#047857)", path: "/pages/profile/index?id=5", keywords: "汉服 古风 西湖 杭州 作品 白鹭" },
  { id: 6, category: "demand", title: "周末三里屯情绪人像", subtitle: "招募摄影师、化妆师，预算 500 元", meta: "北京朝阳 · 6 月 20 日", icon: "i-lucide-megaphone", cover: "linear-gradient(135deg,#f43f5e,#9f1239)", path: "/pages/demand/detail?id=6", keywords: "北京 三里屯 人像 写真 摄影师 化妆师 需求" },
  { id: 7, category: "demand", title: "西湖宋制汉服互勉", subtitle: "招募摄影师、模特进行互勉创作", meta: "杭州西湖 · 6 月 22 日", icon: "i-lucide-megaphone", cover: "linear-gradient(135deg,#10b981,#065f46)", path: "/pages/demand/detail?id=7", keywords: "杭州 西湖 汉服 古风 互勉 摄影师 模特" },
  { id: 8, category: "venue", title: "光屿自然光摄影棚", subtitle: "大面积落地窗、纯白景与生活化布景", meta: "北京朝阳 · 199 元/小时", icon: "i-lucide-map-pinned", cover: "linear-gradient(135deg,#fbbf24,#b45309)", path: "/pages/venue/detail?id=8", keywords: "北京 朝阳 摄影棚 场地 自然光 室内" },
];

const hasSearched = computed(() => Boolean(submittedKeyword.value.trim()));
const matchedResults = computed(() => {
  const words = submittedKeyword.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  return allResults.filter((item) => words.every((word) => `${item.title} ${item.subtitle} ${item.keywords}`.toLowerCase().includes(word)));
});
const filteredResults = computed(() => activeTab.value === "all" ? matchedResults.value : matchedResults.value.filter((item) => item.category === activeTab.value));
const tabs = computed(() => [
  { label: "全部", value: "all", count: matchedResults.value.length },
  { label: "创作者", value: "creator", count: matchedResults.value.filter((item) => item.category === "creator").length },
  { label: "模特", value: "model", count: matchedResults.value.filter((item) => item.category === "model").length },
  { label: "作品", value: "work", count: matchedResults.value.filter((item) => item.category === "work").length },
  { label: "约拍", value: "demand", count: matchedResults.value.filter((item) => item.category === "demand").length },
  { label: "场地", value: "venue", count: matchedResults.value.filter((item) => item.category === "venue").length },
]);

function loadHistory() {
  try {
    return uni.getStorageSync("yuepai_search_history") || ["人像写真", "婚纱摄影", "古风", "北京摄影师"];
  } catch (error) {
    return ["人像写真", "婚纱摄影", "古风", "北京摄影师"];
  }
}

function submitSearch() {
  const value = keyword.value.trim();
  if (!value) {
    uni.showToast({ title: "请输入搜索内容", icon: "none" });
    return;
  }
  submittedKeyword.value = value;
  activeTab.value = "all";
  history.value = [value, ...history.value.filter((item) => item !== value)].slice(0, 10);
  uni.setStorageSync("yuepai_search_history", history.value);
}

function quickSearch(value) {
  keyword.value = value;
  submitSearch();
}

function clearHistory() {
  history.value = [];
  uni.removeStorageSync("yuepai_search_history");
}

function categoryLabel(category) {
  return { creator: "摄影师", model: "模特", work: "作品", demand: "约拍", venue: "场地" }[category] || "内容";
}

function openResult(item) {
  proxy.$tab.navigateTo(item.path);
}

function goBack() {
  proxy.$tab.navigateBack();
}
</script>
