<template>
  <view class="yp-page pb-24">
    <view class="relative h-[520px]" :style="{ background: work.cover }">
      <view class="absolute inset-0" style="background:linear-gradient(180deg,rgba(0,0,0,.08),rgba(0,0,0,.08) 55%,rgba(0,0,0,.78))"></view>
      <view :style="{ height: statusBarH + 'px' }"></view>
      <view class="relative z-10 px-5 pt-3 flex items-center justify-between">
        <view class="size-10 rounded-full bg-black/25 backdrop-blur-sm flex items-center justify-center" @click="goBack">
          <view class="i-lucide-arrow-left text-white text-lg"></view>
        </view>
        <view class="flex items-center space-x-2">
          <view class="size-10 rounded-full bg-black/25 backdrop-blur-sm flex items-center justify-center" @click="shareWork">
            <view class="i-lucide-share-2 text-white text-lg"></view>
          </view>
          <view class="size-10 rounded-full bg-black/25 backdrop-blur-sm flex items-center justify-center" @click="toggleFavorite">
            <view class="i-lucide-bookmark text-lg" :class="favorite ? 'text-rose-400' : 'text-white'"></view>
          </view>
        </view>
      </view>

      <view class="absolute left-5 right-5 bottom-6 z-10">
        <view class="flex flex-wrap gap-2 mb-3">
          <view v-for="tag in work.tags" :key="tag" class="rounded-full bg-white/15 border border-white/15 px-3 py-1 text-[10px] text-white">#{{ tag }}</view>
        </view>
        <text class="text-[26px] leading-tight font-black text-white block">{{ work.title }}</text>
        <text class="text-xs leading-relaxed text-white/60 block mt-3">{{ work.subtitle }}</text>
        <view class="mt-4 flex items-center justify-between">
          <view class="flex items-center" @click="openAuthor">
            <view class="size-10 rounded-2xl flex items-center justify-center text-white font-black border border-white/20" :style="{ background: work.avatar }">{{ work.author[0] }}</view>
            <view class="ml-3">
              <view class="flex items-center"><text class="text-sm font-black text-white">{{ work.author }}</text><view class="i-lucide-badge-check text-rose-300 text-xs ml-1"></view></view>
              <text class="text-[10px] text-white/50 block mt-1">{{ work.authorTitle }}</text>
            </view>
          </view>
          <view class="rounded-full px-4 py-2 text-[10px] font-bold" :class="followed ? 'bg-white/15 text-white' : 'bg-white text-zinc-900'" @click="toggleFollow">{{ followed ? '已关注' : '+ 关注' }}</view>
        </view>
      </view>
    </view>

    <view class="px-5 pt-5 pb-8 space-y-5">
      <view class="yp-card p-4 grid grid-cols-4">
        <view v-for="item in stats" :key="item.label" class="text-center">
          <text class="text-base font-black text-zinc-900 block">{{ item.value }}</text>
          <text class="text-[10px] text-zinc-400 block mt-1">{{ item.label }}</text>
        </view>
      </view>

      <view class="yp-card p-4">
        <text class="yp-section-title block mb-3">创作故事</text>
        <text class="text-xs text-zinc-500 leading-relaxed">{{ work.description }}</text>
        <view class="mt-4 flex flex-wrap gap-2">
          <view v-for="item in metadata" :key="item.label" class="rounded-2xl bg-zinc-50 px-3 py-2 flex items-center">
            <view :class="item.icon" class="text-xs text-rose-500 mr-1.5"></view>
            <text class="text-[10px] text-zinc-500">{{ item.label }}：{{ item.value }}</text>
          </view>
        </view>
      </view>

      <view>
        <view class="flex items-end justify-between mb-3">
          <view><text class="yp-section-title block">创作成员</text><text class="text-[10px] text-zinc-400 block mt-1">共同完成这组作品的人</text></view>
          <text class="text-xs text-zinc-400">{{ credits.length }} 位</text>
        </view>
        <view class="yp-card overflow-hidden">
          <view v-for="(item, index) in credits" :key="item.name" class="flex items-center px-4 py-3.5" :class="index < credits.length - 1 ? 'border-b border-black/5' : ''" @click="openCredit(item)">
            <view class="size-10 rounded-2xl flex items-center justify-center text-white text-xs font-black" :style="{ background: item.avatar }">{{ item.name[0] }}</view>
            <view class="flex-1 ml-3"><text class="text-xs font-black text-zinc-800 block">{{ item.name }}</text><text class="text-[10px] text-zinc-400 block mt-1">{{ item.role }}</text></view>
            <view class="i-lucide-chevron-right text-zinc-300 text-sm"></view>
          </view>
        </view>
      </view>

      <view>
        <view class="flex items-end justify-between mb-3">
          <view><text class="yp-section-title block">评论</text><text class="text-[10px] text-zinc-400 block mt-1">关于作品与创作的交流</text></view>
          <text class="text-xs font-bold text-rose-500" @click="commentVisible = true">写评论</text>
        </view>
        <view class="space-y-3">
          <view v-for="item in comments" :key="item.id" class="yp-card p-4">
            <view class="flex items-center"><view class="size-8 rounded-full flex items-center justify-center text-white text-[10px] font-black" :style="{ background: item.avatar }">{{ item.name[0] }}</view><view class="flex-1 ml-2"><text class="text-xs font-black text-zinc-800 block">{{ item.name }}</text><text class="text-[9px] text-zinc-400 block mt-0.5">{{ item.time }}</text></view><view class="flex items-center text-zinc-400" @click="toggleCommentLike(item)"><view class="i-lucide-heart text-xs" :class="item.liked ? 'text-rose-500' : ''"></view><text class="text-[10px] ml-1">{{ item.likes }}</text></view></view>
            <text class="text-xs text-zinc-500 leading-relaxed block mt-3">{{ item.content }}</text>
          </view>
        </view>
      </view>

      <view>
        <view class="flex items-end justify-between mb-3">
          <view><text class="yp-section-title block">更多灵感</text><text class="text-[10px] text-zinc-400 block mt-1">相似风格作品推荐</text></view>
          <text class="text-xs font-bold text-rose-500" @click="openDiscover">查看更多</text>
        </view>
        <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
          <view class="inline-flex space-x-3 pr-5">
            <view v-for="item in relatedWorks" :key="item.id" class="relative inline-block w-44 h-56 rounded-3xl overflow-hidden" :style="{ background: item.cover }" @click="openRelated(item)">
              <view class="absolute inset-0" style="background:linear-gradient(180deg,transparent,rgba(0,0,0,.68))"></view>
              <view class="absolute left-3 right-3 bottom-3"><text class="text-sm font-black text-white block whitespace-normal">{{ item.title }}</text><text class="text-[10px] text-white/55 block mt-1">{{ item.author }}</text></view>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3">
      <view class="flex items-center space-x-4 px-2">
        <view class="flex flex-col items-center" @click="toggleLike"><view class="i-lucide-heart text-xl" :class="liked ? 'text-rose-500' : 'text-zinc-700'"></view><text class="text-[9px] text-zinc-400 mt-0.5">{{ likeCount }}</text></view>
        <view class="flex flex-col items-center" @click="commentVisible = true"><view class="i-lucide-message-circle text-xl text-zinc-700"></view><text class="text-[9px] text-zinc-400 mt-0.5">{{ comments.length }}</text></view>
      </view>
      <view class="flex-1 h-12 rounded-2xl border border-black/10 flex items-center justify-center text-sm font-bold text-zinc-700" @click="openChat">咨询创作者</view>
      <view class="flex-1 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="createSameStyle">同款约拍</view>
    </view>

    <view v-if="commentVisible" class="fixed inset-0 z-50 flex items-end" @click="commentVisible = false">
      <view class="absolute inset-0 bg-black/35"></view>
      <view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop>
        <view class="flex items-center justify-between"><view><text class="text-lg font-black text-zinc-900 block">发表评论</text><text class="text-[10px] text-zinc-400 block mt-1">友善交流创作与审美</text></view><view class="i-lucide-x text-zinc-500 text-lg" @click="commentVisible = false"></view></view>
        <textarea v-model="commentDraft" maxlength="200" placeholder="说说你对这组作品的感受…" placeholder-class="text-zinc-300" class="mt-5 h-28 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" />
        <view class="mt-5 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="submitComment">发布评论</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";

