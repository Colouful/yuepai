<template>
  <view class="yp-page flex h-full flex-col">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3">
      <view class="flex items-end justify-between">
        <view>
          <text class="yp-eyebrow block">OPPORTUNITIES</text>
          <text class="yp-title block mt-1">需求大厅</text>
        </view>
        <view class="rounded-full bg-zinc-900 px-4 py-2.5 flex items-center" @click="openPublish">
          <view class="i-lucide-plus text-white text-sm mr-1"></view>
          <text class="text-xs font-bold text-white">发布约拍</text>
        </view>
      </view>

      <view class="mt-4 h-11 rounded-2xl bg-white border border-black/5 px-4 flex items-center">
        <view class="i-lucide-search text-zinc-400 text-sm mr-2"></view>
        <input
          v-model="keyword"
          confirm-type="search"
          placeholder="搜索主题、地点或角色"
          placeholder-class="text-zinc-300"
          class="flex-1 text-sm text-zinc-900"
          @confirm="reload"
        />
        <view v-if="keyword" class="i-lucide-circle-x text-zinc-300" @click="clearKeyword"></view>
      </view>

      <scroll-view scroll-x class="mt-4 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2 pr-5">
          <view
            v-for="item in categories"
            :key="item.value"
            class="yp-chip"
            :class="activeCategory === item.value ? 'yp-chip-active' : ''"
            @click="selectCategory(item.value)"
          >
            {{ item.label }}
          </view>
        </view>
      </scroll-view>
    </view>

    <scroll-view
      scroll-y
      refresher-enabled
      :refresher-triggered="refreshing"
      :show-scrollbar="false"
      class="flex-1"
      @refresherrefresh="refresh"
      @scrolltolower="loadMore"
    >
      <view class="px-5 pb-28 space-y-3">
        <view v-if="loading && !records.length" class="space-y-3">
          <view v-for="item in 4" :key="item" class="yp-card h-40 animate-pulse bg-white/70"></view>
        </view>

        <view v-else-if="errorMessage && !records.length" class="py-20 flex flex-col items-center">
          <view class="size-16 rounded-full bg-rose-50 flex items-center justify-center">
            <view class="i-lucide-wifi-off text-2xl text-rose-500"></view>
          </view>
          <text class="text-sm font-black text-zinc-700 mt-4">需求加载失败</text>
          <text class="text-xs text-zinc-400 mt-2 text-center">{{ errorMessage }}</text>
          <view class="mt-4 rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="reload">重新加载</view>
        </view>

        <view v-else-if="!records.length" class="py-20 flex flex-col items-center">
          <view class="size-16 rounded-full bg-zinc-100 flex items-center justify-center">
            <view class="i-lucide-megaphone-off text-2xl text-zinc-400"></view>
          </view>
          <text class="text-sm font-black text-zinc-700 mt-4">暂无公开招募</text>
          <text class="text-xs text-zinc-400 mt-2">发布自己的约拍需求，等待创作者报名</text>
        </view>

        <view v-for="item in visibleRecords" :key="item.demandId" class="yp-card p-4" @click="openDetail(item)">
          <view class="flex items-start justify-between">
            <view class="flex-1 min-w-0">
              <view class="flex items-center">
                <view
                  class="rounded-full px-2 py-1 text-[9px] font-bold"
                  :class="isMutual(item) ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-500'"
                >
                  {{ isMutual(item) ? '互勉' : '付费' }}
                </view>
                <text class="text-sm font-black text-zinc-900 ml-2 truncate">{{ item.title }}</text>
              </view>
              <text class="text-[10px] text-zinc-400 block mt-2">
                {{ item.cityCode }} · {{ formatDate(item.shootAt) }} · {{ formatDuration(item.durationMinutes) }}
              </text>
            </view>
            <text class="text-base font-black ml-3" :class="isMutual(item) ? 'text-emerald-600' : 'text-rose-500'">
              {{ formatBudget(item) }}
            </text>
          </view>

          <text class="text-xs text-zinc-500 leading-relaxed block mt-3 line-clamp-2">{{ item.description }}</text>

          <view class="mt-3 flex flex-wrap gap-1.5">
            <view v-for="role in item.roles" :key="role" class="rounded-full bg-zinc-100 px-2 py-1 text-[9px] text-zinc-500">
              招 {{ role }}
            </view>
            <view class="rounded-full border border-black/5 px-2 py-1 text-[9px] text-zinc-400">{{ item.demandType }}</view>
          </view>

          <view class="mt-4 flex items-center justify-between">
            <text class="text-[10px] text-zinc-400">报名截止 {{ formatDate(item.applicationDeadline) }}</text>
            <text class="text-[10px] text-zinc-300">{{ item.applicantCount || 0 }} / {{ item.applicantLimit }} 人</text>
          </view>
        </view>

        <view v-if="loading && records.length" class="py-4 text-center text-xs text-zinc-400">正在加载更多…</view>
        <view v-else-if="records.length && records.length >= total" class="py-4 text-center text-xs text-zinc-300">已经到底了</view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { listDemands } from "@/api/yuepai/core";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const keyword = ref("");
