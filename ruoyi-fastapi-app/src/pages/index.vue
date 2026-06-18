<template>
  <view class="flex h-full flex-col bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50">
    <!-- Header Area -->
    <view class="bg-white pb-5 rounded-b-[28px] shadow-sm z-50">
      <!-- Title -->
      <view class="pt-12 pb-3 px-5 flex justify-between items-center">
        <text class="text-xl font-bold tracking-tight text-slate-900">约拍</text>
        <text class="text-xs text-slate-400">记录美好瞬间</text>
      </view>

      <!-- Search & Notification -->
      <view class="px-5 pb-1">
        <view class="flex items-center space-x-3">
          <!-- Search Input -->
          <view class="flex-1 relative">
            <view
              class="absolute left-3.5 top-0 bottom-0 flex items-center text-slate-400"
            >
              <view class="i-lucide-search text-base"></view>
            </view>
            <input
              type="text"
              placeholder="搜索摄影师、模特、作品..."
              placeholder-class="text-slate-400"
              class="w-full h-10 rounded-xl bg-slate-100/80 pl-10 pr-4 text-sm text-slate-800"
            />
          </view>
          <!-- Notification -->
          <view
            class="relative flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100/80 text-slate-500 active:scale-95 transition-transform"
          >
            <view class="i-lucide-bell text-lg"></view>
            <view
              class="absolute top-2 right-2 h-2 w-2 rounded-full bg-rose-500 border-2 border-white"
            ></view>
          </view>
        </view>
      </view>
    </view>

    <scroll-view
      scroll-y
      class="flex-1 overflow-hidden"
      :show-scrollbar="false"
    >
      <view class="px-5 pt-5 pb-24 space-y-6">
        <!-- Hero Card - Photography themed -->
        <view
          class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-rose-400 to-violet-400 p-6 text-white"
        >
          <view
            class="absolute -right-8 -top-8 h-40 w-40 rounded-full bg-rose-500/10 blur-3xl"
          ></view>
          <view
            class="absolute -bottom-12 -left-12 h-32 w-32 rounded-full bg-rose-500/5 blur-2xl"
          ></view>

          <view class="relative z-10">
            <view class="mb-3 flex items-center space-x-2">
              <view class="i-lucide-camera text-rose-400 text-lg"></view>
              <text class="text-sm font-medium text-rose-400/90">今日精选</text>
            </view>
            <text class="text-2xl font-bold tracking-tight leading-tight"
              >发现你的专属摄影师</text
            >
            <text class="mt-2 text-sm text-slate-400 leading-relaxed"
              >专业约拍，让每一次拍摄都值得期待</text
            >
            <view class="mt-4 flex items-center space-x-3">
              <view
                class="rounded-xl bg-rose-500 px-5 py-2.5 text-sm font-semibold text-slate-900 active:scale-95 transition-transform"
              >
                立即预约
              </view>
              <view
                class="rounded-xl border border-slate-600 px-5 py-2.5 text-sm font-medium text-slate-300 active:scale-95 transition-transform"
              >
                浏览作品
              </view>
            </view>
          </view>
        </view>

        <!-- Stats Grid - Photography platform stats -->
        <view class="grid grid-cols-3 gap-3">
          <view
            class="rounded-2xl bg-white/80 backdrop-blur-sm p-3.5 flex flex-col items-center space-y-1.5"
          >
            <view
              class="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-50 text-rose-400"
            >
              <view class="i-lucide-camera text-lg"></view>
            </view>
            <text class="text-lg font-bold text-slate-800">128</text>
            <text class="text-[10px] text-slate-400">摄影师</text>
          </view>
          <view
            class="rounded-2xl bg-white/80 backdrop-blur-sm p-3.5 flex flex-col items-center space-y-1.5"
          >
            <view
              class="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-50 text-rose-500"
            >
              <view class="i-lucide-image text-lg"></view>
            </view>
            <text class="text-lg font-bold text-slate-800">2.4k</text>
            <text class="text-[10px] text-slate-400">作品集</text>
          </view>
          <view
            class="rounded-2xl bg-white/80 backdrop-blur-sm p-3.5 flex flex-col items-center space-y-1.5"
          >
            <view
              class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
            >
              <view class="i-lucide-calendar-check text-lg"></view>
            </view>
            <text class="text-lg font-bold text-slate-800">56</text>
            <text class="text-[10px] text-slate-400">今日预约</text>
          </view>
        </view>

        <!-- Quick Functions -->
        <view>
          <view class="mb-3 flex items-center justify-between">
            <text class="text-base font-bold tracking-tight text-slate-800"
              >快捷入口</text
            >
          </view>
          <view
            class="grid grid-cols-4 gap-3 rounded-2xl bg-white p-5"
          >
            <view
              class="flex flex-col items-center space-y-2 active:scale-95 transition-transform"
            >
              <view
                class="flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-50 text-rose-400"
              >
                <view class="i-lucide-camera text-xl"></view>
              </view>
              <text class="text-[11px] font-medium text-slate-600">预约拍摄</text>
            </view>
            <view
              class="flex flex-col items-center space-y-2 active:scale-95 transition-transform"
            >
              <view
                class="flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-50 text-rose-500"
              >
                <view class="i-lucide-heart text-xl"></view>
              </view>
              <text class="text-[11px] font-medium text-slate-600">我的收藏</text>
            </view>
            <view
              class="flex flex-col items-center space-y-2 active:scale-95 transition-transform"
            >
              <view
                class="flex h-12 w-12 items-center justify-center rounded-2xl bg-sky-50 text-sky-600"
              >
                <view class="i-lucide-bar-chart-3 text-xl"></view>
              </view>
              <text class="text-[11px] font-medium text-slate-600">数据统计</text>
            </view>
            <view
              class="flex flex-col items-center space-y-2 active:scale-95 transition-transform"
            >
              <view
                class="flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-50 text-violet-500"
              >
                <view class="i-lucide-message-circle text-xl"></view>
              </view>
              <text class="text-[11px] font-medium text-slate-600">消息</text>
            </view>
          </view>
        </view>

        <!-- Recent Activity -->
        <view>
          <view class="mb-3 flex items-center justify-between">
            <text class="text-base font-bold tracking-tight text-slate-800"
              >最近动态</text
            >
            <text class="text-xs text-slate-400">查看全部</text>
          </view>
          <view class="space-y-3">
            <view
              class="flex items-center rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform"
            >
              <view
                class="flex h-11 w-11 items-center justify-center rounded-xl bg-rose-50 text-rose-400 shrink-0"
              >
                <view class="i-lucide-camera text-lg"></view>
              </view>
              <view class="ml-3.5 flex-1 min-w-0">
                <text class="font-semibold text-sm text-slate-800">人像写真拍摄</text>
                <text class="mt-0.5 text-xs text-slate-400 block"
                  >摄影师: 林默 - 今日 14:00</text
                >
              </view>
              <view
                class="rounded-lg bg-rose-50 px-2.5 py-1 text-[10px] font-semibold text-amber-700 shrink-0"
                >待确认</view
              >
            </view>
            <view
              class="flex items-center rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform"
            >
              <view
                class="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 shrink-0"
              >
                <view class="i-lucide-check-circle text-lg"></view>
              </view>
              <view class="ml-3.5 flex-1 min-w-0">
                <text class="font-semibold text-sm text-slate-800">婚纱照修图完成</text>
                <text class="mt-0.5 text-xs text-slate-400 block"
                  >已交付 36 张精修照片</text
                >
              </view>
              <view
                class="rounded-lg bg-emerald-50 px-2.5 py-1 text-[10px] font-semibold text-emerald-700 shrink-0"
                >已完成</view
              >
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
const globalConfig = getApp().globalData.config;
</script>
