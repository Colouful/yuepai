<template>
  <view class="yp-page pb-24">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between">
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view>
      <text class="text-base font-black text-zinc-900">订单详情</text>
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="showMore"><view class="i-lucide-ellipsis text-zinc-700 text-lg"></view></view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-4">
        <view class="yp-card-strong p-5 relative overflow-hidden">
          <view class="absolute -right-12 -top-12 size-40 rounded-full" style="background:rgba(244,63,94,.25);filter:blur(24px)"></view>
          <view class="relative z-10 flex items-center justify-between">
            <view><text class="text-xl font-black text-white block">{{ statusInfo.title }}</text><text class="text-xs text-white/55 block mt-2">{{ statusInfo.description }}</text></view>
            <view class="size-14 rounded-2xl bg-white/10 flex items-center justify-center"><view :class="statusInfo.icon" class="text-2xl text-white"></view></view>
          </view>
          <view v-if="order.status === 'pending_service'" class="relative z-10 mt-5 rounded-2xl bg-white/10 px-4 py-3 flex items-center justify-between"><view><text class="text-[10px] text-white/50 block">距离拍摄</text><text class="text-sm font-black text-white block mt-1">1 天 18 小时</text></view><view class="rounded-full bg-white px-3 py-1.5 text-[10px] font-bold text-zinc-900" @click="addCalendar">加入日历</view></view>
        </view>

        <view class="yp-card p-4">
          <view class="flex items-center">
            <view class="size-14 rounded-2xl flex items-center justify-center text-white font-black" :style="{ background: order.cover }">{{ order.creator[0] }}</view>
            <view class="flex-1 ml-3"><view class="flex items-center"><text class="text-sm font-black text-zinc-900">{{ order.creator }}</text><view class="i-lucide-badge-check text-rose-500 text-xs ml-1"></view></view><text class="text-[10px] text-zinc-400 block mt-1">{{ order.creatorTitle }} · 回复率 98%</text></view>
            <view class="flex space-x-2"><view class="size-9 rounded-xl bg-zinc-100 flex items-center justify-center" @click="callCreator"><view class="i-lucide-phone text-zinc-700 text-sm"></view></view><view class="size-9 rounded-xl bg-zinc-900 flex items-center justify-center" @click="openChat"><view class="i-lucide-message-circle text-white text-sm"></view></view></view>
          </view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-4">服务信息</text>
          <view class="flex items-center mb-4"><view class="size-16 rounded-2xl flex items-center justify-center" :style="{ background: order.cover }"><view class="i-lucide-camera text-white text-xl"></view></view><view class="flex-1 ml-3"><text class="text-sm font-black text-zinc-900 block">{{ order.title }}</text><text class="text-[10px] text-zinc-400 block mt-1">3 小时 · 含妆造 · 30 张精修</text></view><text class="text-base font-black text-zinc-900">¥{{ order.serviceAmount }}</text></view>
          <view class="space-y-3 pt-3 border-t border-black/5">
            <view v-for="item in serviceDetails" :key="item.label" class="flex items-start"><view :class="item.icon" class="w-5 text-sm text-rose-500 mt-0.5"></view><text class="w-20 text-xs text-zinc-400">{{ item.label }}</text><text class="flex-1 text-xs text-zinc-700 text-right">{{ item.value }}</text></view>
          </view>
        </view>

        <view class="yp-card p-4">
          <view class="flex items-center justify-between mb-4"><text class="yp-section-title">订单进度</text><text class="text-[10px] text-zinc-400">订单号 {{ order.no }}</text></view>
          <view class="space-y-0">
            <view v-for="(item, index) in timeline" :key="item.title" class="flex items-stretch">
              <view class="w-6 flex flex-col items-center"><view class="size-3 rounded-full border-2 mt-1" :class="item.done ? 'bg-zinc-900 border-zinc-900' : 'bg-white border-zinc-200'"></view><view v-if="index < timeline.length - 1" class="w-px flex-1 min-h-12" :class="timeline[index + 1].done ? 'bg-zinc-900' : 'bg-zinc-200'"></view></view>
              <view class="flex-1 pb-5 ml-2"><view class="flex items-center justify-between"><text class="text-xs font-bold" :class="item.done ? 'text-zinc-800' : 'text-zinc-400'">{{ item.title }}</text><text class="text-[9px] text-zinc-300">{{ item.time }}</text></view><text class="text-[10px] text-zinc-400 block mt-1">{{ item.description }}</text></view>
            </view>
          </view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-4">费用明细</text>
          <view class="space-y-3"><view v-for="item in feeItems" :key="item.label" class="flex items-center justify-between"><text class="text-xs text-zinc-400">{{ item.label }}</text><text class="text-xs text-zinc-700">{{ item.value }}</text></view><view class="h-px bg-black/5"></view><view class="flex items-center justify-between"><text class="text-sm font-black text-zinc-900">实付金额</text><text class="text-xl font-black text-rose-500">¥{{ order.paidAmount }}</text></view></div>
        </view>

        <view class="rounded-2xl bg-amber-50 p-4 flex items-start"><view class="i-lucide-shield-check text-amber-600 text-base mt-0.5 mr-3"></view><view><text class="text-xs font-black text-amber-800 block">交易保障</text><text class="text-[10px] text-amber-700 leading-relaxed block mt-1">拍摄与交付完成前，服务款由平台托管。出现争议可申请平台介入。</text></view></view>
      </view>
    </scroll-view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3">
      <view v-if="secondaryAction" class="flex-1 h-12 rounded-2xl border border-black/10 flex items-center justify-center text-sm font-bold text-zinc-700" @click="handleSecondary">{{ secondaryAction }}</view>
      <view class="flex-1 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="handlePrimary">{{ primaryAction }}</view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const orderId = ref("1");
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 80; } catch (error) { console.warn("获取设备信息失败", error); }
onLoad((options) => { orderId.value = options?.id || "1"; });
const order = reactive({ no: "YP20260617001", title: "精致人像写真", creator: "林默", creatorTitle: "人像摄影师", serviceAmount: 1200, paidAmount: 1207.5, status: "pending_service", cover: "linear-gradient(135deg,#fb7185,#be123c)" });
const serviceDetails = [{ label: "拍摄时间", value: "6 月 20 日 14:00 - 17:00", icon: "i-lucide-calendar-days" }, { label: "拍摄地点", value: "北京朝阳区三里屯", icon: "i-lucide-map-pin" }, { label: "联系人", value: "李女士 138****6688", icon: "i-lucide-user-round" }, { label: "订单备注", value: "希望以自然光和城市街景为主", icon: "i-lucide-message-square-text" }];
const feeItems = [{ label: "服务费用", value: "¥1200.00" }, { label: "优惠金额", value: "-¥50.00" }, { label: "平台服务费", value: "¥57.50" }];
const timeline = computed(() => {
  const steps = [
    { key: "paid", title: "订单已支付", description: "平台已托管服务款", time: "6 月 17 日 18:24" },
    { key: "confirmed", title: "摄影师已确认", description: "档期已锁定，请按时到达", time: "6 月 17 日 18:32" },
    { key: "shooting", title: "开始拍摄", description: "双方到场后确认开始", time: "6 月 20 日 14:00" },
    { key: "delivery", title: "作品交付", description: "摄影师上传精修作品", time: "预计 6 月 23 日" },
    { key: "completed", title: "订单完成", description: "验收并完成评价", time: "-" }
  ];
  const progress = { pending_payment: 0, pending_service: 2, shooting: 3, pending_delivery: 3, pending_review: 4, completed: 5 }[order.status] || 1;
  return steps.map((item, index) => ({ ...item, done: index < progress }));
});
const statusInfo = computed(() => ({ pending_payment: { title: "等待付款", description: "付款后为你锁定摄影师档期", icon: "i-lucide-wallet-cards" }, pending_service: { title: "等待拍摄", description: "请提前与摄影师确认地点和造型", icon: "i-lucide-camera" }, shooting: { title: "拍摄进行中", description: "祝你享受这次创作体验", icon: "i-lucide-aperture" }, pending_delivery: { title: "等待交付", description: "摄影师正在进行选片和精修", icon: "i-lucide-images" }, pending_review: { title: "等待评价", description: "分享你的真实拍摄体验", icon: "i-lucide-star" }, completed: { title: "订单已完成", description: "感谢你使用约拍服务", icon: "i-lucide-circle-check" } }[order.status] || { title: "订单处理中", description: "请关注后续状态更新", icon: "i-lucide-clock-3" }));
const primaryAction = computed(() => ({ pending_payment: "立即支付", pending_service: "确认到场", shooting: "联系摄影师", pending_delivery: "查看交付", pending_review: "立即评价", completed: "再次预约" }[order.status] || "查看详情"));
const secondaryAction = computed(() => ({ pending_payment: "取消订单", pending_service: "修改预约", shooting: "申请帮助", pending_delivery: "联系摄影师", pending_review: "查看作品", completed: "查看作品" }[order.status] || ""));
function handlePrimary() { if (order.status === "pending_payment") return proxy.$tab.navigateTo(`/pages/order/confirm?orderId=${orderId.value}`); if (order.status === "pending_delivery") return proxy.$tab.navigateTo(`/pages/order/deliver?id=${orderId.value}`); if (order.status === "pending_review") return proxy.$tab.navigateTo(`/pages/order/review?id=${orderId.value}`); if (order.status === "completed") return proxy.$tab.navigateTo("/pages/photographer/detail?id=1"); if (order.status === "pending_service") { uni.showModal({ title: "确认到场", content: "到达拍摄地点后再确认，确认后订单进入拍摄中。", success(result) { if (result.confirm) order.status = "shooting"; } }); return; } openChat(); }
function handleSecondary() { if (order.status === "pending_payment") return uni.showModal({ title: "取消订单", content: "确认取消当前订单吗？", success(result) { if (result.confirm) order.status = "cancelled"; } }); if (order.status === "pending_service") return uni.showToast({ title: "改期申请已提交", icon: "none" }); if (["shooting"].includes(order.status)) return proxy.$tab.navigateTo("/pages/service/index"); if (["pending_delivery"].includes(order.status)) return openChat(); proxy.$tab.navigateTo(`/pages/order/deliver?id=${orderId.value}`); }
function openChat() { proxy.$tab.navigateTo(`/pages/chat/index?id=1&name=${encodeURIComponent(order.creator)}`); }
function callCreator() { uni.showModal({ title: "联系摄影师", content: "为保护隐私，请优先使用平台聊天。紧急情况下可通过订单预留号码联系。", confirmText: "去聊天", success(result) { if (result.confirm) openChat(); } }); }
function addCalendar() { uni.showToast({ title: "已添加到日历提醒", icon: "success" }); }
function showMore() { uni.showActionSheet({ itemList: ["复制订单号", "申请售后", "举报问题"], success(result) { if (result.tapIndex === 0) uni.setClipboardData({ data: order.no }); if (result.tapIndex === 1) proxy.$tab.navigateTo(`/pages/refund/index?id=${orderId.value}`); if (result.tapIndex === 2) proxy.$tab.navigateTo(`/pages/report/index?id=${orderId.value}`); } }); }
function goBack() { proxy.$tab.navigateBack(); }
</script>
