import config from "@/config";
import { getToken } from "@/utils/auth";

export function chooseAndUploadImage() {
  return new Promise((resolve, reject) => {
    uni.chooseImage({
      count: 1,
      sizeType: ["compressed"],
      sourceType: ["album", "camera"],
      success(result) {
        const file = result.tempFiles?.[0];
        const filePath = file?.path || result.tempFilePaths?.[0];
        if (!filePath) return reject(new Error("未选择图片"));
        if (Number(file?.size || 0) > 10 * 1024 * 1024) return reject(new Error("图片不能超过10MB"));
        uploadImage(filePath).then(resolve).catch(reject);
      },
      fail(error) {
        if (String(error?.errMsg || "").includes("cancel")) resolve("");
        else reject(error);
      },
    });
  });
}

export function uploadImage(filePath) {
  return new Promise((resolve, reject) => {
    if (!config.baseUrl) return reject(new Error("未配置服务端地址"));
    uni.uploadFile({
      url: `${config.baseUrl}/common/upload`,
      filePath,
      name: "file",
      timeout: 60000,
      header: { Authorization: `Bearer ${getToken()}` },
      success(response) {
        try {
          const body = typeof response.data === "string" ? JSON.parse(response.data) : response.data;
          if (response.statusCode !== 200 || body.code !== 200 || !body.url) {
            reject(new Error(body?.msg || "图片上传失败"));
            return;
          }
          resolve(body.url);
        } catch (error) {
          reject(new Error("上传响应解析失败"));
        }
      },
      fail(error) {
        reject(new Error(error?.errMsg || "图片上传失败"));
      },
    });
  });
}
