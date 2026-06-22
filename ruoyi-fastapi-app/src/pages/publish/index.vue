<template>
  <view class="yp-page flex h-full flex-col">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3">
      <text class="yp-eyebrow block">CREATE</text>
      <text class="yp-title block mt-1">发布约拍</text>
      <text class="text-xs text-zinc-400 block mt-2">发布后进入平台审核，审核通过才会公开展示</text>
    </view>

    <scroll-view scroll-y class="flex-1" :show-scrollbar="false">
      <view class="px-5 pb-28 space-y-4">
        <view class="yp-card p-4">
          <text class="text-sm font-black text-zinc-800 block mb-3">约拍类型</text>
          <view class="flex flex-wrap gap-2">
            <view v-for="item in types" :key="item" class="yp-chip" :class="form.demandType === item ? 'yp-chip-active' : ''" @click="form.demandType = item">{{ item }}</view>
          </view>
        </view>

        <view class="yp-card p-4 space-y-4">
          <view>
            <view class="flex items-center justify-between mb-2"><text class="text-sm font-black text-zinc-800">需求标题</text><text class="text-[10px] text-zinc-400">{{ form.title.length }}/80</text></view>
            <input v-model.trim="form.title" maxlength="80" placeholder="清楚说明拍摄主题和招募对象" placeholder-class="text-zinc-300" class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900" />
          </view>
          <view>
            <view class="flex items-center justify-between mb-2"><text class="text-sm font-black text-zinc-800">详细说明</text><text class="text-[10px] text-zinc-400">{{ form.description.length }}/5000</text></view>
            <textarea v-model="form.description" maxlength="5000" placeholder="说明风格、交付、服装、妆造、器材和合作要求，至少 20 个字" placeholder-class="text-zinc-300" class="h-32 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" />
          </view>
        </view>

        <view class="yp-card p-4">
          <text class="text-sm font-black text-zinc-800 block mb-3">招募角色</text>
          <view class="flex flex-wrap gap-2">
            <view v-for="role in roleOptions" :key="role" class="yp-chip" :class="form.roles.includes(role) ? 'yp-chip-active' : ''" @click="toggleRole(role)">{{ role }}</view>
          </view>
        </view>

        <view class="yp-card p-4 space-y-4">
          <view class="grid grid-cols-2 gap-3">
            <picker mode="date" :value="form.shootDate" @change="form.shootDate = $event.detail.value">
              <view class="rounded-2xl bg-zinc-50 p-3"><text class="text-[10px] text-zinc-400 block">拍摄日期</text><text class="text-xs font-bold text-zinc-800 block mt-2">{{ form.shootDate }}</text></view>
            </picker>
            <picker mode="time" :value="form.shootTime" @change="form.shootTime = $event.detail.value">
              <view class="rounded-2xl bg-zinc-50 p-3"><text class="text-[10px] text-zinc-400 block">开始时间</text><text class="text-xs font-bold text-zinc-800 block mt-2">{{ form.shootTime }}</text></view>
            </picker>
          </view>

          <view class="grid grid-cols-2 gap-3">
            <view><text class="text-xs font-bold text-zinc-600 block mb-2">拍摄城市</text><input v-model.trim="form.cityCode" maxlength="20" placeholder="例如：北京" class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900" /></view>
            <view><text class="text-xs font-bold text-zinc-600 block mb-2">具体地点</text><input v-model.trim="form.locationName" maxlength="160" placeholder="例如：三里屯" class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900" /></view>
          </view>

          <view><text class="text-xs font-bold text-zinc-600 block mb-2">预计时长</text><picker :range="durationOptions" range-key="label" @change="form.durationMinutes = durationOptions[Number($event.detail.value)].value"><view class="h-11 rounded-2xl bg-zinc-50 px-4 flex items-center justify-between"><text class="text-sm text-zinc-800">{{ durationLabel }}</text><view class="i-lucide-chevron-down text-zinc-400"></view></view></picker></view>
        </view>

        <view class="yp-card p-4">
          <text class="text-sm font-black text-zinc-800 block mb-3">合作预算</text>
          <view class="flex flex-wrap gap-2"><view v-for="item in budgetOptions" :key="item.value" class="yp-chip" :class="form.budgetType === item.value ? 'yp-chip-active' : ''" @click="selectBudget(item.value)">{{ item.label }}</view></view>
          <view v-if="['fixed', 'range'].includes(form.budgetType)" class="mt-4 flex items-center space-x-3">
            <view class="flex-1 h-11 rounded-2xl bg-zinc-50 px-4 flex items-center"><text class="text-sm text-zinc-500 mr-2">¥</text><input v-model="form.budgetMin" type="digit" :placeholder="form.budgetType === 'range' ? '最低预算' : '预算金额'" class="flex-1 text-sm text-zinc-900" /></view>
            <view v-if="form.budgetType === 'range'" class="flex-1 h-11 rounded-2xl bg-zinc-50 px-4 flex items-center"><text class="text-sm text-zinc-500 mr-2">¥</text><input v-model="form.budgetMax" type="digit" placeholder="最高预算" class="flex-1 text-sm text-zinc-900" /></view>
          </view>
        </view>

        <view class="yp-card p-4 space-y-4">
          <view class="grid grid-cols-2 gap-3">
            <picker mode="date" :value="form.deadlineDate" @change="form.deadlineDate = $event.detail.value"><view class="rounded-2xl bg-zinc-50 p-3"><text class="text-[10px] text-zinc-400 block">报名截止日期</text><text class="text-xs font-bold text-zinc-800 block mt-2">{{ form.deadlineDate }}</text></view></picker>
            <picker mode="time" :value="form.deadlineTime" @change="form.deadlineTime = $event.detail.value"><view class="rounded-2xl bg-zinc-50 p-3"><text class="text-[10px] text-zinc-400 block">截止时间</text><text class="text-xs font-bold text-zinc-800 block mt-2">{{ form.deadlineTime }}</text></view></picker>
          </view>
          <view><text class="text-xs font-bold text-zinc-600 block mb-2">报名人数上限</text><input v-model="form.applicantLimit" type="number" maxlength="3" class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900" /></view>
        </view>

        <view class="rounded-2xl bg-amber-50 p-4 flex items-start"><view class="i-lucide-info text-amber-600 text-base mt-0.5 mr-3"></view><text class="text-[10px] text-amber-700 leading-relaxed">本地草稿只用于断点恢复。创建、审核和公开状态以服务端数据为准。</text></view>
      </view>
    </scroll-view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 border-t border-black/5 px-5 pt-3 pb-6">
      <view class="h-12 rounded-2xl flex items-center justify-center text-sm font-black" :class="submitting ? 'bg-zinc-200 text-zinc-400' : 'bg-zinc-900 text-white'" @click="publish">{{ submitting ? '正在提交…' : '创建并提交审核' }}</view>
    </view>
  </view>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";
