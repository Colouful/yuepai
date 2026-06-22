import request from "@/utils/request";

export const saveCreatorProfile = (data) => request({ url: "/yuepai/creator-center/profile", method: "put", data });
export const createCreatorWork = (data) => request({ url: "/yuepai/creator-center/works", method: "post", data });
export const createServicePackage = (data) => request({ url: "/yuepai/creator-center/packages", method: "post", data });
