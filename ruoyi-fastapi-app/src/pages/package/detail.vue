<template>
  <view class="yp-page min-h-screen pb-28">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between">
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack">
        <view class="i-lucide-arrow-left text-zinc-700 text-lg"></view>
      </view>
      <text class="text-base font-black text-zinc-900">服务套餐</text>
      <view class="w-10"></view>
    </view>

    <view v-if="loading" class="px-5 pt-4 space-y-4">
      <view class="h-52 rounded-[32rpx] bg-white/70 animate-pulse"></view>
      <view class="h-40 rounded-[24rpx] bg-white/70 animate-pulse"></view>
      <view class="h-48 rounded-[24rpx] bg-white/70 animate-pulse"></view>
    </view>

    <view v-else-if="errorMessage" class="pt-28 px-8 text-center">
      <view class="i-lucide-package-x text-3xl text-rose-400"></view>
      <text class="text-base font-black text-zinc-800 block mt-4">套餐加载失败</text>
      <text class="text-xs text-zinc-400 block mt-2">{{ errorMessage }}</text>
      <view class="mt-5 inline-flex rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="loadPackage">重新加载</view>
    </view>

    <view v-else-if="servicePackage" class="px-5 pt-4 space-y-4">
      <view class="yp-card-strong p-5 relative overflow-hidden">
        <view class="absolute -right-12 -top-16 size-48 rounded-full" style="background:rgba(244,63,94,.28);filter:blur(30px)"></view>
        <view class="relative z-10">
          <text class="text-[10px] text-white/45 tracking-[4rpx]">SERVICE PACKAGE</text>
          <text class="text-2xl font-black text-white block mt-3">{{ servicePackage.packageName }}</text>
          <text class="text-xs text-white/60 block mt-3 leading-relaxed">{{ servicePackage.description }}</text>
          <view class="mt-6 flex items-end justify-between">
            <view><text class="text-[10px] text-white/45 block">服务价格</text><text class="text-3xl font-black text-rose-300 block mt-1">¥{{ money(servicePackage.price) }}</text></view>
            <view class="text-right"><text class="text-[10px] text-white/45 block">预计时长</text><text class="text-sm font-black text-white block mt-1">{{ duration(servicePackage.durationMinutes) }}</text></view>
          </view>
        </view>
      </view>

      <view class="yp-card p-4">
        <text class="yp-section-title block mb-4">交付标准</text>
        <view class="grid grid-cols-4 gap-2">
          <view class="rounded-2xl bg-zinc-50 p-3 text-center"><text class="text-base font-black text-zinc-800 block">{{ servicePackage.originalCount }}</text><text class="text-[9px] text-zinc-400">原片</text></view>
          <view class="rounded-2xl bg-zinc-50 p-3 text-center"><text class="text-base font-black text-zinc-800 block">{{ servicePackage.retouchedCount }}</text><text class="text-[9px] text-zinc-400">精修</text></view>
          <view class="rounded-2xl bg-zinc-50 p-3 text-center"><text class="text-base font-black text-zinc-800 block">{{ servicePackage.deliveryDays }}</text><text class="text-[9px] text-zinc-400">交付天数</text></view>
          <view class="rounded-2xl bg-zinc-50 p-3 text-center"><text class="text-base font-black text-zinc-800 block">{{ servicePackage.revisionCount }}</text><text class="text-[9px] text-zinc-400">修改次数</text></view>
        </view>
      </view>

      <view v-if="servicePackage.includes?.length" class="yp-card p-4">
        <text class="yp-section-title block mb-3">套餐包含</text>
        <view class="space-y-2">
          <view v-for="item in servicePackage.includes" :key="item" class="flex items-start"><view class="i-lucide-circle-check text-emerald-500 text-sm mt-0.5 mr-2"></view><text class="text-xs text-zinc-600 flex-1">{{ item }}</text></view>
        </view>
      </view>

      <view v-if="servicePackage.excludes?.length" class="yp-card p-4">
        <text class="yp-section-title block mb-3">不包含</text>
        <view class="space-y-2">
          <view v-for="item in servicePackage.excludes" :key="item" class="flex items-start"><view class="i-lucide-circle-minus text-zinc-400 text-sm mt-0.5 mr-2"></view><text class="text-xs text-zinc-500 flex-1">{{ item }}</text></view>
        </view>
      </view>

      <view v-if="servicePackage.addons?.length" class="yp-card p-4">
        <text class="yp-section-title block mb-3">可选增值服务</text>
        <view class="space-y-2">
          <view v-for="(item, index) in servicePackage.addons" :key="index" class="rounded-2xl bg-zinc-50 p-3 flex items-center justify-between"><text class="text-xs text-zinc-600">{{ item.name || item.title }}</text><text class="text-xs font-black text-rose-500">+¥{{ money(item.price) }}</text></view>
        </view>
      </view>

      <view class="yp-card p-4">
        <text class="yp-section-title block mb-4">预约信息</text>
        <view class="grid grid-cols-2 gap-3">
          <picker mode="date" :value="form.shootDate" @change="form.shootDate = $event.detail.value">
            <view class="rounded-2xl bg-zinc-50 p-3"><text class="text-[10px] text-zinc-400 block">拍摄日期</text><text class="text-xs font-bold text-zinc-800 block mt-2">{{ form.shootDate }}</text></view>
          </picker>
          <picker mode="time" :value="form.shootTime" @change="form.shootTime = $event.detail.value">
            <view class="rounded-2xl bg-zinc-50 p-3"><text class="text-[10px] text-zinc-400 block">开始时间</text><text class="text-xs font-bold text-zinc-800 block mt-2">{{ form.shootTime }}</text></view>
          </picker>
        </view>
        <view class="mt-3"><text class="text-xs font-bold text-zinc-600 block mb-2">拍摄地点</text><input v-model.trim="form.location" maxlength="160" placeholder="填写城市和具体地点" placeholder-class="text-zinc-300" class="h-11 rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900 w-full" /></view>
        <view class="mt-3 grid grid-cols-2 gap-3"><view><text class="text-xs font-bold text-zinc-600 block mb-2">联系人</text><input v-model.trim="form.contactName" maxlength="30" placeholder="真实姓名" class="h-11 rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900 w-full" /></view><view><text class="text-xs font-bold text-zinc-600 block mb-2">联系电话</text><input v-model.trim="form.contactPhone" type="number" maxlength="11" placeholder="手机号" class="h-11 rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900 w-full" /></view></view>
        <view class="mt-3"><text class="text-xs font-bold text-zinc-600 block mb-2">补充要求</text><textarea v-model="form.remark" maxlength="500" placeholder="说明风格、人数、服装、妆造等需求" placeholder-class="text-zinc-300" class="h-24 rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900 w-full" /></view>
      </view>

      <view v-if="servicePackage.bookingNotice" class="yp-card p-4"><text class="yp-section-title block mb-3">预约须知</text><text class="text-xs text-zinc-500 leading-relaxed whitespace-pre-wrap">{{ servicePackage.bookingNotice }}</text></view>
      <view v-if="servicePackage.refundRule" class="yp-card p-4"><text class="yp-section-title block mb-3">退款规则</text><text class="text-xs text-zinc-500 leading-relaxed whitespace-pre-wrap">{{ servicePackage.refundRule }}</text></view>

      <view class="rounded-2xl bg-amber-50 p-4 flex items-start"><view class="i-lucide-shield-check text-amber-600 text-base mt-0.5 mr-3"></view><text class="text-[10px] text-amber-700 leading-relaxed">提交后生成预约报价，等待创作者确认。确认后才生成待支付订单，未生成订单前不会扣款。</text></view>
    </view>

    <view v-if="servicePackage" class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 border-t border-black/5 px-5 pt-3 pb-6 flex items-center">
      <view class="mr-4"><text class="text-[9px] text-zinc-400 block">套餐价格</text><text class="text-xl font-black text-rose-500">¥{{ money(servicePackage.price) }}</text></view>
      <view class="flex-1 h-12 rounded-2xl flex items-center justify-center text-sm font-black" :class="submitting ? 'bg-zinc-200 text-zinc-400' : 'bg-zinc-900 text-white'" @click="submitBooking">{{ submitting ? '正在发送…' : '发送预约申请' }}</view>
    </view>
  </view>
