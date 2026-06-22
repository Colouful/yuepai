<template>
  <view class="yp-page min-h-screen pb-28">
    <view v-if="loading" class="pt-24 px-5 space-y-4">
      <view class="h-72 rounded-[32rpx] bg-white/70 animate-pulse"></view>
      <view class="h-36 rounded-[24rpx] bg-white/70 animate-pulse"></view>
      <view class="h-52 rounded-[24rpx] bg-white/70 animate-pulse"></view>
    </view>

    <view v-else-if="errorMessage" class="pt-36 px-8 text-center">
      <view class="size-16 rounded-full bg-rose-50 mx-auto flex items-center justify-center">
        <view class="i-lucide-circle-alert text-2xl text-rose-500"></view>
      </view>
      <text class="text-base font-black text-zinc-800 block mt-4">摄影师详情加载失败</text>
      <text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text>
      <view class="mt-5 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="loadAll">重新加载</view>
    </view>

    <template v-else-if="creator">
      <view class="relative h-[620rpx] overflow-hidden bg-zinc-900">
        <image v-if="creator.coverUrl" :src="creator.coverUrl" mode="aspectFill" class="absolute inset-0 w-full h-full" />
        <view v-else class="absolute inset-0" style="background:linear-gradient(145deg,#18181b 0%,#3f3f46 52%,#881337 140%)"></view>
        <view class="absolute inset-0" style="background:linear-gradient(180deg,rgba(0,0,0,.08),rgba(0,0,0,.8))"></view>
        <view :style="{ height: statusBarH + 'px' }"></view>
        <view class="relative z-10 px-5 pt-3 flex items-center justify-between">
          <view class="size-10 rounded-full bg-black/30 backdrop-blur flex items-center justify-center" @click="goBack">
            <view class="i-lucide-arrow-left text-white text-lg"></view>
          </view>
          <view class="flex items-center space-x-2">
            <view class="size-10 rounded-full bg-black/30 backdrop-blur flex items-center justify-center" @click="shareProfile">
              <view class="i-lucide-share-2 text-white text-base"></view>
            </view>
            <view class="size-10 rounded-full bg-black/30 backdrop-blur flex items-center justify-center" @click="toggleFollow">
              <view class="text-lg" :class="followed ? 'i-lucide-heart fill-rose-500 text-rose-500' : 'i-lucide-heart text-white'"></view>
            </view>
          </view>
        </view>

        <view class="absolute left-0 right-0 bottom-0 z-10 px-5 pb-6">
          <view class="flex items-end">
            <image v-if="creator.avatarUrl" :src="creator.avatarUrl" mode="aspectFill" class="size-24 rounded-[32rpx] border-4 border-white/80 bg-zinc-100 shrink-0" />
            <view v-else class="size-24 rounded-[32rpx] border-4 border-white/80 bg-white flex items-center justify-center text-3xl font-black text-zinc-900 shrink-0">
              {{ creator.displayName?.slice(0, 1) || '摄' }}
            </view>
            <view class="flex-1 min-w-0 ml-4 pb-1">
              <view class="flex items-center">
                <text class="text-2xl font-black text-white truncate">{{ creator.displayName }}</text>
                <view v-if="creator.certificationStatus === 'approved'" class="i-lucide-badge-check text-amber-300 text-xl ml-2"></view>
              </view>
              <text class="text-xs text-white/70 block mt-1 truncate">{{ creator.headline || '专业摄影师' }}</text>
              <view class="flex items-center space-x-3 mt-3">
                <text class="text-[10px] text-white/60">{{ creator.cityCode }}</text>
                <text class="text-[10px] text-white/60">从业 {{ creator.yearsExperience }} 年</text>
                <text v-if="creator.acceptMutual" class="text-[10px] text-emerald-300">接受互勉</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <view class="px-5 -mt-1 relative z-20">
        <view class="yp-card grid grid-cols-4 py-4">
          <view class="text-center border-r border-black/5"><text class="text-base font-black text-zinc-900 block">{{ Number(creator.rating || 0).toFixed(1) }}</text><text class="text-[9px] text-zinc-400">综合评分</text></view>
          <view class="text-center border-r border-black/5"><text class="text-base font-black text-zinc-900 block">{{ creator.completedOrders }}</text><text class="text-[9px] text-zinc-400">完成订单</text></view>
          <view class="text-center border-r border-black/5"><text class="text-base font-black text-zinc-900 block">{{ creator.responseRate }}%</text><text class="text-[9px] text-zinc-400">回复率</text></view>
          <view class="text-center"><text class="text-base font-black text-zinc-900 block">{{ creator.followerCount }}</text><text class="text-[9px] text-zinc-400">关注人数</text></view>
        </view>
      </view>

      <view class="px-5 pt-5 space-y-5">
        <view v-if="creator.tags?.length" class="flex flex-wrap gap-2">
          <view v-for="tag in creator.tags" :key="tag" class="yp-chip">{{ tag }}</view>
        </view>

        <view class="yp-card p-4">
          <view class="flex items-center justify-between mb-3">
            <text class="yp-section-title">关于摄影师</text>
            <text class="text-[10px] text-zinc-400">服务城市 {{ creator.serviceCities?.length || 1 }} 个</text>
          </view>
          <text class="text-xs text-zinc-500 leading-relaxed whitespace-pre-wrap">{{ creator.bio || '摄影师暂未填写详细介绍。' }}</text>
          <view class="mt-4 flex flex-wrap gap-2">
            <view v-for="city in serviceCities" :key="city" class="rounded-full bg-zinc-100 px-3 py-1.5 text-[10px] text-zinc-500">{{ city }}</view>
          </view>
        </view>

        <view>
          <view class="flex items-end justify-between mb-3">
            <view><text class="yp-section-title block">代表作品</text><text class="text-[10px] text-zinc-400 block mt-1">真实公开作品 {{ worksTotal }} 组</text></view>
            <text v-if="worksTotal > works.length" class="text-xs font-bold text-rose-500" @click="openAllWorks">查看全部</text>
          </view>
          <view v-if="works.length" class="grid grid-cols-3 gap-2">
            <image
              v-for="work in works.slice(0, 6)"
              :key="work.workId"
              :src="work.coverUrl"
              mode="aspectFill"
              class="w-full h-32 rounded-2xl bg-zinc-100"
              @click="openWork(work)"
            />
          </view>
          <view v-else class="yp-card py-10 text-center"><view class="i-lucide-images text-2xl text-zinc-300"></view><text class="text-xs text-zinc-400 block mt-2">暂无公开作品</text></view>
        </view>

        <view>
          <view class="flex items-end justify-between mb-3">
            <view><text class="yp-section-title block">服务套餐</text><text class="text-[10px] text-zinc-400 block mt-1">价格、交付和修改次数均以套餐快照为准</text></view>
          </view>
          <view v-if="packages.length" class="space-y-3">
            <view v-for="item in packages" :key="item.packageId" class="yp-card p-4" @click="openPackage(item)">
              <view class="flex items-start justify-between">
                <view class="flex-1 min-w-0"><text class="text-sm font-black text-zinc-900 block truncate">{{ item.packageName }}</text><text class="text-xs text-zinc-500 block mt-2 line-clamp-2">{{ item.description }}</text></view>
                <view class="ml-3 text-right"><text class="text-lg font-black text-rose-500">¥{{ money(item.price) }}</text><text class="text-[9px] text-zinc-400 block mt-1">{{ duration(item.durationMinutes) }}</text></view>
              </view>
              <view class="mt-4 grid grid-cols-3 gap-2">
                <view class="rounded-xl bg-zinc-50 p-2 text-center"><text class="text-xs font-black text-zinc-700 block">{{ item.retouchedCount }}</text><text class="text-[9px] text-zinc-400">精修张数</text></view>
                <view class="rounded-xl bg-zinc-50 p-2 text-center"><text class="text-xs font-black text-zinc-700 block">{{ item.deliveryDays }}天</text><text class="text-[9px] text-zinc-400">交付周期</text></view>
                <view class="rounded-xl bg-zinc-50 p-2 text-center"><text class="text-xs font-black text-zinc-700 block">{{ item.revisionCount }}次</text><text class="text-[9px] text-zinc-400">修改次数</text></view>
              </view>
              <view class="mt-4 flex items-center justify-between"><text class="text-[10px] text-zinc-400">点击查看完整服务与退款规则</text><view class="i-lucide-chevron-right text-zinc-300"></view></view>
            </view>
          </view>
          <view v-else class="yp-card py-10 text-center"><view class="i-lucide-package-open text-2xl text-zinc-300"></view><text class="text-xs text-zinc-400 block mt-2">摄影师暂未发布服务套餐</text></view>
        </view>

        <view>
          <view class="flex items-end justify-between mb-3">
            <view><text class="yp-section-title block">真实评价</text><text class="text-[10px] text-zinc-400 block mt-1">仅完成订单的下单用户可以评价</text></view>
            <text class="text-xs text-zinc-400">{{ reviewsTotal }} 条</text>
          </view>
          <view v-if="reviews.length" class="space-y-3">
            <view v-for="review in reviews" :key="review.reviewId" class="yp-card p-4">
              <view class="flex items-center">
                <image v-if="review.reviewer?.avatar" :src="review.reviewer.avatar" mode="aspectFill" class="size-9 rounded-full bg-zinc-100" />
                <view v-else class="size-9 rounded-full bg-zinc-900 flex items-center justify-center text-[10px] font-bold text-white">{{ review.reviewer?.nickName?.slice(0, 1) || '用' }}</view>
                <view class="flex-1 ml-3"><text class="text-xs font-bold text-zinc-700 block">{{ review.reviewer?.nickName || '用户' }}</text><text class="text-[9px] text-zinc-400 block mt-1">{{ formatDate(review.createTime) }}</text></view>
                <view class="flex items-center"><view class="i-lucide-star fill-amber-400 text-amber-400 text-xs mr-1"></view><text class="text-xs font-black text-zinc-700">{{ review.rating }}</text></view>
              </view>
              <text class="text-xs text-zinc-500 leading-relaxed block mt-3">{{ review.content }}</text>
              <view v-if="review.creatorReply" class="mt-3 rounded-xl bg-zinc-50 p-3"><text class="text-[10px] font-bold text-zinc-600">摄影师回复：</text><text class="text-[10px] text-zinc-500">{{ review.creatorReply }}</text></view>
            </view>
          </view>
          <view v-else class="yp-card py-10 text-center"><view class="i-lucide-message-square-more text-2xl text-zinc-300"></view><text class="text-xs text-zinc-400 block mt-2">暂无真实订单评价</text></view>
        </view>

        <view class="rounded-2xl bg-amber-50 p-4 flex items-start">
          <view class="i-lucide-shield-check text-amber-600 text-base mt-0.5 mr-3"></view>
          <view><text class="text-xs font-black text-amber-800 block">平台交易保障</text><text class="text-[10px] text-amber-700 leading-relaxed block mt-1">请通过平台套餐、报价、订单与支付完成交易，不要脱离平台私下转账。</text></view>
        </view>
      </view>

      <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3">
        <view class="size-12 rounded-2xl border border-black/10 flex items-center justify-center" @click="openChat"><view class="i-lucide-message-circle text-zinc-700 text-lg"></view></view>
        <view class="flex-1 h-12 rounded-2xl bg-zinc-900 text-white flex items-center justify-center text-sm font-black" @click="bookNow">{{ packages.length ? '选择套餐预约' : '咨询档期' }}</view>
      </view>
    </template>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getToken } from "@/utils/auth";
