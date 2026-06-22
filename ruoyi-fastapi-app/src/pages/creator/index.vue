<template>
  <view class="yp-page min-h-screen pb-24">
    <view :style="{ height: statusBarH + 'px' }"></view>
    <view class="px-5 pt-3 pb-3">
      <text class="yp-eyebrow block">CREATOR CENTER</text>
      <text class="yp-title block mt-1">创作者工作台</text>
      <text class="text-xs text-zinc-400 block mt-2">资料、作品和套餐审核通过后才会公开展示</text>
    </view>

    <view v-if="loading" class="px-5 pt-4 space-y-4">
      <view class="yp-card h-36 animate-pulse bg-white/70"></view>
      <view class="yp-card h-64 animate-pulse bg-white/70"></view>
    </view>

    <view v-else class="px-5 pt-3 space-y-4">
      <view class="yp-card p-4">
        <view class="flex items-center justify-between">
          <text class="yp-section-title">创作者身份</text>
          <view class="rounded-full bg-zinc-900 px-3 py-2 text-[10px] font-bold text-white" @click="startNewProfile">新增身份</view>
        </view>
        <scroll-view v-if="profiles.length" scroll-x class="mt-3 whitespace-nowrap" :show-scrollbar="false">
          <view class="inline-flex space-x-2 pr-5">
            <view
              v-for="item in profiles"
              :key="item.creatorId"
              class="rounded-2xl border px-4 py-3 min-w-36"
              :class="selected?.creatorId === item.creatorId ? 'bg-zinc-900 border-zinc-900 text-white' : 'bg-zinc-50 border-black/5 text-zinc-700'"
              @click="selectProfile(item)"
            >
              <text class="text-xs font-black block">{{ item.displayName }}</text>
              <text class="text-[9px] opacity-60 block mt-1">{{ roleLabel(item.roleCode) }} · {{ statusLabel(item.status) }}</text>
              <text class="text-[9px] opacity-60 block mt-1">{{ item.workCount }} 作品 · {{ item.packageCount }} 套餐</text>
            </view>
          </view>
        </scroll-view>
        <view v-else class="mt-4 rounded-2xl bg-zinc-50 py-8 text-center"><text class="text-xs text-zinc-400">尚未创建创作者身份</text></view>
      </view>

      <view class="flex items-center space-x-2">
        <view v-for="item in tabs" :key="item.value" class="flex-1 yp-chip" :class="activeTab === item.value ? 'yp-chip-active' : ''" @click="activeTab = item.value">{{ item.label }}</view>
      </view>

      <view v-if="activeTab === 'profile'" class="yp-card p-4 space-y-4">
        <view class="flex items-center justify-between"><text class="yp-section-title">资料与认证</text><text class="text-[10px]" :class="statusColor(profileStatus)">{{ statusLabel(profileStatus) }}</text></view>
        <view class="flex items-center space-x-3">
          <view class="relative" @click="uploadAvatar">
            <image v-if="profile.avatarUrl" :src="profile.avatarUrl" mode="aspectFill" class="size-20 rounded-3xl bg-zinc-100" />
            <view v-else class="size-20 rounded-3xl bg-zinc-100 flex items-center justify-center"><view class="i-lucide-user-round-plus text-2xl text-zinc-400"></view></view>
            <view class="absolute -right-1 -bottom-1 size-7 rounded-full bg-zinc-900 text-white flex items-center justify-center"><view class="i-lucide-camera text-xs"></view></view>
          </view>
          <view class="flex-1" @click="uploadCover"><text class="text-xs font-bold text-zinc-700 block">主页封面</text><view class="mt-2 h-16 rounded-2xl bg-zinc-100 overflow-hidden flex items-center justify-center"><image v-if="profile.coverUrl" :src="profile.coverUrl" mode="aspectFill" class="w-full h-full"/><text v-else class="text-[10px] text-zinc-400">点击上传横版封面</text></view></view>
        </view>
        <view><text class="form-label">创作者身份</text><picker :range="roleOptions" range-key="label" @change="profile.roleCode = roleOptions[Number($event.detail.value)].value"><view class="form-input flex items-center justify-between"><text>{{ roleLabel(profile.roleCode) }}</text><view class="i-lucide-chevron-down text-zinc-400"></view></view></picker></view>
        <view><text class="form-label">展示名称</text><input v-model.trim="profile.displayName" maxlength="50" class="form-input" placeholder="摄影师或模特名称" /></view>
        <view><text class="form-label">一句话介绍</text><input v-model.trim="profile.headline" maxlength="120" class="form-input" placeholder="擅长风格、服务特色" /></view>
        <view><text class="form-label">详细介绍</text><textarea v-model="profile.bio" maxlength="5000" class="form-area" placeholder="从业经历、拍摄理念、合作方式等" /></view>
        <view class="grid grid-cols-2 gap-3"><view><text class="form-label">所在城市</text><input v-model.trim="profile.cityCode" maxlength="20" class="form-input" placeholder="北京" /></view><view><text class="form-label">从业年限</text><input v-model="profile.yearsExperience" type="number" class="form-input" placeholder="0" /></view></view>
        <view class="grid grid-cols-2 gap-3"><view><text class="form-label">起步价格</text><input v-model="profile.basePrice" type="digit" class="form-input" placeholder="500" /></view><view><text class="form-label">服务城市</text><input v-model.trim="profile.serviceCitiesText" class="form-input" placeholder="北京,天津" /></view></view>
        <view><text class="form-label">风格标签</text><input v-model.trim="profile.tagsText" class="form-input" placeholder="人像,日系,婚纱" /></view>
        <view class="flex items-center justify-between rounded-2xl bg-zinc-50 p-3"><view><text class="text-xs font-bold text-zinc-700 block">接受互勉</text><text class="text-[9px] text-zinc-400 block mt-1">允许用户通过互勉方式邀请约拍</text></view><switch :checked="profile.acceptMutual" color="#18181b" @change="profile.acceptMutual = $event.detail.value" /></view>
        <view class="primary-action" @click="submitProfile">提交资料审核</view>
      </view>

      <view v-if="activeTab === 'works'" class="space-y-4">
        <view class="yp-card p-4 space-y-4">
          <view class="flex items-center justify-between"><text class="yp-section-title">发布作品</text><text class="text-[10px] text-zinc-400">{{ work.assets.length }}/30 张</text></view>
          <view><text class="form-label">作品图片</text><view class="grid grid-cols-3 gap-2"><view v-for="(url,index) in work.assets" :key="url" class="relative"><image :src="url" mode="aspectFill" class="w-full h-28 rounded-2xl"/><view class="absolute right-1 top-1 size-6 rounded-full bg-black/50 text-white flex items-center justify-center" @click="removeWorkImage(index)"><view class="i-lucide-x text-xs"></view></view></view><view class="h-28 rounded-2xl border border-dashed border-zinc-300 flex flex-col items-center justify-center" @click="addWorkImage"><view class="i-lucide-image-plus text-xl text-zinc-400"></view><text class="text-[9px] text-zinc-400 mt-1">添加图片</text></view></view></view>
          <view><text class="form-label">作品标题</text><input v-model.trim="work.title" maxlength="100" class="form-input" placeholder="作品主题" /></view>
          <view class="grid grid-cols-2 gap-3"><view><text class="form-label">作品分类</text><input v-model.trim="work.category" maxlength="32" class="form-input" placeholder="人像" /></view><view><text class="form-label">拍摄城市</text><input v-model.trim="work.cityCode" maxlength="20" class="form-input" placeholder="北京" /></view></view>
          <view><text class="form-label">作品标签</text><input v-model.trim="work.tagsText" class="form-input" placeholder="清新,日系,胶片" /></view>
          <view><text class="form-label">创作说明</text><textarea v-model="work.description" maxlength="5000" class="form-area" placeholder="拍摄背景、创意和使用器材" /></view>
          <view class="primary-action" @click="submitWork">提交作品审核</view>
        </view>
        <view class="yp-card p-4"><text class="yp-section-title block mb-3">作品状态</text><view v-if="content.works.length" class="space-y-2"><view v-for="item in content.works" :key="item.workId" class="rounded-2xl bg-zinc-50 p-3 flex items-center"><image :src="item.coverUrl" mode="aspectFill" class="size-12 rounded-xl"/><view class="flex-1 min-w-0 ml-3"><text class="text-xs font-bold text-zinc-700 block truncate">{{ item.title }}</text><text class="text-[9px] block mt-1" :class="statusColor(item.status)">{{ statusLabel(item.status) }}</text></view></view></view><text v-else class="text-xs text-zinc-400">暂无作品</text></view>
      </view>

      <view v-if="activeTab === 'packages'" class="space-y-4">
        <view class="yp-card p-4 space-y-4">
          <view class="flex items-center justify-between"><text class="yp-section-title">新建服务套餐</text><text class="text-[10px]" :class="selected?.certificationStatus === 'approved' ? 'text-emerald-600' : 'text-amber-600'">{{ selected?.certificationStatus === 'approved' ? '可发布' : '认证通过后可发布' }}</text></view>
          <view><text class="form-label">套餐名称</text><input v-model.trim="pkg.packageName" maxlength="80" class="form-input" placeholder="基础人像写真" /></view>
          <view><text class="form-label">服务说明</text><textarea v-model="pkg.description" maxlength="5000" class="form-area" placeholder="适合人群、拍摄内容和服务范围" /></view>
          <view class="grid grid-cols-2 gap-3"><view><text class="form-label">套餐价格</text><input v-model="pkg.price" type="digit" class="form-input" placeholder="500" /></view><view><text class="form-label">拍摄时长/分钟</text><input v-model="pkg.durationMinutes" type="number" class="form-input" placeholder="120" /></view></view>
          <view class="grid grid-cols-2 gap-3"><view><text class="form-label">原片数量</text><input v-model="pkg.originalCount" type="number" class="form-input" /></view><view><text class="form-label">精修数量</text><input v-model="pkg.retouchedCount" type="number" class="form-input" /></view></view>
          <view class="grid grid-cols-2 gap-3"><view><text class="form-label">交付天数</text><input v-model="pkg.deliveryDays" type="number" class="form-input" /></view><view><text class="form-label">修改次数</text><input v-model="pkg.revisionCount" type="number" class="form-input" /></view></view>
          <view><text class="form-label">套餐包含</text><input v-model.trim="pkg.includesText" class="form-input" placeholder="场景策划,拍摄指导,精修" /></view>
          <view><text class="form-label">预约须知</text><textarea v-model="pkg.bookingNotice" maxlength="3000" class="form-area" placeholder="提前预约时间、迟到处理等" /></view>
          <view><text class="form-label">退款规则</text><textarea v-model="pkg.refundRule" maxlength="3000" class="form-area" placeholder="不同取消时间对应的退款比例" /></view>
          <view class="primary-action" @click="submitPackage">提交套餐审核</view>
        </view>
        <view class="yp-card p-4"><text class="yp-section-title block mb-3">套餐状态</text><view v-if="content.packages.length" class="space-y-2"><view v-for="item in content.packages" :key="item.packageId" class="rounded-2xl bg-zinc-50 p-3 flex items-center justify-between"><view><text class="text-xs font-bold text-zinc-700 block">{{ item.packageName }}</text><text class="text-[9px] block mt-1" :class="statusColor(item.status)">{{ statusLabel(item.status) }}</text></view><text class="text-sm font-black text-rose-500">¥{{ Number(item.price||0).toFixed(0) }}</text></view></view><text v-else class="text-xs text-zinc-400">暂无套餐</text></view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { onLoad, onShow } from "@dcloudio/uni-app";
