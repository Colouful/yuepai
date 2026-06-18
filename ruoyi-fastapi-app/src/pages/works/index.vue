<template>
  <view class="min-h-screen" style="background:linear-gradient(180deg,#F5F3FF 0%,#FFFFFF 40%,#FDF2F8 100%)">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-2 pb-3">
      <text class="text-[22px] font-black tracking-tight" style="background:linear-gradient(135deg,#8B5CF6,#EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent">发现</text>
      <scroll-view scroll-x class="mt-3 whitespace-nowrap" :show-scrollbar="false">
        <view class="inline-flex space-x-2">
          <view v-for="(t,i) in tabs" :key="t" class="inline-block rounded-full px-4 py-2 text-xs font-bold transition-all duration-300"
            :style="tabIdx===i ? 'background:linear-gradient(135deg,#A78BFA,#F472B6);color:#fff;box-shadow:0 4px 15px rgba(167,139,250,0.3)' : 'background:rgba(255,255,255,0.9);color:#64748B;box-shadow:0 2px 8px rgba(167,139,250,0.06)'"
            @click="tabIdx=i">{{ t }}</view>
        </view>
      </scroll-view>
    </view>
    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-24">
        <view class="flex flex-wrap gap-2.5">
          <view v-for="(w,i) in works" :key="i" class="rounded-2xl bg-white overflow-hidden active:scale-95 transition-transform duration-200" style="box-shadow:0 2px 12px rgba(167,139,250,0.06)" :class="i%3===0?'w-[48%]':'w-[48%]'">
            <view class="bg-gradient-to-br" :class="w.gradient" :style="{height:w.h+'px'}"></view>
            <view class="p-3">
              <text class="text-xs font-bold text-slate-800 block truncate">{{ w.title }}</text>
              <text class="text-[10px] text-slate-400 block mt-0.5">{{ w.tag }}</text>
              <view class="mt-2 flex items-center justify-between">
                <view class="flex items-center space-x-1.5">
                  <view class="size-5 rounded-full flex items-center justify-center text-white text-[7px] font-bold" :style="{background:w.avatarBg}">{{ w.author[0] }}</view>
                  <text class="text-[10px] text-slate-500 font-medium">{{ w.author }}</text>
                </view>
                <view class="flex items-center space-x-0.5">
                  <view class="i-lucide-heart text-rose-300 text-[10px]"></view>
                  <text class="text-[10px] text-slate-400">{{ w.likes }}</text>
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
const statusBarH = ref(44); const scrollH = ref(600);
try { const s=uni.getSystemInfoSync(); statusBarH.value=s.statusBarHeight||44; scrollH.value=s.windowHeight-statusBarH.value-100; } catch(e){}
const tabs = ["推荐","人像","古风","婚纱","JK","街拍","旅拍"]; const tabIdx = ref(0);
const works = [
  { title:"夏日清新人像写真", tag:"#人像 #清新", author:"林默", likes:326, h:180, gradient:"from-rose-200 to-pink-200", avatarBg:"linear-gradient(135deg,#F472B6,#EC4899)" },
  { title:"汉服古风 · 西湖", tag:"#古风 #汉服", author:"苏晴", likes:218, h:220, gradient:"from-violet-200 to-purple-200", avatarBg:"linear-gradient(135deg,#A78BFA,#8B5CF6)" },
  { title:"城市夜景街拍", tag:"#街拍 #夜景", author:"陈风", likes:156, h:160, gradient:"from-sky-200 to-cyan-200", avatarBg:"linear-gradient(135deg,#38BDF8,#0EA5E9)" },
  { title:"日系胶片风格", tag:"#日系 #胶片", author:"叶知秋", likes:412, h:200, gradient:"from-emerald-200 to-teal-200", avatarBg:"linear-gradient(135deg,#34D399,#10B981)" },
  { title:"婚纱客片精选", tag:"#婚纱", author:"白鹭", likes:89, h:190, gradient:"from-amber-200 to-orange-200", avatarBg:"linear-gradient(135deg,#FBBF24,#F59E0B)" },
  { title:"JK制服日常", tag:"#JK", author:"林默", likes:267, h:170, gradient:"from-pink-200 to-rose-200", avatarBg:"linear-gradient(135deg,#F472B6,#EC4899)" },
  { title:"商业产品拍摄", tag:"#商业", author:"陈风", likes:98, h:185, gradient:"from-slate-200 to-zinc-200", avatarBg:"linear-gradient(135deg,#38BDF8,#0EA5E9)" },
  { title:"亲子家庭写真", tag:"#亲子", author:"苏晴", likes:178, h:210, gradient:"from-orange-200 to-amber-200", avatarBg:"linear-gradient(135deg,#A78BFA,#8B5CF6)" },
];
</script>
