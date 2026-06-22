<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <view class="px-5 pt-3 pb-3">
      <view class="flex items-center justify-between">
        <view>
          <text class="yp-eyebrow block">CREATORS</text>
          <text class="yp-title block mt-1">找摄影师</text>
        </view>
        <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="openMap">
          <view class="i-lucide-map text-zinc-700 text-lg"></view>
        </view>
      </view>

      <view class="mt-4 flex items-center space-x-2">
        <view class="flex-1 h-11 rounded-2xl bg-white border border-black/5 px-4 flex items-center">
          <view class="i-lucide-search text-zinc-400 text-sm mr-2"></view>
          <input v-model="keyword" placeholder="搜索姓名、风格或城市" placeholder-class="text-zinc-300" class="flex-1 text-sm text-zinc-900" />
          <view v-if="keyword" class="i-lucide-circle-x text-zinc-300 text-sm" @click="keyword = ''"></view>
        </view>
        <view class="relative size-11 rounded-2xl bg-zinc-900 flex items-center justify-center" @click="filterVisible = true">
          <view class="i-lucide-sliders-horizontal text-white text-base"></view>
          <view v-if="activeFilterCount" class="absolute -right-1 -top-1 min-w-4 h-4 rounded-full bg-rose-500 px-1 flex items-center justify-center text-[9px] text-white">{{ activeFilterCount }}</view>
        </view>
      </view>

      <scroll-view scroll-x class="mt-4 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2 pr-5">
          <view v-for="tag in styleTags" :key="tag" class="yp-chip" :class="activeStyle === tag ? 'yp-chip-active' : ''" @click="activeStyle = tag">{{ tag }}</view>
        </view>
      </scroll-view>

      <view class="mt-3 flex items-center justify-between">
        <text class="text-xs text-zinc-400">找到 {{ filteredPhotographers.length }} 位创作者</text>
        <picker :range="sortOptions" range-key="label" @change="changeSort">
          <view class="flex items-center">
            <text class="text-xs font-bold text-zinc-700">{{ currentSort.label }}</text>
            <view class="i-lucide-chevron-down text-zinc-400 text-xs ml-1"></view>
          </view>
        </picker>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-24 space-y-3">
        <view v-for="item in filteredPhotographers" :key="item.id" class="yp-card overflow-hidden" @click="openDetail(item)">
          <view class="relative h-36" :style="{ background: item.cover }">
            <view class="absolute inset-0" style="background:linear-gradient(180deg,rgba(0,0,0,.02),rgba(0,0,0,.55))"></view>
            <view class="absolute left-4 top-4 rounded-full bg-white/90 px-3 py-1.5 text-[10px] font-bold text-zinc-800">{{ item.distance }} · {{ item.city }}</view>
            <view class="absolute right-4 top-4 size-8 rounded-full bg-white/90 flex items-center justify-center" @click.stop="toggleFavorite(item)">
              <view class="i-lucide-heart text-base" :class="item.favorite ? 'text-rose-500' : 'text-zinc-700'"></view>
            </view>
            <view class="absolute left-4 right-4 bottom-4 flex items-end">
              <view class="size-14 rounded-2xl bg-white/15 border border-white/20 flex items-center justify-center text-xl font-black text-white">{{ item.name[0] }}</view>
              <view class="flex-1 ml-3 min-w-0">
                <view class="flex items-center">
                  <text class="text-lg font-black text-white truncate">{{ item.name }}</text>
                  <view v-if="item.verified" class="i-lucide-badge-check text-rose-300 text-sm ml-1"></view>
                </view>
                <text class="text-xs text-white/65 block mt-1">{{ item.style }} · 从业 {{ item.experience }} 年</text>
              </view>
              <view class="text-right">
                <text class="text-lg font-black text-white">¥{{ item.price }}</text>
                <text class="text-[9px] text-white/55 block">起/次</text>
              </view>
            </view>
          </view>

          <view class="p-4">
            <view class="flex items-center justify-between">
              <view class="flex items-center space-x-3">
                <view class="flex items-center">
                  <view class="i-lucide-star text-amber-400 text-xs"></view>
                  <text class="text-xs font-black text-zinc-700 ml-1">{{ item.rating }}</text>
                  <text class="text-[10px] text-zinc-300 ml-1">({{ item.reviews }})</text>
                </view>
                <text class="text-[10px] text-zinc-400">{{ item.orders }} 单</text>
                <text class="text-[10px] text-zinc-400">回复 {{ item.responseRate }}%</text>
              </view>
              <text class="text-[10px] text-emerald-600">{{ item.available ? '本周可约' : '下周可约' }}</text>
            </view>

            <view class="mt-3 flex items-center justify-between">
              <view class="flex flex-wrap gap-1.5">
                <view v-for="tag in item.tags.slice(0, 3)" :key="tag" class="rounded-full bg-zinc-100 px-2 py-1 text-[9px] text-zinc-500">{{ tag }}</view>
              </view>
              <view class="rounded-full bg-zinc-900 px-4 py-2 text-[10px] font-bold text-white">查看主页</view>
            </view>
          </view>
        </view>

        <view v-if="!filteredPhotographers.length" class="py-20 flex flex-col items-center">
          <view class="size-16 rounded-full bg-zinc-100 flex items-center justify-center"><view class="i-lucide-user-search text-2xl text-zinc-400"></view></view>
          <text class="text-sm font-black text-zinc-700 mt-4">没有找到合适的摄影师</text>
          <text class="text-xs text-zinc-400 mt-2">调整风格、价格或城市后再试试</text>
          <view class="mt-4 rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="resetFilters">重置筛选</view>
        </view>
      </view>
    </scroll-view>

    <view v-if="filterVisible" class="fixed inset-0 z-50 flex items-end" @click="filterVisible = false">
      <view class="absolute inset-0 bg-black/35"></view>
      <view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop>
        <view class="flex items-center justify-between">
          <text class="text-lg font-black text-zinc-900">筛选摄影师</text>
          <view class="i-lucide-x text-zinc-500 text-lg" @click="filterVisible = false"></view>
        </view>

        <view class="mt-5">
          <text class="text-sm font-black text-zinc-800 block mb-3">所在城市</text>
          <view class="flex flex-wrap gap-2">
            <view v-for="city in cities" :key="city" class="yp-chip" :class="selectedCity === city ? 'yp-chip-active' : ''" @click="selectedCity = city">{{ city }}</view>
          </view>
        </view>

        <view class="mt-5">
          <text class="text-sm font-black text-zinc-800 block mb-3">价格区间</text>
          <view class="flex flex-wrap gap-2">
            <view v-for="price in priceRanges" :key="price.value" class="yp-chip" :class="selectedPrice === price.value ? 'yp-chip-active' : ''" @click="selectedPrice = price.value">{{ price.label }}</view>
          </view>
        </view>

        <view class="mt-5 flex items-center justify-between yp-card px-4 py-3">
          <view>
            <text class="text-sm font-black text-zinc-800 block">仅看本周可约</text>
            <text class="text-[10px] text-zinc-400 block mt-1">过滤档期已满的摄影师</text>
          </view>
          <switch :checked="onlyAvailable" color="#18181b" style="transform:scale(.78)" @change="onlyAvailable = $event.detail.value" />
        </view>

        <view class="mt-6 flex space-x-3">
          <view class="flex-1 h-12 rounded-2xl border border-black/10 flex items-center justify-center text-sm font-bold text-zinc-700" @click="resetFilters">重置</view>
          <view class="flex-1 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-bold text-white" @click="filterVisible = false">查看 {{ filteredPhotographers.length }} 位</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const scrollH = ref(600);
