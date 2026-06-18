<template>
  <view
    class="flex h-full flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-stone-100 px-6 pb-20 overflow-hidden"
  >
    <!-- Logo Section -->
    <view class="mb-8 flex flex-col items-center">
      <view
        class="mb-4 flex size-16 items-center justify-center rounded-2xl bg-white shadow-lg shadow-slate-200/50"
      >
        <image
          class="size-10"
          :src="globalConfig.appInfo.logo"
          mode="widthFix"
        />
      </view>
      <text class="text-xl font-bold tracking-tight text-slate-800"
        >创建账号</text
      >
      <text class="mt-1 text-sm text-slate-400">加入约拍社区</text>
    </view>

    <!-- Form Section -->
    <view class="w-full rounded-2xl bg-white p-6 shadow-lg shadow-slate-200/30">
      <!-- Username -->
      <view class="group relative mb-4">
        <view
          class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-amber-500"
        >
          <view class="i-lucide-user text-lg"></view>
        </view>
        <input
          v-model="registerForm.username"
          class="h-12 w-full rounded-xl bg-slate-50 pl-11 pr-4 text-sm text-slate-700 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-amber-400/50"
          type="text"
          placeholder="请输入账号"
          maxlength="30"
        />
      </view>

      <!-- Password -->
      <view class="group relative mb-4">
        <view
          class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-amber-500"
        >
          <view class="i-lucide-lock text-lg"></view>
        </view>
        <input
          v-model="registerForm.password"
          type="password"
          class="h-12 w-full rounded-xl bg-slate-50 pl-11 pr-4 text-sm text-slate-700 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-amber-400/50"
          placeholder="请输入密码"
          maxlength="20"
        />
      </view>

      <!-- Confirm Password -->
      <view class="group relative mb-4">
        <view
          class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-amber-500"
        >
          <view class="i-lucide-lock text-lg"></view>
        </view>
        <input
          v-model="registerForm.confirmPassword"
          type="password"
          class="h-12 w-full rounded-xl bg-slate-50 pl-11 pr-4 text-sm text-slate-700 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-amber-400/50"
          placeholder="请输入重复密码"
          maxlength="20"
        />
      </view>

      <!-- Captcha -->
      <view
        class="mb-6 flex items-center justify-between"
        v-if="captchaEnabled"
      >
        <view class="group relative mr-3 flex-1">
          <view
            class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-amber-500"
          >
            <view class="i-lucide-shield-check text-lg"></view>
          </view>
          <input
            v-model="registerForm.code"
            type="number"
            class="h-12 w-full rounded-xl bg-slate-50 pl-11 pr-4 text-sm text-slate-700 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-amber-400/50"
            placeholder="验证码"
            maxlength="4"
          />
        </view>
        <view
          class="h-12 w-28 overflow-hidden rounded-xl bg-slate-100 transition-opacity active:opacity-80"
          @click="getCode"
        >
          <image :src="codeUrl" class="size-full object-cover"></image>
        </view>
      </view>

      <!-- Register Button -->
      <button
        @click="handleRegister"
        class="flex h-12 w-full items-center justify-center rounded-xl bg-gradient-to-r from-slate-800 to-slate-900 text-base font-semibold text-white active:scale-[0.98] transition-transform"
      >
        注 册
      </button>

      <!-- Footer Links -->
      <view class="mt-5 flex flex-col items-center space-y-3">
        <view class="flex items-center text-sm text-slate-400">
          <text
            @click="handleUserLogin"
            class="font-medium text-slate-700 active:opacity-70"
            >使用已有账号登录</text
          >
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { getCodeImg, register } from "@/api/login";
import { ref, getCurrentInstance } from "vue";
import { useConfigStore } from "@/store";

const { proxy } = getCurrentInstance();
const globalConfig = useConfigStore().config;
const codeUrl = ref("");
// 验证码开关
const captchaEnabled = ref(true);
const registerForm = ref({
  username: "",
  password: "",
  confirmPassword: "",
  code: "",
  uuid: "",
});

// 用户登录
function handleUserLogin() {
  proxy.$tab.navigateTo(`/pages/login`);
}

// 获取图形验证码
function getCode() {
  getCodeImg().then((res) => {
    captchaEnabled.value =
      res.captchaEnabled === undefined ? true : res.captchaEnabled;
    if (captchaEnabled.value) {
      codeUrl.value = "data:image/gif;base64," + res.img;
      registerForm.value.uuid = res.uuid;
    }
  });
}

// 注册方法
async function handleRegister() {
  if (registerForm.value.username === "") {
    proxy.$modal.msgError("请输入您的账号");
  } else if (registerForm.value.password === "") {
    proxy.$modal.msgError("请输入您的密码");
  } else if (registerForm.value.confirmPassword === "") {
    proxy.$modal.msgError("请再次输入您的密码");
  } else if (
    registerForm.value.password !== registerForm.value.confirmPassword
  ) {
    proxy.$modal.msgError("两次输入的密码不一致");
  } else if (registerForm.value.code === "" && captchaEnabled.value) {
    proxy.$modal.msgError("请输入验证码");
  } else {
    proxy.$modal.loading("注册中，请耐心等待...");
    userRegister();
  }
}

// 用户注册
async function userRegister() {
  register(registerForm.value)
    .then((res) => {
      proxy.$modal.closeLoading();
      uni.showModal({
        title: "系统提示",
        content:
          "恭喜你，您的账号 " + registerForm.value.username + " 注册成功！",
        success: function (res) {
          if (res.confirm) {
            uni.redirectTo({ url: `/pages/login` });
          }
        },
      });
    })
    .catch(() => {
      if (captchaEnabled.value) {
        getCode();
      }
    });
}

getCode();
</script>

<style lang="scss" scoped>
page {
  background-color: #f5f5f4;
  height: 100%;
}
</style>
