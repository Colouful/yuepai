<template>
  <view class="yp-page flex h-full flex-col">
    <view :style="{height:statusBarH+'px'}"></view>
    <view class="px-5 pt-3 pb-3 bg-white/90 border-b border-black/5">
      <text class="yp-eyebrow block">MESSAGES</text>
      <text class="yp-title block mt-1">消息中心</text>
      <view class="mt-4 flex items-center space-x-2"><view v-for="item in tabs" :key="item.value" class="flex-1 yp-chip" :class="activeTab===item.value?'yp-chip-active':''" @click="activeTab=item.value">{{ item.label }}<text v-if="item.value==='chat'&&unreadTotal" class="ml-1">{{ unreadTotal }}</text><text v-if="item.value==='quote'&&pendingQuotes" class="ml-1">{{ pendingQuotes }}</text></view></view>
    </view>

    <scroll-view scroll-y refresher-enabled :refresher-triggered="refreshing" class="flex-1" @refresherrefresh="refresh">
      <view class="px-5 pt-4 pb-24 space-y-3">
        <view v-if="loading" class="space-y-3"><view v-for="n in 4" :key="n" class="yp-card h-24 animate-pulse bg-white/70"></view></view>
        <template v-else-if="activeTab==='chat'">
          <view v-if="!conversations.length" class="py-20 text-center"><view class="i-lucide-message-circle-off text-3xl text-zinc-300"></view><text class="text-sm font-black text-zinc-700 block mt-4">暂无会话</text><text class="text-xs text-zinc-400 block mt-2">在创作者详情页点击私信即可开始沟通</text></view>
          <view v-for="item in conversations" :key="item.conversationId" class="yp-card p-4 flex items-center" @click="openConversation(item)">
            <view class="relative"><image v-if="avatar(item.otherUser?.avatar)" :src="avatar(item.otherUser?.avatar)" mode="aspectFill" class="size-12 rounded-2xl bg-zinc-100"/><view v-else class="size-12 rounded-2xl bg-zinc-900 text-white font-black flex items-center justify-center">{{ item.otherUser?.nickName?.slice(0,1)||'用' }}</view><view v-if="item.unreadCount" class="absolute -right-1 -top-1 min-w-5 h-5 px-1 rounded-full bg-rose-500 text-white text-[9px] font-bold flex items-center justify-center">{{ item.unreadCount>99?'99+':item.unreadCount }}</view></view>
            <view class="flex-1 min-w-0 ml-3"><view class="flex items-center justify-between"><text class="text-sm font-black text-zinc-800 truncate">{{ item.otherUser?.nickName||'用户' }}</text><text class="text-[9px] text-zinc-300 ml-2">{{ relativeTime(item.lastMessageTime) }}</text></view><text class="text-xs block mt-1 truncate" :class="item.unreadCount?'text-zinc-700 font-bold':'text-zinc-400'">{{ item.lastMessagePreview||'开始沟通约拍细节' }}</text></view>
          </view>
        </template>

        <template v-else>
          <view class="flex items-center space-x-2 mb-1"><view class="yp-chip" :class="quoteBox==='received'?'yp-chip-active':''" @click="quoteBox='received';loadQuotes()">收到的</view><view class="yp-chip" :class="quoteBox==='sent'?'yp-chip-active':''" @click="quoteBox='sent';loadQuotes()">发出的</view></view>
          <view v-if="!quotes.length" class="py-20 text-center"><view class="i-lucide-file-text text-3xl text-zinc-300"></view><text class="text-sm font-black text-zinc-700 block mt-4">暂无报价</text><text class="text-xs text-zinc-400 block mt-2">套餐预约或需求合作报价会显示在这里</text></view>
          <view v-for="item in quotes" :key="item.quoteId" class="yp-card p-4" @click="openQuote(item)">
            <view class="flex items-start justify-between"><view class="flex-1 min-w-0"><view class="flex items-center"><text class="text-sm font-black text-zinc-900 truncate">{{ item.serviceSnapshot?.title||'约拍服务报价' }}</text><text class="ml-2 rounded-full px-2 py-1 text-[8px] font-bold" :class="quoteStatusClass(item.status)">{{ quoteStatus(item.status) }}</text></view><text class="text-[10px] text-zinc-400 block mt-2">{{ quoteBox==='received'?'来自用户 '+item.senderUserId:'发送给用户 '+item.receiverUserId }}</text><text class="text-xs text-zinc-500 block mt-2 line-clamp-2">{{ item.remark||item.serviceSnapshot?.description||'查看服务、时间和交付明细' }}</text></view><text class="text-lg font-black text-rose-500 ml-3">¥{{ Number(item.amount||0).toFixed(2) }}</text></view>
            <view class="mt-3 pt-3 border-t border-black/5 flex items-center justify-between"><text class="text-[9px] text-zinc-400">有效期至 {{ formatDate(item.expiresAt) }}</text><view class="flex items-center"><text class="text-[10px] font-bold text-zinc-700">查看详情</text><view class="i-lucide-chevron-right text-zinc-300 ml-1"></view></view></view>
          </view>
        </template>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { computed,getCurrentInstance,ref } from "vue";import { onLoad,onShow } from "@dcloudio/uni-app";import config from "@/config";import { listConversations } from "@/api/yuepai/message-api";import { listQuotes } from "@/api/yuepai/quote-query";
