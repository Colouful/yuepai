<template>
  <view class="min-h-screen bg-gradient-to-b from-violet-50 via-white to-rose-50">
    <view :style="{ height: statusBarHeight + 'px' }"></view>

    <!-- Header -->
    <view class="px-5 pt-2 pb-3">
      <text class="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-violet-500 to-rose-500 bg-clip-text text-transparent">发现</text>
      <view class="mt-3 flex space-x-2">
        <view v-for="(tab, i) in tabs" :key="tab"
          class="rounded-full px-4 py-2 text-xs font-semibold transition-all duration-300"
          :class="activeTab === i ? 'bg-gradient-to-r from-violet-400 to-rose-400 text-white shadow-md shadow-violet-200/50' : 'bg-white/80 text-slate-500'"
          @click="activeTab = i">{{ tab }}</view>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollHeight + 'px' }">
      <view class="px-5 pb-8">
        <!-- 瀑布流作品 -->
        <view class="flex flex-wrap gap-2.5">
          <view v-for="(work, i) in works" :key="i"
            class="rounded-2xl bg-white/80 backdrop-blur-sm overflow-hidden shadow-sm shadow-violet-100/30 active:scale-[0.97] transition-transform"
            :class="i % 3 === 0 ? 'w-[48%]' : 'w-[48%]'">
            <view class="bg-gradient-to-br" :class="work.gradient" :style="{ height: work.h + 'px' }"></view>
            <view class="p-3">
              <text class="text-xs font-bold text-slate-800 block truncate">{{ work.title }}</text>
              <text class="text-[10px] text-slate-400 block mt-0.5">{{ work.tag }}</text>
              <view class="mt-2 flex items-center justify-between">
                <view class="flex items-center space-x-1.5">
                  <view class="size-5 rounded-full bg-gradient-to-br flex items-center justify-center text-white text-[7px] font-bold" :class="work.color">{{ work.author[0] }}</view>
                  <text class="text-[10px] text-slate-500 font-medium">{{ work.author }}</text>
                </view>
                <view class="flex items-center space-x-0.5">
                  <view class="i-lucide-heart text-rose-300 text-[10px]"></view>
                  <text class="text-[10px] text-slate-400">{{ work.likes }}</text>
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
import { ref } from "vue";

const statusBarHeight = ref(44);
const scrollHeight = ref(600);
try {
  const sys = uni.getSystemInfoSync();
  statusBarHeight.value = sys.statusBarHeight || 44;
  scrollHeight.value = sys.windowHeight - statusBarHeight.value - 50;
} catch(e) {}

const tabs = ["推荐", "人像", "古风", "婚纱", "JK", "街拍", "旅拍"];
const activeTab = ref(0);

const works = [
  { title: "夏日清新人像写真", tag: "#人像 #清新", author: "林默", likes: 326, h: 180, gradient: "from-rose-200 to-pink-300", color: "from-rose-400 to-pink-400" },
  { title: "汉服古风 · 西湖取景", tag: "#古风 #汉服", author: "苏晴", likes: 218, h: 220, gradient: "from-violet-200 to-purple-300", color: "from-violet-400 to-purple-400" },
  { title: "城市夜景街拍", tag: "#街拍 #夜景", author: "陈风", likes: 156, h: 160, gradient: "from-sky-200 to-cyan-300", color: "from-sky-400 to-cyan-400" },
  { title: "日系胶片风格", tag: "#日系 #胶片", author: "叶知秋", likes: 412, h: 200, gradient: "from-emerald-200 to-teal-300", color: "from-emerald-400 to-teal-400" },
  { title: "婚纱客片精选", tag: "#婚纱 #浪漫", author: "白鹭", likes: 89, h: 190, gradient: "from-amber-200 to-orange-300", color: "from-amber-400 to-orange-400" },
  { title: "JK制服日常", tag: "#JK #校园", author: "林默", likes: 267, h: 170, gradient: "from-pink-200 to-rose-300", color: "from-pink-400 to-rose-400" },
  { title: "商业产品拍摄", tag: "#商业 #产品", author: "陈风", likes: 98, h: 185, gradient: "from-slate-200 to-zinc-300", color: "from-slate-400 to-zinc-400" },
  { title: "亲子家庭写真", tag: "#亲子 #温馨", author: "苏晴", likes: 178, h: 210, gradient: "from-orange-200 to-amber-300", color: "from-orange-400 to-amber-400" },
];
</script>