import { getCreator, listCreatorPackages, listCreatorReviews, listWorks } from "@/api/yuepai/creator-api";
import { followCreator, getCreatorState, unfollowCreator } from "@/api/yuepai/creator-social";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const creatorId = ref("");
const creator = ref(null);
const works = ref([]);
const worksTotal = ref(0);
const packages = ref([]);
const reviews = ref([]);
const reviewsTotal = ref(0);
const followed = ref(false);
const loading = ref(true);
const errorMessage = ref("");
const operating = ref(false);
const serviceCities = computed(() => creator.value?.serviceCities?.length ? creator.value.serviceCities : [creator.value?.cityCode].filter(Boolean));

onLoad((options) => {
  creatorId.value = options?.id || "";
  try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (error) { console.warn(error); }
  loadAll();
});

async function loadAll() {
  if (!creatorId.value) { errorMessage.value = "缺少摄影师编号"; loading.value = false; return; }
  loading.value = true;
  errorMessage.value = "";
  try {
    const [creatorRes, workRes, packageRes, reviewRes] = await Promise.all([
      getCreator(creatorId.value),
      listWorks({ creatorId: creatorId.value, pageNum: 1, pageSize: 6 }),
      listCreatorPackages(creatorId.value),
      listCreatorReviews(creatorId.value, { pageNum: 1, pageSize: 5 }),
    ]);
    creator.value = creatorRes.data || creatorRes;
    works.value = Array.isArray(workRes.rows) ? workRes.rows : [];
    worksTotal.value = Number(workRes.total || works.value.length);
    packages.value = Array.isArray(packageRes.rows) ? packageRes.rows : [];
    reviews.value = Array.isArray(reviewRes.rows) ? reviewRes.rows : [];
    reviewsTotal.value = Number(reviewRes.total || reviews.value.length);
    if (getToken()) {
      try { const state = await getCreatorState(creatorId.value); followed.value = Boolean((state.data || state).followed); } catch (error) { console.warn("读取关注状态失败", error); }
    }
  } catch (error) {
    errorMessage.value = error?.message || "网络异常，请稍后重试";
  } finally {
    loading.value = false;
  }
}

