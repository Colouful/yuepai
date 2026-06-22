<template>
  <view class="yp-page flex h-full flex-col">
    <view class="bg-white/90 px-5 pt-4 pb-3 border-b border-black/5">
      <view class="flex items-end justify-between">
        <view>
          <text class="yp-eyebrow block">PHOTOGRAPHERS</text>
          <text class="yp-title block mt-1">找摄影师</text>
        </view>
        <view class="rounded-full bg-zinc-100 px-3 py-2 flex items-center" @click="showSort = !showSort">
          <view class="i-lucide-arrow-up-down text-zinc-500 text-xs mr-1"></view>
          <text class="text-[10px] font-bold text-zinc-600">{{ sortLabel }}</text>
        </view>
      </view>

      <view class="mt-4 h-11 rounded-2xl bg-zinc-100 px-4 flex items-center">
        <view class="i-lucide-search text-zinc-400 text-sm mr-2"></view>
        <input
          v-model="keyword"
          confirm-type="search"
          placeholder="搜索摄影师、擅长风格"
          placeholder-class="text-zinc-300"
          class="flex-1 text-sm text-zinc-900"
          @confirm="reload"
        />
        <view v-if="keyword" class="i-lucide-circle-x text-zinc-300" @click="clearKeyword"></view>
      </view>

      <scroll-view scroll-x class="mt-3 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2 pr-5">
          <view
            v-for="tag in tags"
            :key="tag"
            class="yp-chip"
            :class="activeTag === tag ? 'yp-chip-active' : ''"
            @click="selectTag(tag)"
          >
            {{ tag }}
          </view>
        </view>
      </scroll-view>

      <view v-if="showSort" class="mt-3 yp-card p-2 grid grid-cols-2 gap-2">
        <view
          v-for="item in sortOptions"
          :key="item.value"
          class="rounded-xl px-3 py-2 text-xs text-center"
          :class="sortBy === item.value ? 'bg-zinc-900 text-white font-bold' : 'bg-zinc-50 text-zinc-500'"
          @click="selectSort(item.value)"
        >
          {{ item.label }}
        </view>
      </view>
    </view>

    <scroll-view
      scroll-y
      refresher-enabled
      :refresher-triggered="refreshing"
      class="flex-1"
      :show-scrollbar="false"
      @refresherrefresh="refresh"
      @scrolltolower="loadMore"
    >
      <view class="px-5 pt-4 pb-24 space-y-3">
        <view v-if="loading && !creators.length" class="space-y-3">
          <view v-for="item in 4" :key="item" class="yp-card h-44 animate-pulse bg-white/70"></view>
        </view>

        <view v-else-if="errorMessage && !creators.length" class="py-20 text-center">
          <view class="i-lucide-wifi-off text-3xl text-rose-400"></view>
          <text class="text-sm font-black text-zinc-700 block mt-4">摄影师加载失败</text>
          <text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text>
          <view class="mt-4 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="reload">重新加载</view>
        </view>

        <view v-else-if="!creators.length" class="py-20 text-center">
          <view class="i-lucide-camera-off text-3xl text-zinc-300"></view>
          <text class="text-sm font-black text-zinc-700 block mt-4">暂无符合条件的摄影师</text>
          <text class="text-xs text-zinc-400 block mt-2">换个关键词或风格试试</text>
        </view>

        <view
          v-for="creator in creators"
          :key="creator.creatorId"
          class="yp-card overflow-hidden active:scale-[0.99] transition-transform"
          @click="openDetail(creator)"
        >
          <view class="p-4 flex items-center">
            <image
              v-if="creator.avatarUrl"
              :src="creator.avatarUrl"
              mode="aspectFill"
              class="size-16 rounded-2xl bg-zinc-100 shrink-0"
            />
            <view v-else class="size-16 rounded-2xl bg-zinc-900 flex items-center justify-center text-xl font-black text-white shrink-0">
              {{ creator.displayName?.slice(0, 1) || '摄' }}
            </view>
            <view class="flex-1 min-w-0 ml-3">
              <view class="flex items-center">
                <text class="text-sm font-black text-zinc-900 truncate">{{ creator.displayName }}</text>
                <view v-if="creator.certificationStatus === 'approved'" class="i-lucide-badge-check text-amber-500 text-sm ml-1"></view>
              </view>
              <text class="text-xs text-zinc-500 block mt-1 truncate">{{ creator.headline || '专业摄影服务' }}</text>
              <text class="text-[10px] text-zinc-400 block mt-1">{{ creator.cityCode }} · 从业 {{ creator.yearsExperience }} 年</text>
              <view class="flex items-center space-x-3 mt-2">
                <view class="flex items-center"><view class="i-lucide-star text-amber-400 text-[10px] mr-1"></view><text class="text-[10px] font-bold text-zinc-600">{{ Number(creator.rating || 0).toFixed(1) }}</text></view>
                <text class="text-[10px] text-zinc-400">{{ creator.completedOrders }} 单</text>
                <text class="text-[10px] text-zinc-400">回复率 {{ creator.responseRate }}%</text>
              </view>
            </view>
            <view class="ml-3 text-right">
              <text class="text-base font-black text-rose-500">¥{{ money(creator.basePrice) }}</text>
              <text class="text-[9px] text-zinc-400 block">起/次</text>
            </view>
          </view>

          <view v-if="creator.workCovers?.length" class="px-4 pb-4 flex space-x-2">
            <image
              v-for="url in creator.workCovers"
              :key="url"
              :src="url"
              mode="aspectFill"
              class="h-20 flex-1 rounded-xl bg-zinc-100"
            />
          </view>

          <view class="px-4 pb-4 flex flex-wrap gap-1.5">
            <view v-for="tag in creator.tags?.slice(0, 5)" :key="tag" class="rounded-full bg-zinc-100 px-2 py-1 text-[9px] text-zinc-500">{{ tag }}</view>
            <view v-if="creator.acceptMutual" class="rounded-full bg-emerald-50 px-2 py-1 text-[9px] text-emerald-600">接受互勉</view>
          </view>
        </view>

        <view v-if="loading && creators.length" class="py-4 text-center text-xs text-zinc-400">正在加载更多…</view>
        <view v-else-if="creators.length && creators.length >= total" class="py-4 text-center text-xs text-zinc-300">已经到底了</view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { listCreators } from "@/api/yuepai/creator-api";

