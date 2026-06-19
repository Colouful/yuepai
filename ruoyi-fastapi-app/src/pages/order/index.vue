<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3">
      <view class="flex items-center justify-between"><view><text class="yp-eyebrow block">ORDERS</text><text class="yp-title block mt-1">我的订单</text></view><view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="openService"><view class="i-lucide-headphones text-zinc-700 text-lg"></view></view></view>
      <scroll-view scroll-x class="mt-4 whitespace-nowrap" :show-scrollbar="false"><view class="inline-flex space-x-2 pr-5"><view v-for="item in tabs" :key="item.value" class="yp-chip" :class="activeTab === item.value ? 'yp-chip-active' : ''" @click="activeTab = item.value">{{ item.label }}<text v-if="statusCount(item.value)" class="ml-1">{{ statusCount(item.value) }}</text></view></view></scroll-view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-3">
        <view v-for="item in filteredOrders" :key="item.no" class="yp-card overflow-hidden" @click="openDetail(item)">
          <view class="px-4 py-3 border-b border-black/5 flex items-center justify-between"><text class="text-[10px] text-zinc-400">订单号 {{ item.no }}</text><text class="text-[10px] font-bold" :class="statusClass(item.status)">{{ statusLabel(item.status) }}</text></view>
          <view class="p-4">
            <view class="flex items-center">
              <view class="size-16 rounded-2xl flex items-center justify-center shrink-0" :style="{ background: item.cover }"><view class="i-lucide-camera text-white text-xl"></view></view>
              <view class="flex-1 min-w-0 ml-3"><text class="text-sm font-black text-zinc-900 block truncate">{{ item.title }}</text><text class="text-xs text-zinc-500 block mt-1">{{ item.creator }} · {{ item.date }}</text><text class="text-[10px] text-zinc-400 block mt-1">{{ item.location }}</text></view>
              <view class="ml-3 text-right"><text class="text-base font-black text-zinc-900">¥{{ item.amount }}</text><text class="text-[9px] text-zinc-400 block mt-1">共 1 项服务</text></view>
            </view>
            <view class="mt-4 pt-3 border-t border-black/5 flex items-center justify-between"><text class="text-[10px] text-zinc-400">{{ item.tip }}</text><view class="flex items-center space-x-2"><view v-if="secondaryAction(item)" class="h-8 rounded-full border border-black/10 px-3 flex items-center justify-center text-[10px] font-bold text-zinc-600" @click.stop="handleSecondary(item)">{{ secondaryAction(item) }}</view><view class="h-8 rounded-full bg-zinc-900 px-4 flex items-center justify-center text-[10px] font-bold text-white" @click.stop="handlePrimary(item)">{{ primaryAction(item) }}</view></view></view>
          </view>
        </view>

        <view v-if="!filteredOrders.length" class="py-20 flex flex-col items-center"><view class="size-16 rounded-full bg-zinc-100 flex items-center justify-center"><view class="i-lucide-clipboard-list text-2xl text-zinc-400"></view></view><text class="text-sm font-black text-zinc-700 mt-4">当前没有相关订单</text><text class="text-xs text-zinc-400 mt-2">去发现喜欢的摄影师并发起约拍</text><view class="mt-4 rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="goDiscover">去发现</view></view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";
