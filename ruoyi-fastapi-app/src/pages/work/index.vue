<template>
  <view class="flex h-full flex-col bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50 overflow-hidden">
    <scroll-view scroll-y class="flex-1" :show-scrollbar="false">
      <view class="px-5 pt-5 pb-24 space-y-6">
        <!-- Banner -->
        <view class="relative h-44 w-full overflow-hidden rounded-2xl">
          <swiper
            class="h-44 w-full"
            :current="swiperDotIndex"
            @change="changeSwiper"
            autoplay
            interval="3000"
            circular
          >
            <swiper-item v-for="(item, index) in data" :key="index">
              <view class="h-full w-full" @click="clickBannerItem(item)">
                <image
                  :src="item.image"
                  mode="scaleToFill"
                  class="block h-full w-full rounded-2xl"
                />
              </view>
            </swiper-item>
          </swiper>
          <view
            class="absolute bottom-3 right-0 left-0 flex justify-center space-x-1.5 pointer-events-none"
          >
            <view
              v-for="(item, index) in data"
              :key="index"
              class="h-1.5 rounded-full transition-all duration-300"
              :class="current === index ? 'bg-white w-5' : 'bg-white/40 w-1.5'"
            ></view>
          </view>
        </view>

        <!-- 智能工具 -->
        <view>
          <view class="mb-3 flex items-center space-x-2.5">
            <view class="h-4 w-1 rounded-full bg-rose-500"></view>
            <text class="text-base font-bold tracking-tight text-slate-800">智能工具</text>
          </view>
          <view class="grid grid-cols-2 gap-3">
            <view
              class="relative overflow-hidden rounded-2xl bg-white p-5 active:scale-[0.97] transition-transform"
              @click="handleToAiChat"
            >
              <view class="absolute -right-6 -top-6 size-24 rounded-full bg-rose-50 opacity-60"></view>
              <view class="relative z-10 flex flex-col">
                <view class="mb-3 flex size-11 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-500 to-amber-600 text-white shadow-lg shadow-amber-200/50">
                  <view class="i-lucide-message-circle text-xl"></view>
                </view>
                <text class="font-bold text-sm text-slate-800">智能助手</text>
                <text class="mt-1 text-[11px] text-slate-400">AI帮你匹配摄影师</text>
              </view>
            </view>
            <view
              class="relative overflow-hidden rounded-2xl bg-white p-5 active:scale-[0.97] transition-transform"
              @click="handleToPortfolio"
            >
              <view class="absolute -right-6 -top-6 size-24 rounded-full bg-rose-50 opacity-60"></view>
              <view class="relative z-10 flex flex-col">
                <view class="mb-3 flex size-11 items-center justify-center rounded-2xl bg-gradient-to-br from-rose-500 to-rose-600 text-white shadow-lg shadow-rose-200/50">
                  <view class="i-lucide-images text-xl"></view>
                </view>
                <text class="font-bold text-sm text-slate-800">作品广场</text>
                <text class="mt-1 text-[11px] text-slate-400">浏览精选作品</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 约拍服务 -->
        <view>
          <view class="mb-3 flex items-center space-x-2.5">
            <view class="h-4 w-1 rounded-full bg-slate-800"></view>
            <text class="text-base font-bold tracking-tight text-slate-800">约拍服务</text>
          </view>
          <view class="rounded-2xl bg-white/80 backdrop-blur-sm p-5">
            <view class="flex flex-wrap justify-between gap-y-5">
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToBooking"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-rose-50 text-rose-400">
                  <view class="i-lucide-camera text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">预约拍摄</text>
              </view>
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToDemand"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-sky-50 text-sky-600">
                  <view class="i-lucide-megaphone text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">发布需求</text>
              </view>
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToPhotographers"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600">
                  <view class="i-lucide-users text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">找摄影师</text>
              </view>
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToModels"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-violet-50 text-violet-500">
                  <view class="i-lucide-user-cog text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">找模特</text>
              </view>
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToOrders"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-rose-50 text-rose-500">
                  <view class="i-lucide-clipboard-list text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">我的订单</text>
              </view>
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToRanking"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-orange-50 text-orange-500">
                  <view class="i-lucide-bar-chart-3 text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">排行榜</text>
              </view>
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToCoupons"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-pink-50 text-pink-500">
                  <view class="i-lucide-ticket text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">优惠券</text>
              </view>
              <view
                class="w-[22%] flex flex-col items-center space-y-1.5 active:scale-95 transition-transform"
                @click="handleToMore"
              >
                <view class="flex size-11 items-center justify-center rounded-2xl bg-slate-100 text-slate-400">
                  <view class="i-lucide-more-horizontal text-lg"></view>
                </view>
                <text class="text-[11px] font-medium text-slate-600">更多</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 热门摄影师 -->
        <view>
          <view class="mb-3 flex items-center justify-between">
            <view class="flex items-center space-x-2.5">
              <view class="h-4 w-1 rounded-full bg-rose-500"></view>
              <text class="text-base font-bold tracking-tight text-slate-800">热门摄影师</text>
            </view>
            <text class="text-xs text-slate-400" @click="handleToPhotographers">查看全部</text>
          </view>
          <scroll-view scroll-x class="whitespace-nowrap" :show-scrollbar="false">
            <view class="inline-flex space-x-3">
              <view
                v-for="item in photographers"
                :key="item.name"
                class="inline-block w-36 rounded-2xl bg-white p-3 active:scale-[0.97] transition-transform"
                @click="handleToPhotographerDetail(item)"
              >
                <view class="flex items-center space-x-2.5 mb-2.5">
                  <view class="size-10 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white font-bold text-sm">
                    {{ item.name[0] }}
                  </view>
                  <view class="flex-1 min-w-0">
                    <text class="text-sm font-semibold text-slate-800 block truncate">{{ item.name }}</text>
                    <text class="text-[10px] text-slate-400 block">{{ item.type }}</text>
                  </view>
                </view>
                <view class="flex items-center justify-between">
                  <text class="text-[10px] text-slate-400">{{ item.city }}</text>
                  <view class="flex items-center space-x-0.5">
                    <view class="i-lucide-star text-rose-400 text-[10px]"></view>
                    <text class="text-[10px] font-medium text-slate-600">{{ item.rating }}</text>
                  </view>
                </view>
              </view>
            </view>
          </scroll-view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance();