import { onLoad, onUnload } from "@dcloudio/uni-app";
import { createDemand, submitDemand } from "@/api/yuepai/core";

const DRAFT_KEY = "yuepai_demand_draft_v2";
const statusBarH = ref(44);
const submitting = ref(false);
const types = ["人像", "婚纱", "古风", "街拍", "旅拍", "商业", "亲子", "宠物"];
const roleOptions = ["摄影师", "模特", "化妆师", "造型师", "场地", "摄像师"];
const budgetOptions = [{ label: "固定预算", value: "fixed" }, { label: "预算区间", value: "range" }, { label: "面议", value: "negotiable" }, { label: "互勉", value: "mutual" }, { label: "免费", value: "free" }];
const durationOptions = [{ label: "1 小时", value: 60 }, { label: "2 小时", value: 120 }, { label: "3 小时", value: 180 }, { label: "半天", value: 240 }, { label: "全天", value: 480 }];

const defaults = buildDefaults();
const form = reactive({ ...defaults });
const durationLabel = computed(() => durationOptions.find((item) => item.value === Number(form.durationMinutes))?.label || "2 小时");

onLoad(() => {
  try { statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44; } catch (error) { console.warn("获取设备信息失败", error); }
  try { const draft = uni.getStorageSync(DRAFT_KEY); if (draft) Object.assign(form, defaults, draft); } catch (error) { console.warn("恢复草稿失败", error); }
});

