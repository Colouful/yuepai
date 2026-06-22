import request from "@/utils/request";

export const getLatestDelivery = (orderId) => request({ url: `/yuepai/deliveries/orders/${orderId}`, method: "get" });
export const listDeliveryVersions = (orderId) => request({ url: `/yuepai/deliveries/orders/${orderId}/versions`, method: "get" });
export const submitDelivery = (orderId, data) => request({ url: `/yuepai/deliveries/orders/${orderId}`, method: "post", data });
export const decideDelivery = (orderId, data) => request({ url: `/yuepai/deliveries/orders/${orderId}/decision`, method: "post", data });
