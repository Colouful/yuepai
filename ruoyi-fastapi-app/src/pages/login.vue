<template>
  <view class="flex h-full flex-col items-center justify-center bg-stone-50 px-6 pb-16 overflow-hidden">
    <view class="mb-8 flex flex-col items-center">
      <view class="mb-4 flex size-16 items-center justify-center rounded-2xl bg-white shadow-lg shadow-zinc-200/50">
        <image class="size-10" :src="globalConfig.appInfo.logo" mode="widthFix" />
      </view>
      <text class="text-xl font-black tracking-tight text-zinc-900">欢迎来到{{ globalConfig.appInfo.name }}</text>
      <text class="mt-1 text-sm text-zinc-400">登录后管理约拍、订单与作品</text>
    </view>

    <view class="w-full rounded-3xl bg-white p-6 shadow-lg shadow-zinc-200/30">
      <view class="relative mb-4">
        <view class="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400">
          <view class="i-lucide-user text-lg"></view>
        </view>
        <input
          v-model.trim="loginForm.username"
          class="h-12 w-full rounded-xl bg-zinc-50 pl-11 pr-4 text-sm text-zinc-800"
          type="text"
          placeholder="请输入账号"
          maxlength="30"
        />
      </view>

      <view class="relative mb-4">
        <view class="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400">
          <view class="i-lucide-lock text-lg"></view>
        </view>
        <input
          v-model="loginForm.password"
          type="password"
          class="h-12 w-full rounded-xl bg-zinc-50 pl-11 pr-4 text-sm text-zinc-800"
          placeholder="请输入密码"
          maxlength="64"
          @confirm="handleLogin"
        />
      </view>

      <view v-if="captchaEnabled" class="mb-6 flex items-center justify-between">
        <view class="relative mr-3 flex-1">
          <view class="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400">
            <view class="i-lucide-shield-check text-lg"></view>
          </view>
          <input
            v-model.trim="loginForm.code"
            type="text"
            class="h-12 w-full rounded-xl bg-zinc-50 pl-11 pr-4 text-sm text-zinc-800"
            placeholder="验证码"
            maxlength="6"
            @confirm="handleLogin"
          />
        </view>
        <view class="h-12 w-28 overflow-hidden rounded-xl bg-zinc-100 active:opacity-80" @click="getCode">
          <image v-if="codeUrl" :src="codeUrl" class="size-full" mode="aspectFill" />
          <view v-else class="size-full flex items-center justify-center text-[10px] text-zinc-400">点击刷新</view>
        </view>
      </view>

      <button
        class="flex h-12 w-full items-center justify-center rounded-xl bg-zinc-900 text-base font-semibold text-white"
        :disabled="submitting"
        @click="handleLogin"
      >
        <view v-if="submitting" class="i-svg-spinners-180-ring mr-2 text-lg"></view>
        {{ submitting ? "登录中" : "登录" }}
      </button>

      <button
        class="mt-3 flex h-12 w-full items-center justify-center rounded-xl bg-zinc-100 text-sm font-semibold text-zinc-700"
        @click="browseAsGuest"
      >
        游客浏览
      </button>

      <view class="mt-5 flex flex-col items-center space-y-3">
        <view v-if="register" class="flex items-center text-sm text-zinc-400">
          <text>没有账号？</text>
          <text class="ml-1 font-medium text-zinc-800" @click="handleUserRegister">立即注册</text>
        </view>
        <view class="flex flex-wrap items-center justify-center text-xs text-zinc-400">
          <text>登录即代表同意</text>
          <text class="mx-1 text-zinc-700" @click="openAgreement(globalConfig.appInfo.agreements[1])">《用户协议》</text>
          <text>和</text>
          <text class="mx-1 text-zinc-700" @click="openAgreement(globalConfig.appInfo.agreements[0])">《隐私政策》</text>
        </view>
      </view>
    </view>

    <text class="mt-5 text-[10px] text-zinc-400">微信授权和手机号验证码登录将在生产账号体系完成后开放</text>
  </view>
</template>

<script setup>
import { getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getCodeImg } from "@/api/login";
import { getToken } from "@/utils/auth";
import { useConfigStore, useUserStore } from "@/store";

const { proxy } = getCurrentInstance();
const globalConfig = useConfigStore().config;
const codeUrl = ref("");
const captchaEnabled = ref(true);
const register = ref(false);
const submitting = ref(false);
const loginForm = ref({
  username: "",
  password: "",
  code: "",
  uuid: "",
});

function handleUserRegister() {
  proxy.$tab.redirectTo("/pages/register");
}

function openAgreement(agreement) {
  if (!agreement?.url) {
    proxy.$modal.msgError("协议地址尚未配置，请联系平台管理员");
    return;
  }
  proxy.$tab.navigateTo(`/pages/common/webview/index?url=${encodeURIComponent(agreement.url)}&title=${encodeURIComponent(agreement.title)}`);
}

async function getCode() {
  try {
    const res = await getCodeImg();
    captchaEnabled.value = res.captchaEnabled === undefined ? true : res.captchaEnabled;
    if (captchaEnabled.value) {
      codeUrl.value = `data:image/gif;base64,${res.img}`;
      loginForm.value.uuid = res.uuid;
    }
  } catch (error) {
    console.error("获取验证码失败", error);
  }
}

async function handleLogin() {
  if (submitting.value) return;
  if (!loginForm.value.username) {
    proxy.$modal.msgError("请输入账号");
    return;
  }
  if (!loginForm.value.password) {
    proxy.$modal.msgError("请输入密码");
    return;
  }
  if (!loginForm.value.code && captchaEnabled.value) {
    proxy.$modal.msgError("请输入验证码");
    return;
  }

  submitting.value = true;
  proxy.$modal.loading("登录中...");
  try {
    await useUserStore().login(loginForm.value);
    await useUserStore().getInfo();
    proxy.$tab.reLaunch("/pages/index");
  } catch (error) {
    console.error("登录失败", error);
    loginForm.value.code = "";
    if (captchaEnabled.value) await getCode();
  } finally {
    submitting.value = false;
    proxy.$modal.closeLoading();
  }
}

function browseAsGuest() {
  proxy.$tab.reLaunch("/pages/index");
}

onLoad(() => {
  // #ifdef H5
  if (getToken()) proxy.$tab.reLaunch("/pages/index");
  // #endif
});

getCode();
</script>

<style lang="scss" scoped>
page {
  background-color: #fafaf9;
}
</style>
