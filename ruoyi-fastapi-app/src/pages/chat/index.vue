<template>
  <view class="yp-page flex flex-col" style="height:100vh">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 py-3 bg-white/95 border-b border-black/5 flex items-center">
      <view class="size-10 rounded-full bg-zinc-100 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view>
      <view class="size-10 rounded-2xl ml-3 flex items-center justify-center text-white font-black" :style="{ background: contact.avatar }">{{ contact.name[0] }}</view>
      <view class="flex-1 ml-3"><view class="flex items-center"><text class="text-sm font-black text-zinc-900">{{ contact.name }}</text><view class="i-lucide-badge-check text-rose-500 text-xs ml-1"></view></view><view class="flex items-center mt-1"><view class="size-1.5 rounded-full bg-emerald-500 mr-1.5"></view><text class="text-[10px] text-zinc-400">在线 · 平均 10 分钟回复</text></view></view>
      <view class="size-10 rounded-full bg-zinc-100 flex items-center justify-center" @click="showMore"><view class="i-lucide-ellipsis text-zinc-700 text-lg"></view></view>
    </view>

    <scroll-view scroll-y :scroll-top="scrollTop" :scroll-with-animation="true" class="flex-1" :show-scrollbar="false">
      <view class="px-5 py-4 pb-8 space-y-4">
        <view class="text-center"><text class="rounded-full bg-zinc-200/60 px-3 py-1 text-[9px] text-zinc-500">今天 14:20</text></view>
        <view v-for="item in messages" :key="item.id" class="flex" :class="item.mine ? 'justify-end' : 'justify-start'">
          <view v-if="!item.mine" class="size-8 rounded-xl flex items-center justify-center text-white text-[10px] font-black mr-2 shrink-0" :style="{ background: contact.avatar }">{{ contact.name[0] }}</view>
          <view class="max-w-[78%]">
            <view v-if="item.type === 'text'" class="rounded-2xl px-4 py-3 text-sm leading-relaxed" :class="item.mine ? 'bg-zinc-900 text-white rounded-tr-md' : 'bg-white border border-black/5 text-zinc-700 rounded-tl-md'">{{ item.text }}</view>

            <view v-else-if="item.type === 'quote'" class="yp-card p-4 min-w-[250px]" @click="openQuote(item)">
              <view class="flex items-center justify-between"><view class="flex items-center"><view class="size-9 rounded-xl bg-rose-50 flex items-center justify-center"><view class="i-lucide-badge-dollar-sign text-rose-500 text-base"></view></view><view class="ml-2"><text class="text-xs font-black text-zinc-900 block">摄影服务报价</text><text class="text-[9px] text-zinc-400 block mt-1">{{ item.packageName }}</text></view></view><text class="text-lg font-black text-rose-500">¥{{ item.amount }}</text></view>
              <view class="mt-3 pt-3 border-t border-black/5 flex items-center justify-between"><text class="text-[10px] text-zinc-400">{{ item.description }}</text><view class="i-lucide-chevron-right text-zinc-300 text-xs"></view></view>
            </view>

            <view v-else-if="item.type === 'order'" class="yp-card p-4 min-w-[250px]" @click="openOrder(item)">
              <view class="flex items-center justify-between"><view class="flex items-center"><view class="size-9 rounded-xl bg-emerald-50 flex items-center justify-center"><view class="i-lucide-calendar-check text-emerald-600 text-base"></view></view><view class="ml-2"><text class="text-xs font-black text-zinc-900 block">约拍订单</text><text class="text-[9px] text-zinc-400 block mt-1">{{ item.orderNo }}</text></view></view><view class="rounded-full bg-amber-50 px-2 py-1 text-[9px] text-amber-600">{{ item.status }}</view></view>
              <text class="text-xs text-zinc-600 block mt-3">{{ item.title }}</text><text class="text-[10px] text-zinc-400 block mt-1">{{ item.date }} · {{ item.location }}</text>
            </view>

            <text v-if="item.mine" class="text-[9px] text-zinc-300 block text-right mt-1">{{ item.read ? '已读' : '送达' }}</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <view v-if="quickPanelVisible" class="bg-white border-t border-black/5 px-5 pt-4 pb-3">
      <view class="grid grid-cols-4 gap-3">
        <view v-for="item in quickActions" :key="item.label" class="flex flex-col items-center" @click="runQuickAction(item)"><view class="size-11 rounded-2xl flex items-center justify-center" :style="{ background: item.background }"><view :class="item.icon" class="text-lg" :style="{ color: item.color }"></view></view><text class="text-[10px] text-zinc-500 mt-1.5">{{ item.label }}</text></view>
      </view>
    </view>

    <view class="bg-white border-t border-black/5 px-4 pt-3 pb-6">
      <scroll-view scroll-x class="whitespace-nowrap mb-3" :show-scrollbar="false"><view class="inline-flex space-x-2 pr-4"><view v-for="text in quickReplies" :key="text" class="yp-chip" @click="insertQuickReply(text)">{{ text }}</view></view></scroll-view>
      <view class="flex items-end space-x-2">
        <view class="size-11 rounded-2xl bg-zinc-100 flex items-center justify-center shrink-0" @click="quickPanelVisible = !quickPanelVisible"><view class="text-xl text-zinc-700" :class="quickPanelVisible ? 'i-lucide-x' : 'i-lucide-plus'"></view></view>
        <view class="flex-1 min-h-11 rounded-2xl bg-zinc-100 px-4 py-2.5 flex items-center"><textarea v-model="draft" auto-height maxlength="500" placeholder="输入消息…" placeholder-class="text-zinc-300" class="w-full max-h-24 text-sm text-zinc-900 leading-relaxed" @confirm="sendMessage" /></view>
        <view class="size-11 rounded-2xl flex items-center justify-center shrink-0" :class="draft.trim() ? 'bg-zinc-900' : 'bg-zinc-200'" @click="sendMessage"><view class="i-lucide-send text-white text-base"></view></view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { getCurrentInstance, nextTick, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const draft = ref(""); const quickPanelVisible = ref(false); const scrollTop = ref(0);
try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (error) { console.warn("获取设备信息失败", error); }
const contact = reactive({ id: "1", name: "林默", avatar: "linear-gradient(135deg,#fb7185,#be123c)" });
onLoad((options) => { contact.id = options?.id || "1"; contact.name = options?.name ? decodeURIComponent(options.name) : "林默"; });
const messages = reactive([
  { id: 1, type: "text", text: "你好，我想咨询一下人像写真的拍摄。", mine: true, read: true },
  { id: 2, type: "text", text: "你好呀！你更喜欢自然清新，还是偏情绪感的风格？", mine: false },
  { id: 3, type: "text", text: "日系清新风格，大概拍 2 到 3 小时。", mine: true, read: true },
  { id: 4, type: "quote", packageName: "精致人像写真", amount: 1200, description: "3 小时 · 含妆造 · 30 张精修", mine: false, quoteId: 1 },
  { id: 5, type: "order", orderNo: "YP20260617001", status: "待确认", title: "精致人像写真", date: "6 月 20 日 14:00", location: "北京朝阳三里屯", mine: false, orderId: 1 }
]);
const quickReplies = ["这周六有档期吗？", "套餐包含妆造吗？", "可以看看更多客片吗？", "交付时间多久？"];
const quickActions = [
  { label: "图片", icon: "i-lucide-image-plus", background: "#fff1f2", color: "#f43f5e", action: "image" },
  { label: "作品", icon: "i-lucide-images", background: "#f5f3ff", color: "#7c3aed", action: "work" },
  { label: "报价", icon: "i-lucide-badge-dollar-sign", background: "#fffbeb", color: "#d97706", action: "quote" },
  { label: "约拍", icon: "i-lucide-calendar-plus", background: "#f0fdf4", color: "#059669", action: "booking" }
];
function insertQuickReply(text) { draft.value = text; }
function sendMessage() { const text = draft.value.trim(); if (!text) return; messages.push({ id: Date.now(), type: "text", text, mine: true, read: false }); draft.value = ""; quickPanelVisible.value = false; moveToBottom(); setTimeout(() => { const target = messages.find((item) => item.id === messages[messages.length - 1].id); if (target) target.read = true; }, 500); }
function moveToBottom() { nextTick(() => { scrollTop.value += 10000; }); }
function runQuickAction(item) { if (item.action === "image") return chooseImage(); if (item.action === "quote") return proxy.$tab.navigateTo("/pages/quote/index"); if (item.action === "booking") return proxy.$tab.navigateTo("/pages/order/confirm"); proxy.$tab.switchTab("/pages/works/index"); }
function chooseImage() { uni.chooseImage({ count: 1, sizeType: ["compressed"], success() { messages.push({ id: Date.now(), type: "text", text: "[图片]", mine: true, read: false }); moveToBottom(); }, fail(error) { if (!String(error.errMsg || "").includes("cancel")) uni.showToast({ title: "选择图片失败", icon: "none" }); } }); }
function openQuote(item) { proxy.$tab.navigateTo(`/pages/quote/index?id=${item.quoteId}`); }
function openOrder(item) { proxy.$tab.navigateTo(`/pages/order/detail?id=${item.orderId}`); }
function showMore() { uni.showActionSheet({ itemList: ["查看主页", "清空聊天记录", "举报用户"], success(result) { if (result.tapIndex === 0) proxy.$tab.navigateTo(`/pages/profile/index?id=${contact.id}`); if (result.tapIndex === 1) messages.splice(0, messages.length); if (result.tapIndex === 2) proxy.$tab.navigateTo(`/pages/report/index?id=${contact.id}`); } }); }
function goBack() { proxy.$tab.navigateBack(); }
</script>
