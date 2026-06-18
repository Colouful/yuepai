<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <view class="px-5 pt-3 pb-3">
      <view class="flex items-end justify-between">
        <view>
          <text class="yp-eyebrow block">DISCOVER</text>
          <text class="yp-title block mt-1">发现灵感</text>
        </view>
        <view class="size-10 rounded-full bg-zinc-900 flex items-center justify-center" @click="openSearch">
          <view class="i-lucide-search text-white text-lg"></view>
        </view>
      </view>

      <view class="mt-4 flex items-center space-x-2">
        <view class="h-11 flex-1 rounded-2xl bg-white border border-black/5 px-4 flex items-center" @click="openSearch">
          <view class="i-lucide-search text-zinc-400 text-sm mr-2"></view>
          <text class="text-sm text-zinc-400">搜索风格、地点或创作者</text>
        </view>
        <view class="size-11 rounded-2xl bg-white border border-black/5 flex items-center justify-center" @click="showFilter">
          <view class="i-lucide-sliders-horizontal text-zinc-700 text-base"></view>
        </view>
      </view>

      <scroll-view scroll-x class="mt-4 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2 pr-5">
          <view
            v-for="(item, index) in tabs"
            :key="item"
            class="yp-chip"
            :class="tabIndex === index ? 'yp-chip-active' : ''"
            @click="tabIndex = index"
          >
            {{ item }}
          </view>
        </view>
      </scroll-view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28">
        <view class="relative h-48 rounded-3xl overflow-hidden mb-5" :style="{ background: featured.cover }" @click="openWork(featured)">
          <view class="absolute inset-0" style="background:linear-gradient(180deg,rgba(0,0,0,.02),rgba(0,0,0,.72))"></view>
          <view class="absolute top-4 left-4 rounded-full bg-white/90 px-3 py-1.5 text-[10px] font-bold text-zinc-900">本周精选</view>
          <view class="absolute left-5 right-5 bottom-5">
            <text class="text-xl font-black text-white block">{{ featured.title }}</text>
            <text class="text-xs text-white/65 block mt-1">{{ featured.subtitle }}</text>
            <view class="mt-3 flex items-center justify-between">
              <view class="flex items-center">
                <view class="size-7 rounded-full bg-white/20 border border-white/20 flex items-center justify-center text-white text-[10px] font-bold">{{ featured.author[0] }}</view>
                <text class="text-xs text-white ml-2">{{ featured.author }}</text>
              </view>
              <view class="flex items-center text-white/80">
                <view class="i-lucide-heart text-sm mr-1"></view>
                <text class="text-xs">{{ featured.likes }}</text>
              </view>
            </view>
          </view>
        </view>

        <view class="flex items-center justify-between mb-3">
          <text class="yp-section-title">今日推荐</text>
          <text class="text-xs text-zinc-400">持续发现新的审美</text>
        </view>

        <view class="flex items-start gap-3">
          <view class="flex-1 space-y-3">
            <view v-for="item in leftWorks" :key="item.id" class="yp-card overflow-hidden" @click="openWork(item)">
              <view class="relative" :style="{ height: item.height + 'px', background: item.cover }">
                <view class="absolute left-3 top-3 rounded-full bg-black/40 px-2.5 py-1 text-[9px] text-white">{{ item.city }}</view>
                <view class="absolute right-3 top-3 size-7 rounded-full bg-white/85 flex items-center justify-center" @click.stop="toggleLike(item)">
                  <view class="i-lucide-heart text-sm" :class="item.liked ? 'text-rose-500' : 'text-zinc-700'"></view>
                </view>
              </view>
              <view class="p-3">
                <text class="text-sm font-black text-zinc-900 block leading-snug">{{ item.title }}</text>
                <text class="text-[10px] text-zinc-400 block mt-1">{{ item.tags }}</text>
                <view class="mt-3 flex items-center justify-between">
                  <view class="flex items-center min-w-0">
                    <view class="size-6 rounded-full flex items-center justify-center text-white text-[9px] font-bold" :style="{ background: item.avatar }">{{ item.author[0] }}</view>
                    <text class="text-[10px] text-zinc-600 ml-1.5 truncate">{{ item.author }}</text>
                  </view>
                  <text class="text-[10px] text-zinc-400">{{ item.likes }}</text>
                </view>
              </view>
            </view>
          </view>

          <view class="flex-1 space-y-3">
            <view v-for="item in rightWorks" :key="item.id" class="yp-card overflow-hidden" @click="openWork(item)">
              <view class="relative" :style="{ height: item.height + 'px', background: item.cover }">
                <view class="absolute left-3 top-3 rounded-full bg-black/40 px-2.5 py-1 text-[9px] text-white">{{ item.city }}</view>
                <view class="absolute right-3 top-3 size-7 rounded-full bg-white/85 flex items-center justify-center" @click.stop="toggleLike(item)">
                  <view class="i-lucide-heart text-sm" :class="item.liked ? 'text-rose-500' : 'text-zinc-700'"></view>
                </view>
              </view>
              <view class="p-3">
                <text class="text-sm font-black text-zinc-900 block leading-snug">{{ item.title }}</text>
                <text class="text-[10px] text-zinc-400 block mt-1">{{ item.tags }}</text>
                <view class="mt-3 flex items-center justify-between">
                  <view class="flex items-center min-w-0">
                    <view class="size-6 rounded-full flex items-center justify-center text-white text-[9px] font-bold" :style="{ background: item.avatar }">{{ item.author[0] }}</view>
                    <text class="text-[10px] text-zinc-600 ml-1.5 truncate">{{ item.author }}</text>
                  </view>
                  <text class="text-[10px] text-zinc-400">{{ item.likes }}</text>
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const scrollH = ref(600);
const tabIndex = ref(0);