const keyword = ref("");
const activeStyle = ref("全部");
const selectedCity = ref("全部");
const selectedPrice = ref("all");
const onlyAvailable = ref(false);
const filterVisible = ref(false);
const sortIndex = ref(0);

try {
  const systemInfo = uni.getSystemInfoSync();
  statusBarH.value = systemInfo.statusBarHeight || 44;
  scrollH.value = systemInfo.windowHeight - statusBarH.value - 190;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

const styleTags = ["全部", "人像", "婚纱", "古风", "街拍", "商业", "旅拍"];
const cities = ["全部", "北京", "上海", "广州", "成都", "杭州"];
const priceRanges = [
  { label: "不限", value: "all" },
  { label: "500 以下", value: "low" },
  { label: "500-1000", value: "medium" },
  { label: "1000 以上", value: "high" },
];
const sortOptions = [
  { label: "综合排序", value: "default" },
  { label: "距离最近", value: "distance" },
  { label: "评分最高", value: "rating" },
  { label: "价格最低", value: "price" },
  { label: "接单最多", value: "orders" },
];
const currentSort = computed(() => sortOptions[sortIndex.value]);
const activeFilterCount = computed(() => [selectedCity.value !== "全部", selectedPrice.value !== "all", onlyAvailable.value].filter(Boolean).length);

const photographers = reactive([
  { id: 1, name: "林默", style: "人像摄影", city: "北京", rating: 4.9, reviews: 128, orders: 326, price: 500, distance: 1.2, experience: 5, responseRate: 98, verified: true, favorite: false, available: true, tags: ["日系清新", "情绪写真", "自然光"], cover: "linear-gradient(145deg,#fecdd3,#fb7185 52%,#881337)" },
  { id: 2, name: "苏晴", style: "婚纱摄影", city: "上海", rating: 4.8, reviews: 96, orders: 218, price: 1200, distance: 2.8, experience: 7, responseRate: 96, verified: true, favorite: true, available: false, tags: ["纪实婚礼", "海边旅拍", "轻复古"], cover: "linear-gradient(145deg,#ddd6fe,#8b5cf6 52%,#3b0764)" },
  { id: 3, name: "陈风", style: "商业摄影", city: "广州", rating: 4.7, reviews: 73, orders: 156, price: 800, distance: 3.6, experience: 6, responseRate: 92, verified: true, favorite: false, available: true, tags: ["品牌视觉", "街头人像", "产品摄影"], cover: "linear-gradient(145deg,#bae6fd,#0ea5e9 52%,#082f49)" },
  { id: 4, name: "叶知秋", style: "街拍摄影", city: "成都", rating: 4.9, reviews: 166, orders: 412, price: 399, distance: 1.8, experience: 4, responseRate: 99, verified: false, favorite: false, available: true, tags: ["城市夜景", "胶片情绪", "纪实"], cover: "linear-gradient(145deg,#c4b5fd,#6d28d9 52%,#18181b)" },
  { id: 5, name: "白鹭", style: "古风摄影", city: "杭州", rating: 4.8, reviews: 58, orders: 89, price: 699, distance: 4.1, experience: 3, responseRate: 94, verified: true, favorite: false, available: false, tags: ["宋制汉服", "园林取景", "妆造统筹"], cover: "linear-gradient(145deg,#d1fae5,#10b981 52%,#022c22)" },
  { id: 6, name: "远川", style: "旅拍摄影", city: "北京", rating: 4.7, reviews: 81, orders: 134, price: 999, distance: 5.2, experience: 5, responseRate: 90, verified: true, favorite: false, available: true, tags: ["户外旅拍", "情侣写真", "自然风光"], cover: "linear-gradient(145deg,#ccfbf1,#2dd4bf 52%,#134e4a)" },
]);

const filteredPhotographers = computed(() => {
  let list = photographers.filter((item) => {
    const keyMatched = !keyword.value.trim() || `${item.name}${item.style}${item.city}${item.tags.join("")}`.toLowerCase().includes(keyword.value.trim().toLowerCase());
    const styleMatched = activeStyle.value === "全部" || item.style.includes(activeStyle.value) || item.tags.some((tag) => tag.includes(activeStyle.value));
    const cityMatched = selectedCity.value === "全部" || item.city === selectedCity.value;
    const availableMatched = !onlyAvailable.value || item.available;
    const priceMatched = selectedPrice.value === "all"
      || (selectedPrice.value === "low" && item.price < 500)
      || (selectedPrice.value === "medium" && item.price >= 500 && item.price <= 1000)
      || (selectedPrice.value === "high" && item.price > 1000);
    return keyMatched && styleMatched && cityMatched && availableMatched && priceMatched;
  });

  list = [...list];
  switch (currentSort.value.value) {
    case "distance": list.sort((a, b) => a.distance - b.distance); break;
    case "rating": list.sort((a, b) => b.rating - a.rating); break;
    case "price": list.sort((a, b) => a.price - b.price); break;
    case "orders": list.sort((a, b) => b.orders - a.orders); break;
    default: list.sort((a, b) => Number(b.available) - Number(a.available) || b.rating - a.rating);
  }
  return list;
});

function changeSort(event) {
  sortIndex.value = Number(event.detail.value);
}

function toggleFavorite(item) {
  item.favorite = !item.favorite;
  uni.showToast({ title: item.favorite ? "已收藏" : "已取消收藏", icon: "none" });
}

function resetFilters() {
  selectedCity.value = "全部";
  selectedPrice.value = "all";
  onlyAvailable.value = false;
  activeStyle.value = "全部";
  keyword.value = "";
}

function openDetail(item) {
  proxy.$tab.navigateTo(`/pages/photographer/detail?id=${item.id}`);
}

function openMap() {
  uni.showToast({ title: "地图找摄影师正在接入", icon: "none" });
}
</script>
