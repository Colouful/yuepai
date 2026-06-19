<template>
  <view class="yp-page pb-24">
    <view class="relative h-64" :style="{ background: profile.cover }">
      <view class="absolute inset-0" style="background:linear-gradient(180deg,rgba(0,0,0,.08),rgba(0,0,0,.72))"></view>
      <view :style="{ height: statusBarH + 'px' }"></view>
      <view class="relative z-10 px-5 pt-3 flex items-center justify-between">
        <view class="size-10 rounded-full bg-black/25 backdrop-blur-sm flex items-center justify-center" @click="goBack">
          <view class="i-lucide-arrow-left text-white text-lg"></view>
        </view>
        <view class="flex items-center space-x-2">
          <view class="size-10 rounded-full bg-black/25 backdrop-blur-sm flex items-center justify-center" @click="shareProfile">
            <view class="i-lucide-share-2 text-white text-lg"></view>
          </view>
          <view class="size-10 rounded-full bg-black/25 backdrop-blur-sm flex items-center justify-center" @click="toggleFavorite">
            <view class="i-lucide-heart text-lg" :class="favorite ? 'text-rose-400' : 'text-white'"></view>
          </view>
        </view>
      </view>

      <view class="absolute left-5 right-5 bottom-5 flex items-end">
        <view class="size-20 rounded-3xl bg-white/15 border border-white/25 backdrop-blur-sm flex items-center justify-center text-3xl font-black text-white">{{ profile.name[0] }}</view>
        <view class="flex-1 ml-4 min-w-0 pb-1">
          <view class="flex items-center">
            <text class="text-2xl font-black text-white truncate">{{ profile.name }}</text>
            <view class="i-lucide-badge-check text-rose-300 text-lg ml-1"></view>
          </view>
          <text class="text-xs text-white/65 block mt-1">{{ profile.style }} · {{ profile.city }} · 从业 {{ profile.experience }} 年</text>
          <view class="flex items-center space-x-3 mt-2">
            <text class="text-[10px] text-white/60">{{ profile.orders }} 单</text>
            <view class="flex items-center"><view class="i-lucide-star text-amber-300 text-[10px]"></view><text class="text-[10px] text-white ml-1">{{ profile.rating }}</text></view>
            <text class="text-[10px] text-white/60">回复率 {{ profile.responseRate }}%</text>
          </view>
        </view>
      </view>
    </view>

    <view class="px-5 -mt-1 pb-5 space-y-5">
      <view class="yp-card p-4 grid grid-cols-4">
        <view v-for="item in stats" :key="item.label" class="text-center">
          <text class="text-base font-black text-zinc-900 block">{{ item.value }}</text>
          <text class="text-[10px] text-zinc-400 block mt-1">{{ item.label }}</text>
        </view>
      </view>

      <view class="flex flex-wrap gap-2">
        <view v-for="tag in profile.tags" :key="tag" class="yp-chip">{{ tag }}</view>
      </view>

      <view class="yp-card p-4">
        <view class="flex items-center justify-between mb-3">
          <text class="yp-section-title">关于我</text>
          <text class="text-[10px] text-emerald-600">{{ profile.available ? '本周可约' : '下周可约' }}</text>
        </view>
        <text class="text-xs text-zinc-500 leading-relaxed">{{ profile.intro }}</text>
        <view class="mt-4 flex items-center space-x-4 text-[10px] text-zinc-400">
          <view class="flex items-center"><view class="i-lucide-map-pin text-rose-500 mr-1"></view>{{ profile.serviceArea }}</view>
          <view class="flex items-center"><view class="i-lucide-clock-3 text-rose-500 mr-1"></view>{{ profile.responseTime }}</view>
        </view>
      </view>

      <view>
        <view class="flex items-end justify-between mb-3">
          <view><text class="yp-section-title block">代表作品</text><text class="text-[10px] text-zinc-400 block mt-1">真实客片与个人创作</text></view>
          <text class="text-xs font-bold text-rose-500" @click="openWorks">全部作品</text>
        </view>
        <view class="grid grid-cols-3 gap-2">
          <view v-for="(work, index) in works" :key="index" class="relative h-32 rounded-2xl overflow-hidden" :style="{ background: work.cover }" @click="previewWork(index)">
            <view class="absolute inset-0" style="background:linear-gradient(180deg,transparent,rgba(0,0,0,.38))"></view>
            <text class="absolute left-2 bottom-2 text-[9px] text-white">{{ work.label }}</text>
          </view>
        </view>
      </view>

      <view>
        <view class="flex items-end justify-between mb-3">
          <view><text class="yp-section-title block">服务套餐</text><text class="text-[10px] text-zinc-400 block mt-1">价格透明，确认后锁定档期</text></view>
          <text class="text-xs text-zinc-400">{{ packages.length }} 个套餐</text>
        </view>
        <view class="space-y-3">
          <view v-for="item in packages" :key="item.id" class="yp-card p-4" :class="selectedPackageId === item.id ? 'ring-1 ring-zinc-900' : ''" @click="selectedPackageId = item.id">
            <view class="flex items-start justify-between">
              <view class="flex-1 min-w-0">
                <view class="flex items-center"><text class="text-sm font-black text-zinc-900">{{ item.name }}</text><view v-if="item.recommended" class="ml-2 rounded-full bg-rose-50 px-2 py-1 text-[9px] font-bold text-rose-500">推荐</view></view>
                <text class="text-xs text-zinc-500 block mt-2 leading-relaxed">{{ item.description }}</text>
              </view>
              <view class="ml-3 text-right"><text class="text-lg font-black text-zinc-900">¥{{ item.price }}</text><text class="text-[9px] text-zinc-400 block">起</text></view>
            </view>
            <view class="mt-3 flex items-center justify-between">
              <view class="flex items-center space-x-3 text-[10px] text-zinc-400"><text>{{ item.duration }}</text><text>{{ item.photos }}</text><text>{{ item.delivery }}</text></view>
              <view class="size-5 rounded-full border flex items-center justify-center" :class="selectedPackageId === item.id ? 'border-zinc-900 bg-zinc-900' : 'border-zinc-300'">
                <view v-if="selectedPackageId === item.id" class="i-lucide-check text-white text-[10px]"></view>
              </view>
            </view>
          </view>
        </view>
      </view>

      <view>
        <view class="flex items-end justify-between mb-3">
          <view><text class="yp-section-title block">用户评价</text><text class="text-[10px] text-zinc-400 block mt-1">近 90 天好评率 98%</text></view>
          <text class="text-xs font-bold text-rose-500">查看全部</text>
        </view>
        <view class="space-y-3">
          <view v-for="item in reviews" :key="item.name" class="yp-card p-4">
            <view class="flex items-center">
              <view class="size-9 rounded-full flex items-center justify-center text-white text-xs font-black" :style="{ background: item.avatar }">{{ item.name[0] }}</view>
              <view class="flex-1 ml-2"><text class="text-xs font-black text-zinc-800 block">{{ item.name }}</text><text class="text-[9px] text-zinc-400 block mt-0.5">{{ item.packageName }} · {{ item.date }}</text></view>
              <view class="flex"><view v-for="index in 5" :key="index" class="i-lucide-star text-[10px] text-amber-400"></view></view>
            </view>
            <text class="text-xs text-zinc-500 leading-relaxed block mt-3">{{ item.content }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3">
      <view class="size-12 rounded-2xl bg-zinc-100 flex flex-col items-center justify-center" @click="openChat">
        <view class="i-lucide-message-circle text-zinc-800 text-lg"></view><text class="text-[9px] text-zinc-500 mt-0.5">咨询</text>
      </view>
      <view class="flex-1 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="bookNow">
        预约 {{ selectedPackage ? `¥${selectedPackage.price}` : '' }}
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const favorite = ref(false);
const selectedPackageId = ref(2);
const profileId = ref("1");

try {
  statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

onLoad((options) => {
  profileId.value = options?.id || "1";
});

const profile = ref({
  name: "林默",
  style: "人像摄影",
  city: "北京",
  experience: 5,
  orders: 326,
  rating: 4.9,
  responseRate: 98,
  available: true,
  tags: ["日系清新", "情绪写真", "自然光", "婚纱", "旅拍"],
  serviceArea: "北京五环内可约",
  responseTime: "平均 10 分钟回复",
  intro: "专注人像摄影五年，擅长在自然光与真实互动中捕捉松弛、细腻的情绪。拍摄前会共同完成风格策划、服装建议和场地选择，让没有镜头经验的人也能自然进入状态。",
  cover: "linear-gradient(145deg,#18181b 0%,#9f1239 55%,#fb7185 100%)",
});

const stats = [
  { value: "326", label: "完成订单" },
  { value: "4.9", label: "综合评分" },
  { value: "128", label: "真实评价" },
  { value: "3.6k", label: "作品获赞" },
];

const works = [
  { label: "自然光人像", cover: "linear-gradient(145deg,#fecdd3,#fb7185 55%,#881337)" },
  { label: "城市夜景", cover: "linear-gradient(145deg,#c4b5fd,#6d28d9 55%,#18181b)" },
  { label: "胶片日常", cover: "linear-gradient(145deg,#fde68a,#d97706 55%,#292524)" },
  { label: "海边旅拍", cover: "linear-gradient(145deg,#bae6fd,#0284c7 55%,#082f49)" },
  { label: "婚纱纪实", cover: "linear-gradient(145deg,#f4f4f5,#a1a1aa 55%,#18181b)" },
  { label: "东方古风", cover: "linear-gradient(145deg,#d1fae5,#10b981 55%,#022c22)" },
];

const packages = [
  { id: 1, name: "轻写真体验", price: 500, description: "适合首次约拍，单场景自然光拍摄，不含妆造。", duration: "1 小时", photos: "10 张精修", delivery: "5 天交付", recommended: false },
  { id: 2, name: "精致人像写真", price: 1200, description: "两套造型、两个场景，包含基础妆造与拍摄策划。", duration: "3 小时", photos: "30 张精修", delivery: "3 天交付", recommended: true },
  { id: 3, name: "全天城市旅拍", price: 3000, description: "全天跟拍与路线规划，不限服装，包含妆造和交通协调。", duration: "8 小时", photos: "80 张精修", delivery: "7 天交付", recommended: false },
];

const selectedPackage = computed(() => packages.find((item) => item.id === selectedPackageId.value));
const reviews = [
  { name: "小雨", packageName: "精致人像写真", date: "6 月 12 日", content: "拍摄前沟通非常细致，完全不用担心不会摆动作，成片比预期更自然。", avatar: "linear-gradient(135deg,#fb7185,#be123c)" },
  { name: "苏晴", packageName: "全天城市旅拍", date: "5 月 28 日", content: "第三次合作了，审美稳定、交付及时，现场也很会调动情绪。", avatar: "linear-gradient(135deg,#a78bfa,#5b21b6)" },
];

function toggleFavorite() {
  favorite.value = !favorite.value;
  uni.showToast({ title: favorite.value ? "已收藏摄影师" : "已取消收藏", icon: "none" });
}

function openChat() {
  proxy.$tab.navigateTo(`/pages/chat/index?id=${profileId.value}&name=${encodeURIComponent(profile.value.name)}`);
}

function bookNow() {
  if (!selectedPackage.value) {
    uni.showToast({ title: "请先选择服务套餐", icon: "none" });
    return;
  }
  proxy.$tab.navigateTo(`/pages/order/confirm?creatorId=${profileId.value}&packageId=${selectedPackage.value.id}`);
}

function previewWork(index) {
  uni.showToast({ title: `查看第 ${index + 1} 组作品`, icon: "none" });
}

function openWorks() {
  proxy.$tab.switchTab("/pages/works/index");
}

function shareProfile() {
  uni.showToast({ title: "分享面板正在接入", icon: "none" });
}

function goBack() {
  proxy.$tab.navigateBack();
}
</script>
