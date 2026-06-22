import request from "@/utils/request";

export function prepareWechatPayment(orderId, data) {
  return request({
    url: `/yuepai/payments/orders/${orderId}/prepare`,
    method: "post",
    data,
  });
}

export function createRefund(orderId, data) {
  return request({
    url: `/yuepai/refunds/orders/${orderId}`,
    method: "post",
    data,
  });
}
