import request from "@/utils/request";

export const getCreatorState = (creatorId, params) => request({ url: `/yuepai/social/creators/${creatorId}/state`, method: "get", params });
export const followCreator = (creatorId) => request({ url: `/yuepai/social/creators/${creatorId}/follow`, method: "post" });
export const unfollowCreator = (creatorId) => request({ url: `/yuepai/social/creators/${creatorId}/follow`, method: "delete" });
export const favoriteWork = (workId) => request({ url: `/yuepai/social/works/${workId}/favorite`, method: "post" });
export const unfavoriteWork = (workId) => request({ url: `/yuepai/social/works/${workId}/favorite`, method: "delete" });
