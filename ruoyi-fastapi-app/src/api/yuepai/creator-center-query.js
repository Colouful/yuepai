import request from "@/utils/request";

export const listMyCreatorProfiles = () => request({ url: "/yuepai/creator-center/profiles", method: "get" });
export const getMyCreatorContent = (creatorId) => request({ url: `/yuepai/creator-center/profiles/${creatorId}/content`, method: "get" });