const {proxy}=getCurrentInstance();const statusBarH=ref(44),activeTab=ref("chat"),loading=ref(false),refreshing=ref(false),conversations=ref([]),quotes=ref([]),quoteBox=ref("received");const tabs=[{label:"聊天",value:"chat"},{label:"报价",value:"quote"}];const unreadTotal=computed(()=>conversations.value.reduce((n,x)=>n+Number(x.unreadCount||0),0)),pendingQuotes=computed(()=>quotes.value.filter(x=>["pending","negotiating"].includes(x.status)).length);
onLoad(()=>{try{statusBarH.value=uni.getSystemInfoSync().statusBarHeight||44}catch(e){console.warn(e)}});onShow(()=>loadAll());async function loadAll(){loading.value=true;try{const [c,q]=await Promise.all([listConversations(),listQuotes({box:quoteBox.value,pageNum:1,pageSize:50})]);conversations.value=c.rows||[];quotes.value=q.rows||[]}finally{loading.value=false;refreshing.value=false;uni.stopPullDownRefresh()}}async function loadQuotes(){const r=await listQuotes({box:quoteBox.value,pageNum:1,pageSize:50});quotes.value=r.rows||[]}function refresh(){refreshing.value=true;loadAll()}function openConversation(i){proxy.$tab.navigateTo(`/pages/chat/index?conversationId=${i.conversationId}&name=${encodeURIComponent(i.otherUser?.nickName||'用户')}`)}function openQuote(i){proxy.$tab.navigateTo(`/pages/quote/index?id=${i.quoteId}`)}function avatar(v){if(!v)return"";return /^https?:/.test(v)?v:config.baseUrl+v}function relativeTime(v){if(!v)return"";const d=new Date(v),diff=Date.now()-d.getTime();if(diff<60000)return"刚刚";if(diff<3600000)return`${Math.floor(diff/60000)}分钟前`;if(diff<86400000)return`${Math.floor(diff/3600000)}小时前`;return`${d.getMonth()+1}-${d.getDate()}`}function formatDate(v){const d=new Date(v);return Number.isNaN(d.getTime())?"":`${d.getMonth()+1}-${d.getDate()} ${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`}function quoteStatus(v){return{pending:"待处理",negotiating:"议价中",accepted:"已接受",rejected:"已拒绝",withdrawn:"已撤回",expired:"已过期"}[v]||v}function quoteStatusClass(v){return v==="accepted"?"bg-emerald-50 text-emerald-600":["pending","negotiating"].includes(v)?"bg-amber-50 text-amber-600":"bg-zinc-100 text-zinc-500"}
</script>