try {
  const systemInfo = uni.getSystemInfoSync();
  statusBarH.value = systemInfo.statusBarHeight || 44;
  scrollH.value = systemInfo.windowHeight - statusBarH.value - 164;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

const tabs = ["推荐", "人像", "古风", "婚纱", "街拍", "旅拍", "胶片"];

const featured = {
  id: "featured",
  title: "在城市缝隙里，收藏一场日落",
  subtitle: "城市人像专题 · 上海",
  author: "林默",
  likes: 1268,
  cover: "linear-gradient(135deg,#27272a 0%,#7c2d12 48%,#fb7185 100%)",
};

const works = reactive([
  { id: 1, title: "风吹过裙摆的夏天", tags: "#清新人像 #自然光", author: "苏晴", city: "北京", likes: 326, liked: false, height: 218, cover: "linear-gradient(145deg,#fecdd3,#fda4af 50%,#be123c)", avatar: "linear-gradient(135deg,#fb7185,#e11d48)" },
  { id: 2, title: "旧街区的胶片情绪", tags: "#胶片 #街拍", author: "陈风", city: "广州", likes: 518, liked: true, height: 176, cover: "linear-gradient(145deg,#d6d3d1,#78716c 48%,#292524)", avatar: "linear-gradient(135deg,#71717a,#18181b)" },
  { id: 3, title: "西湖边的一场宋韵", tags: "#汉服 #古风", author: "白鹭", city: "杭州", likes: 890, liked: false, height: 186, cover: "linear-gradient(145deg,#d1fae5,#6ee7b7 52%,#065f46)", avatar: "linear-gradient(135deg,#34d399,#047857)" },
  { id: 4, title: "夜色与霓虹的距离", tags: "#夜景 #情绪", author: "叶知秋", city: "成都", likes: 742, liked: false, height: 232, cover: "linear-gradient(145deg,#c4b5fd,#6d28d9 55%,#18181b)", avatar: "linear-gradient(135deg,#a78bfa,#5b21b6)" },
  { id: 5, title: "海边婚纱纪实", tags: "#婚纱 #纪实", author: "南山影像", city: "厦门", likes: 405, liked: false, height: 206, cover: "linear-gradient(145deg,#e0f2fe,#7dd3fc 52%,#0369a1)", avatar: "linear-gradient(135deg,#38bdf8,#0369a1)" },
  { id: 6, title: "雨后的日系小巷", tags: "#日系 #生活感", author: "木子", city: "南京", likes: 219, liked: true, height: 168, cover: "linear-gradient(145deg,#fef3c7,#fbbf24 52%,#92400e)", avatar: "linear-gradient(135deg,#fbbf24,#b45309)" },
  { id: 7, title: "山野旅拍计划", tags: "#旅拍 #自然", author: "远川", city: "大理", likes: 663, liked: false, height: 226, cover: "linear-gradient(145deg,#ccfbf1,#2dd4bf 52%,#134e4a)", avatar: "linear-gradient(135deg,#2dd4bf,#0f766e)" },
  { id: 8, title: "黑白肖像练习", tags: "#黑白 #棚拍", author: "一格", city: "上海", likes: 351, liked: false, height: 184, cover: "linear-gradient(145deg,#f4f4f5,#a1a1aa 48%,#18181b)", avatar: "linear-gradient(135deg,#71717a,#18181b)" },
]);

const leftWorks = computed(() => works.filter((_, index) => index % 2 === 0));
const rightWorks = computed(() => works.filter((_, index) => index % 2 === 1));

function toggleLike(item) {
  item.liked = !item.liked;
  item.likes += item.liked ? 1 : -1;
}

function openSearch() {
  proxy.$tab.navigateTo("/pages/search/index");
}

function showFilter() {
  uni.showToast({ title: "筛选功能正在完善", icon: "none" });
}

function openWork(item) {
  proxy.$tab.navigateTo(`/pages/profile/index?id=${item.id}`);
}
</script>
