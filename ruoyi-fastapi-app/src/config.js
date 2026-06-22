const env = import.meta.env || {};

function normalizeUrl(value = "") {
  return String(value).trim().replace(/\/$/, "");
}

const baseUrl = normalizeUrl(env.VITE_APP_BASE_API);
const siteUrl = normalizeUrl(env.VITE_APP_SITE_URL);
const privacyUrl = normalizeUrl(env.VITE_APP_PRIVACY_URL);
const agreementUrl = normalizeUrl(env.VITE_APP_AGREEMENT_URL);

if (env.PROD && !baseUrl) {
  console.error(
    "[91约拍Pro] 缺少 VITE_APP_BASE_API，生产环境无法发起真实接口请求。",
  );
}

export default {
  baseUrl,
  appInfo: {
    name: env.VITE_APP_NAME || "91约拍Pro",
    version: env.VITE_APP_VERSION || "1.0.0",
    logo: env.VITE_APP_LOGO || "/static/logo.png",
    site_url: siteUrl,
    agreements: [
      {
        title: "隐私政策",
        url: privacyUrl,
      },
      {
        title: "用户服务协议",
        url: agreementUrl,
      },
    ],
  },
};