const current = ref(0);
const swiperDotIndex = ref(0);

const data = ref([
  { image: "/static/images/banner/banner01.jpg" },
  { image: "/static/images/banner/banner02.jpg" },
  { image: "/static/images/banner/banner03.jpg" },
]);

const photographers = ref([
  { name: "林默", type: "人像摄影", city: "北京", rating: "4.9" },
  { name: "苏晴", type: "婚纱摄影", city: "上海", rating: "4.8" },
  { name: "陈风", type: "商业摄影", city: "广州", rating: "4.7" },
  { name: "叶知秋", type: "写真摄影", city: "成都", rating: "4.9" },
  { name: "白鹭", type: "古风摄影", city: "杭州", rating: "4.8" },
]);

function clickBannerItem(item) {
  console.info(item);
}

function changeSwiper(e) {
  current.value = e.detail.current;
}

function handleToAiChat() { proxy.$tab.navigateTo('/pages/message/index'); }
function handleToPortfolio() { proxy.$tab.navigateTo('/pages/works/index'); }
function handleToBooking() { proxy.$tab.navigateTo('/pages/publish/index'); }
function handleToDemand() { proxy.$tab.navigateTo('/pages/demand/index'); }
function handleToPhotographers() { proxy.$tab.navigateTo('/pages/photographer/index'); }
function handleToModels() { proxy.$tab.navigateTo('/pages/model/index'); }
function handleToOrders() { proxy.$tab.navigateTo('/pages/order/index'); }
function handleToRanking() { proxy.$tab.navigateTo('/pages/works/index'); }
function handleToCoupons() { proxy.$tab.navigateTo('/pages/wallet/index'); }
function handleToMore() { handleBuilding(); }
function handleToPhotographerDetail(item) { handleBuilding(); }

function handleBuilding() {
  proxy.$modal.msg("模块建设中~");
}
</script>
