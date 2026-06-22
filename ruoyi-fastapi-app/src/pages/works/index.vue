<template>
  <view class="yp-page flex h-full flex-col">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 bg-white/90 border-b border-black/5">
      <view class="flex items-end justify-between"><view><text class="yp-eyebrow block">DISCOVER</text><text class="yp-title block mt-1">作品发现</text></view><view class="rounded-full bg-zinc-100 px-3 py-2" @click="toggleSort"><text class="text-[10px] font-bold text-zinc-600">{{ sortBy === 'popular' ? '热门' : '最新' }}</text></view></view>
      <view class="mt-4 h-11 rounded-2xl bg-zinc-100 px-4 flex items-center"><view class="i-lucide-search text-zinc-400 mr-2"></view><input v-model="keyword" confirm-type="search" placeholder="搜索作品" class="flex-1 text-sm" @confirm="reload" /></view>
      <scroll-view scroll-x class="mt-3 whitespace-nowrap" :show-scrollbar="false"><view class="inline-flex space-x-2 pr-5"><view v-for="item in categories" :key="item" class="yp-chip" :class="activeCategory === item ? 'yp-chip-active' : ''" @click="selectCategory(item)">{{ item }}</view></view></scroll-view>
    </view>

    <scroll-view scroll-y refresher-enabled :refresher-triggered="refreshing" class="flex-1" @refresherrefresh="refresh" @scrolltolower="loadMore">
      <view class="px-4 pt-4 pb-24">
        <view v-if="loading && !works.length" class="grid grid-cols-2 gap-3"><view v-for="n in 6" :key="n" class="h-72 rounded-3xl bg-white/70 animate-pulse"></view></view>
        <view v-else-if="errorMessage && !works.length" class="py-20 text-center"><text class="text-sm font-black text-zinc-700 block">作品加载失败</text><text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text><view class="mt-4 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="reload">重新加载</view></view>
        <view v-else-if="!works.length" class="py-20 text-center"><view class="i-lucide-image-off text-3xl text-zinc-300"></view><text class="text-sm font-black text-zinc-700 block mt-4">暂无公开作品</text></view>
        <view v-else class="columns-2 gap-3">
          <view v-for="work in works" :key="work.workId" class="yp-card overflow-hidden mb-3 break-inside-avoid" @click="openDetail(work)">
            <image :src="work.coverUrl" mode="widthFix" class="w-full bg-zinc-100 block" />
            <view class="p-3"><text class="text-xs font-black text-zinc-900 block line-clamp-2">{{ work.title }}</text><text class="text-[9px] text-zinc-400 block mt-1">{{ work.category }} · {{ work.cityCode || '未标注城市' }}</text><view class="mt-3 flex items-center justify-between"><view class="flex items-center min-w-0"><image v-if="work.creator?.avatarUrl" :src="work.creator.avatarUrl" mode="aspectFill" class="size-6 rounded-full"/><view v-else class="size-6 rounded-full bg-zinc-900 text-white text-[8px] flex items-center justify-center">{{ work.creator?.displayName?.slice(0,1) || '创' }}</view><text class="text-[9px] text-zinc-500 ml-1.5 truncate">{{ work.creator?.displayName }}</text></view><text class="text-[9px] text-rose-400">♥ {{ work.favoriteCount }}</text></view></view>
          </view>
        </view>
        <view v-if="loading && works.length" class="py-4 text-center text-xs text-zinc-400">正在加载更多…</view>
        <view v-else-if="works.length >= total && works.length" class="py-4 text-center text-xs text-zinc-300">已经到底了</view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { listWorks } from "@/api/yuepai/creator-api";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44), categories = ["全部","人像","古风","婚纱","街拍","旅拍","商业"], activeCategory = ref("全部"), keyword = ref(""), sortBy = ref("popular"), works = ref([]), total = ref(0), pageNum = ref(1), loading = ref(false), refreshing = ref(false), errorMessage = ref("");
onLoad(() => { try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (e) { console.warn(e); } reload(); });
async function fetchPage(reset=false){ if(loading.value)return; loading.value=true; errorMessage.value=""; try{ const r=await listWorks({category:activeCategory.value==="全部"?undefined:activeCategory.value,keyword:keyword.value.trim()||undefined,sortBy:sortBy.value,pageNum:reset?1:pageNum.value,pageSize:20}); const rows=Array.isArray(r.rows)?r.rows:[]; total.value=Number(r.total||rows.length); if(reset){works.value=rows;pageNum.value=2;}else{works.value.push(...rows.filter(x=>!works.value.some(y=>y.workId===x.workId)));pageNum.value+=1;} }catch(e){errorMessage.value=e?.message||"网络异常";}finally{loading.value=false;refreshing.value=false;uni.stopPullDownRefresh();}}
function reload(){pageNum.value=1;total.value=0;fetchPage(true);} function refresh(){refreshing.value=true;reload();} function loadMore(){if(!loading.value&&works.value.length<total.value)fetchPage();} function selectCategory(v){activeCategory.value=v;reload();} function toggleSort(){sortBy.value=sortBy.value==="popular"?"latest":"popular";reload();} function openDetail(w){proxy.$tab.navigateTo(`/pages/works/detail?id=${w.workId}`);}
</script>