async function toggleFollow() {
  if (operating.value) return;
  if (!getToken()) return proxy.$tab.navigateTo("/pages/login");
  operating.value = true;
  try {
    const response = followed.value ? await unfollowCreator(creatorId.value) : await followCreator(creatorId.value);
    const data = response.data || response;
    followed.value = Boolean(data.followed);
    creator.value.followerCount = Number(data.followerCount || 0);
    uni.showToast({ title: followed.value ? "关注成功" : "已取消关注", icon: "none" });
  } finally { operating.value = false; }
}

function openWork(work) { proxy.$tab.navigateTo(`/pages/works/detail?id=${work.workId}`); }
function openAllWorks() { proxy.$tab.switchTab("/pages/works/index"); }
function openPackage(item) { proxy.$tab.navigateTo(`/pages/package/detail?id=${item.packageId}&creatorId=${creatorId.value}`); }
function bookNow() { if (packages.value.length) openPackage(packages.value[0]); else openChat(); }
function openChat() { if (!getToken()) return proxy.$tab.navigateTo("/pages/login"); proxy.$tab.navigateTo(`/pages/chat/index?userId=${creator.value.userId}&creatorId=${creatorId.value}&name=${encodeURIComponent(creator.value.displayName)}`); }
function shareProfile() { const path = `/pages/photographer/detail?id=${creatorId.value}`; uni.setClipboardData({ data: path, success() { uni.showToast({ title: "页面路径已复制", icon: "none" }); } }); }
function money(value) { return Number(value || 0).toFixed(0); }
function duration(minutes) { const value = Number(minutes || 0); return value >= 480 ? "全天" : value >= 60 ? `${Math.round(value / 60)}小时` : `${value}分钟`; }
function formatDate(value) { if (!value) return ""; const date = new Date(value); return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`; }
function goBack() { proxy.$tab.navigateBack(); }
</script>