const stopWatch = watch(form, () => {
  try { uni.setStorageSync(DRAFT_KEY, { ...form }); } catch (error) { console.warn("保存草稿失败", error); }
}, { deep: true });

onUnload(() => stopWatch());

function buildDefaults() {
  const shoot = new Date(Date.now() + 7 * 86400000);
  const deadline = new Date(Date.now() + 5 * 86400000);
  return { demandType: "人像", title: "", description: "", roles: ["摄影师"], cityCode: "", locationName: "", shootDate: formatDay(shoot), shootTime: "14:00", durationMinutes: 120, budgetType: "fixed", budgetMin: "500", budgetMax: "", applicantLimit: "20", deadlineDate: formatDay(deadline), deadlineTime: "20:00" };
}

function formatDay(date) { const year = date.getFullYear(); const month = String(date.getMonth() + 1).padStart(2, "0"); const day = String(date.getDate()).padStart(2, "0"); return `${year}-${month}-${day}`; }
function toggleRole(role) { const index = form.roles.indexOf(role); if (index >= 0) { if (form.roles.length === 1) return uni.showToast({ title: "至少选择一个角色", icon: "none" }); form.roles.splice(index, 1); } else form.roles.push(role); }
function selectBudget(value) { form.budgetType = value; if (!["fixed", "range"].includes(value)) { form.budgetMin = ""; form.budgetMax = ""; } }

function validate() {
  if (form.title.trim().length < 4) return "标题至少填写 4 个字";
  if (form.description.trim().length < 20) return "详细说明至少填写 20 个字";
  if (!form.cityCode.trim()) return "请填写拍摄城市";
  if (!form.roles.length) return "至少选择一个招募角色";
  const shootAt = new Date(`${form.shootDate}T${form.shootTime}:00`);
  const deadline = new Date(`${form.deadlineDate}T${form.deadlineTime}:00`);
  if (shootAt <= new Date()) return "拍摄时间必须晚于当前时间";
  if (deadline >= shootAt) return "报名截止时间必须早于拍摄时间";
  if (form.budgetType === "fixed" && Number(form.budgetMin) <= 0) return "请填写有效预算";
  if (form.budgetType === "range" && (Number(form.budgetMin) < 0 || Number(form.budgetMax) < Number(form.budgetMin))) return "请填写正确预算区间";
  const limit = Number(form.applicantLimit);
  if (!Number.isInteger(limit) || limit < 1 || limit > 200) return "报名人数应为 1 到 200";
  return "";
}

async function publish() {
  if (submitting.value) return;
  const message = validate();
  if (message) return uni.showToast({ title: message, icon: "none" });
  submitting.value = true;
  try {
    const created = await createDemand({ demandType: form.demandType, title: form.title.trim(), description: form.description.trim(), roles: [...form.roles], cityCode: form.cityCode.trim(), locationName: form.locationName.trim() || null, shootAt: new Date(`${form.shootDate}T${form.shootTime}:00`).toISOString(), durationMinutes: Number(form.durationMinutes), budgetType: form.budgetType, budgetMin: form.budgetMin === "" ? null : Number(form.budgetMin), budgetMax: form.budgetMax === "" ? null : Number(form.budgetMax), applicantLimit: Number(form.applicantLimit), applicationDeadline: new Date(`${form.deadlineDate}T${form.deadlineTime}:00`).toISOString(), referenceAssets: [] });
    const demand = created.data || created;
    await submitDemand(demand.demandId);
    uni.removeStorageSync(DRAFT_KEY);
    Object.assign(form, buildDefaults());
    uni.showModal({ title: "提交成功", content: "需求已进入平台审核，审核通过后会在需求大厅公开。", showCancel: false, success() { uni.switchTab({ url: "/pages/mine/index" }); } });
  } finally { submitting.value = false; }
}
</script>
