<template>
  <view class="min-h-screen bg-stone-50 p-5">
    <view class="space-y-5">
      <!-- Old Password -->
      <view class="group relative">
        <text class="mb-2 block text-sm font-medium text-slate-700">旧密码</text>
        <input
          v-model="user.oldPassword"
          class="h-11 w-full rounded-xl bg-white px-4 text-sm text-slate-800 outline-none ring-1 ring-slate-200 transition-all focus:ring-2 focus:ring-amber-400/50"
          type="password"
          placeholder="请输入旧密码"
        />
      </view>
      <!-- New Password -->
      <view class="group relative">
        <text class="mb-2 block text-sm font-medium text-slate-700">新密码</text>
        <input
          v-model="user.newPassword"
          class="h-11 w-full rounded-xl bg-white px-4 text-sm text-slate-800 outline-none ring-1 ring-slate-200 transition-all focus:ring-2 focus:ring-amber-400/50"
          type="password"
          placeholder="请输入新密码"
        />
      </view>
      <!-- Confirm Password -->
      <view class="group relative">
        <text class="mb-2 block text-sm font-medium text-slate-700"
          >确认密码</text
        >
        <input
          v-model="user.confirmPassword"
          class="h-11 w-full rounded-xl bg-white px-4 text-sm text-slate-800 outline-none ring-1 ring-slate-200 transition-all focus:ring-2 focus:ring-amber-400/50"
          type="password"
          placeholder="请确认新密码"
        />
      </view>

      <!-- Submit Button -->
      <view class="pt-6">
        <button
          @click="submit"
          class="flex h-12 w-full items-center justify-center rounded-xl bg-gradient-to-r from-slate-800 to-slate-900 text-base font-semibold text-white active:scale-[0.98] transition-transform"
        >
          提 交
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { updateUserPwd } from "@/api/system/user";
import { ref, reactive, getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance();
const user = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
});

function submit() {
  if (!user.oldPassword) {
    proxy.$modal.msgError("旧密码不能为空");
    return;
  }
  if (!user.newPassword) {
    proxy.$modal.msgError("新密码不能为空");
    return;
  }
  if (user.newPassword.length < 6 || user.newPassword.length > 20) {
    proxy.$modal.msgError("长度在 6 到 20 个字符");
    return;
  }
  if (!user.confirmPassword) {
    proxy.$modal.msgError("确认密码不能为空");
    return;
  }
  if (user.newPassword !== user.confirmPassword) {
    proxy.$modal.msgError("两次输入的密码不一致");
    return;
  }

  updateUserPwd(user.oldPassword, user.newPassword).then((response) => {
    proxy.$modal.msgSuccess("修改成功");
    setTimeout(() => {
      proxy.$tab.navigateBack();
    }, 1500);
  });
}
</script>
