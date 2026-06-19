<template>
  <view class="yp-page pb-24">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3 flex items-center justify-between">
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="goBack"><view class="i-lucide-arrow-left text-zinc-700 text-lg"></view></view>
      <text class="text-base font-black text-zinc-900">报价详情</text>
      <view class="size-10 rounded-full bg-white border border-black/5 flex items-center justify-center" @click="showRules"><view class="i-lucide-circle-help text-zinc-700 text-lg"></view></view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-28 space-y-4">
        <view class="yp-card-strong p-5 relative overflow-hidden">
          <view class="absolute -right-12 -top-12 size-40 rounded-full" style="background:rgba(244,63,94,.26);filter:blur(24px)"></view>
          <view class="relative z-10">
            <view class="flex items-center justify-between"><view class="rounded-full bg-white/10 px-3 py-1.5 text-[10px] text-white/75">摄影师报价</view><text class="text-[10px] text-white/45">{{ quote.expireText }}</text></view>
            <text class="text-4xl font-black text-white block mt-5">¥{{ quote.total }}</text>
            <text class="text-xs text-white/55 block mt-2">{{ quote.packageName }} · {{ quote.creator }}</text>
            <view class="mt-5 flex items-center justify-between"><text class="text-[10px] text-white/45">报价编号 {{ quote.no }}</text><view class="rounded-full bg-emerald-500/20 px-3 py-1 text-[9px] text-emerald-200">平台担保交易</view></div>
          </view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-4">费用明细</text>
          <view class="space-y-3">
            <view v-for="item in quote.fees" :key="item.label" class="flex items-center justify-between"><view><text class="text-xs font-bold text-zinc-700 block">{{ item.label }}</text><text v-if="item.note" class="text-[9px] text-zinc-400 block mt-1">{{ item.note }}</text></view><text class="text-xs font-black text-zinc-900">¥{{ item.amount }}</text></view>
            <view class="h-px bg-black/5"></view>
            <view class="flex items-center justify-between"><text class="text-sm font-black text-zinc-900">合计</text><text class="text-xl font-black text-rose-500">¥{{ quote.total }}</text></view>
          </view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-4">服务内容</text>
          <view class="grid grid-cols-2 gap-3">
            <view v-for="item in serviceItems" :key="item.label" class="rounded-2xl bg-zinc-50 p-3"><view class="flex items-center"><view :class="item.icon" class="text-sm text-rose-500 mr-2"></view><text class="text-[10px] text-zinc-400">{{ item.label }}</text></view><text class="text-xs font-bold text-zinc-800 block mt-2">{{ item.value }}</text></view>
          </view>
        </view>

        <view class="yp-card p-4">
          <text class="yp-section-title block mb-3">补充说明</text>
          <text class="text-xs text-zinc-500 leading-relaxed">{{ quote.remark }}</text>
        </view>

        <view class="rounded-2xl bg-emerald-50 p-4 flex items-start"><view class="i-lucide-shield-check text-emerald-600 text-base mt-0.5 mr-3"></view><view><text class="text-xs font-black text-emerald-800 block">平台资金担保</text><text class="text-[10px] text-emerald-700 leading-relaxed block mt-1">款项由平台托管，完成拍摄并确认交付后再结算给服务方。</text></view></view>
      </view>
    </scroll-view>

    <view class="fixed left-0 right-0 bottom-0 z-40 bg-white/95 backdrop-blur-sm border-t border-black/5 px-5 pt-3 pb-6 flex items-center space-x-3">
      <view class="flex-1 h-12 rounded-2xl border border-black/10 flex items-center justify-center text-sm font-bold text-zinc-700" @click="negotiateVisible = true">发起议价</view>
      <view class="flex-1 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="acceptQuote">接受报价</view>
    </view>

    <view v-if="negotiateVisible" class="fixed inset-0 z-50 flex items-end" @click="negotiateVisible = false">
      <view class="absolute inset-0 bg-black/35"></view>
      <view class="relative w-full rounded-t-[28px] bg-white px-5 pt-5 pb-8" @click.stop>
        <view class="flex items-center justify-between"><view><text class="text-lg font-black text-zinc-900 block">发起议价</text><text class="text-[10px] text-zinc-400 block mt-1">合理说明预算和调整需求</text></view><view class="i-lucide-x text-zinc-500 text-lg" @click="negotiateVisible = false"></view></view>
        <view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-2">期望价格</text><view class="h-11 rounded-2xl bg-zinc-50 px-4 flex items-center"><text class="text-sm text-zinc-500 mr-2">¥</text><input v-model="negotiation.price" type="digit" placeholder="填写期望价格" placeholder-class="text-zinc-300" class="flex-1 text-sm text-zinc-900" /></view></view>
        <view class="mt-5"><text class="text-sm font-black text-zinc-800 block mb-2">议价说明</text><textarea v-model="negotiation.message" maxlength="200" placeholder="例如：不需要服装租赁，希望调整对应费用" placeholder-class="text-zinc-300" class="h-28 w-full rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-900" /></view>
        <view class="mt-6 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center text-sm font-black text-white" @click="submitNegotiation">发送议价</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { getCurrentInstance, reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
const { proxy } = getCurrentInstance();
const statusBarH = ref(44); const scrollH = ref(600); const quoteId = ref("1"); const negotiateVisible = ref(false);
try { const info = uni.getSystemInfoSync(); statusBarH.value = info.statusBarHeight || 44; scrollH.value = info.windowHeight - statusBarH.value - 80; } catch (error) { console.warn("获取设备信息失败", error); }
onLoad((options) => { quoteId.value = options?.id || "1"; });
const quote = reactive({ no: "QT20260618001", creator: "林默", packageName: "精致人像写真", total: 1200, expireText: "23 小时后失效", fees: [{ label: "拍摄服务", amount: 800, note: "3 小时城市人像拍摄" }, { label: "基础妆造", amount: 200, note: "妆发与一次补妆" }, { label: "服装租赁", amount: 200, note: "两套服装" }], remark: "拍摄前会建立风格沟通群，确认场地、服装和妆容。天气原因可免费改期一次，其他原因改期需提前 48 小时沟通。" });
const serviceItems = [{ label: "拍摄时长", value: "3 小时", icon: "i-lucide-clock-3" }, { label: "精修数量", value: "30 张", icon: "i-lucide-images" }, { label: "交付周期", value: "3 个工作日", icon: "i-lucide-calendar-clock" }, { label: "原片交付", value: "全部原片", icon: "i-lucide-folder-down" }];
const negotiation = reactive({ price: "1000", message: "" });
function submitNegotiation() { const price = Number(negotiation.price); if (!price || price <= 0) return uni.showToast({ title: "请填写有效价格", icon: "none" }); if (negotiation.message.trim().length < 5) return uni.showToast({ title: "请简要说明议价原因", icon: "none" }); uni.setStorageSync(`yuepai_negotiation_${quoteId.value}`, { ...negotiation, createdAt: Date.now() }); negotiateVisible.value = false; uni.showToast({ title: "议价已发送", icon: "success" }); }
function acceptQuote() { uni.showModal({ title: "确认接受报价", content: `确认以 ¥${quote.total} 预订「${quote.packageName}」吗？`, confirmText: "确认", success(result) { if (!result.confirm) return; const order = { id: Date.now(), no: `YP${Date.now()}`, title: quote.packageName, creator: quote.creator, amount: quote.total, status: "待付款", createdAt: new Date().toISOString() }; const orders = uni.getStorageSync("yuepai_local_orders") || []; uni.setStorageSync("yuepai_local_orders", [order, ...orders]); proxy.$tab.navigateTo(`/pages/order/confirm?orderId=${order.id}`); } }); }
function showRules() { uni.showModal({ title: "报价规则", content: "报价在有效期内可接受或发起一次议价。接受后将生成待支付订单，未支付前不会锁定档期。", showCancel: false }); }
function goBack() { proxy.$tab.navigateBack(); }
</script>
