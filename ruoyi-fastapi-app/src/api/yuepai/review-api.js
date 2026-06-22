import request from "@/utils/request";

export const publishOrderReview = (orderId, data) => request({
  url: `/yuepai/orders/${orderId}/review`,
  method: "post",
  data,
});
