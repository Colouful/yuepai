<template>
  <view class="yp-page flex h-full flex-col">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3">
      <text class="yp-eyebrow block">ORDERS</text>
      <text class="yp-title block mt-1">我的订单</text>
      <scroll-view scroll-x class="mt-4 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2 pr-5">
          <view v-for="tab in tabs" :key="tab.value" class="yp-chip" :class="activeTab === tab.value ? 'yp-chip-active' : ''" @click="changeTab(tab.value)">{{ tab.label }}</view>
        </view>
      </scroll-view>
    </view>

    <scroll-view scroll-y refresher-enabled :refresher-triggered="refreshing" class="flex-1" :show-scrollbar="false" @refresherrefresh="refresh">
      <view class="px-5 pb-28 space-y-3">
        <view v-if="loading" class="space-y-3"><view v-for="item in 3" :key="item" class="yp-card h-32 animate-pulse bg-white/70"></view></view>
        <view v-else-if="errorMessage" class="py-20 text-center"><text class="text-sm font-black text-zinc-700 block">订单加载失败</text><text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text><view class="mt-4 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="loadOrders">重新加载</view></view>
        <view v-else-if="!orders.length" class="py-20 text-center"><view class="i-lucide-clipboard-list text-3xl text-zinc-300"></view><text class="text-sm font-black text-zinc-700 block mt-4">暂无相关订单</text><text class="text-xs text-zinc-400 block mt-2">接受报价后会生成真实订单</text></view>

        <view v-for="order in orders" :key="order.orderId" class="yp-card p-4" @click="openDetail(order)">
          <view class="flex items-center justify-between"><text class="text-[10px] text-zinc-400">{{ order.orderNo }}</text><text class="text-[10px] font-bold text-rose-500">{{ label(order.status) }}</text></view>
          <view class="mt-3 flex items-center"><view class="size-14 rounded-2xl bg-zinc-900 flex items-center justify-center"><view class="i-lucide-camera text-white text-xl"></view></view><view class="flex-1 min-w-0 ml-3"><text class="text-sm font-black text-zinc-900 block truncate">{{ order.serviceSnapshot?.title || order.serviceSnapshot?.packageName || '约拍服务' }}</text><text class="text-xs text-zinc-400 block mt-1">{{ formatDate(order.shootAt) }}</text></view><text class="text-base font-black text-zinc-900">¥{{ money(order.payableAmount) }}</text></view>
          <view class="mt-3 pt-3 border-t border-black/5 flex items-center justify-between"><text class="text-[10px] text-zinc-400">{{ order.paymentStatus === 'paid' ? '已支付' : '未支付' }}</text><view class="flex items-center"><text class="text-[10px] font-bold text-zinc-700">查看详情</text><view class="i-lucide-chevron-right text-zinc-300 text-xs ml-1"></view></view></view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { getCurrentInstance, ref } from "vue";
import { onLoad, onShow } from "@dcloudio/uni-app";
import { listOrders } from "@/api/yuepai/core";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const activeTab = ref("");
const orders = ref([]);
const loading = ref(false);
const refreshing = ref(false);
const errorMessage = ref("");
const tabs = [{ label: "全部", value: "" }, { label: "待付款", value: "pending_payment" }, { label: "待服务", value: "pending_service" }, { label: "服务中", value: "in_service" }, { label: "待验收", value: "pending_acceptance" }, { label: "已完成", value: "completed" }];

onLoad(() => { try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (error) { console.warn(error); } });
onShow(() => loadOrders());

async function loadOrders() {
  if (loading.value) return;
  loading.value = true;
  errorMessage.value = "";
  try { const response = await listOrders(activeTab.value ? { status: activeTab.value } : {}); orders.value = Array.isArray(response.rows) ? response.rows : []; }
  catch (error) { errorMessage.value = error?.message || "网络异常"; }
  finally { loading.value = false; refreshing.value = false; uni.stopPullDownRefresh(); }
}
function changeTab(value) { activeTab.value = value; loadOrders(); }
function refresh() { refreshing.value = true; loadOrders(); }
function openDetail(order) { proxy.$tab.navigateTo(`/pages/order/detail?id=${order.orderId}`); }
function money(value) { return Number(value || 0).toFixed(2); }
function formatDate(value) { if (!value) return "时间待确认"; const date = new Date(value); return `${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`; }
function label(status) { return { pending_payment: "待付款", paid: "已付款", pending_service: "待服务", in_service: "服务中", pending_upload: "待交付", pending_acceptance: "待验收", completed: "已完成", cancelled: "已取消" }[status] || status; }
</script>