import { onShow } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const activeTab = ref("all");
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 120; } catch (error) { console.warn("获取设备信息失败", error); }
const tabs = [{ label: "全部", value: "all" }, { label: "待付款", value: "pending_payment" }, { label: "进行中", value: "active" }, { label: "待交付", value: "pending_delivery" }, { label: "待评价", value: "pending_review" }, { label: "售后", value: "after_sale" }];
const orders = reactive([
  { id: 1, no: "YP20260617001", title: "精致人像写真", creator: "林默", date: "6 月 20 日 14:00", location: "北京朝阳三里屯", amount: 1200, status: "pending_service", tip: "距离拍摄还有 1 天", cover: "linear-gradient(135deg,#fb7185,#be123c)" },
  { id: 2, no: "YP20260615002", title: "婚纱纪实旅拍", creator: "苏晴", date: "6 月 18 日 09:00", location: "上海外滩", amount: 2000, status: "pending_delivery", tip: "摄影师预计 6 月 21 日交付", cover: "linear-gradient(135deg,#a78bfa,#5b21b6)" },
  { id: 3, no: "YP20260610003", title: "轻写真体验", creator: "陈风", date: "6 月 12 日 15:00", location: "广州天河", amount: 500, status: "pending_review", tip: "评价后可获得成长值", cover: "linear-gradient(135deg,#38bdf8,#0369a1)" },
  { id: 4, no: "YP20260606004", title: "汉服古风写真", creator: "白鹭", date: "6 月 8 日 13:00", location: "杭州西湖", amount: 899, status: "completed", tip: "订单已完成", cover: "linear-gradient(135deg,#34d399,#047857)" },
  { id: 5, no: "YP20260601005", title: "城市街拍", creator: "叶知秋", date: "6 月 5 日 19:00", location: "成都太古里", amount: 399, status: "after_sale", tip: "售后处理中", cover: "linear-gradient(135deg,#c4b5fd,#6d28d9)" }
]);
onShow(() => { try { const local = uni.getStorageSync("yuepai_local_orders") || []; local.forEach((item) => { if (!orders.some((order) => order.id === item.id)) orders.unshift({ ...item, creator: item.creator || "林默", date: "待确认", location: "待确认", cover: "linear-gradient(135deg,#fb7185,#be123c)", tip: "请尽快完成支付", status: "pending_payment" }); }); } catch (error) { console.warn("读取本地订单失败", error); } });
const filteredOrders = computed(() => orders.filter((item) => { if (activeTab.value === "all") return true; if (activeTab.value === "active") return ["pending_service", "shooting"].includes(item.status); return item.status === activeTab.value; }));
function statusCount(value) { if (value === "all") return 0; if (value === "active") return orders.filter((item) => ["pending_service", "shooting"].includes(item.status)).length; return orders.filter((item) => item.status === value).length; }
function statusLabel(status) { return { pending_payment: "待付款", pending_service: "待拍摄", shooting: "拍摄中", pending_delivery: "待交付", pending_review: "待评价", completed: "已完成", after_sale: "售后中", cancelled: "已取消" }[status] || "处理中"; }
function statusClass(status) { return { pending_payment: "text-rose-500", pending_service: "text-amber-600", shooting: "text-sky-600", pending_delivery: "text-violet-600", pending_review: "text-emerald-600", completed: "text-zinc-400", after_sale: "text-orange-600" }[status] || "text-zinc-500"; }
function primaryAction(item) { return { pending_payment: "立即支付", pending_service: "查看行程", shooting: "联系摄影师", pending_delivery: "查看交付", pending_review: "立即评价", completed: "再次预约", after_sale: "查看进度" }[item.status] || "查看详情"; }
function secondaryAction(item) { return { pending_payment: "取消订单", pending_service: "联系对方", pending_delivery: "联系对方", pending_review: "查看作品", completed: "查看作品", after_sale: "联系客服" }[item.status] || ""; }
function handlePrimary(item) { if (item.status === "pending_payment") return proxy.$tab.navigateTo(`/pages/order/confirm?orderId=${item.id}`); if (item.status === "pending_delivery") return proxy.$tab.navigateTo(`/pages/order/deliver?id=${item.id}`); if (item.status === "pending_review") return proxy.$tab.navigateTo(`/pages/order/review?id=${item.id}`); if (item.status === "shooting") return proxy.$tab.navigateTo(`/pages/chat/index?id=${item.id}&name=${encodeURIComponent(item.creator)}`); if (item.status === "completed") return proxy.$tab.navigateTo(`/pages/photographer/detail?id=${item.id}`); openDetail(item); }
function handleSecondary(item) { if (item.status === "pending_payment") { uni.showModal({ title: "取消订单", content: "确定取消该订单吗？", success(result) { if (result.confirm) item.status = "cancelled"; } }); return; } if (["pending_service", "pending_delivery"].includes(item.status)) return proxy.$tab.navigateTo(`/pages/chat/index?id=${item.id}&name=${encodeURIComponent(item.creator)}`); if (item.status === "after_sale") return proxy.$tab.navigateTo("/pages/service/index"); proxy.$tab.navigateTo(`/pages/order/deliver?id=${item.id}`); }
function openDetail(item) { proxy.$tab.navigateTo(`/pages/order/detail?id=${item.id}`); }
function openService() { proxy.$tab.navigateTo("/pages/service/index"); }
function goDiscover() { proxy.$tab.switchTab("/pages/works/index"); }
</script>
