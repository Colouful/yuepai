<template>
  <view class="yp-page">
    <view :style="{ height: statusBarH + 'px' }"></view>

    <view class="px-5 pt-3 pb-3">
      <text class="yp-eyebrow block">CREATE</text>
      <text class="yp-title block mt-1">发布创作</text>
      <text class="text-xs text-zinc-500 block mt-2">把想法说清楚，更容易遇见合适的合作伙伴</text>

      <view class="mt-4 rounded-2xl bg-zinc-100 p-1 flex">
        <view
          v-for="item in publishModes"
          :key="item.value"
          class="flex-1 h-10 rounded-xl flex items-center justify-center text-xs font-bold"
          :class="mode === item.value ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-400'"
          @click="switchMode(item.value)"
        >
          {{ item.label }}
        </view>
      </view>
    </view>

    <scroll-view scroll-y :show-scrollbar="false" :style="{ height: scrollH + 'px' }">
      <view class="px-5 pb-32 space-y-5">
        <view class="yp-card p-4">
          <view class="flex items-center justify-between mb-3">
            <text class="text-sm font-black text-zinc-900">{{ modeConfig.typeTitle }}</text>
            <text class="text-[10px] text-zinc-400">单选</text>
          </view>
          <view class="flex flex-wrap gap-2">
            <view
              v-for="item in modeConfig.types"
              :key="item"
              class="yp-chip"
              :class="form.type === item ? 'yp-chip-active' : ''"
              @click="form.type = item"
            >
              {{ item }}
            </view>
          </view>
        </view>

        <view class="yp-card p-4 space-y-5">
          <view>
            <view class="flex items-center justify-between mb-2">
              <text class="text-sm font-black text-zinc-900">{{ modeConfig.titleLabel }}</text>
              <text class="text-[10px] text-zinc-400">{{ form.title.length }}/30</text>
            </view>
            <input
              v-model="form.title"
              maxlength="30"
              :placeholder="modeConfig.titlePlaceholder"
              placeholder-class="text-zinc-300"
              class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900"
            />
          </view>

          <view>
            <view class="flex items-center justify-between mb-2">
              <text class="text-sm font-black text-zinc-900">内容说明</text>
              <text class="text-[10px] text-zinc-400">{{ form.description.length }}/500</text>
            </view>
            <textarea
              v-model="form.description"
              maxlength="500"
              :placeholder="modeConfig.descriptionPlaceholder"
              placeholder-class="text-zinc-300"
              class="h-32 w-full rounded-2xl bg-zinc-50 p-4 text-sm leading-relaxed text-zinc-900"
            />
          </view>

          <view>
            <view class="flex items-center justify-between mb-3">
              <text class="text-sm font-black text-zinc-900">参考图片</text>
              <text class="text-[10px] text-zinc-400">最多 6 张</text>
            </view>
            <view class="flex flex-wrap gap-2.5">
              <view v-for="(image, index) in form.images" :key="image" class="relative size-[94px] rounded-2xl overflow-hidden bg-zinc-100">
                <image :src="image" mode="aspectFill" class="w-full h-full" @click="previewImage(index)" />
                <view class="absolute right-1.5 top-1.5 size-6 rounded-full bg-black/55 flex items-center justify-center" @click.stop="removeImage(index)">
                  <view class="i-lucide-x text-white text-xs"></view>
                </view>
              </view>
              <view v-if="form.images.length < 6" class="size-[94px] rounded-2xl border border-dashed border-zinc-300 bg-zinc-50 flex flex-col items-center justify-center" @click="chooseImages">
                <view class="i-lucide-image-plus text-xl text-zinc-500"></view>
                <text class="text-[10px] text-zinc-400 mt-1.5">添加图片</text>
              </view>
            </view>
          </view>
        </view>

        <view v-if="mode === 'demand'" class="yp-card p-4 space-y-5">
          <view>
            <text class="text-sm font-black text-zinc-900 block mb-3">需要哪些角色</text>
            <view class="flex flex-wrap gap-2">
              <view
                v-for="item in roles"
                :key="item"
                class="yp-chip"
                :class="form.roles.includes(item) ? 'yp-chip-active' : ''"
                @click="toggleRole(item)"
              >
                {{ item }}
              </view>
            </view>
          </view>

          <view class="grid grid-cols-2 gap-3">
            <picker mode="date" :value="form.date" @change="onDateChange">
              <view>
                <text class="text-xs font-bold text-zinc-600 block mb-2">拍摄日期</text>
                <view class="h-11 rounded-2xl bg-zinc-50 px-3 flex items-center justify-between">
                  <text class="text-xs" :class="form.date ? 'text-zinc-900' : 'text-zinc-300'">{{ form.date || '选择日期' }}</text>
                  <view class="i-lucide-calendar-days text-zinc-400 text-sm"></view>
                </view>
              </view>
            </picker>
            <view>
              <text class="text-xs font-bold text-zinc-600 block mb-2">拍摄城市</text>
              <view class="h-11 rounded-2xl bg-zinc-50 px-3 flex items-center">
                <input v-model="form.city" placeholder="例如：北京" placeholder-class="text-zinc-300" class="flex-1 text-xs text-zinc-900" />
                <view class="i-lucide-map-pin text-zinc-400 text-sm"></view>
              </view>
            </view>
          </view>

          <view>
            <view class="flex items-center justify-between mb-3">
              <text class="text-sm font-black text-zinc-900">预算方式</text>
              <view class="flex items-center">
                <text class="text-[10px] text-zinc-400 mr-2">接受互勉</text>
                <switch :checked="form.mutual" color="#18181b" style="transform:scale(.72)" @change="form.mutual = $event.detail.value" />
              </view>
            </view>
            <view class="flex flex-wrap gap-2">
              <view
                v-for="item in budgets"
                :key="item"
                class="yp-chip"
                :class="form.budget === item ? 'yp-chip-active' : ''"
                @click="form.budget = item"
              >
                {{ item }}
              </view>
            </view>
          </view>
        </view>

        <view v-else class="yp-card p-4">
          <text class="text-sm font-black text-zinc-900 block mb-3">{{ mode === 'work' ? '作品标签' : '服务价格' }}</text>
          <input
            v-model="form.extra"
            :placeholder="mode === 'work' ? '例如：人像、胶片、北京' : '例如：699 元起 / 可互勉'"
            placeholder-class="text-zinc-300"
            class="h-11 w-full rounded-2xl bg-zinc-50 px-4 text-sm text-zinc-900"
          />
        </view>

        <view class="flex items-start px-1">
          <view class="i-lucide-shield-check text-emerald-500 text-sm mt-0.5 mr-2"></view>
          <text class="text-[10px] text-zinc-400 leading-relaxed">发布内容需真实、合法，不得包含政治敏感、色情低俗、引流诈骗及侵犯他人权益的信息。</text>
        </view>

        <button class="yp-primary-button w-full" :disabled="submitting" @click="submit">
          <view v-if="submitting" class="i-svg-spinners-180-ring text-white text-lg mr-2"></view>
          {{ submitting ? '正在保存' : modeConfig.submitText }}
        </button>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { computed, reactive, ref } from "vue";

