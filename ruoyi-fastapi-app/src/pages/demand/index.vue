<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3">
      <view class="flex items-end justify-between">
        <view><text class="yp-eyebrow block">OPPORTUNITIES</text><text class="yp-title block mt-1">需求大厅</text></view>
        <view class="rounded-full bg-zinc-900 px-4 py-2.5 flex items-center" @click="openPublish"><view class="i-lucide-plus text-white text-sm mr-1"></view><text class="text-xs font-bold text-white">发布约拍</text></view>
      </view>
      <view class="mt-4 flex items-center space-x-2">
        <view class="flex-1 h-11 rounded-2xl bg-white border border-black/5 px-4 flex items-center"><view class="i-lucide-search text-zinc-400 text-sm mr-2"></view><input v-model="keyword" placeholder="搜索主题、城市或角色" placeholder-class="text-zinc-300" class="flex-1 text-sm text-zinc-900" /></view>
        <view class="size-11 rounded-2xl bg-white border border-black/5 flex items-center justify-center" @click="filterVisible = true"><view class="i-lucide-sliders-horizontal text-zinc-700 text-base"></view></view>
      </view>
      <scroll-view scroll-x class="mt-4 whitespace-nowrap" :show-scrollbar="false"><view class="inline-flex space-x-2 pr-5"><view v-for="item in categories" :key="item" class="yp-chip" :class="activeCategory === item ? 'yp-chip-active' : ''" @click="activeCategory = item">{{ item }}</view></view></scroll-view>
      <view class="mt-3 flex items-center justify-between"><text class="text-xs text-zinc-400">{{ filteredDemands.length }} 个招募正在进行</text><picker :range="sortLabels" @change="sortIndex = Number($event.detail.value)"><view class="flex items-center"><text class="text-xs font-bold text-zinc-700">{{ sortLabels[sortIndex] }}</text><view class="i-lucide-chevron-down text-zinc-400 text-xs ml-1"></view></view></picker></view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-3">
        <view v-for="item in filteredDemands" :key="item.id" class="yp-card p-4" @click="openDetail(item)">
          <view class="flex items-start">
            <view class="size-12 rounded-2xl flex items-center justify-center shrink-0" :style="{ background: item.iconBg }"><view :class="item.icon" class="text-xl" :style="{ color: item.iconColor }"></view></view>
            <view class="flex-1 min-w-0 ml-3">
              <view class="flex items-start justify-between">
                <view class="flex-1 min-w-0"><view class="flex items-center"><view class="rounded-full px-2 py-1 text-[9px] font-bold" :class="item.mutual ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-500'">{{ item.mutual ? '互勉' : '付费' }}</view><text class="text-sm font-black text-zinc-900 ml-2 truncate">{{ item.title }}</text></view><text class="text-[10px] text-zinc-400 block mt-2">{{ item.city }} · {{ item.date }} · {{ item.duration }}</text></view>
                <view class="ml-3 text-right"><text class="text-base font-black" :class="item.mutual ? 'text-emerald-600' : 'text-rose-500'">{{ item.budget }}</text><text class="text-[9px] text-zinc-300 block">{{ item.deadline }}</text></view>
              </view>
              <text class="text-xs text-zinc-500 leading-relaxed block mt-3">{{ item.description }}</text>
              <view class="mt-3 flex flex-wrap gap-1.5"><view v-for="role in item.roles" :key="role" class="rounded-full bg-zinc-100 px-2 py-1 text-[9px] text-zinc-500">招 {{ role }}</view><view v-for="tag in item.tags" :key="tag" class="rounded-full border border-black/5 px-2 py-1 text-[9px] text-zinc-400">#{{ tag }}</view></view>
              <view class="mt-4 flex items-center justify-between"><view class="flex items-center"><view class="size-7 rounded-full flex items-center justify-center text-white text-[10px] font-black" :style="{ background: item.avatar }">{{ item.user[0] }}</view><view class="ml-2"><text class="text-[10px] font-bold text-zinc-700 block">{{ item.user }}</text><text class="text-[9px] text-zinc-400 block">{{ item.identity }}</text></view></view><view class="flex items-center space-x-3"><view class="flex items-center" @click.stop="toggleFavorite(item)"><view class="i-lucide-heart text-xs mr-1" :class="item.favorite ? 'text-rose-500' : 'text-zinc-400'"></view><text class="text-[10px] text-zinc-400">{{ item.favorite ? '已收藏' : '收藏' }}</text></view><text class="text-[10px] text-zinc-300">{{ item.applicants }} 人报名</text></view></view>
            </view>
          </view>
        </view>
        <view v-if="!filteredDemands.length" class="py-20 flex flex-col items-center"><view class="size-16 rounded-full bg-zinc-100 flex items-center justify-center"><view class="i-lucide-megaphone-off text-2xl text-zinc-400"></view></view><text class="text-sm font-black text-zinc-700 mt-4">暂无符合条件的需求</text><text class="text-xs text-zinc-400 mt-2">调整筛选条件，或发布自己的约拍</text></view>
      </view>
    </scroll-view>

    <view v-if="filterVisible" class="fixed inset-0 z-50 flex items-end" @click="filterVisible = false">
      <view class="absolute inset-0 bg-black/35"></view>
      <view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop>
        <view class="flex items-center justify-between"><text class="text-lg font-black text-zinc-900">筛选需求</text><view class="i-lucide-x text-zinc-500 text-lg" @click="filterVisible = false"></view></view>
        <view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-3">合作方式</text><view class="flex gap-2"><view v-for="item in cooperationOptions" :key="item.value" class="yp-chip" :class="cooperation === item.value ? 'yp-chip-active' : ''" @click="cooperation = item.value">{{ item.label }}</view></view></view>
        <view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-3">城市</text><view class="flex flex-wrap gap-2"><view v-for="city in cities" :key="city" class="yp-chip" :class="selectedCity === city ? 'yp-chip-active' : ''" @click="selectedCity = city">{{ city }}</view></view></view>
        <view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-3">需要角色</text><view class="flex flex-wrap gap-2"><view v-for="role in roles" :key="role" class="yp-chip" :class="selectedRole === role ? 'yp-chip-active' : ''" @click="selectedRole = role">{{ role }}</view></view></view>
        <view class="mt-6 flex space-x-3"><view class="flex-1 h-12 rounded-2xl border border-black/10 flex items-center justify-center text-sm font-bold text-zinc-700" @click="resetFilters">重置</view><view class="flex-1 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-bold text-white" @click="filterVisible = false">查看 {{ filteredDemands.length }} 个</view></view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const keyword = ref(""); const activeCategory = ref("全部"); const cooperation = ref("all"); const selectedCity = ref("全部"); const selectedRole = ref("全部"); const filterVisible = ref(false); const sortIndex = ref(0);
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 190; } catch (error) { console.warn("获取设备信息失败", error); }
const categories = ["全部", "人像", "婚纱", "古风", "街拍", "旅拍", "商业"];
const cities = ["全部", "北京", "上海", "杭州", "成都", "广州"];
const roles = ["全部", "摄影师", "模特", "化妆师", "造型师", "场地"];
const cooperationOptions = [{ label: "全部", value: "all" }, { label: "付费", value: "paid" }, { label: "互勉", value: "mutual" }];
const sortLabels = ["最新发布", "截止时间", "预算最高", "报名最少"];
const demands = reactive([
  { id: 1, title: "周末三里屯情绪人像", type: "人像", city: "北京", date: "6 月 20 日", duration: "3 小时", deadline: "明天截止", budget: "¥500", budgetValue: 500, user: "小雨", identity: "实名认证", applicants: 12, mutual: false, favorite: false, roles: ["摄影师", "化妆师"], tags: ["日系", "自然光"], description: "想拍一组松弛自然的城市人像，希望摄影师擅长引导动作。", avatar: "linear-gradient(135deg,#fb7185,#be123c)", icon: "i-lucide-aperture", iconBg: "#fff1f2", iconColor: "#f43f5e", created: 6, deadlineOrder: 1 },
  { id: 2, title: "西湖宋制汉服互勉创作", type: "古风", city: "杭州", date: "6 月 22 日", duration: "半天", deadline: "3 天后截止", budget: "互勉", budgetValue: 0, user: "苏晴", identity: "摄影师", applicants: 8, mutual: true, favorite: true, roles: ["摄影师", "模特"], tags: ["宋制汉服", "园林"], description: "已有服装和妆造，希望寻找审美相近的伙伴共同创作。", avatar: "linear-gradient(135deg,#a78bfa,#5b21b6)", icon: "i-lucide-flower-2", iconBg: "#f0fdf4", iconColor: "#059669", created: 5, deadlineOrder: 3 },
  { id: 3, title: "城市品牌夏季 Lookbook", type: "商业", city: "上海", date: "6 月 25 日", duration: "全天", deadline: "5 天后截止", budget: "¥2000", budgetValue: 2000, user: "ONCE Studio", identity: "企业认证", applicants: 5, mutual: false, favorite: false, roles: ["模特", "造型师"], tags: ["品牌", "夏季"], description: "独立服装品牌拍摄夏季 Lookbook，需要平面模特和造型师。", avatar: "linear-gradient(135deg,#38bdf8,#0369a1)", icon: "i-lucide-sparkles", iconBg: "#eff6ff", iconColor: "#0284c7", created: 4, deadlineOrder: 5 },
  { id: 4, title: "成都夜景胶片街拍", type: "街拍", city: "成都", date: "6 月 21 日", duration: "2 小时", deadline: "2 天后截止", budget: "¥300", budgetValue: 300, user: "叶知秋", identity: "实名认证", applicants: 15, mutual: false, favorite: false, roles: ["模特"], tags: ["夜景", "胶片"], description: "拍摄春熙路夜景，希望模特有街头感穿搭。", avatar: "linear-gradient(135deg,#c4b5fd,#6d28d9)", icon: "i-lucide-moon-star", iconBg: "#f5f3ff", iconColor: "#7c3aed", created: 3, deadlineOrder: 2 },
  { id: 5, title: "大理双廊情侣旅拍", type: "旅拍", city: "北京", date: "7 月 2 日", duration: "全天", deadline: "7 天后截止", budget: "¥2800", budgetValue: 2800, user: "阿禾", identity: "实名认证", applicants: 3, mutual: false, favorite: false, roles: ["摄影师", "化妆师"], tags: ["情侣", "大理"], description: "计划在洱海边拍摄轻婚纱旅拍，希望提供妆造和路线建议。", avatar: "linear-gradient(135deg,#2dd4bf,#0f766e)", icon: "i-lucide-plane", iconBg: "#f0fdfa", iconColor: "#0f766e", created: 2, deadlineOrder: 7 }
]);
const filteredDemands = computed(() => {
  let list = demands.filter((item) => {
    const key = keyword.value.trim().toLowerCase();
    const keyOk = !key || `${item.title}${item.city}${item.roles.join("")}${item.tags.join("")}`.toLowerCase().includes(key);
    return keyOk && (activeCategory.value === "全部" || item.type === activeCategory.value) && (cooperation.value === "all" || (cooperation.value === "mutual" ? item.mutual : !item.mutual)) && (selectedCity.value === "全部" || item.city === selectedCity.value) && (selectedRole.value === "全部" || item.roles.includes(selectedRole.value));
  });
  list = [...list];
  if (sortIndex.value === 1) list.sort((a, b) => a.deadlineOrder - b.deadlineOrder);
  else if (sortIndex.value === 2) list.sort((a, b) => b.budgetValue - a.budgetValue);
  else if (sortIndex.value === 3) list.sort((a, b) => a.applicants - b.applicants);
  else list.sort((a, b) => b.created - a.created);
  return list;
});
function toggleFavorite(item) { item.favorite = !item.favorite; uni.showToast({ title: item.favorite ? "已收藏需求" : "已取消收藏", icon: "none" }); }
function resetFilters() { cooperation.value = "all"; selectedCity.value = "全部"; selectedRole.value = "全部"; activeCategory.value = "全部"; keyword.value = ""; }
function openDetail(item) { proxy.$tab.navigateTo(`/pages/demand/detail?id=${item.id}`); }
function openPublish() { proxy.$tab.switchTab("/pages/publish/index"); }
</script>
