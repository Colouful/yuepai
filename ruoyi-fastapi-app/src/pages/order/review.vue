<template>
  <view class="yp-page pb-24">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between"><view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view><text class="text-base font-black text-zinc-900">评价服务</text><view class="w-10"></view></view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-4">
        <view class="yp-card p-4"><view class="flex items-center"><view class="size-14 rounded-2xl flex items-center justify-center text-white font-black" style="background:linear-gradient(135deg,#fb7185,#be123c)">林</view><view class="flex-1 ml-3"><text class="text-sm font-black text-zinc-900 block">精致人像写真</text><text class="text-[10px] text-zinc-400 block mt-1">摄影师：林默 · 6 月 20 日</text></view><view class="rounded-full bg-emerald-50 px-3 py-1.5 text-[10px] font-bold text-emerald-600">已完成</view></view></view>

        <view class="yp-card p-4">
          <view class="text-center pb-4"><text class="yp-section-title block">这次拍摄体验怎么样？</text><text class="text-xs text-zinc-400 block mt-2">你的评价会帮助其他用户做出选择</text><view class="mt-4 flex items-center justify-center space-x-2"><view v-for="index in 5" :key="index" class="i-lucide-star text-3xl" :class="index <= overallScore ? 'text-amber-400' : 'text-zinc-200'" @click="setOverallScore(index)"></view></view><text class="text-xs font-bold text-zinc-600 block mt-2">{{ scoreText }}</text></view>
          <view class="pt-4 border-t border-black/5 space-y-4"><view v-for="item in dimensions" :key="item.name" class="flex items-center justify-between"><text class="text-xs text-zinc-500">{{ item.name }}</text><view class="flex space-x-1"><view v-for="index in 5" :key="index" class="i-lucide-star text-lg" :class="index <= item.score ? 'text-amber-400' : 'text-zinc-200'" @click="item.score = index"></view></view></view></div>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-3">选择印象</text>
          <view class="flex flex-wrap gap-2"><view v-for="tag in availableTags" :key="tag" class="yp-chip" :class="selectedTags.includes(tag) ? 'yp-chip-active' : ''" @click="toggleTag(tag)">{{ tag }}</view></view>
        </view>

        <view class="yp-card p-4">
          <view class="flex items-center justify-between mb-3"><text class="yp-section-title">评价内容</text><text class="text-[10px] text-zinc-400">{{ content.length }}/500</text></view>
          <textarea v-model="content" maxlength="500" placeholder="分享拍摄过程、沟通体验和成片感受…" placeholder-class="text-zinc-300" class="h-32 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" />
          <view class="mt-4 flex flex-wrap gap-2.5"><view v-for="(image, index) in images" :key="image" class="relative size-[94px] rounded-2xl overflow-hidden bg-zinc-100"><image :src="image" mode="aspectFill" class="w-full h-full" @click="previewImage(index)" /><view class="absolute right-1.5 top-1.5 size-6 rounded-full bg-black/55 flex items-center justify-center" @click.stop="removeImage(index)"><view class="i-lucide-x text-white text-xs"></view></view></view><view v-if="images.length < 6" class="size-[94px] rounded-2xl border border-dashed border-zinc-300 bg-zinc-50 flex flex-col items-center justify-center" @click="chooseImages"><view class="i-lucide-camera text-xl text-zinc-500"></view><text class="text-[10px] text-zinc-400 mt-1.5">添加照片</text></view></view>
        </view>

        <view class="yp-card px-4 py-3 flex items-center justify-between"><view><text class="text-sm font-black text-zinc-800 block">匿名评价</text><text class="text-[10px] text-zinc-400 block mt-1">开启后不会展示你的昵称和头像</text></view><switch :checked="anonymous" color="#18181b" style="transform:scale(.78)" @change="anonymous = $event.detail.value" /></view>

        <view class="rounded-2xl bg-amber-50 p-4 flex items-start"><view class="i-lucide-gift text-amber-600 text-base mt-0.5 mr-3"></view><view><text class="text-xs font-black text-amber-800 block">评价奖励</text><text class="text-[10px] text-amber-700 leading-relaxed block mt-1">完成真实评价可获得 20 成长值，上传照片额外获得 10 成长值。</text></view></view>
      </view>
    </scroll-view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6"><view class="h-12 rounded-2xl flex items-center justify-center text-sm font-black" :class="submitting ? 'bg-zinc-200 text-zinc-400' : 'bg-zinc-900 text-white'" @click="submitReview">{{ submitting ? '正在提交…' : '提交评价' }}</view></view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const orderId = ref("1"); const overallScore = ref(5); const content = ref(""); const selectedTags = ref([]); const images = ref([]); const anonymous = ref(false); const submitting = ref(false);
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 80; } catch (error) { console.warn("获取设备信息失败", error); }
onLoad((options) => { orderId.value = options?.id || "1"; });
const dimensions = reactive([{ name: "服务态度", score: 5 }, { name: "专业能力", score: 5 }, { name: "成片质量", score: 5 }, { name: "准时程度", score: 5 }, { name: "性价比", score: 5 }]);
const availableTags = ["沟通顺畅", "审美在线", "很会引导", "准时守约", "交付及时", "成片惊艳", "性价比高", "还会再约"];
const scoreText = computed(() => ({ 1: "体验较差", 2: "有待改进", 3: "符合预期", 4: "非常满意", 5: "超出预期" }[overallScore.value]));
function setOverallScore(score) { overallScore.value = score; dimensions.forEach((item) => { item.score = score; }); }
function toggleTag(tag) { const index = selectedTags.value.indexOf(tag); if (index >= 0) selectedTags.value.splice(index, 1); else if (selectedTags.value.length < 6) selectedTags.value.push(tag); else uni.showToast({ title: "最多选择 6 个标签", icon: "none" }); }
function chooseImages() { uni.chooseImage({ count: 6 - images.value.length, sizeType: ["compressed"], sourceType: ["album", "camera"], success(result) { images.value.push(...result.tempFilePaths.slice(0, 6 - images.value.length)); }, fail(error) { if (!String(error.errMsg || "").includes("cancel")) uni.showToast({ title: "选择图片失败", icon: "none" }); } }); }
function previewImage(index) { uni.previewImage({ current: index, urls: images.value }); }
function removeImage(index) { images.value.splice(index, 1); }
function submitReview() { if (submitting.value) return; if (overallScore.value <= 3 && content.value.trim().length < 10) return uni.showToast({ title: "请详细说明需要改进的地方", icon: "none" }); submitting.value = true; const review = { orderId: orderId.value, overallScore: overallScore.value, dimensions: JSON.parse(JSON.stringify(dimensions)), tags: [...selectedTags.value], content: content.value.trim(), images: [...images.value], anonymous: anonymous.value, createdAt: new Date().toISOString() }; setTimeout(() => { try { const reviews = uni.getStorageSync("yuepai_reviews") || []; uni.setStorageSync("yuepai_reviews", [review, ...reviews]); submitting.value = false; uni.showToast({ title: "评价成功", icon: "success" }); setTimeout(() => proxy.$tab.switchTab("/pages/mine/index"), 500); } catch (error) { submitting.value = false; uni.showToast({ title: "评价保存失败", icon: "none" }); } }, 600); }
function goBack() { proxy.$tab.navigateBack(); }
</script>
