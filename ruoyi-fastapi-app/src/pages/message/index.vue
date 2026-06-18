<template>
  <view class="min-h-screen" style="background:linear-gradient(180deg,#ECFDF5 0%,#FFFFFF 40%,#F5F3FF 100%)">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-2 pb-3">
      <text class="text-[22px] font-black tracking-tight" style="background:linear-gradient(135deg,#34D399,#38BDF8);-webkit-background-clip:text;-webkit-text-fill-color:transparent">消息</text>
    </view>
    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-24 space-y-2.5">
        <!-- 系统通知 -->
        <view class="rounded-2xl p-4 text-white flex items-center active:scale-[0.98] transition-transform duration-200" style="background:linear-gradient(135deg,#F472B6,#A78BFA);box-shadow:0 8px 30px rgba(244,114,182,0.2)">
          <view class="size-12 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center mr-3">
            <view class="i-lucide-bell text-2xl text-white"></view>
          </view>
          <view class="flex-1">
            <text class="text-sm font-bold block">系统通知</text>
            <text class="text-xs opacity-80 block mt-0.5">您的摄影师认证已通过</text>
          </view>
          <view class="size-5 rounded-full bg-white/30 flex items-center justify-center text-[10px] font-bold">3</view>
        </view>

        <!-- 对话列表 -->
        <view v-for="m in messages" :key="m.name" class="rounded-2xl bg-white p-4 flex items-center space-x-3 active:scale-[0.98] transition-transform duration-200" style="box-shadow:0 2px 12px rgba(52,211,153,0.06)">
          <view class="relative shrink-0">
            <view class="size-12 rounded-2xl flex items-center justify-center text-white font-bold" :style="{background:m.bg}">{{ m.name[0] }}</view>
            <view v-if="m.unread" class="absolute -top-0.5 -right-0.5 size-3 rounded-full bg-rose-400 border-2 border-white"></view>
          </view>
          <view class="flex-1 min-w-0">
            <view class="flex items-center justify-between">
              <text class="text-sm font-bold text-slate-800">{{ m.name }}</text>
              <text class="text-[10px] text-slate-300">{{ m.time }}</text>
            </view>
            <text class="text-xs text-slate-400 block mt-0.5 truncate">{{ m.last }}</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref } from "vue";
const statusBarH = ref(44); const scrollH = ref(600);
try { const s=uni.getSystemInfoSync(); statusBarH.value=s.statusBarHeight||44; scrollH.value=s.windowHeight-statusBarH.value-80; } catch(e){}
const messages = ref([
  { name:"林默", last:"好的，周六下午2点见！", time:"刚刚", unread:true, bg:"linear-gradient(135deg,#F472B6,#EC4899)" },
  { name:"苏晴", last:"作品修好了，看看效果", time:"10分钟前", unread:true, bg:"linear-gradient(135deg,#A78BFA,#8B5CF6)" },
  { name:"小雨", last:"套餐包含化妆吗？", time:"1小时前", unread:false, bg:"linear-gradient(135deg,#38BDF8,#0EA5E9)" },
  { name:"陈风", last:"感谢好评！期待下次", time:"昨天", unread:false, bg:"linear-gradient(135deg,#34D399,#10B981)" },
  { name:"白鹭", last:"古风服装我准备", time:"昨天", unread:false, bg:"linear-gradient(135deg,#FBBF24,#F59E0B)" },
  { name:"叶知秋", last:"定金已收，档期保留", time:"2天前", unread:false, bg:"linear-gradient(135deg,#FB923C,#F97316)" },
]);
</script>
