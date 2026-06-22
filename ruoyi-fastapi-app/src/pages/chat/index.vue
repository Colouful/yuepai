<template>
  <view class="yp-page h-full flex flex-col">
    <view :style="{height:statusBarH+'px'}"></view>
    <view class="px-5 py-3 bg-white/95 border-b border-black/5 flex items-center">
      <view class="i-lucide-arrow-left text-zinc-700 text-xl mr-3" @click="goBack"></view>
      <view class="size-9 rounded-2xl bg-zinc-900 text-white text-xs font-black flex items-center justify-center">{{ displayName.slice(0,1)||'用' }}</view>
      <view class="flex-1 ml-3"><text class="text-sm font-black text-zinc-800 block">{{ displayName }}</text><text class="text-[9px] text-zinc-400 block mt-0.5">平台内沟通 · 消息已加密传输</text></view>
      <view class="i-lucide-shield-check text-emerald-500"></view>
    </view>

    <scroll-view
      scroll-y
      class="flex-1"
      :show-scrollbar="false"
      :scroll-into-view="scrollTarget"
      @scrolltoupper="loadOlder"
    >
      <view class="px-5 py-4 space-y-4">
        <view v-if="hasMore" class="text-center"><text class="text-[10px] text-zinc-400" @click="loadOlder">{{ loadingOlder?'加载中…':'查看更早消息' }}</text></view>
        <view v-if="loading&&!messages.length" class="py-24 text-center"><view class="i-lucide-loader-circle animate-spin text-2xl text-zinc-300"></view></view>
        <view v-else-if="errorMessage&&!messages.length" class="py-24 text-center"><text class="text-xs text-zinc-500 block">{{ errorMessage }}</text><view class="mt-4 inline-flex rounded-full bg-zinc-900 px-4 py-2 text-[10px] font-bold text-white" @click="initialize">重新加载</view></view>
        <view v-else-if="!messages.length" class="py-16 text-center"><view class="i-lucide-message-circle text-3xl text-zinc-300"></view><text class="text-xs text-zinc-400 block mt-3">开始沟通拍摄时间、风格和交付要求</text></view>

        <view v-for="msg in messages" :id="`msg-${msg.messageId}`" :key="msg.messageId" class="flex" :class="isMine(msg)?'justify-end':'justify-start'">
          <view v-if="!isMine(msg)" class="size-8 rounded-full bg-zinc-900 text-white text-[10px] font-bold flex items-center justify-center mr-2 shrink-0">{{ displayName.slice(0,1)||'用' }}</view>
          <view class="max-w-[76%]">
            <view v-if="msg.messageType==='text'" class="rounded-2xl px-4 py-3 text-sm leading-relaxed" :class="isMine(msg)?'bg-zinc-900 text-white rounded-tr-md':'bg-white text-zinc-700 rounded-tl-md border border-black/5'">{{ msg.text }}</view>
            <image v-else-if="msg.messageType==='image'" :src="msg.payload?.url" mode="widthFix" class="max-w-56 rounded-2xl bg-zinc-100" @click="previewImage(msg.payload?.url)" />
            <view v-else class="rounded-2xl bg-white border border-black/5 p-3" @click="openBusinessMessage(msg)"><text class="text-xs font-black text-zinc-800 block">{{ msg.messageType==='quote'?'服务报价':'订单消息' }}</text><text class="text-[10px] text-zinc-400 block mt-1">点击查看详情</text></view>
            <text class="text-[8px] text-zinc-300 block mt-1" :class="isMine(msg)?'text-right':'text-left'">{{ messageTime(msg.createTime) }}</text>
          </view>
        </view>
        <view id="chat-bottom" class="h-1"></view>
      </view>
    </scroll-view>

    <view class="bg-white/95 px-4 pt-3 pb-6 border-t border-black/5 flex items-end space-x-2">
      <view class="size-10 rounded-xl bg-zinc-100 flex items-center justify-center shrink-0" @click="sendImage"><view class="i-lucide-image-plus text-zinc-600"></view></view>
      <textarea v-model="draft" auto-height maxlength="2000" :disabled="sending" placeholder="输入消息，请勿发送站外联系方式" placeholder-class="text-zinc-300" class="flex-1 max-h-28 min-h-10 rounded-xl bg-zinc-100 px-4 py-2.5 text-sm text-zinc-800" @confirm="sendText" />
      <view class="size-10 rounded-xl flex items-center justify-center shrink-0" :class="draft.trim()&&!sending?'bg-zinc-900':'bg-zinc-200'" @click="sendText"><view class="i-lucide-send text-white text-sm"></view></view>
    </view>
  </view>
