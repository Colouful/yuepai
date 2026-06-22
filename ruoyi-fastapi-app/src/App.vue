<script setup>
import config from "./config";
import { getToken } from "@/utils/auth";
import { useConfigStore } from "@/store";
import { getCurrentInstance } from "vue";
import { onLaunch } from "@dcloudio/uni-app";

const { proxy } = getCurrentInstance();

onLaunch(() => {
  initApp();
});

function initApp() {
  initConfig();
  //#ifdef H5
  checkLogin();
  //#endif
}

function initConfig() {
  useConfigStore().setConfig(config);
}

function checkLogin() {
  if (!getToken()) {
    proxy.$tab.reLaunch("/pages/login");
  }
}
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

page,
body {
  --yp-brand: #f43f5e;
  --yp-brand-dark: #e11d48;
  --yp-ink: #18181b;
  --yp-text: #27272a;
  --yp-muted: #71717a;
  --yp-subtle: #a1a1aa;
  --yp-line: rgba(24, 24, 27, 0.08);
  --yp-surface: #ffffff;
  --yp-canvas: #f7f5f2;
  --yp-success: #10b981;
  --yp-warning: #f59e0b;
  height: 100%;
  min-height: 100%;
  overflow-x: hidden;
  background: var(--yp-canvas);
  color: var(--yp-text);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}

page,
view,
scroll-view,
image,
text,
button,
input,
textarea,
label,
navigator {
  box-sizing: border-box;
}

button::after {
  border: 0;
}

.yp-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at 100% 0%, rgba(244, 63, 94, 0.08), transparent 30%),
    linear-gradient(180deg, #fbfaf8 0%, var(--yp-canvas) 100%);
}

.yp-card {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid var(--yp-line);
  border-radius: 24rpx;
  box-shadow: 0 12rpx 36rpx rgba(24, 24, 27, 0.04);
}

.yp-card-strong {
  background: var(--yp-ink);
  border-radius: 32rpx;
  color: #fff;
  box-shadow: 0 24rpx 64rpx rgba(24, 24, 27, 0.18);
}

.yp-eyebrow {
  color: var(--yp-brand);
  font-size: 20rpx;
  font-weight: 700;
  letter-spacing: 4rpx;
  text-transform: uppercase;
}

.yp-title {
  color: var(--yp-ink);
  font-size: 40rpx;
  font-weight: 800;
  letter-spacing: -1rpx;
}

.yp-section-title {
  color: var(--yp-ink);
  font-size: 30rpx;
  font-weight: 800;
}

.yp-muted {
  color: var(--yp-muted);
}

.yp-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52rpx;
  padding: 0 24rpx;
  border: 1px solid var(--yp-line);
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.9);
  color: var(--yp-muted);
  font-size: 22rpx;
  font-weight: 600;
}

.yp-chip-active {
  border-color: var(--yp-ink);
  background: var(--yp-ink);
  color: #fff;
}

.yp-primary-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 96rpx;
  border-radius: 28rpx;
  background: var(--yp-ink);
  color: #fff;
  font-size: 28rpx;
  font-weight: 700;
  box-shadow: 0 20rpx 44rpx rgba(24, 24, 27, 0.16);
}

.yp-primary-button:active {
  transform: scale(0.98);
}

/* #ifdef H5 */
uni-toast img,
uni-toast svg {
  display: inline-block !important;
}
/* #endif */

::-webkit-scrollbar {
  display: none;
  width: 0 !important;
  height: 0 !important;
  -webkit-appearance: none;
  background: transparent;
}
</style>