</template>

<script setup>
import { getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getToken } from "@/utils/auth";
import { createQuote } from "@/api/yuepai/core";
import { getCreator, listCreatorPackages } from "@/api/yuepai/creator-api";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const packageId = ref("");
const creatorId = ref("");
const creator = ref(null);
const servicePackage = ref(null);
const loading = ref(true);
const errorMessage = ref("");
const submitting = ref(false);
const form = reactive(buildDefaultForm());

onLoad((options) => {
  packageId.value = options?.id || "";
  creatorId.value = options?.creatorId || "";
  try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (error) { console.warn(error); }
  loadPackage();
});

function buildDefaultForm() {
  const date = new Date(Date.now() + 7 * 86400000);
  return {
    shootDate: `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`,
    shootTime: "14:00",
    location: "",
    contactName: "",
    contactPhone: "",
    remark: "",
  };
}

async function loadPackage() {
  if (!packageId.value || !creatorId.value) { errorMessage.value = "套餐参数不完整"; loading.value = false; return; }
  loading.value = true;
  errorMessage.value = "";
  try {
    const [creatorRes, packageRes] = await Promise.all([getCreator(creatorId.value), listCreatorPackages(creatorId.value)]);
    creator.value = creatorRes.data || creatorRes;
    const rows = Array.isArray(packageRes.rows) ? packageRes.rows : [];
    servicePackage.value = rows.find((item) => String(item.packageId) === String(packageId.value));
    if (!servicePackage.value) throw new Error("套餐不存在或已下架");
  } catch (error) { errorMessage.value = error?.message || "网络异常，请稍后重试"; }
  finally { loading.value = false; }
}

