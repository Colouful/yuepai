<template>
  <view class="flex h-full flex-col bg-gradient-to-br from-rose-50 via-pink-50 to-violet-50 overflow-hidden">
    <!-- Header Section -->
    <view
      class="relative overflow-hidden bg-gradient-to-br from-rose-400 to-violet-400 pb-20 pt-16"
    >
      <view
        class="absolute -right-10 -top-10 size-64 rounded-full bg-rose-500/8 blur-3xl"
      ></view>
      <view
        class="absolute -bottom-10 -left-10 size-40 rounded-full bg-rose-500/5 blur-2xl"
      ></view>

      <view class="relative z-10 flex items-center justify-between px-6">
        <view class="flex items-center space-x-4">
          <!-- Avatar -->
          <view
            class="relative overflow-hidden rounded-full border-2 border-white/20 bg-white/10 transition-transform active:scale-95"
          >
            <image
              v-if="avatar"
              @click="handleToAvatar"
              :src="avatar"
              class="size-20 object-cover"
            />
            <view
              v-else
              class="flex size-20 items-center justify-center bg-white/10 text-slate-400"
            >
              <view class="i-lucide-user text-5xl"></view>
            </view>
          </view>

          <!-- User Info -->
          <view class="flex flex-col">
            <template v-if="name">
              <text
                class="text-xl font-bold tracking-tight text-white"
                @click="handleToInfo"
              >
                {{ name }}
              </text>
              <view
                class="mt-1 flex items-center text-sm text-slate-400"
                @click="handleToInfo"
              >
                <text>查看个人信息</text>
                <view class="i-lucide-chevron-right ml-1 text-xs"></view>
              </view>
            </template>
            <view v-else class="text-xl font-bold text-white" @click="handleToLogin">
              点击登录
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- Content Section -->
    <view class="relative z-20 -mt-12 flex-1 px-5 overflow-y-auto">
      <!-- Quick Actions -->
      <view
        class="mb-5 flex items-center justify-between rounded-2xl bg-white p-5"
      >
        <view
          class="flex flex-1 flex-col items-center justify-center space-y-2 active:scale-95 transition-transform"
          @click="handleJiaoLiuQun"
        >
          <view
            class="flex size-12 items-center justify-center rounded-2xl bg-rose-50 text-rose-500"
          >
            <view class="i-lucide-users text-xl"></view>
          </view>
          <text class="text-[11px] font-medium text-slate-600">交流群</text>
        </view>
        <view
          class="flex flex-1 flex-col items-center justify-center space-y-2 active:scale-95 transition-transform"
          @click="handleBuilding"
        >
          <view
            class="flex size-12 items-center justify-center rounded-2xl bg-sky-50 text-sky-600"
          >
            <view class="i-lucide-headphones text-xl"></view>
          </view>
          <text class="text-[11px] font-medium text-slate-600">在线客服</text>
        </view>
        <view
          class="flex flex-1 flex-col items-center justify-center space-y-2 active:scale-95 transition-transform"
          @click="handleBuilding"
        >
          <view
            class="flex size-12 items-center justify-center rounded-2xl bg-violet-50 text-violet-500"
          >
            <view class="i-lucide-message-square text-xl"></view>
          </view>
          <text class="text-[11px] font-medium text-slate-600">反馈社区</text>
        </view>
        <view
          class="flex flex-1 flex-col items-center justify-center space-y-2 active:scale-95 transition-transform"
          @click="handleBuilding"
        >
          <view
            class="flex size-12 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600"
          >
            <view class="i-lucide-thumbs-up text-xl"></view>
          </view>
          <text class="text-[11px] font-medium text-slate-600">点赞我们</text>
        </view>
      </view>

      <!-- Menu List -->
      <view
        class="overflow-hidden rounded-2xl bg-white"
      >
        <view
          class="group flex items-center justify-between border-b border-slate-100 p-4 active:bg-slate-50 transition-colors"
          @click="handleToEditInfo"
        >
          <view class="flex items-center space-x-3.5">
            <view class="i-lucide-user-pen text-lg text-slate-500"></view>
            <text class="text-[15px] text-slate-700">编辑资料</text>
          </view>
          <view class="i-lucide-chevron-right text-slate-300"></view>
        </view>

        <view
          class="group flex items-center justify-between border-b border-slate-100 p-4 active:bg-slate-50 transition-colors"
          @click="handleHelp"
        >
          <view class="flex items-center space-x-3.5">
            <view class="i-lucide-circle-help text-lg text-slate-500"></view>
            <text class="text-[15px] text-slate-700">常见问题</text>
          </view>
          <view class="i-lucide-chevron-right text-slate-300"></view>
        </view>

        <view
          class="group flex items-center justify-between border-b border-slate-100 p-4 active:bg-slate-50 transition-colors"
          @click="handleAbout"
        >
          <view class="flex items-center space-x-3.5">
            <view class="i-lucide-heart text-lg text-slate-500"></view>
            <text class="text-[15px] text-slate-700">关于我们</text>
          </view>
          <view class="i-lucide-chevron-right text-slate-300"></view>
        </view>

        <view
          class="group flex items-center justify-between p-4 active:bg-slate-50 transition-colors"
          @click="handleToSetting"
        >
          <view class="flex items-center space-x-3.5">
            <view class="i-lucide-settings text-lg text-slate-500"></view>
            <text class="text-[15px] text-slate-700">应用设置</text>
          </view>
          <view class="i-lucide-chevron-right text-slate-300"></view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { useUserStore } from "@/store";
import { computed, getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance();
const userStore = useUserStore();

const name = computed(() => userStore.name);
const avatar = computed(() => userStore.avatar);
const windowHeight = computed(() => uni.getSystemInfoSync().windowHeight - 50);

function handleToInfo() {
  proxy.$tab.navigateTo("/pages/mine/info/index");
}

function handleToEditInfo() {
  proxy.$tab.navigateTo("/pages/mine/info/edit");
}

function handleToSetting() {
  proxy.$tab.navigateTo("/pages/mine/setting/index");
}

function handleToLogin() {
  proxy.$tab.reLaunch("/pages/login");
}

function handleToAvatar() {
  proxy.$tab.navigateTo("/pages/mine/avatar/index");
}

function handleHelp() {
  proxy.$tab.navigateTo("/pages/mine/help/index");
}

function handleAbout() {
  proxy.$tab.navigateTo("/pages/mine/about/index");
}

function handleJiaoLiuQun() {
  proxy.$tab.navigateTo('/pages/message/index');
}

function handleBuilding() {
  proxy.$modal.showToast("模块建设中~");
}
</script>