const { proxy } = getCurrentInstance();
const statusBarH = ref(44);
const workId = ref("1");
const liked = ref(false);
const favorite = ref(false);
const followed = ref(false);
const commentVisible = ref(false);
const commentDraft = ref("");

try {
  statusBarH.value = uni.getSystemInfoSync().statusBarHeight || 44;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

onLoad((options) => {
  workId.value = options?.id || "1";
});

const work = reactive({
  title: "旧街区的胶片情绪",
  subtitle: "在日落前的一小时，记录城市旧街区里真实、松弛的瞬间。",
  author: "陈风",
  authorTitle: "人像摄影师 · 广州",
  likes: 518,
  favorites: 126,
  views: "3.2k",
  tags: ["胶片", "街拍", "城市人像"],
  avatar: "linear-gradient(135deg,#71717a,#18181b)",
  cover: "linear-gradient(145deg,#d6d3d1 0%,#78716c 42%,#292524 78%,#18181b 100%)",
  description: "这组作品没有预设复杂剧情，只选择一条保留着老建筑和生活痕迹的街道，让模特在散步、等待与交谈中自然进入状态。后期保留了偏暖的颗粒和低饱和色彩，希望画面更接近记忆中的城市。",
});

const likeCount = computed(() => work.likes + (liked.value ? 1 : 0));
const stats = computed(() => [
  { value: likeCount.value, label: "喜欢" },
  { value: work.favorites, label: "收藏" },
  { value: work.views, label: "浏览" },
  { value: comments.length, label: "评论" },
]);

const metadata = [
  { label: "地点", value: "广州东山口", icon: "i-lucide-map-pin" },
  { label: "器材", value: "Sony A7M4", icon: "i-lucide-camera" },
  { label: "镜头", value: "35mm F1.4", icon: "i-lucide-aperture" },
  { label: "时间", value: "傍晚自然光", icon: "i-lucide-sunset" },
];

const credits = [
  { name: "陈风", role: "摄影师 / 后期", avatar: "linear-gradient(135deg,#71717a,#18181b)", path: "/pages/photographer/detail?id=3" },
  { name: "木子", role: "出镜模特", avatar: "linear-gradient(135deg,#38bdf8,#0369a1)", path: "/pages/model/detail?id=3" },
  { name: "安然", role: "造型与妆发", avatar: "linear-gradient(135deg,#fb7185,#be123c)", path: "/pages/profile/index?id=9" },
];

const comments = reactive([
  { id: 1, name: "叶知秋", time: "20 分钟前", content: "光线和街道质感处理得很好，尤其喜欢第三张人物和环境的关系。", likes: 18, liked: false, avatar: "linear-gradient(135deg,#a78bfa,#5b21b6)" },
  { id: 2, name: "白鹭", time: "2 小时前", content: "色调很克制，胶片颗粒没有抢掉人物情绪。", likes: 9, liked: false, avatar: "linear-gradient(135deg,#34d399,#047857)" },
]);

const relatedWorks = [
  { id: 4, title: "夜色与霓虹的距离", author: "叶知秋", cover: "linear-gradient(145deg,#c4b5fd,#6d28d9 55%,#18181b)" },
  { id: 6, title: "雨后的日系小巷", author: "木子", cover: "linear-gradient(145deg,#fef3c7,#fbbf24 52%,#92400e)" },
  { id: 8, title: "黑白肖像练习", author: "一格", cover: "linear-gradient(145deg,#f4f4f5,#a1a1aa 48%,#18181b)" },
];

function toggleLike() {
  liked.value = !liked.value;
}

function toggleFavorite() {
  favorite.value = !favorite.value;
  uni.showToast({ title: favorite.value ? "已收藏作品" : "已取消收藏", icon: "none" });
}

function toggleFollow() {
  followed.value = !followed.value;
  uni.showToast({ title: followed.value ? "已关注创作者" : "已取消关注", icon: "none" });
}

function toggleCommentLike(item) {
  item.liked = !item.liked;
  item.likes += item.liked ? 1 : -1;
}

function submitComment() {
  const content = commentDraft.value.trim();
  if (content.length < 2) {
    uni.showToast({ title: "请输入评论内容", icon: "none" });
    return;
  }
  comments.unshift({ id: Date.now(), name: "我", time: "刚刚", content, likes: 0, liked: false, avatar: "linear-gradient(135deg,#f43f5e,#9f1239)" });
  commentDraft.value = "";
  commentVisible.value = false;
  uni.showToast({ title: "评论已发布", icon: "success" });
}

function openAuthor() {
  proxy.$tab.navigateTo("/pages/photographer/detail?id=3");
}

function openCredit(item) {
  proxy.$tab.navigateTo(item.path);
}

function openChat() {
  proxy.$tab.navigateTo(`/pages/chat/index?id=3&name=${encodeURIComponent(work.author)}`);
}

function createSameStyle() {
  const draft = {
    mode: "demand",
    type: "个人写真",
    title: `想拍同款：${work.title}`,
    description: `参考作品《${work.title}》，希望拍摄相似的${work.tags.join("、")}风格。`,
    sourceWorkId: workId.value,
  };
  uni.setStorageSync("yuepai_same_style_draft", draft);
  proxy.$tab.switchTab("/pages/publish/index");
}

function openRelated(item) {
  proxy.$tab.redirectTo(`/pages/works/detail?id=${item.id}`);
}

function openDiscover() {
  proxy.$tab.switchTab("/pages/works/index");
}

function shareWork() {
  uni.showToast({ title: "分享面板正在接入", icon: "none" });
}

function goBack() {
  proxy.$tab.navigateBack();
}
</script>
