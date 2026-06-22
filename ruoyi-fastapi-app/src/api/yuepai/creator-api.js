import request from "@/utils/request";

export const listCreators = (params) => request({ url: "/yuepai/creators", method: "get", params, headers: { isToken: false } });
export const getCreator = (creatorId) => request({ url: `/yuepai/creators/${creatorId}`, method: "get", headers: { isToken: false } });
export const listCreatorPackages = (creatorId) => request({ url: `/yuepai/creator-packages/${creatorId}`, method: "get", headers: { isToken: false } });
export const listCreatorReviews = (creatorId, params) => request({ url: `/yuepai/reviews/creator/${creatorId}`, method: "get", params, headers: { isToken: false } });
export const listWorks = (params) => request({ url: "/yuepai/works", method: "get", params, headers: { isToken: false } });
export const getWork = (workId) => request({ url: `/yuepai/works/${workId}`, method: "get", headers: { isToken: false } });