import { createCreatorWork, createServicePackage, saveCreatorProfile } from "@/api/yuepai/creator-manage";
import { getMyCreatorContent, listMyCreatorProfiles } from "@/api/yuepai/creator-center-query";
import { chooseAndUploadImage } from "@/api/yuepai/upload";

const statusBarH = ref(44), loading = ref(true), profiles = ref([]), selected = ref(null), activeTab = ref("profile");
const tabs = [{label:"资料",value:"profile"},{label:"作品",value:"works"},{label:"套餐",value:"packages"}];
const roleOptions = [{label:"摄影师",value:"photographer"},{label:"模特",value:"model"},{label:"化妆师",value:"makeup"},{label:"造型师",value:"stylist"},{label:"摄像师",value:"videographer"}];
const profile = reactive(emptyProfile()), work = reactive(emptyWork()), pkg = reactive(emptyPackage()), content = reactive({works:[],packages:[]});
const profileStatus = computed(() => selected.value?.status || "draft");

onLoad(()=>{try{statusBarH.value=uni.getSystemInfoSync().statusBarHeight||44}catch(e){console.warn(e)}});onShow(()=>loadProfiles());
function emptyProfile(){return{roleCode:"photographer",displayName:"",headline:"",bio:"",avatarUrl:"",coverUrl:"",cityCode:"",serviceCitiesText:"",tagsText:"",yearsExperience:0,basePrice:"",acceptMutual:false}}
function emptyWork(){return{title:"",description:"",category:"人像",cityCode:"",tagsText:"",assets:[]}}
function emptyPackage(){return{packageName:"",description:"",price:"",durationMinutes:120,originalCount:0,retouchedCount:10,deliveryDays:7,revisionCount:1,includesText:"",bookingNotice:"",refundRule:""}}
async function loadProfiles(){loading.value=true;try{const r=await listMyCreatorProfiles();profiles.value=r.rows||[];if(selected.value){selected.value=profiles.value.find(x=>x.creatorId===selected.value.creatorId)||profiles.value[0]||null}else selected.value=profiles.value[0]||null;if(selected.value){fillProfile(selected.value);await loadContent()}}finally{loading.value=false}}
async function loadContent(){if(!selected.value)return;const r=await getMyCreatorContent(selected.value.creatorId);Object.assign(content,r.data||r)}
function fillProfile(item){Object.assign(profile,{roleCode:item.roleCode,displayName:item.displayName||"",headline:item.headline||"",bio:item.bio||"",avatarUrl:item.avatarUrl||"",coverUrl:item.coverUrl||"",cityCode:item.cityCode||"",serviceCitiesText:(item.serviceCities||[]).join(","),tagsText:(item.tags||[]).join(","),yearsExperience:item.yearsExperience||0,basePrice:item.basePrice??"",acceptMutual:Boolean(item.acceptMutual)})}
function selectProfile(item){selected.value=item;fillProfile(item);loadContent()}function startNewProfile(){selected.value=null;Object.assign(profile,emptyProfile());Object.assign(content,{works:[],packages:[]});activeTab.value="profile"}
async function uploadAvatar(){const url=await chooseAndUploadImage();if(url)profile.avatarUrl=url}async function uploadCover(){const url=await chooseAndUploadImage();if(url)profile.coverUrl=url}async function addWorkImage(){const url=await chooseAndUploadImage();if(url&&work.assets.length<30)work.assets.push(url)}function removeWorkImage(i){work.assets.splice(i,1)}
async function submitProfile(){if(profile.displayName.trim().length<2||!profile.cityCode.trim())return uni.showToast({title:"请填写名称和城市",icon:"none"});const r=await saveCreatorProfile({roleCode:profile.roleCode,displayName:profile.displayName.trim(),headline:profile.headline.trim()||null,bio:profile.bio.trim()||null,avatarUrl:profile.avatarUrl||null,coverUrl:profile.coverUrl||null,cityCode:profile.cityCode.trim(),serviceCities:split(profile.serviceCitiesText),tags:split(profile.tagsText),yearsExperience:Number(profile.yearsExperience||0),basePrice:profile.basePrice===""?null:Number(profile.basePrice),acceptMutual:profile.acceptMutual});selected.value=r.data||r;uni.showToast({title:"已提交审核",icon:"success"});loadProfiles()}
async function submitWork(){if(!selected.value)return uni.showToast({title:"请先创建创作者资料",icon:"none"});if(!work.assets.length||work.title.trim().length<2)return uni.showToast({title:"请上传图片并填写标题",icon:"none"});await createCreatorWork({creatorId:selected.value.creatorId,title:work.title.trim(),description:work.description.trim()||null,category:work.category.trim(),coverUrl:work.assets[0],assets:[...work.assets],tags:split(work.tagsText),cityCode:work.cityCode.trim()||null,shotDate:null});Object.assign(work,emptyWork());uni.showToast({title:"作品已提交",icon:"success"});loadContent()}
async function submitPackage(){if(!selected.value)return uni.showToast({title:"请先创建创作者资料",icon:"none"});if(selected.value.certificationStatus!=="approved")return uni.showToast({title:"资料审核通过后才能发布套餐",icon:"none"});if(pkg.packageName.trim().length<2||pkg.description.trim().length<10||Number(pkg.price)<=0)return uni.showToast({title:"请完整填写套餐信息",icon:"none"});await createServicePackage({creatorId:selected.value.creatorId,packageName:pkg.packageName.trim(),description:pkg.description.trim(),coverUrl:null,price:Number(pkg.price),durationMinutes:Number(pkg.durationMinutes),originalCount:Number(pkg.originalCount),retouchedCount:Number(pkg.retouchedCount),deliveryDays:Number(pkg.deliveryDays),revisionCount:Number(pkg.revisionCount),includes:split(pkg.includesText),excludes:[],addons:[],bookingNotice:pkg.bookingNotice.trim()||null,refundRule:pkg.refundRule.trim()||null});Object.assign(pkg,emptyPackage());uni.showToast({title:"套餐已提交",icon:"success"});loadContent()}
function split(v){return String(v||"").split(/[,，]/).map(x=>x.trim()).filter(Boolean)}function roleLabel(v){return roleOptions.find(x=>x.value===v)?.label||v}function statusLabel(v){return{draft:"草稿",pending_audit:"审核中",published:"已发布",rejected:"已驳回"}[v]||v}function statusColor(v){return v==="published"?"text-emerald-600":v==="rejected"?"text-rose-500":"text-amber-600"}
</script>

<style scoped>
.form-label{display:block;margin-bottom:12rpx;font-size:22rpx;font-weight:700;color:#52525b}.form-input{width:100%;height:88rpx;padding:0 28rpx;border-radius:28rpx;background:#fafafa;font-size:26rpx;color:#18181b}.form-area{width:100%;height:200rpx;padding:28rpx;border-radius:28rpx;background:#fafafa;font-size:26rpx;color:#18181b}.primary-action{height:96rpx;border-radius:28rpx;background:#18181b;color:#fff;display:flex;align-items:center;justify-content:center;font-size:28rpx;font-weight:800}
</style>
