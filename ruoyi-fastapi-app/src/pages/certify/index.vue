<template>
  <view class="min-h-screen bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <view class="bg-white/80 backdrop-blur-sm px-5 pt-12 pb-4">
      <text class="text-xl font-bold tracking-tight text-slate-800">实名认证</text>
      <text class="text-xs text-slate-400 block mt-1">完成认证后可享受更多服务</text>
    </view>
    <view class="px-5 pt-5 space-y-4">
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">真实姓名</text>
        <input placeholder="请输入真实姓名" placeholder-class="text-slate-300"
          class="h-11 w-full rounded-xl bg-rose-50/50 px-4 text-sm text-slate-700 ring-1 ring-rose-100 focus:ring-2 focus:ring-rose-300" />
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-2">身份证号码</text>
        <input placeholder="请输入18位身份证号码" placeholder-class="text-slate-300"
          class="h-11 w-full rounded-xl bg-rose-50/50 px-4 text-sm text-slate-700 ring-1 ring-rose-100" />
      </view>
      <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5 shadow-sm">
        <text class="text-sm font-semibold text-slate-700 block mb-3">身份证照片</text>
        <view class="flex space-x-3">
          <view class="flex-1 h-28 rounded-xl bg-rose-50 border-2 border-dashed border-rose-200 flex flex-col items-center justify-center">
            <view class="i-lucide-upload text-rose-300 text-2xl"></view>
            <text class="text-[10px] text-rose-300 mt-1">人像面</text>
          </view>
          <view class="flex-1 h-28 rounded-xl bg-rose-50 border-2 border-dashed border-rose-200 flex flex-col items-center justify-center">
            <view class="i-lucide-upload text-rose-300 text-2xl"></view>
            <text class="text-[10px] text-rose-300 mt-1">国徽面</text>
          </view>
        </view>
      </view>
      <button class="h-12 w-full rounded-2xl bg-gradient-to-r from-rose-400 to-violet-400 text-white font-semibold shadow-lg shadow-rose-200/50 active:scale-[0.98] transition-transform">
        提交认证
      </button>
    </view>
  </view>
</template>
<script setup>
</script>