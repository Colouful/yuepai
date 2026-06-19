<template>
  <view class="yp-page pb-24">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between"><view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view><text class="text-base font-black text-zinc-900">作品验收</text><view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="showHelp"><view class="i-lucide-circle-help text-zinc-700 text-lg"></view></view></view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-4">
        <view class="yp-card-strong p-5 relative overflow-hidden"><view class="absolute -right-12 -top-12 size-40 rounded-full" style="background:rgba(244,63,94,.25);filter:blur(24px)"></view><view class="relative z-10"><view class="flex items-center justify-between"><view><text class="text-lg font-black text-white block">摄影师已交付作品</text><text class="text-xs text-white/55 block mt-2">请在 72 小时内完成验收</text></view><view class="size-14 rounded-2xl bg-white/10 flex items-center justify-center"><view class="i-lucide-images text-white text-2xl"></view></view></view><view class="mt-5 flex items-center justify-between"><text class="text-[10px] text-white/45">交付时间：6 月 23 日 18:30</text><text class="text-[10px] text-rose-200">剩余 2 天 06:24</text></view></view></view>

        <view class="yp-card p-4"><view class="flex items-center"><view class="size-12 rounded-2xl flex items-center justify-center text-white font-black" style="background:linear-gradient(135deg,#fb7185,#be123c)">林</view><view class="flex-1 ml-3"><text class="text-sm font-black text-zinc-900 block">林默</text><text class="text-[10px] text-zinc-400 block mt-1">精致人像写真 · 订单 YP20260617001</text></view><view class="rounded-full bg-emerald-50 px-3 py-1.5 text-[10px] font-bold text-emerald-600">已交付</view></view></view>

        <view class="yp-card p-4">
          <view class="flex items-center justify-between mb-4"><view><text class="yp-section-title block">精修照片</text><text class="text-[10px] text-zinc-400 block mt-1">30 张 · 已展示 12 张预览</text></view><view class="rounded-full bg-zinc-100 px-3 py-1.5 text-[10px] text-zinc-600" @click="downloadAll"><view class="i-lucide-download inline-block mr-1"></view>下载全部</view></view>
          <view class="grid grid-cols-3 gap-2"><view v-for="(item, index) in photos" :key="item.id" class="relative h-32 rounded-2xl overflow-hidden" :style="{ background: item.cover }" @click="previewPhoto(index)"><view class="absolute inset-0" style="background:linear-gradient(180deg,transparent,rgba(0,0,0,.3))"></view><view class="absolute left-2 bottom-2 rounded-full bg-black/35 px-2 py-1 text-[9px] text-white">{{ index + 1 }}/{{ photos.length }}</view><view v-if="item.selected" class="absolute right-2 top-2 size-6 rounded-full bg-emerald-500 flex items-center justify-center"><view class="i-lucide-check text-white text-xs"></view></view></view></view>
          <view class="mt-4 rounded-2xl bg-zinc-50 p-3 flex items-start"><view class="i-lucide-info text-zinc-500 text-sm mt-0.5 mr-2"></view><text class="text-[10px] text-zinc-500 leading-relaxed">当前为带水印预览。确认验收后可下载无水印高清文件，原片和精修文件将保留 90 天。</text></view>
        </view>

        <view class="yp-card p-4"><text class="yp-section-title block mb-3">摄影师留言</text><text class="text-xs text-zinc-500 leading-relaxed">你好，这组照片已完成整体色调和皮肤细节处理。第 6、9 张额外做了两种色调版本，如需微调可在验收前提交修改意见。</text></view>

        <view class="yp-card p-4"><view class="flex items-center justify-between"><view><text class="text-sm font-black text-zinc-900 block">是否符合约定交付</text><text class="text-[10px] text-zinc-400 block mt-1">30 张精修 · 全部原片 · 3 天内交付</text></view><view class="i-lucide-circle-check-big text-emerald-500 text-2xl"></view></view></view>
      </view>
    </scroll-view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3"><view class="flex-1 h-12 rounded-2xl border border-black/10 flex items-center justify-center text-sm font-bold text-zinc-700" @click="revisionVisible = true">申请修改</view><view class="flex-1 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="acceptDelivery">确认验收</view></view>

    <view v-if="revisionVisible" class="fixed inset-0 z-50 flex items-end" @click="revisionVisible = false"><view class="absolute inset-0 bg-black/35"></view><view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop><view class="flex items-center justify-between"><view><text class="text-lg font-black text-zinc-900 block">申请修改</text><text class="text-[10px] text-zinc-400 block mt-1">请具体说明需要调整的照片和内容</text></view><view class="i-lucide-x text-zinc-500 text-lg" @click="revisionVisible = false"></view></view><view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-2">修改类型</text><view class="flex flex-wrap gap-2"><view v-for="item in revisionTypes" :key="item" class="yp-chip" :class="revision.type === item ? 'yp-chip-active' : ''" @click="revision.type = item">{{ item }}</view></view></view><view class="mt-5"><view class="flex items-center justify-between mb-2"><text class="text-sm font-black text-zinc-800">修改说明</text><text class="text-[10px] text-zinc-400">{{ revision.message.length }}/300</text></view><textarea v-model="revision.message" maxlength="300" placeholder="例如：第 6 张希望降低磨皮强度并调整为暖色调" placeholder-class="text-zinc-300" class="h-28 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" /></view><view class="mt-6 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="submitRevision">提交修改申请</view></view></view>
  </view>
