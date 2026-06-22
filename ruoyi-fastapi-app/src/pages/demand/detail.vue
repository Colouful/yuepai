<template>
  <view class="yp-page pb-24">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between">
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view>
      <text class="text-base font-black text-zinc-900">需求详情</text>
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="toggleFavorite"><view class="i-lucide-heart text-lg" :class="favorite ? 'text-rose-500' : 'text-zinc-700'"></view></view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-4">
        <view class="yp-card-strong p-5 relative overflow-hidden">
          <view class="absolute -right-12 -top-12 size-40 rounded-full" style="background:rgba(244,63,94,.24);filter:blur(24px)"></view>
          <view class="relative z-10">
            <view class="flex items-center justify-between">
              <view class="rounded-full px-3 py-1.5 text-[10px] font-bold" :class="demand.mutual ? 'bg-emerald-500/20 text-emerald-200' : 'bg-rose-500/20 text-rose-200'">{{ demand.mutual ? '互勉创作' : '付费约拍' }}</view>
              <text class="text-[10px] text-white/45">{{ demand.deadline }}</text>
            </view>
            <text class="text-2xl font-black text-white block mt-4 leading-tight">{{ demand.title }}</text>
            <text class="text-xs text-white/55 block mt-3">{{ demand.summary }}</text>
            <view class="mt-5 flex items-end justify-between">
              <view class="flex items-center space-x-3 text-[10px] text-white/55"><text>{{ demand.city }}</text><text>{{ demand.date }}</text><text>{{ demand.duration }}</text></view>
              <text class="text-2xl font-black" :class="demand.mutual ? 'text-emerald-300' : 'text-rose-300'">{{ demand.budget }}</text>
            </view>
          </view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-4">招募信息</text>
          <view class="grid grid-cols-2 gap-3">
            <view v-for="item in infoItems" :key="item.label" class="rounded-2xl bg-zinc-50 p-3">
              <view class="flex items-center"><view :class="item.icon" class="text-sm text-rose-500 mr-2"></view><text class="text-[10px] text-zinc-400">{{ item.label }}</text></view>
              <text class="text-xs font-bold text-zinc-800 block mt-2">{{ item.value }}</text>
            </view>
          </view>
          <view class="mt-4 flex flex-wrap gap-2"><view v-for="role in demand.roles" :key="role" class="yp-chip yp-chip-active">招募 {{ role }}</view><view v-for="tag in demand.tags" :key="tag" class="yp-chip">#{{ tag }}</view></view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-3">详细说明</text>
          <text class="text-xs text-zinc-500 leading-relaxed">{{ demand.description }}</text>
          <view class="mt-4 rounded-2xl bg-amber-50 p-3 flex items-start"><view class="i-lucide-lightbulb text-amber-500 text-sm mt-0.5 mr-2"></view><text class="text-[10px] text-amber-700 leading-relaxed">报名时请附上与你擅长风格相关的作品链接，能显著提高被选中的机会。</text></view>
        </view>

        <view>
          <view class="flex items-end justify-between mb-3"><view><text class="yp-section-title block">参考风格</text><text class="text-[10px] text-zinc-400 block mt-1">发布者期望的画面方向</text></view><text class="text-xs text-zinc-400">3 张</text></view>
          <view class="grid grid-cols-3 gap-2"><view v-for="(item, index) in references" :key="index" class="h-28 rounded-2xl overflow-hidden" :style="{ background: item }" @click="previewReference(index)"></view></view>
        </view>

        <view class="yp-card p-4" @click="openPublisher">
          <view class="flex items-center justify-between mb-3"><text class="yp-section-title">发布者</text><text class="text-[10px] text-emerald-600">信用良好</text></view>
          <view class="flex items-center">
            <view class="size-12 rounded-2xl flex items-center justify-center text-white font-black" :style="{ background: demand.avatar }">{{ demand.user[0] }}</view>
            <view class="flex-1 ml-3"><view class="flex items-center"><text class="text-sm font-black text-zinc-900">{{ demand.user }}</text><view class="i-lucide-badge-check text-rose-500 text-xs ml-1"></view></view><text class="text-[10px] text-zinc-400 block mt-1">实名认证 · 已发布 {{ demand.publishCount }} 次 · 回复率 {{ demand.responseRate }}%</text></view>
            <view class="i-lucide-chevron-right text-zinc-300 text-sm"></view>
          </view>
        </view>

        <view class="yp-card p-4">
          <view class="flex items-center justify-between"><text class="yp-section-title">报名情况</text><text class="text-xs text-zinc-400">{{ demand.applicants }} 人已报名</text></view>
          <view class="mt-4 flex items-center">
            <view v-for="(item, index) in applicantAvatars" :key="index" class="size-9 rounded-full border-2 border-white flex items-center justify-center text-white text-[10px] font-black" :style="{ background: item, marginLeft: index ? '-8px' : '0' }">{{ applicantNames[index][0] }}</view>
            <text class="text-[10px] text-zinc-400 ml-3">发布者通常在 24 小时内回复</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3">
      <view class="size-12 rounded-2xl bg-zinc-100 flex flex-col items-center justify-center" @click="openChat"><view class="i-lucide-message-circle text-zinc-800 text-lg"></view><text class="text-[9px] text-zinc-500">咨询</text></view>
      <view class="flex-1 h-12 rounded-2xl flex items-center justify-center text-sm font-black" :class="applied ? 'bg-emerald-50 text-emerald-600' : 'bg-zinc-900 text-white'" @click="openApply">{{ applied ? '已报名，等待确认' : '立即报名' }}</view>
    </view>

    <view v-if="applyVisible" class="fixed inset-0 z-50 flex items-end" @click="applyVisible = false">
      <view class="absolute inset-0 bg-black/35"></view>
      <view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop>
        <view class="flex items-center justify-between"><view><text class="text-lg font-black text-zinc-900 block">报名约拍</text><text class="text-[10px] text-zinc-400 block mt-1">清楚介绍自己和合作方案</text></view><view class="i-lucide-x text-zinc-500 text-lg" @click="applyVisible = false"></view></view>
        <view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-2">报名身份</text><view class="flex flex-wrap gap-2"><view v-for="role in demand.roles" :key="role" class="yp-chip" :class="application.role === role ? 'yp-chip-active' : ''" @click="application.role = role">{{ role }}</view></view></view>
        <view class="mt-5"><view class="flex items-center justify-between mb-2"><text class="text-sm font-black text-zinc-800">自我介绍</text><text class="text-[10px] text-zinc-400">{{ application.message.length }}/200</text></view><textarea v-model="application.message" maxlength="200" placeholder="介绍经验、擅长风格和本次合作想法" placeholder-class="text-zinc-300" class="h-28 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" /></view>
        <view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-2">报价</text><view class="h-11 rounded-2xl bg-zinc-50 px-4 flex items-center"><text class="text-sm text-zinc-500 mr-2">¥</text><input v-model="application.price" type="digit" placeholder="填写报价，互勉可填 0" placeholder-class="text-zinc-300" class="flex-1 text-sm text-zinc-900" /></view></view>
        <view class="mt-6 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="submitApplication">提交报名</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const demandId = ref("1"); const favorite = ref(false); const applied = ref(false); const applyVisible = ref(false);
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 80; } catch (error) { console.warn("获取设备信息失败", error); }
onLoad((options) => { demandId.value = options?.id || "1"; });
const demand = reactive({ title: "周末三里屯情绪人像", summary: "寻找擅长日系清新风格的摄影师与化妆师", city: "北京朝阳", date: "6 月 20 日 14:00", duration: "3 小时", deadline: "明天 20:00 截止", budget: "¥500", mutual: false, roles: ["摄影师", "化妆师"], tags: ["日系", "自然光", "城市人像"], description: "计划在三里屯附近拍摄一组轻松自然的个人写真。希望摄影师能够协助完成场地选择和动作引导，整体风格偏日系清新与城市生活感。需要交付至少 10 张精修照片，期望 5 天内完成交付。", user: "小雨", publishCount: 3, responseRate: 96, applicants: 12, avatar: "linear-gradient(135deg,#fb7185,#be123c)" });
const infoItems = [{ label: "拍摄地点", value: "三里屯及周边", icon: "i-lucide-map-pin" }, { label: "拍摄时间", value: "14:00 - 17:00", icon: "i-lucide-calendar-days" }, { label: "交付要求", value: "10 张精修", icon: "i-lucide-images" }, { label: "报名人数", value: "12 / 20 人", icon: "i-lucide-users" }];
const references = ["linear-gradient(145deg,#fecdd3,#fb7185 55%,#881337)", "linear-gradient(145deg,#bae6fd,#0284c7 55%,#082f49)", "linear-gradient(145deg,#fde68a,#d97706 55%,#292524)"];
const applicantNames = ["林默", "陈风", "木子", "苏晴"]; const applicantAvatars = ["linear-gradient(135deg,#fb7185,#be123c)", "linear-gradient(135deg,#38bdf8,#0369a1)", "linear-gradient(135deg,#fbbf24,#b45309)", "linear-gradient(135deg,#a78bfa,#5b21b6)"];
const application = reactive({ role: "摄影师", message: "", price: "500" });
function toggleFavorite() { favorite.value = !favorite.value; uni.showToast({ title: favorite.value ? "已收藏需求" : "已取消收藏", icon: "none" }); }
function openApply() { if (applied.value) { uni.showToast({ title: "报名信息已提交", icon: "none" }); return; } applyVisible.value = true; }
function submitApplication() { if (!application.role) return uni.showToast({ title: "请选择报名身份", icon: "none" }); if (application.message.trim().length < 10) return uni.showToast({ title: "请至少填写 10 个字的介绍", icon: "none" }); if (application.price === "") return uni.showToast({ title: "请填写报价", icon: "none" }); applied.value = true; applyVisible.value = false; uni.setStorageSync(`yuepai_demand_application_${demandId.value}`, { ...application, createdAt: Date.now() }); uni.showToast({ title: "报名成功", icon: "success" }); }
function previewReference(index) { uni.showToast({ title: `查看参考图 ${index + 1}`, icon: "none" }); }
function openChat() { proxy.$tab.navigateTo(`/pages/chat/index?id=${demandId.value}&name=${encodeURIComponent(demand.user)}`); }
function openPublisher() { proxy.$tab.navigateTo(`/pages/profile/index?id=${demandId.value}`); }
function goBack() { proxy.$tab.navigateBack(); }
</script>
