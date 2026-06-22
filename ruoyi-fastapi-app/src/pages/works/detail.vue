<template>
  <view class="yp-page min-h-screen pb-24">
    <view v-if="loading" class="pt-24 px-5 space-y-4">
      <view class="h-[720rpx] rounded-[32rpx] bg-white/70 animate-pulse"></view>
      <view class="h-36 rounded-[24rpx] bg-white/70 animate-pulse"></view>
    </view>

    <view v-else-if="errorMessage" class="pt-36 px-8 text-center">
      <view class="size-16 rounded-full bg-rose-50 mx-auto flex items-center justify-center">
        <view class="i-lucide-image-off text-2xl text-rose-500"></view>
      </view>
      <text class="text-base font-black text-zinc-800 block mt-4">作品加载失败</text>
      <text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text>
      <view class="mt-5 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="loadWork">重新加载</view>
    </view>

    <template v-else-if="work">
      <view class="relative bg-zinc-950">
        <swiper class="h-[860rpx]" circular :indicator-dots="work.assets?.length > 1" indicator-color="rgba(255,255,255,.35)" indicator-active-color="#fff">
          <swiper-item v-for="(url, index) in displayAssets" :key="url">
            <image :src="url" mode="aspectFit" class="w-full h-full" @click="preview(index)" />
          </swiper-item>
        </swiper>
        <view :style="{ height: statusBarH + 'px' }" class="absolute top-0 left-0 right-0"></view>
        <view class="absolute left-5 right-5 top-0 flex items-center justify-between" :style="{ paddingTop: statusBarH + 12 + 'px' }">
          <view class="size-10 rounded-full bg-black/35 backdrop-blur flex items-center justify-center" @click="goBack">
            <view class="i-lucide-arrow-left text-white text-lg"></view>
          </view>
          <view class="flex items-center space-x-2">
            <view class="size-10 rounded-full bg-black/35 backdrop-blur flex items-center justify-center" @click="shareWork">
              <view class="i-lucide-share-2 text-white"></view>
            </view>
            <view class="size-10 rounded-full bg-black/35 backdrop-blur flex items-center justify-center" @click="toggleFavorite">
              <view class="text-lg" :class="favorited ? 'i-lucide-heart fill-rose-500 text-rose-500' : 'i-lucide-heart text-white'"></view>
            </view>
          </view>
        </view>
      </view>

      <view class="px-5 pt-5 space-y-5">
        <view>
          <view class="flex items-start justify-between">
            <view class="flex-1 min-w-0">
              <text class="text-xl font-black text-zinc-900 block">{{ work.title }}</text>
              <text class="text-xs text-zinc-400 block mt-2">{{ work.cityCode || '未标注城市' }} · {{ formatDate(work.shotDate || work.createTime) }}</text>
            </view>
            <view class="ml-4 text-right">
              <view class="flex items-center justify-end"><view class="i-lucide-heart text-rose-400 text-xs mr-1"></view><text class="text-xs font-bold text-zinc-600">{{ work.favoriteCount }}</text></view>
              <view class="flex items-center justify-end mt-1"><view class="i-lucide-eye text-zinc-400 text-xs mr-1"></view><text class="text-[10px] text-zinc-400">{{ work.viewCount }}</text></view>
            </view>
          </view>
          <view class="flex flex-wrap gap-2 mt-4">
            <view class="rounded-full bg-zinc-900 px-3 py-1.5 text-[10px] font-bold text-white">{{ work.category }}</view>
            <view v-for="tag in work.tags" :key="tag" class="yp-chip">{{ tag }}</view>
          </view>
        </view>

        <view v-if="work.description" class="yp-card p-4">
          <text class="yp-section-title block mb-3">创作说明</text>
          <text class="text-xs text-zinc-500 leading-relaxed whitespace-pre-wrap">{{ work.description }}</text>
        </view>

        <view class="yp-card p-4 flex items-center" @click="openCreator">
          <image v-if="work.creator?.avatarUrl" :src="work.creator.avatarUrl" mode="aspectFill" class="size-12 rounded-2xl bg-zinc-100" />
          <view v-else class="size-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white">{{ work.creator?.displayName?.slice(0, 1) || '创' }}</view>
          <view class="flex-1 min-w-0 ml-3">
            <view class="flex items-center"><text class="text-sm font-black text-zinc-900 truncate">{{ work.creator?.displayName }}</text><view v-if="work.creator?.certificationStatus === 'approved'" class="i-lucide-badge-check text-amber-500 text-sm ml-1"></view></view>
            <text class="text-[10px] text-zinc-400 block mt-1">查看创作者资料、作品和服务套餐</text>
          </view>
          <view class="i-lucide-chevron-right text-zinc-300"></view>
        </view>

        <view class="rounded-2xl bg-amber-50 p-4 flex items-start">
          <view class="i-lucide-copyright text-amber-600 text-base mt-0.5 mr-3"></view>
          <text class="text-[10px] text-amber-700 leading-relaxed">作品版权归创作者或订单约定权利人所有。未经授权，不得下载、转载或用于商业用途。</text>
        </view>
      </view>

      <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3">
        <view class="size-12 rounded-2xl border border-black/10 flex items-center justify-center" @click="toggleFavorite">
          <view class="text-lg" :class="favorited ? 'i-lucide-heart fill-rose-500 text-rose-500' : 'i-lucide-heart text-zinc-700'"></view>
        </view>
        <view class="flex-1 h-12 rounded-2xl bg-zinc-900 text-white flex items-center justify-center text-sm font-black" @click="openCreator">联系创作者</view>
      </view>
    </template>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getToken } from "@/utils/auth";
