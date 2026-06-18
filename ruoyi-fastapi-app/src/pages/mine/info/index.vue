<template>
  <view class="flex h-full flex-col overflow-y-auto bg-stone-50 pt-4 pb-10">
    <view class="mx-5 overflow-hidden rounded-2xl bg-white">
      <!-- Nickname -->
      <view
        class="flex items-center justify-between border-b border-slate-100 px-5 py-4 active:bg-slate-50 transition-colors"
      >
        <view class="flex items-center">
          <view
            class="flex size-9 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
          >
            <view class="i-lucide-user text-lg"></view>
          </view>
          <text class="ml-3 text-[15px] text-slate-700">昵称</text>
        </view>
        <text class="text-sm text-slate-400">{{ user.nickName }}</text>
      </view>

      <!-- Phone -->
      <view
        class="flex items-center justify-between border-b border-slate-100 px-5 py-4 active:bg-slate-50 transition-colors"
      >
        <view class="flex items-center">
          <view
            class="flex size-9 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
          >
            <view class="i-lucide-phone text-lg"></view>
          </view>
          <text class="ml-3 text-[15px] text-slate-700">手机号码</text>
        </view>
        <text class="text-sm text-slate-400">{{ user.phonenumber }}</text>
      </view>

      <!-- Email -->
      <view
        class="flex items-center justify-between border-b border-slate-100 px-5 py-4 active:bg-slate-50 transition-colors"
      >
        <view class="flex items-center">
          <view
            class="flex size-9 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
          >
            <view class="i-lucide-mail text-lg"></view>
          </view>
          <text class="ml-3 text-[15px] text-slate-700">邮箱</text>
        </view>
        <text class="text-sm text-slate-400">{{ user.email }}</text>
      </view>

      <!-- Post -->
      <view
        class="flex items-center justify-between border-b border-slate-100 px-5 py-4 active:bg-slate-50 transition-colors"
      >
        <view class="flex items-center">
          <view
            class="flex size-9 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
          >
            <view class="i-lucide-shield-user text-lg"></view>
          </view>
          <text class="ml-3 text-[15px] text-slate-700">岗位</text>
        </view>
        <text class="text-sm text-slate-400">{{ postGroup }}</text>
      </view>

      <!-- Role -->
      <view
        class="flex items-center justify-between border-b border-slate-100 px-5 py-4 active:bg-slate-50 transition-colors"
      >
        <view class="flex items-center">
          <view
            class="flex size-9 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
          >
            <view class="i-lucide-user-cog text-lg"></view>
          </view>
          <text class="ml-3 text-[15px] text-slate-700">角色</text>
        </view>
        <text class="text-sm text-slate-400">{{ roleGroup }}</text>
      </view>

      <!-- Create Time -->
      <view
        class="flex items-center justify-between px-5 py-4 active:bg-slate-50 transition-colors"
      >
        <view class="flex items-center">
          <view
            class="flex size-9 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
          >
            <view class="i-lucide-calendar text-lg"></view>
          </view>
          <text class="ml-3 text-[15px] text-slate-700">创建日期</text>
        </view>
        <text class="text-sm text-slate-400">{{ user.createTime }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { getUserProfile } from "@/api/system/user";
import { ref } from "vue";

const user = ref({});
const roleGroup = ref("");
const postGroup = ref("");

function getUser() {
  getUserProfile().then((response) => {
    user.value = response.data;
    roleGroup.value = response.roleGroup;
    postGroup.value = response.postGroup;
  });
}

getUser();
</script>

<style>
page {
  height: 100%;
  background-color: #f5f5f4;
}
</style>
