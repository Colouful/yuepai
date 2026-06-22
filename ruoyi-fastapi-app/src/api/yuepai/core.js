import request from "@/utils/request";

export function listDemands(params) {
  return request({
    url: "/yuepai/demands",
    method: "get",
    params,
    headers: { isToken: false },
  });
}

export function getDemand(demandId) {
  return request({
    url: `/yuepai/demands/${demandId}`,
    method: "get",
    headers: { isToken: false },
  });
}

export function createDemand(data) {
  return request({
    url: "/yuepai/demands",
    method: "post",
    data,
  });
}

export function submitDemand(demandId) {
  return request({
    url: `/yuepai/demands/${demandId}/submit`,
    method: "post",
  });
}

export function applyDemand(demandId, data) {
  return request({
    url: `/yuepai/demands/${demandId}/applications`,
    method: "post",
    data,
  });
}

export function listDemandApplications(demandId) {
  return request({
    url: `/yuepai/demands/${demandId}/applications`,
    method: "get",
  });
}

export function createQuote(data) {
  return request({
    url: "/yuepai/quotes",
    method: "post",
    data,
  });
}

export function acceptQuote(quoteId, data) {
  return request({
    url: `/yuepai/quotes/${quoteId}/accept`,
    method: "post",
    data,
  });
}

export function listOrders(params) {
  return request({
    url: "/yuepai/orders",
    method: "get",
    params,
  });
}

export function getOrder(orderId) {
  return request({
    url: `/yuepai/orders/${orderId}`,
    method: "get",
  });
}

export function transitionOrder(orderId, data) {
  return request({
    url: `/yuepai/orders/${orderId}/transition`,
    method: "post",
    data,
  });
}