const activeCategory = ref("");
const records = ref([]);
const pageNum = ref(1);
const pageSize = 20;
const total = ref(0);
const loading = ref(false);
const refreshing = ref(false);
const errorMessage = ref("");

const categories = [
  { label: "全部", value: "" },
  { label: "人像", value: "人像" },
  { label: "婚纱", value: "婚纱" },
  { label: "古风", value: "古风" },
  { label: "街拍", value: "街拍" },
  { label: "旅拍", value: "旅拍" },
  { label: "商业", value: "商业" },
];

const visibleRecords = computed(() => {
  const query = keyword.value.trim().toLowerCase();
  return records.value.filter((item) => {
    const categoryMatched = !activeCategory.value || item.demandType === activeCategory.value;
    const text = `${item.title || ""}${item.description || ""}${item.cityCode || ""}${(item.roles || []).join("")}`.toLowerCase();
    return categoryMatched && (!query || text.includes(query));
  });
});

onLoad(() => {
  try {
    statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44;
  } catch (error) {
    console.warn("获取设备信息失败", error);
  }
  reload();
});

async function fetchPage(reset = false) {
  if (loading.value) return;
  loading.value = true;
  errorMessage.value = "";
  try {
    const response = await listDemands({
      pageNum: reset ? 1 : pageNum.value,
      pageSize,
    });
    const rows = Array.isArray(response.rows) ? response.rows : [];
    total.value = Number(response.total || rows.length);
    if (reset) {
      records.value = rows;
      pageNum.value = 2;
    } else {
      records.value.push(...rows.filter((row) => !records.value.some((item) => item.demandId === row.demandId)));
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

function reload() {
  pageNum.value = 1;
  total.value = 0;
  fetchPage(true);
}

function refresh() {
  refreshing.value = true;
  reload();
}

function loadMore() {
  if (!loading.value && records.value.length < total.value) fetchPage(false);
}

function selectCategory(value) {
  activeCategory.value = value;
}

function clearKeyword() {
  keyword.value = "";
}

function isMutual(item) {
  return ["mutual", "free"].includes(item.budgetType);
}

function formatBudget(item) {
  if (isMutual(item)) return item.budgetType === "free" ? "免费" : "互勉";
  if (item.budgetType === "range") return `¥${item.budgetMin || 0}-${item.budgetMax || 0}`;
  if (item.budgetType === "quote" || item.budgetType === "negotiable") return "面议";
  return `¥${item.budgetMin || 0}`;
}

function formatDate(value) {
  if (!value) return "待确认";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hour = String(date.getHours()).padStart(2, "0");
  const minute = String(date.getMinutes()).padStart(2, "0");
  return `${month}-${day} ${hour}:${minute}`;
}

function formatDuration(minutes) {
  const value = Number(minutes || 0);
  if (value >= 480) return "全天";
  if (value >= 60) return `${Math.round(value / 60)} 小时`;
  return `${value} 分钟`;
}

function openDetail(item) {
  proxy.$tab.navigateTo(`/pages/demand/detail?id=${item.demandId}`);
}

function openPublish() {
  proxy.$tab.switchTab("/pages/publish/index");
}
</script>