const statusBarH = ref(44);
const scrollH = ref(600);
const mode = ref("demand");
const submitting = ref(false);

try {
  const systemInfo = uni.getSystemInfoSync();
  statusBarH.value = systemInfo.statusBarHeight || 44;
  scrollH.value = systemInfo.windowHeight - statusBarH.value - 150;
} catch (error) {
  console.warn("获取设备信息失败", error);
}

const publishModes = [
  { label: "发约拍", value: "demand" },
  { label: "发作品", value: "work" },
  { label: "发服务", value: "service" },
];

const configs = {
  demand: {
    typeTitle: "约拍类型",
    types: ["个人写真", "情侣写真", "婚纱摄影", "旅拍", "商业拍摄", "互勉创作", "同城陪拍", "证件照"],
    titleLabel: "需求标题",
    titlePlaceholder: "一句话说明你想拍什么",
    descriptionPlaceholder: "描述拍摄风格、人员要求、服装妆造和期望效果……",
    submitText: "发布约拍需求",
  },
  work: {
    typeTitle: "作品类型",
    types: ["人像", "古风", "婚纱", "街拍", "旅拍", "胶片", "商业", "其他"],
    titleLabel: "作品标题",
    titlePlaceholder: "为这组作品取一个好名字",
    descriptionPlaceholder: "分享拍摄故事、器材、地点和创作灵感……",
    submitText: "发布作品",
  },
  service: {
    typeTitle: "服务类型",
    types: ["写真跟拍", "婚礼摄影", "商业摄影", "活动跟拍", "妆造服务", "模特服务", "场地服务", "其他"],
    titleLabel: "服务名称",
    titlePlaceholder: "例如：城市情绪写真套餐",
    descriptionPlaceholder: "说明服务内容、时长、交付数量、改期规则等……",
    submitText: "发布服务",
  },
};