const { proxy } = getCurrentInstance();
const tags = ["全部", "人像", "婚纱", "古风", "街拍", "商业", "旅拍"];
const sortOptions = [
  { label: "最新入驻", value: "latest" },
  { label: "评分最高", value: "rating" },
  { label: "成交最多", value: "orders" },
  { label: "价格从低到高", value: "priceAsc" },
  { label: "价格从高到低", value: "priceDesc" },
];
const activeTag = ref("全部");
const keyword = ref("");
const sortBy = ref("rating");
const showSort = ref(false);
const creators = ref([]);
const total = ref(0);
const pageNum = ref(1);
const pageSize = 20;
const loading = ref(false);
const refreshing = ref(false);
const errorMessage = ref("");
const sortLabel = computed(() => sortOptions.find((item) => item.value === sortBy.value)?.label || "综合排序");

onLoad(() => reload());

async function fetchPage(reset = false) {
  if (loading.value) return;
  loading.value = true;
  errorMessage.value = "";
  try {
    const response = await listCreators({
      roleCode: "photographer",
      keyword: keyword.value.trim() || undefined,
      tag: activeTag.value === "全部" ? undefined : activeTag.value,
      sortBy: sortBy.value,
      pageNum: reset ? 1 : pageNum.value,
      pageSize,
    });
    const rows = Array.isArray(response.rows) ? response.rows : [];
    total.value = Number(response.total || rows.length);
    if (reset) {
      creators.value = rows;
      pageNum.value = 2;
    } else {
      creators.value.push(...rows.filter((row) => !creators.value.some((item) => item.creatorId === row.creatorId)));
      pageNum.value += 1;
    }
  } catch (error) {
    errorMessage.value = error?.message || "网络异常，请稍后重试";
  } finally {
    loading.value = false;
    refreshing.value = false;
    uni.stopPullDownRefresh();
  }
}

function reload() { pageNum.value = 1; total.value = 0; fetchPage(true); }
function refresh() { refreshing.value = true; reload(); }
function loadMore() { if (!loading.value && creators.value.length < total.value) fetchPage(false); }
function selectTag(tag) { activeTag.value = tag; reload(); }
function selectSort(value) { sortBy.value = value; showSort.value = false; reload(); }
function clearKeyword() { keyword.value = ""; reload(); }
function openDetail(creator) { proxy.$tab.navigateTo(`/pages/photographer/detail?id=${creator.creatorId}`); }
function money(value) { return Number(value || 0).toFixed(0); }
</script>
