<template>
  <view class="yp-page flex h-full flex-col">
    <view class="bg-white px-5 pt-4 pb-3 border-b border-black/5">
      <view class="flex items-end justify-between"><view><text class="yp-eyebrow block">MODELS</text><text class="yp-title block mt-1">找模特</text></view><view class="yp-chip" :class="mutualOnly?'yp-chip-active':''" @click="mutualOnly=!mutualOnly;reload()">仅看互勉</view></view>
      <view class="mt-4 h-11 rounded-2xl bg-zinc-100 px-4 flex items-center"><view class="i-lucide-search text-zinc-400 mr-2"></view><input v-model="keyword" confirm-type="search" placeholder="搜索模特或风格" class="flex-1 text-sm" @confirm="reload" /></view>
      <scroll-view scroll-x class="mt-3 whitespace-nowrap" :show-scrollbar="false"><view class="inline-flex space-x-2 pr-5"><view v-for="tag in tags" :key="tag" class="yp-chip" :class="activeTag===tag?'yp-chip-active':''" @click="activeTag=tag;reload()">{{ tag }}</view></view></scroll-view>
    </view>
    <scroll-view scroll-y refresher-enabled :refresher-triggered="refreshing" class="flex-1" @refresherrefresh="refresh" @scrolltolower="loadMore">
      <view class="px-5 pt-4 pb-24 space-y-3">
        <view v-if="loading&&!models.length" class="space-y-3"><view v-for="n in 4" :key="n" class="yp-card h-32 animate-pulse bg-white/70"></view></view>
        <view v-else-if="errorMessage&&!models.length" class="py-20 text-center"><text class="text-sm font-black text-zinc-700 block">模特加载失败</text><text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text><view class="mt-4 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="reload">重新加载</view></view>
        <view v-else-if="!models.length" class="py-20 text-center"><view class="i-lucide-user-round-search text-3xl text-zinc-300"></view><text class="text-sm font-black text-zinc-700 block mt-4">暂无符合条件的模特</text></view>
        <view v-for="item in models" :key="item.creatorId" class="yp-card p-4" @click="openDetail(item)">
          <view class="flex items-center"><image v-if="item.avatarUrl" :src="item.avatarUrl" mode="aspectFill" class="size-16 rounded-2xl"/><view v-else class="size-16 rounded-2xl bg-zinc-900 text-white text-xl font-black flex items-center justify-center">{{ item.displayName?.slice(0,1)||'模' }}</view><view class="flex-1 min-w-0 ml-3"><view class="flex items-center"><text class="text-sm font-black text-zinc-900 truncate">{{ item.displayName }}</text><view v-if="item.certificationStatus==='approved'" class="i-lucide-badge-check text-amber-500 ml-1"></view></view><text class="text-xs text-zinc-500 block mt-1 truncate">{{ item.headline||'约拍模特' }}</text><text class="text-[10px] text-zinc-400 block mt-1">{{ item.cityCode }} · {{ item.completedOrders }} 次合作 · {{ Number(item.rating||0).toFixed(1) }} 分</text></view><view class="ml-3 text-right"><text v-if="item.acceptMutual" class="text-xs font-black text-emerald-600">接受互勉</text><text v-else class="text-base font-black text-rose-500">¥{{ Number(item.basePrice||0).toFixed(0) }}</text></view></view>
          <view class="mt-3 flex flex-wrap gap-1"><text v-for="tag in item.tags?.slice(0,5)" :key="tag" class="rounded-full bg-zinc-100 px-2 py-1 text-[9px] text-zinc-500">{{ tag }}</text></view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { listCreators } from "@/api/yuepai/creator-api";
const { proxy }=getCurrentInstance();const tags=["全部","人像","古风","JK","婚纱","商业"],activeTag=ref("全部"),keyword=ref(""),mutualOnly=ref(false),models=ref([]),total=ref(0),pageNum=ref(1),loading=ref(false),refreshing=ref(false),errorMessage=ref("");
onLoad(()=>reload());async function fetchPage(reset=false){if(loading.value)return;loading.value=true;errorMessage.value="";try{const r=await listCreators({roleCode:"model",keyword:keyword.value.trim()||undefined,tag:activeTag.value==="全部"?undefined:activeTag.value,acceptMutual:mutualOnly.value?true:undefined,sortBy:"rating",pageNum:reset?1:pageNum.value,pageSize:20});const rows=Array.isArray(r.rows)?r.rows:[];total.value=Number(r.total||rows.length);if(reset){models.value=rows;pageNum.value=2}else{models.value.push(...rows.filter(x=>!models.value.some(y=>y.creatorId===x.creatorId)));pageNum.value++}}catch(e){errorMessage.value=e?.message||"网络异常"}finally{loading.value=false;refreshing.value=false;uni.stopPullDownRefresh()}}function reload(){pageNum.value=1;total.value=0;fetchPage(true)}function refresh(){refreshing.value=true;reload()}function loadMore(){if(!loading.value&&models.value.length<total.value)fetchPage()}function openDetail(item){proxy.$tab.navigateTo(`/pages/model/detail?id=${item.creatorId}`)}
</script>
