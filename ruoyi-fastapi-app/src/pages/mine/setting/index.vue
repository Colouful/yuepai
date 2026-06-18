<template>
  <view class="flex h-full flex-col overflow-y-auto bg-stone-50 pt-4 pb-10">
    <view class="mx-5 bg-white rounded-2xl overflow-hidden">
      <!-- Change Password -->
      <view
        class="flex items-center justify-between border-b border-slate-100 px-5 py-4 active:bg-slate-50 transition-colors"
        @click="handleToPwd"
      >
        <view class="flex items-center">
          <view class="i-lucide-lock text-lg text-slate-500 mr-3.5"></view>
          <text class="text-[15px] text-slate-700">修改密码</text>
        </view>
        <view class="i-lucide-chevron-right text-base text-slate-300"></view>
      </view>

      <!-- Check Update -->
      <view
        class="flex items-center justify-between border-b border-slate-100 px-5 py-4 active:bg-slate-50 transition-colors"
        @click="handleToUpgrade"
      >
        <view class="flex items-center">
          <view class="i-lucide-refresh-cw text-lg text-slate-500 mr-3.5"></view>
          <text class="text-[15px] text-slate-700">检查更新</text>
        </view>
        <view class="i-lucide-chevron-right text-base text-slate-300"></view>
      </view>

      <!-- Clean Cache -->
      <view
        class="flex items-center justify-between px-5 py-4 active:bg-slate-50 transition-colors"
        @click="handleCleanTmp"
      >
        <view class="flex items-center">
          <view class="i-lucide-trash-2 text-lg text-slate-500 mr-3.5"></view>
          <text class="text-[15px] text-slate-700">清理缓存</text>
        </view>
        <view class="i-lucide-chevron-right text-base text-slate-300"></view>
      </view>
    </view>

    <!-- Logout -->
    <view class="mt-8 px-5">
      <view
        class="flex h-12 w-full items-center justify-center rounded-2xl bg-white text-base font-semibold text-slate-700 transition-colors active:bg-slate-100"
        @click="handleLogout"
        >退出登录</view
      >
    </view>
  </view>
</template>

<script setup>
import { useUserStore } from "@/store";
import { getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance();

function handleToPwd() {
  proxy.$tab.navigateTo("/pages/mine/pwd/index");
}

function handleToUpgrade() {
  proxy.$modal.showToast("模块建设中~");
}

function handleCleanTmp() {
  proxy.$modal.showToast("模块建设中~");
}

function handleLogout() {
  proxy.$modal.confirm("确定注销并退出系统吗？").then(() => {
    useUserStore()
      .logOut()
      .then(() => {})
      .finally(() => {
        proxy.$tab.reLaunch("/pages/index");
      });
  });
}
</script>

<style>
page {
  height: 100%;
  background-color: #f5f5f4;
}
</style>