async function submitBooking() {
  if (submitting.value) return;
  if (!getToken()) return proxy.$tab.navigateTo("/pages/login");
  if (!form.location.trim()) return uni.showToast({ title: "请填写拍摄地点", icon: "none" });
  if (!form.contactName.trim()) return uni.showToast({ title: "请填写联系人", icon: "none" });
  if (!/^1\d{10}$/.test(form.contactPhone)) return uni.showToast({ title: "请填写正确手机号", icon: "none" });
  const shootAt = new Date(`${form.shootDate}T${form.shootTime}:00`);
  if (shootAt <= new Date()) return uni.showToast({ title: "拍摄时间必须晚于当前时间", icon: "none" });
  submitting.value = true;
  try {
    const price = Number(servicePackage.value.price || 0);
    await createQuote({
      receiverUserId: creator.value.userId,
      amount: price,
      feeBreakdown: { service: price },
      serviceSnapshot: {
        packageId: servicePackage.value.packageId,
        creatorId: creator.value.creatorId,
        creatorName: creator.value.displayName,
        title: servicePackage.value.packageName,
        description: servicePackage.value.description,
        durationMinutes: servicePackage.value.durationMinutes,
        originalCount: servicePackage.value.originalCount,
        retouchedCount: servicePackage.value.retouchedCount,
        deliveryDays: servicePackage.value.deliveryDays,
        revisionCount: servicePackage.value.revisionCount,
        includes: servicePackage.value.includes,
        refundRule: servicePackage.value.refundRule,
        proposedShootAt: shootAt.toISOString(),
        proposedLocation: form.location.trim(),
        contact: { name: form.contactName.trim(), phone: form.contactPhone },
      },
      remark: form.remark.trim() || null,
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
    });
    uni.showModal({ title: "预约申请已发送", content: "创作者确认报价后会生成订单，请在消息和订单中心关注进度。", showCancel: false, success() { proxy.$tab.switchTab("/pages/message/index"); } });
  } finally { submitting.value = false; }
}

function money(value) { return Number(value || 0).toFixed(0); }
function duration(minutes) { const value = Number(minutes || 0); return value >= 480 ? "全天" : value >= 60 ? `${Math.round(value / 60)}小时` : `${value}分钟`; }
function goBack() { proxy.$tab.navigateBack(); }
</script>