</template>
<script setup>
import { computed,getCurrentInstance,nextTick,ref } from "vue";import { onHide,onLoad,onShow,onUnload } from "@dcloudio/uni-app";import { useUserStore } from "@/store";import { chooseAndUploadImage } from "@/api/yuepai/upload";import { createConversation,listMessages,markConversationRead,sendMessage } from "@/api/yuepai/message-api";
const {proxy}=getCurrentInstance(),userStore=useUserStore();const statusBarH=ref(44),conversationId=ref(""),targetUserId=ref(""),creatorId=ref(""),displayName=ref("用户"),messages=ref([]),draft=ref(""),loading=ref(true),loadingOlder=ref(false),sending=ref(false),hasMore=ref(false),errorMessage=ref(""),scrollTarget=ref("chat-bottom");let pollTimer=null;const myId=computed(()=>Number(userStore.id));
onLoad(o=>{conversationId.value=o?.conversationId||"";targetUserId.value=o?.userId||"";creatorId.value=o?.creatorId||"";displayName.value=decodeURIComponent(o?.name||"用户");try{statusBarH.value=uni.getSystemInfoSync().statusBarHeight||44}catch(e){console.warn(e)}initialize()});onShow(()=>startPolling());onHide(()=>stopPolling());onUnload(()=>stopPolling());
async function initialize(){loading.value=true;errorMessage.value="";try{if(!conversationId.value){if(!targetUserId.value)throw new Error("缺少会话对象");const r=await createConversation({targetUserId:Number(targetUserId.value),creatorId:creatorId.value?Number(creatorId.value):null,orderId:null});conversationId.value=String((r.data||r).conversationId)}await loadLatest(true)}catch(e){errorMessage.value=e?.message||"会话加载失败"}finally{loading.value=false}}
async function loadLatest(scroll=false){if(!conversationId.value)return;const r=await listMessages(conversationId.value,{pageSize:50});mergeMessages(r.rows||[]);hasMore.value=Boolean(r.hasMore);if(messages.value.length)await markConversationRead(conversationId.value,{lastMessageId:messages.value[messages.value.length-1].messageId});if(scroll)scrollBottom()}
async function loadOlder(){if(!hasMore.value||loadingOlder.value||!messages.value.length)return;loadingOlder.value=true;try{const r=await listMessages(conversationId.value,{beforeId:messages.value[0].messageId,pageSize:30});messages.value=[...(r.rows||[]),...messages.value];hasMore.value=Boolean(r.hasMore)}finally{loadingOlder.value=false}}
function mergeMessages(rows){const map=new Map(messages.value.map(x=>[x.messageId,x]));rows.forEach(x=>map.set(x.messageId,x));messages.value=[...map.values()].sort((a,b)=>a.messageId-b.messageId)}
async function sendText(){const text=draft.value.trim();if(!text||sending.value)return;sending.value=true;const clientId=reqId();try{const r=await sendMessage(conversationId.value,{clientMessageId:clientId,messageType:"text",text,payload:{}});draft.value="";mergeMessages([r.data||r]);scrollBottom()}finally{sending.value=false}}
async function sendImage(){if(sending.value)return;const url=await chooseAndUploadImage();if(!url)return;sending.value=true;try{const r=await sendMessage(conversationId.value,{clientMessageId:reqId(),messageType:"image",text:null,payload:{url}});mergeMessages([r.data||r]);scrollBottom()}finally{sending.value=false}}
function startPolling(){stopPolling();pollTimer=setInterval(()=>{if(conversationId.value&&!sending.value)loadLatest(false)},4000)}function stopPolling(){if(pollTimer){clearInterval(pollTimer);pollTimer=null}}function scrollBottom(){nextTick(()=>{scrollTarget.value="";nextTick(()=>scrollTarget.value="chat-bottom")})}function isMine(msg){return Number(msg.senderUserId)===myId.value}function reqId(){return`${Date.now()}-${Math.random().toString(36).slice(2)}-${Math.random().toString(36).slice(2)}`}function messageTime(v){if(!v)return"";const d=new Date(v);return`${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`}function previewImage(url){if(url)uni.previewImage({current:url,urls:[url]})}function openBusinessMessage(msg){if(msg.messageType==="quote"&&msg.payload?.quoteId)proxy.$tab.navigateTo(`/pages/quote/index?id=${msg.payload.quoteId}`);if(msg.messageType==="order"&&msg.payload?.orderId)proxy.$tab.navigateTo(`/pages/order/detail?id=${msg.payload.orderId}`)}function goBack(){proxy.$tab.navigateBack()}
</script>
