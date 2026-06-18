<template>
  <view class="flex h-full flex-col bg-stone-50">
    <view class="bg-white px-5 pt-12 pb-3">
      <text class="text-xl font-bold tracking-tight text-slate-900">需求大厅</text>
      <view class="mt-3 flex space-x-2">
        <view v-for="tab in tabs" :key="tab" class="rounded-full px-4 py-1.5 text-xs font-medium transition-colors"
          :class="activeTab === tab ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-500'"
          @click="activeTab = tab">{{ tab }}</view>
      </view>
    </view>
    <scroll-view scroll-y class="flex-1 px-5 pt-4 pb-24" :show-scrollbar="false">
      <view class="space-y-3">
        <view v-for="item in demands" :key="item.title"
          class="rounded-2xl bg-white p-4 active:scale-[0.98] transition-transform">
          <view class="flex items-start justify-between">
            <view class="flex-1">
              <view class="flex items-center space-x-2">
                <view class="rounded-md px-1.5 py-0.5 text-[10px] font-semibold"
                  :class="item.mutual ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'">
                  {{ item.mutual ? '互勉' : '付费' }}</view>
                <text class="font-bold text-sm text-slate-800">{{ item.title }}</text>
              </view>
              <text class="mt-1.5 text-xs text-slate-400 block">{{ item.type }} · {{ item.city }}</text>
              <text class="mt-1 text-xs text-slate-400 block">{{ item.date }}</text>
            </view>
            <text class="text-base font-bold text-amber-600">{{ item.budget }}</text>
          </view>
          <view class="mt-3 flex items-center justify-between">
            <view class="flex items-center space-x-1.5">
              <view class="size-6 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white text-[10px] font-bold">{{ item.user[0] }}</view>
              <text class="text-xs text-slate-400">{{ item.user }}</text>
            </view>
            <text class="text-[10px] text-slate-300">{{ item.apply }}人报名</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const tabs = ["全部", "人像", "婚纱", "写真", "旅拍", "互勉"];
const activeTab = ref("全部");
const demands = ref([
  { title: "周末人像写真拍摄", type: "人像摄影", city: "北京朝阳", date: "6月20日 14:00", budget: "¥500", user: "小雨", apply: 12, mutual: false },
  { title: "古风汉服互勉创作", type: "古风摄影", city: "杭州西湖", date: "6月22日 全天", budget: "互勉", user: "苏晴", apply: 8, mutual: true },
  { title: "婚纱照拍摄招募", type: "婚纱摄影", city: "上海外滩", date: "6月25日 上午", budget: "¥2000", user: "陈先生", apply: 5, mutual: false },
  { title: "JK制服写真", type: "JK摄影", city: "成都春熙路", date: "6月21日 15:00", budget: "¥300", user: "叶知秋", apply: 15, mutual: false },
  { title: "宠物家庭照", type: "宠物摄影", city: "广州天河", date: "6月23日 上午", budget: "¥400", user: "白鹭", apply: 6, mutual: false },
]);
</script>