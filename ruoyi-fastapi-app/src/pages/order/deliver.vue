<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4 flex items-center">
      <view class="i-lucide-arrow-left text-slate-700 text-xl mr-3" @click="goBack"></view>
      <text class="text-lg font-bold text-slate-800">作品验收</text>
    </view>
    <view class="px-5 pt-4 pb-24 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">精修照片 (30张)</text>
        <view class="flex flex-wrap gap-2">
          <view v-for="i in 9" :key="i" class="h-24 w-[31%] rounded-xl bg-gradient-to-br from-rose-100 to-violet-100 relative">
            <view class="absolute bottom-1 right-1 size-5 rounded-full bg-white/80 flex items-center justify-center">
              <view class="i-lucide-check text-emerald-500 text-[10px]"></view>
            </view>
          </view>
        </view>
        <text class="text-[10px] text-slate-300 block mt-2 text-center">点击图片查看大图，长按选择精修</text>
      </view>
      <view class="flex space-x-3">
        <view class="flex-1 h-11 rounded-xl bg-white text-slate-700 flex items-center justify-center text-sm font-semibold ring-1 ring-rose-200 active:scale-95 transition-transform">申请修改</view>
        <view class="flex-1 h-11 rounded-xl bg-gradient-to-r from-rose-400 to-violet-400 text-white flex items-center justify-center text-sm font-semibold active:scale-95 transition-transform">确认验收</view>
      </view>
    </view>
  </view>
</template>
<script setup>
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance();
function goBack() { proxy.$tab.navigateBack(); }
</script>
