<template>
  <view class="yp-page min-h-screen pb-28">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between">
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack">
        <view class="i-lucide-arrow-left text-zinc-700 text-lg"></view>
      </view>
      <text class="text-base font-black text-zinc-900">需求详情</text>
      <view class="w-10"></view>
    </view>

    <view v-if="loading" class="px-5 pt-4 space-y-4">
      <view class="yp-card h-52 animate-pulse bg-white/70"></view>
      <view class="yp-card h-36 animate-pulse bg-white/70"></view>
    </view>

    <view v-else-if="errorMessage" class="px-5 pt-24 flex flex-col items-center">
      <view class="size-16 rounded-full bg-rose-50 flex items-center justify-center">
        <view class="i-lucide-circle-alert text-2xl text-rose-500"></view>
      </view>
      <text class="text-sm font-black text-zinc-700 mt-4">详情加载失败</text>
      <text class="text-xs text-zinc-400 mt-2 text-center">{{ errorMessage }}</text>
      <view class="mt-4 rounded-full bg-zinc-900 px-5 py-2 text-xs font-bold text-white" @click="loadDetail">重新加载</view>
    </view>

    <view v-else-if="demand" class="px-5 pt-4 space-y-4">
      <view class="yp-card-strong p-5 relative overflow-hidden">
        <view class="absolute -right-12 -top-12 size-40 rounded-full" style="background:rgba(244,63,94,.24);filter:blur(24px)"></view>
        <view class="relative z-10">
          <view class="flex items-center justify-between">
            <view class="rounded-full px-3 py-1.5 text-[10px] font-bold" :class="isMutual ? 'bg-emerald-500/20 text-emerald-200' : 'bg-rose-500/20 text-rose-200'">
              {{ isMutual ? '互勉创作' : '付费约拍' }}
            </view>
            <text class="text-[10px] text-white/45">{{ deadlineText }}</text>
          </view>
          <text class="text-2xl font-black text-white block mt-4 leading-tight">{{ demand.title }}</text>
          <text class="text-xs text-white/55 block mt-3">{{ demand.demandType }} · {{ demand.cityCode }}</text>
          <view class="mt-5 flex items-end justify-between">
            <view class="text-[10px] text-white/55">
              <text class="block">{{ formatDate(demand.shootAt) }}</text>
              <text class="block mt-1">预计 {{ formatDuration(demand.durationMinutes) }}</text>
            </view>
            <text class="text-2xl font-black" :class="isMutual ? 'text-emerald-300' : 'text-rose-300'">{{ budgetText }}</text>
          </view>
        </view>
      </view>

      <view class="yp-card p-4">
        <text class="yp-section-title block mb-3">招募信息</text>
        <view class="grid grid-cols-2 gap-3">
          <view class="rounded-2xl bg-zinc-50 p-3">
            <text class="text-[10px] text-zinc-400 block">拍摄地点</text>
            <text class="text-xs font-bold text-zinc-800 block mt-2">{{ demand.locationName || demand.cityCode }}</text>
          </view>
          <view class="rounded-2xl bg-zinc-50 p-3">
            <text class="text-[10px] text-zinc-400 block">报名人数</text>
            <text class="text-xs font-bold text-zinc-800 block mt-2">{{ demand.applicantCount || 0 }} / {{ demand.applicantLimit }} 人</text>
          </view>
        </view>
        <view class="mt-4 flex flex-wrap gap-2">
          <view v-for="role in demand.roles" :key="role" class="yp-chip yp-chip-active">招募 {{ role }}</view>
        </view>
      </view>

      <view class="yp-card p-4">
        <text class="yp-section-title block mb-3">详细说明</text>
        <text class="text-xs text-zinc-500 leading-relaxed whitespace-pre-wrap">{{ demand.description }}</text>
      </view>

      <view v-if="demand.referenceAssets?.length">
        <view class="flex items-end justify-between mb-3">
          <text class="yp-section-title">参考风格</text>
          <text class="text-xs text-zinc-400">{{ demand.referenceAssets.length }} 张</text>
        </view>
        <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
          <view class="inline-flex space-x-3 pr-5">
            <image
              v-for="(url, index) in demand.referenceAssets"
              :key="url"
              :src="url"
              mode="aspectFill"
              class="inline-block w-36 h-44 rounded-3xl bg-zinc-100"
              @click="previewReference(index)"
            />
          </view>
        </scroll-view>
      </view>

      <view class="rounded-2xl bg-amber-50 p-4 flex items-start">
        <view class="i-lucide-shield-check text-amber-600 text-base mt-0.5 mr-3"></view>
        <view>
          <text class="text-xs font-black text-amber-800 block">平台安全提示</text>
          <text class="text-[10px] text-amber-700 leading-relaxed block mt-1">请通过平台报名、沟通和支付，不要提前向陌生账户转账。</text>
        </view>
      </view>
    </view>

    <view v-if="demand" class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 border-t border-black/5 px-5 pt-3 pb-6">
      <view
        class="h-12 rounded-2xl flex items-center justify-center text-sm font-black"
        :class="applied ? 'bg-emerald-50 text-emerald-600' : 'bg-zinc-900 text-white'"
        @click="openApply"
      >
        {{ applied ? '报名已提交' : '立即报名' }}
      </view>
    </view>

    <view v-if="applyVisible" class="fixed inset-0 z-50 flex items-end" @click="applyVisible = false">
      <view class="absolute inset-0 bg-black/35"></view>
      <view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop>
        <view class="flex items-center justify-between">
          <view>
            <text class="text-lg font-black text-zinc-900 block">报名约拍</text>
            <text class="text-[10px] text-zinc-400 block mt-1">请真实填写经验和合作方案</text>
          </view>
          <view class="i-lucide-x text-zinc-500 text-lg" @click="applyVisible = false"></view>
        </view>

        <view class="mt-5">
          <text class="text-sm font-black text-zinc-800 block mb-2">报名身份</text>
          <view class="flex flex-wrap gap-2">
            <view v-for="role in demand.roles" :key="role" class="yp-chip" :class="form.roleCode === role ? 'yp-chip-active' : ''" @click="form.roleCode = role">{{ role }}</view>
          </view>
        </view>

        <view class="mt-5">
          <view class="flex items-center justify-between mb-2">
            <text class="text-sm font-black text-zinc-800">自我介绍</text>
            <text class="text-[10px] text-zinc-400">{{ form.introduction.length }}/500</text>
          </view>
          <textarea v-model="form.introduction" maxlength="500" placeholder="介绍经验、擅长风格和本次合作方案，至少 10 个字" placeholder-class="text-zinc-300" class="h-28 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" />
        </view>

        <view class="mt-5">
          <text class="text-sm font-black text-zinc-800 block mb-2">报价</text>
          <view class="h-11 rounded-2xl bg-zinc-50 px-4 flex items-center">
            <text class="text-sm text-zinc-500 mr-2">¥</text>
            <input v-model="form.quoteAmount" type="digit" placeholder="互勉可填 0" placeholder-class="text-zinc-300" class="flex-1 text-sm text-zinc-900" />
          </view>
        </view>

        <view class="mt-6 h-12 rounded-2xl flex items-center justify-center text-sm font-black" :class="submitting ? 'bg-zinc-200 text-zinc-400' : 'bg-zinc-900 text-white'" @click="submitApplication">
          {{ submitting ? '正在提交…' : '提交报名' }}
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { applyDemand, getDemand } from "@/api/yuepai/core";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const demandId = ref("");
const demand = ref(null);
const loading = ref(true);
const errorMessage = ref("");
const applyVisible = ref(false);
const submitting = ref(false);
const applied = ref(false);
const form = reactive({ roleCode: "", introduction: "", quoteAmount: "" });

