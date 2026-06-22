<template>
  <view class="yp-page min-h-screen pb-28">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between"><view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view><text class="text-base font-black text-zinc-900">订单详情</text><view class="w-10"></view></view>

    <view v-if="loading" class="px-5 pt-4 space-y-4"><view class="yp-card h-40 animate-pulse bg-white/70"></view><view class="yp-card h-56 animate-pulse bg-white/70"></view></view>
    <view v-else-if="errorMessage" class="px-5 pt-24 text-center"><text class="text-sm font-black text-zinc-700 block">订单加载失败</text><text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text><view class="mt-4 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="loadOrder">重新加载</view></view>

    <view v-else-if="order" class="px-5 pt-4 space-y-4">
      <view class="yp-card-strong p-5"><text class="text-xl font-black text-white block">{{ statusLabel }}</text><text class="text-xs text-white/55 block mt-2">{{ statusDescription }}</text><view class="mt-5 flex items-center justify-between"><text class="text-[10px] text-white/45">{{ order.orderNo }}</text><text class="text-[10px] text-white/60">版本 {{ order.version }}</text></view></view>

      <view class="yp-card p-4"><text class="yp-section-title block mb-4">服务信息</text><view class="space-y-3"><view class="flex justify-between"><text class="text-xs text-zinc-400">服务内容</text><text class="text-xs text-zinc-700 text-right max-w-[65%]">{{ order.serviceSnapshot?.title || order.serviceSnapshot?.packageName || '约拍服务' }}</text></view><view class="flex justify-between"><text class="text-xs text-zinc-400">拍摄时间</text><text class="text-xs text-zinc-700">{{ formatDate(order.shootAt) }}</text></view><view class="flex justify-between"><text class="text-xs text-zinc-400">预计时长</text><text class="text-xs text-zinc-700">{{ order.durationMinutes }} 分钟</text></view><view class="flex justify-between"><text class="text-xs text-zinc-400">拍摄地点</text><text class="text-xs text-zinc-700 text-right max-w-[65%]">{{ locationText }}</text></view><view class="flex justify-between"><text class="text-xs text-zinc-400">订单备注</text><text class="text-xs text-zinc-700 text-right max-w-[65%]">{{ order.remark || '无' }}</text></view></view></view>

      <view class="yp-card p-4"><text class="yp-section-title block mb-4">费用明细</text><view class="space-y-3"><view class="flex justify-between"><text class="text-xs text-zinc-400">服务金额</text><text class="text-xs text-zinc-700">¥{{ money(order.amount) }}</text></view><view class="flex justify-between"><text class="text-xs text-zinc-400">平台服务费</text><text class="text-xs text-zinc-700">¥{{ money(order.platformFee) }}</text></view><view class="flex justify-between"><text class="text-xs text-zinc-400">优惠金额</text><text class="text-xs text-emerald-600">-¥{{ money(order.discountAmount) }}</text></view><view class="h-px bg-black/5"></view><view class="flex justify-between"><text class="text-sm font-black text-zinc-900">应付金额</text><text class="text-xl font-black text-rose-500">¥{{ money(order.payableAmount) }}</text></view><view class="flex justify-between"><text class="text-xs text-zinc-400">支付状态</text><text class="text-xs font-bold text-zinc-700">{{ order.paymentStatus === 'paid' ? '已支付' : '未支付' }}</text></view></view></view>

      <view class="rounded-2xl bg-amber-50 p-4 flex items-start"><view class="i-lucide-shield-check text-amber-600 text-base mt-0.5 mr-3"></view><text class="text-[10px] text-amber-700 leading-relaxed">订单状态只能按平台状态机流转。重复提交、越权操作和旧版本操作会被服务端拒绝。</text></view>
    </view>

    <view v-if="order && actions.length" class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3"><view v-for="action in actions" :key="action.status" class="flex-1 h-12 rounded-2xl flex items-center justify-center text-sm font-black" :class="action.primary ? 'bg-zinc-900 text-white' : 'border border-black/10 text-zinc-700'" @click="runAction(action)">{{ action.label }}</view></view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getOrder, transitionOrder } from "@/api/yuepai/core";
