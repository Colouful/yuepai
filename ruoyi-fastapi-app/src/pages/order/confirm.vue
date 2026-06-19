<template>
  <view class="yp-page pb-24">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between">
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view>
      <text class="text-base font-black text-zinc-900">确认订单</text>
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="showHelp"><view class="i-lucide-circle-help text-zinc-700 text-lg"></view></view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-4">
        <view class="yp-card p-4">
          <view class="flex items-center">
            <view class="size-16 rounded-2xl flex items-center justify-center" :style="{ background: order.cover }"><view class="i-lucide-camera text-white text-xl"></view></view>
            <view class="flex-1 min-w-0 ml-3"><text class="text-sm font-black text-zinc-900 block truncate">{{ order.title }}</text><text class="text-xs text-zinc-500 block mt-1">摄影师：{{ order.creator }}</text><text class="text-[10px] text-zinc-400 block mt-1">{{ order.serviceSummary }}</text></view>
            <text class="text-lg font-black text-zinc-900">¥{{ order.serviceAmount }}</text>
          </view>
        </view>

        <view class="yp-card p-4 space-y-4">
          <view class="flex items-center justify-between" @click="openDatePicker"><view class="flex items-center"><view class="size-9 rounded-xl bg-rose-50 flex items-center justify-center"><view class="i-lucide-calendar-days text-rose-500 text-sm"></view></view><view class="ml-3"><text class="text-xs font-black text-zinc-800 block">拍摄日期</text><text class="text-[10px] text-zinc-400 block mt-1">{{ form.date || '请选择拍摄日期' }}</text></view></view><view class="i-lucide-chevron-right text-zinc-300 text-sm"></view></view>
          <view class="h-px bg-black/5"></view>
          <view class="flex items-center justify-between" @click="chooseLocation"><view class="flex items-center"><view class="size-9 rounded-xl bg-sky-50 flex items-center justify-center"><view class="i-lucide-map-pin text-sky-600 text-sm"></view></view><view class="ml-3"><text class="text-xs font-black text-zinc-800 block">拍摄地点</text><text class="text-[10px] text-zinc-400 block mt-1">{{ form.location || '请选择拍摄地点' }}</text></view></view><view class="i-lucide-chevron-right text-zinc-300 text-sm"></view></view>
          <view class="h-px bg-black/5"></view>
          <view class="flex items-center justify-between" @click="contactVisible = true"><view class="flex items-center"><view class="size-9 rounded-xl bg-emerald-50 flex items-center justify-center"><view class="i-lucide-user-round text-emerald-600 text-sm"></view></view><view class="ml-3"><text class="text-xs font-black text-zinc-800 block">联系人</text><text class="text-[10px] text-zinc-400 block mt-1">{{ form.contactName }} {{ maskedPhone }}</text></view></view><view class="i-lucide-chevron-right text-zinc-300 text-sm"></view></view>
        </view>

        <view class="yp-card p-4">
          <view class="flex items-center justify-between mb-3"><text class="yp-section-title">订单备注</text><text class="text-[10px] text-zinc-400">{{ form.remark.length }}/200</text></view>
          <textarea v-model="form.remark" maxlength="200" placeholder="补充拍摄风格、服装、忌讳或其他需求" placeholder-class="text-zinc-300" class="h-24 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" />
        </view>

        <view class="yp-card overflow-hidden">
          <view class="flex items-center justify-between px-4 py-4 border-b border-black/5" @click="couponVisible = true"><view class="flex items-center"><view class="i-lucide-ticket-percent text-rose-500 text-base mr-3"></view><text class="text-sm font-bold text-zinc-800">优惠券</text></view><view class="flex items-center"><text class="text-xs text-rose-500">{{ selectedCoupon ? selectedCoupon.name : '请选择优惠券' }}</text><view class="i-lucide-chevron-right text-zinc-300 text-sm ml-1"></view></view></view>
          <view class="flex items-center justify-between px-4 py-4"><view class="flex items-center"><view class="i-lucide-wallet-cards text-amber-500 text-base mr-3"></view><text class="text-sm font-bold text-zinc-800">支付方式</text></view><view class="flex items-center"><view class="i-lucide-message-circle text-emerald-500 text-sm mr-1"></view><text class="text-xs text-zinc-600">微信支付</text></view></view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-4">费用明细</text>
          <view class="space-y-3"><view class="flex items-center justify-between"><text class="text-xs text-zinc-400">服务费用</text><text class="text-xs text-zinc-700">¥{{ order.serviceAmount.toFixed(2) }}</text></view><view class="flex items-center justify-between"><text class="text-xs text-zinc-400">优惠金额</text><text class="text-xs text-emerald-600">-¥{{ discountAmount.toFixed(2) }}</text></view><view class="flex items-center justify-between"><text class="text-xs text-zinc-400">平台服务费</text><text class="text-xs text-zinc-700">¥{{ serviceFee.toFixed(2) }}</text></view><view class="h-px bg-black/5"></view><view class="flex items-center justify-between"><text class="text-sm font-black text-zinc-900">需支付</text><text class="text-xl font-black text-rose-500">¥{{ payableAmount.toFixed(2) }}</text></view></div>
        </view>

        <view class="rounded-2xl bg-emerald-50 p-4 flex items-start"><view class="i-lucide-shield-check text-emerald-600 text-base mt-0.5 mr-3"></view><view><text class="text-xs font-black text-emerald-800 block">平台担保交易</text><text class="text-[10px] text-emerald-700 leading-relaxed block mt-1">支付后由平台托管资金，作品交付并确认验收后再结算。</text></view></view>

        <view class="flex items-start px-1"><checkbox :checked="agreed" color="#18181b" style="transform:scale(.72)" @click="agreed = !agreed" /><text class="text-[10px] text-zinc-400 leading-relaxed ml-1">我已阅读并同意《约拍服务协议》《取消与退款规则》</text></view>
      </view>
    </scroll-view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6 flex items-center">
      <view class="flex-1"><text class="text-[10px] text-zinc-400 block">合计</text><text class="text-xl font-black text-rose-500 block">¥{{ payableAmount.toFixed(2) }}</text></view>
      <view class="w-48 h-12 rounded-2xl flex items-center justify-center text-sm font-black" :class="agreed && !paying ? 'bg-zinc-900 text-white' : 'bg-zinc-200 text-zinc-400'" @click="pay">{{ paying ? '正在支付…' : '确认支付' }}</view>
    </view>

    <picker v-if="false" mode="date"></picker>

    <view v-if="dateVisible" class="fixed inset-0 z-50 flex items-end" @click="dateVisible = false"><view class="absolute inset-0 bg-black/35"></view><view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop><view class="flex items-center justify-between"><text class="text-lg font-black text-zinc-900">选择拍摄日期</text><view class="i-lucide-x text-zinc-500 text-lg" @click="dateVisible = false"></view></view><view class="mt-5 space-y-2"><view v-for="item in dateOptions" :key="item" class="h-12 rounded-2xl flex items-center justify-between px-4" :class="form.date === item ? 'bg-zinc-900 text-white' : 'bg-zinc-50 text-zinc-700'" @click="selectDate(item)"><text class="text-sm font-bold">{{ item }}</text><view v-if="form.date === item" class="i-lucide-check text-sm"></view></view></div></view></view>

    <view v-if="couponVisible" class="fixed inset-0 z-50 flex items-end" @click="couponVisible = false"><view class="absolute inset-0 bg-black/35"></view><view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop><view class="flex items-center justify-between"><text class="text-lg font-black text-zinc-900">选择优惠券</text><view class="i-lucide-x text-zinc-500 text-lg" @click="couponVisible = false"></view></view><view class="mt-5 space-y-3"><view v-for="item in coupons" :key="item.id" class="yp-card p-4 flex items-center" :class="selectedCouponId === item.id ? 'ring-1 ring-zinc-900' : ''" @click="selectCoupon(item)"><view class="w-20 text-center"><text class="text-2xl font-black text-rose-500">¥{{ item.amount }}</text><text class="text-[9px] text-zinc-400 block">满 {{ item.threshold }} 可用</text></view><view class="flex-1 ml-3 border-l border-dashed border-zinc-200 pl-3"><text class="text-sm font-black text-zinc-900 block">{{ item.name }}</text><text class="text-[10px] text-zinc-400 block mt-1">{{ item.expire }}</text></view></view><view class="yp-card p-4 text-center text-xs font-bold text-zinc-500" @click="selectCoupon(null)">不使用优惠券</view></div></view></view>

    <view v-if="contactVisible" class="fixed inset-0 z-50 flex items-end" @click="contactVisible = false"><view class="absolute inset-0 bg-black/35"></view><view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop><view class="flex items-center justify-between"><text class="text-lg font-black text-zinc-900">联系人信息</text><view class="i-lucide-x text-zinc-500 text-lg" @click="contactVisible = false"></view></view><view class="mt-5 space-y-4"><view><text class="text-xs font-bold text-zinc-600 block mb-2">姓名</text><input v-model="form.contactName" placeholder="请输入联系人姓名" class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900" /></view><view><text class="text-xs font-bold text-zinc-600 block mb-2">手机号</text><input v-model="form.phone" type="number" maxlength="11" placeholder="请输入手机号" class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900" /></view><view class="h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="saveContact">保存</view></div></view></view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const orderId = ref(""); const dateVisible = ref(false); const couponVisible = ref(false); const contactVisible = ref(false); const selectedCouponId = ref(1); const agreed = ref(true); const paying = ref(false);
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 80; } catch (error) { console.warn("获取设备信息失败", error); }
onLoad((options) => { orderId.value = options?.orderId || ""; });
const order = reactive({ title: "精致人像写真", creator: "林默", serviceAmount: 1200, serviceSummary: "3 小时 · 含妆造 · 30 张精修", cover: "linear-gradient(135deg,#fb7185,#be123c)" });
const form = reactive({ date: "6 月 20 日 14:00 - 17:00", location: "北京朝阳区三里屯", contactName: "李女士", phone: "13800136688", remark: "希望以自然光和城市街景为主。" });
const dateOptions = ["6 月 20 日 14:00 - 17:00", "6 月 21 日 09:00 - 12:00", "6 月 21 日 14:00 - 17:00", "6 月 22 日 10:00 - 13:00"];
const coupons = [{ id: 1, name: "新人约拍券", amount: 50, threshold: 500, expire: "2026 年 6 月 30 日到期" }, { id: 2, name: "会员专享券", amount: 100, threshold: 1000, expire: "2026 年 7 月 15 日到期" }];
const selectedCoupon = computed(() => coupons.find((item) => item.id === selectedCouponId.value));
const discountAmount = computed(() => selectedCoupon.value && order.serviceAmount >= selectedCoupon.value.threshold ? selectedCoupon.value.amount : 0);
const serviceFee = computed(() => Number(((order.serviceAmount - discountAmount.value) * 0.05).toFixed(2)));
const payableAmount = computed(() => order.serviceAmount - discountAmount.value + serviceFee.value);
const maskedPhone = computed(() => form.phone ? `${form.phone.slice(0, 3)}****${form.phone.slice(-4)}` : "未填写手机号");
function openDatePicker() { dateVisible.value = true; }
function selectDate(item) { form.date = item; dateVisible.value = false; }
function chooseLocation() { uni.chooseLocation({ success(result) { form.location = result.name || result.address; }, fail(error) { if (!String(error.errMsg || "").includes("cancel")) uni.showToast({ title: "定位失败，请手动确认地点", icon: "none" }); } }); }
function selectCoupon(item) { selectedCouponId.value = item?.id || 0; couponVisible.value = false; }
function saveContact() { if (!form.contactName.trim()) return uni.showToast({ title: "请填写联系人姓名", icon: "none" }); if (!/^1\d{10}$/.test(form.phone)) return uni.showToast({ title: "请填写正确手机号", icon: "none" }); contactVisible.value = false; }
function pay() { if (paying.value) return; if (!agreed.value) return uni.showToast({ title: "请先同意服务协议", icon: "none" }); if (!form.date || !form.location) return uni.showToast({ title: "请完善拍摄时间和地点", icon: "none" }); paying.value = true; setTimeout(() => { paying.value = false; const paidOrder = { id: orderId.value || Date.now(), no: `YP${Date.now()}`, title: order.title, creator: order.creator, amount: payableAmount.value, status: "pending_service", date: form.date, location: form.location, createdAt: new Date().toISOString() }; const paidOrders = uni.getStorageSync("yuepai_paid_orders") || []; uni.setStorageSync("yuepai_paid_orders", [paidOrder, ...paidOrders]); uni.showToast({ title: "支付成功", icon: "success" }); setTimeout(() => proxy.$tab.navigateTo(`/pages/order/detail?id=${paidOrder.id}`), 500); }, 800); }
function showHelp() { uni.showModal({ title: "支付说明", content: "当前为前端演示支付流程。正式上线后需接入微信支付，并以服务端支付结果为准。", showCancel: false }); }
function goBack() { proxy.$tab.navigateBack(); }
</script>