const isMutual = computed(() => ["mutual", "free"].includes(demand.value?.budgetType));
const budgetText = computed(() => {
  const item = demand.value;
  if (!item) return "";
  if (item.budgetType === "mutual") return "互勉";
  if (item.budgetType === "free") return "免费";
  if (["quote", "negotiable"].includes(item.budgetType)) return "面议";
  if (item.budgetType === "range") return `¥${item.budgetMin || 0}-${item.budgetMax || 0}`;
  return `¥${item.budgetMin || 0}`;
});
const deadlineText = computed(() => demand.value ? `截止 ${formatDate(demand.value.applicationDeadline)}` : "");

onLoad((options) => {
  try {
    statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44;
  } catch (error) {
    console.warn("获取设备信息失败", error);
  }
  demandId.value = options?.id || "";
  loadDetail();
});

async function loadDetail() {
  if (!demandId.value) {
    errorMessage.value = "需求参数无效";
    loading.value = false;
    return;
  }
  loading.value = true;
  errorMessage.value = "";
  try {
    const response = await getDemand(demandId.value);
    demand.value = response.data || response;
    form.roleCode = demand.value?.roles?.[0] || "";
  } catch (error) {
    errorMessage.value = error?.message || "网络异常，请稍后重试";
  } finally {
    loading.value = false;
  }
}

function openApply() {
  if (applied.value) {
    uni.showToast({ title: "报名已提交，请等待发布者处理", icon: "none" });
    return;
  }
  applyVisible.value = true;
}

async function submitApplication() {
  if (submitting.value) return;
  if (!form.roleCode) return uni.showToast({ title: "请选择报名身份", icon: "none" });
  if (form.introduction.trim().length < 10) return uni.showToast({ title: "自我介绍至少填写 10 个字", icon: "none" });
  const amount = form.quoteAmount === "" ? null : Number(form.quoteAmount);
  if (amount !== null && (!Number.isFinite(amount) || amount < 0)) return uni.showToast({ title: "请填写有效报价", icon: "none" });

  submitting.value = true;
  try {
    await applyDemand(demandId.value, {
      roleCode: form.roleCode,
      introduction: form.introduction.trim(),
      quoteAmount: amount,
      portfolioAssets: [],
    });
    applied.value = true;
    applyVisible.value = false;
    if (demand.value) demand.value.applicantCount = Number(demand.value.applicantCount || 0) + 1;
    uni.showToast({ title: "报名成功", icon: "success" });
  } finally {
    submitting.value = false;
  }
}

function previewReference(index) {
  uni.previewImage({ current: index, urls: demand.value.referenceAssets });
}

function formatDate(value) {
  if (!value) return "待确认";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hour = String(date.getHours()).padStart(2, "0");
  const minute = String(date.getMinutes()).padStart(2, "0");
  return `${month}-${day} ${hour}:${minute}`;
}

function formatDuration(minutes) {
  const value = Number(minutes || 0);
  if (value >= 480) return "全天";
  if (value >= 60) return `${Math.round(value / 60)} 小时`;
  return `${value} 分钟`;
}

function goBack() {
  proxy.$tab.navigateBack();
}
</script>