</template>

<script setup>
import { getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const orderId = ref("1"); const revisionVisible = ref(false);
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 80; } catch (error) { console.warn("获取设备信息失败", error); }
onLoad((options) => { orderId.value = options?.id || "1"; });
const colors = ["#fecdd3,#fb7185,#881337", "#bae6fd,#0284c7,#082f49", "#fde68a,#d97706,#292524", "#d1fae5,#10b981,#022c22", "#ddd6fe,#8b5cf6,#3b0764", "#f4f4f5,#a1a1aa,#18181b"];
const photos = reactive(Array.from({ length: 12 }, (_, index) => ({ id: index + 1, selected: true, cover: `linear-gradient(145deg,${colors[index % colors.length]})` })));
const revisionTypes = ["色调调整", "皮肤处理", "构图裁剪", "瑕疵修复", "其他"];
const revision = reactive({ type: "色调调整", message: "" });
function previewPhoto(index) { photos[index].selected = !photos[index].selected; uni.showToast({ title: photos[index].selected ? "已标记满意" : "已取消标记", icon: "none" }); }
function downloadAll() { uni.showToast({ title: "确认验收后可下载高清文件", icon: "none" }); }
function submitRevision() { if (revision.message.trim().length < 10) return uni.showToast({ title: "请详细填写修改意见", icon: "none" }); uni.setStorageSync(`yuepai_revision_${orderId.value}`, { ...revision, createdAt: Date.now() }); revisionVisible.value = false; uni.showToast({ title: "修改申请已提交", icon: "success" }); }
function acceptDelivery() { uni.showModal({ title: "确认验收作品", content: "确认后平台将向摄影师结算服务款，且订单进入待评价状态。", confirmText: "确认验收", success(result) { if (!result.confirm) return; uni.setStorageSync(`yuepai_delivery_accepted_${orderId.value}`, true); uni.showToast({ title: "验收成功", icon: "success" }); setTimeout(() => proxy.$tab.navigateTo(`/pages/order/review?id=${orderId.value}`), 500); } }); }
function showHelp() { uni.showModal({ title: "验收说明", content: "发现交付数量、质量或内容与约定不符时，可先申请修改；协商无果可在订单详情发起售后。", showCancel: false }); }
function goBack() { proxy.$tab.navigateBack(); }
</script>