import { useUserStore } from "@/store";

const { proxy } = getCurrentInstance();
const userStore = useUserStore();
const statusBarH = ref(44);
const orderId = ref("");
const order = ref(null);
const loading = ref(true);
const errorMessage = ref("");
const operating = ref(false);

const statusLabel = computed(() => ({ pending_payment: "等待付款", paid: "支付成功", pending_service: "等待服务", in_service: "服务进行中", pending_upload: "等待交付", pending_acceptance: "等待验收", modifying: "作品修改中", completed: "订单已完成", reviewed: "已评价", cancel_requested: "取消申请中", cancelled: "订单已取消", dispute: "平台处理中" }[order.value?.status] || order.value?.status || "订单处理中"));
const statusDescription = computed(() => ({ pending_payment: "完成支付后才能锁定服务与档期", paid: "服务方确认后进入待服务", pending_service: "请按约定时间和地点履约", in_service: "双方已确认服务开始", pending_upload: "服务方正在上传交付内容", pending_acceptance: "请检查交付内容并完成验收", modifying: "服务方正在按意见修改", completed: "资金将按平台规则结算", reviewed: "订单流程已结束", cancel_requested: "等待对方或平台处理", cancelled: "该订单不再继续履约" }[order.value?.status] || "请关注订单后续更新"));
const locationText = computed(() => order.value?.locationSnapshot?.name || order.value?.locationSnapshot?.address || "待确认");
const isBuyer = computed(() => Number(userStore.id) === Number(order.value?.buyerUserId));
const isSeller = computed(() => Number(userStore.id) === Number(order.value?.sellerUserId));
const actions = computed(() => {
  if (!order.value) return [];
  const status = order.value.status;
  if (isBuyer.value && status === "pending_payment") return [{ label: "取消订单", status: "cancelled" }];
  if (isSeller.value && status === "paid") return [{ label: "确认接单", status: "pending_service", primary: true }];
  if (isSeller.value && status === "pending_service") return [{ label: "开始服务", status: "in_service", primary: true }];
  if (isSeller.value && status === "in_service") return [{ label: "完成拍摄", status: "pending_upload", primary: true }];
  if (isSeller.value && status === "pending_upload") return [{ label: "提交交付", status: "pending_acceptance", primary: true }];
  if (isBuyer.value && status === "pending_acceptance") return [{ label: "申请修改", status: "modifying" }, { label: "确认验收", status: "completed", primary: true }];
  if (isSeller.value && status === "modifying") return [{ label: "重新交付", status: "pending_acceptance", primary: true }];
  return [];
});

onLoad((options) => { try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (error) { console.warn(error); } orderId.value = options?.id || ""; loadOrder(); });

async function loadOrder() { loading.value = true; errorMessage.value = ""; try { const response = await getOrder(orderId.value); order.value = response.data || response; } catch (error) { errorMessage.value = error?.message || "网络异常"; } finally { loading.value = false; } }
function runAction(action) { if (operating.value) return; uni.showModal({ title: action.label, content: `确认执行“${action.label}”吗？`, success(result) { if (result.confirm) submitTransition(action.status); } }); }
async function submitTransition(toStatus) { operating.value = true; try { const response = await transitionOrder(orderId.value, { toStatus, expectedVersion: order.value.version, requestId: requestId() }); order.value = response.data || response; uni.showToast({ title: "状态已更新", icon: "success" }); } finally { operating.value = false; } }
function requestId() { return `${Date.now()}-${Math.random().toString(36).slice(2)}-${Math.random().toString(36).slice(2)}`; }
function money(value) { return Number(value || 0).toFixed(2); }
function formatDate(value) { if (!value) return "待确认"; const date = new Date(value); return `${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`; }
function goBack() { proxy.$tab.navigateBack(); }
</script>
