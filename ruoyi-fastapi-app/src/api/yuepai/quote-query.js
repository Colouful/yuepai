import request from "@/utils/request";

export const listQuotes = (params) => request({ url: "/yuepai/quotes", method: "get", params });
export const getQuote = (quoteId) => request({ url: `/yuepai/quotes/${quoteId}`, method: "get" });