import { getWork } from "@/api/yuepai/creator-api";
import { favoriteWork, getCreatorState, unfavoriteWork } from "@/api/yuepai/creator-social";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const workId = ref("");
const work = ref(null);
const favorited = ref(false);
const loading = ref(true);
const errorMessage = ref("");
const operating = ref(false);
const displayAssets = computed(() => work.value?.assets?.length ? work.value.assets : [work.value?.coverUrl].filter(Boolean));

onLoad((options) => {
  workId.value = options?.id || "";
  try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (error) { console.warn(error); }
  loadWork();
});

async function loadWork() {
  if (!workId.value) { errorMessage.value = "缺少作品编号"; loading.value = false; return; }
  loading.value = true;
  errorMessage.value = "";
  try {
    const response = await getWork(workId.value);
    work.value = response.data || response;
    if (getToken()) {
      try {
        const state = await getCreatorState(work.value.creatorId, { workId: workId.value });
        favorited.value = Boolean((state.data || state).favorited);
      } catch (error) { console.warn("读取收藏状态失败", error); }
    }
  } catch (error) {
    errorMessage.value = error?.message || "网络异常，请稍后重试";
  } finally { loading.value = false; }
}

async function toggleFavorite() {
  if (operating.value) return;
  if (!getToken()) return proxy.$tab.navigateTo("/pages/login");
  operating.value = true;
  try {
    const response = favorited.value ? await unfavoriteWork(workId.value) : await favoriteWork(workId.value);
    const data = response.data || response;
    favorited.value = Boolean(data.favorited);
    work.value.favoriteCount = Number(data.favoriteCount || 0);
    uni.showToast({ title: favorited.value ? "收藏成功" : "已取消收藏", icon: "none" });
  } finally { operating.value = false; }
}

function preview(index) { uni.previewImage({ current: index, urls: displayAssets.value }); }
function openCreator() { const role = work.value?.creator?.roleCode; const page = role === "model" ? "model" : "photographer"; proxy.$tab.navigateTo(`/pages/${page}/detail?id=${work.value.creatorId}`); }
function shareWork() { uni.setClipboardData({ data: `/pages/works/detail?id=${workId.value}`, success() { uni.showToast({ title: "页面路径已复制", icon: "none" }); } }); }
function formatDate(value) { if (!value) return ""; const date = new Date(value); if (Number.isNaN(date.getTime())) return String(value); return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`; }
function goBack() { proxy.$tab.navigateBack(); }
</script>
