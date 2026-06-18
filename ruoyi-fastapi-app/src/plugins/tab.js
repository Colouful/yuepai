const tabBarPages = [
  "/pages/index",
  "/pages/works/index",
  "/pages/publish/index",
  "/pages/message/index",
  "/pages/mine/index",
];

function getPagePath(url = "") {
  return url.split("?")[0];
}

export default {
  // 关闭所有页面，打开到应用内的某个页面
  reLaunch(url) {
    return uni.reLaunch({
      url,
    });
  },

  // 跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面
  switchTab(url) {
    return uni.switchTab({
      url: getPagePath(url),
    });
  },

  // 关闭当前页面，跳转到应用内的某个页面
  redirectTo(url) {
    return uni.redirectTo({
      url,
    });
  },

  // 保留当前页面，跳转到应用内的某个页面
  // 当目标属于底部导航时自动改用 switchTab，避免 UniApp 跳转失败
  navigateTo(url) {
    const pagePath = getPagePath(url);
    if (tabBarPages.includes(pagePath)) {
      return uni.switchTab({
        url: pagePath,
      });
    }

    return uni.navigateTo({
      url,
    });
  },

  // 关闭当前页面，返回上一页面或多级页面
  navigateBack(delta = 1) {
    return uni.navigateBack({
      delta,
    });
  },
};
