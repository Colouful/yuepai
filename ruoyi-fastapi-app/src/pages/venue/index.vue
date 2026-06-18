<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">拍摄场地</text>
      <view class="mt-3 flex space-x-2">
        <view v-for="tab in tabs" :key="tab" class="rounded-full px-4 py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-500'"
          @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="v in venues" :key="v.name"
          class="rounded-2xl bg-white overflow-hidden active:scale-[0.98] transition-transform">
          <view class="h-36 bg-gradient-to-br from-slate-200 to-slate-300"></view>
          <view class="p-4">
            <text class="text-sm font-bold text-slate-800">{{ v.name }}</text>
            <text class="text-xs text-slate-400 block mt-0.5">{{ v.type }} · {{ v.city }}</text>
            <view class="mt-2 flex items-center justify-between">
              <view class="flex items-center space-x-1">
                <view class="i-lucide-star text-amber-400 text-[10px]"></view>
                <text class="text-[10px] font-medium text-slate-600">{{ v.rating }}</text>
                <text class="text-[10px] text-slate-400">· {{ v.reviews }}条评价</text>
              </view>
              <text class="text-sm font-bold text-amber-600">¥{{ v.price }}/小时</text>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const tabs = ["全部", "摄影棚", "咖啡馆", "民宿", "户外"];
const activeTab = ref("全部");
const venues = ref([
  { name: "光圈摄影棚", type: "摄影棚", city: "北京朝阳", rating: "4.9", reviews: 128, price: 200 },
  { name: "花间集民宿", type: "民宿", city: "杭州西湖", rating: "4.8", reviews: 89, price: 150 },
  { name: "拾光咖啡馆", type: "咖啡馆", city: "上海静安", rating: "4.7", reviews: 56, price: 80 },
]);
</script>