const modeConfig = computed(() => configs[mode.value]);
const roles = ["摄影师", "模特", "化妆师", "造型师", "场地", "搭档"];
const budgets = ["200 以下", "200-500", "500-1000", "1000-2000", "2000 以上", "面议"];

const form = reactive(createInitialForm());

function createInitialForm() {
  return {
    type: configs[mode.value].types[0],
    title: "",
    description: "",
    images: [],
    roles: ["摄影师"],
    date: "",
    city: "",
    mutual: false,
    budget: "500-1000",
    extra: "",
  };
}

function switchMode(value) {
  mode.value = value;
  Object.assign(form, createInitialForm());
}

function toggleRole(role) {
  const index = form.roles.indexOf(role);
  if (index >= 0) {
    form.roles.splice(index, 1);
  } else {
    form.roles.push(role);
  }
}

function onDateChange(event) {
  form.date = event.detail.value;
}

function chooseImages() {
  uni.chooseImage({
    count: 6 - form.images.length,
    sizeType: ["compressed"],
    sourceType: ["album", "camera"],
    success(result) {
      form.images.push(...result.tempFilePaths.slice(0, 6 - form.images.length));
    },
    fail(error) {
      if (!String(error.errMsg || "").includes("cancel")) {
        uni.showToast({ title: "选择图片失败，请重试", icon: "none" });
      }
    },
  });
}

function previewImage(index) {
  uni.previewImage({ current: index, urls: form.images });
}

function removeImage(index) {
  form.images.splice(index, 1);
}

function validate() {
  if (!form.title.trim()) return "请填写标题";
  if (!form.description.trim()) return "请填写内容说明";
  if (mode.value === "demand" && !form.roles.length) return "请至少选择一个需要的角色";
  if (mode.value === "demand" && !form.date) return "请选择拍摄日期";
  if (mode.value === "demand" && !form.city.trim()) return "请填写拍摄城市";
  if (mode.value === "work" && !form.images.length) return "请至少添加一张作品图片";
  return "";
}

function submit() {
  const errorMessage = validate();
  if (errorMessage) {
    uni.showToast({ title: errorMessage, icon: "none" });
    return;
  }

  submitting.value = true;
  try {
    const drafts = uni.getStorageSync("yuepai_publish_drafts") || [];
    drafts.unshift({
      id: Date.now(),
      mode: mode.value,
      createdAt: new Date().toISOString(),
      ...JSON.parse(JSON.stringify(form)),
    });
    uni.setStorageSync("yuepai_publish_drafts", drafts.slice(0, 20));

    setTimeout(() => {
      submitting.value = false;
      uni.showToast({ title: "内容已保存", icon: "success" });
    }, 500);
  } catch (error) {
    submitting.value = false;
    console.error("保存发布内容失败", error);
    uni.showToast({ title: "保存失败，请稍后重试", icon: "none" });
  }
}
</script>
