import request from "@/utils/request";

export const createConversation = (data) => request({ url: "/yuepai/messages/conversations", method: "post", data });
export const listConversations = () => request({ url: "/yuepai/messages/conversations", method: "get" });
export const listMessages = (conversationId, params) => request({ url: `/yuepai/messages/conversations/${conversationId}`, method: "get", params });
export const sendMessage = (conversationId, data) => request({ url: `/yuepai/messages/conversations/${conversationId}`, method: "post", data });
export const markConversationRead = (conversationId, params) => request({ url: `/yuepai/messages/conversations/${conversationId}/read`, method: "post", params });
