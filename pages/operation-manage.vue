<template>
  <div class="operation-container">
    <el-card shadow="never">
      <el-tabs v-model="activeTab">
        <!-- 轮播图管理 -->
        <el-tab-pane label="轮播图管理" name="banner">
          <div class="tab-header">
            <el-button type="primary" :icon="Plus" @click="handleAddBanner">新增轮播图</el-button>
          </div>
          <el-table :data="bannerData" border stripe>
            <el-table-column label="图片预览" width="180" align="center">
              <template #default="{ row }">
                <el-image :src="row.image" fit="cover" class="banner-preview" :preview-src-list="[row.image]" />
              </template>
            </el-table-column>
            <el-table-column prop="title" label="标题" min-width="150" />
            <el-table-column prop="link" label="链接地址" min-width="200" show-overflow-tooltip />
            <el-table-column prop="sort" label="排序" width="100" align="center" />
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-switch
                  v-model="row.status"
                  :active-value="1"
                  :inactive-value="0"
                  active-text="启用"
                  inactive-text="禁用"
                  @change="handleBannerStatusChange(row)"
                />
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="180" align="center" />
            <el-table-column label="操作" width="180" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditBanner(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteBanner(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 推荐位管理 -->
        <el-tab-pane label="推荐位管理" name="recommend">
          <div class="tab-header">
            <el-button type="primary" :icon="Plus" @click="handleAddRecommend">新增推荐</el-button>
          </div>
          <el-table :data="recommendData" border stripe>
            <el-table-column prop="title" label="标题" min-width="150" />
            <el-table-column prop="type" label="推荐类型" width="120" align="center">
              <template #default="{ row }">
                <el-tag effect="plain">{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="targetId" label="关联ID" width="120" align="center" />
            <el-table-column prop="sort" label="排序" width="100" align="center" />
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-switch v-model="row.status" :active-value="1" :inactive-value="0" />
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="180" align="center" />
            <el-table-column label="操作" width="180" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditRecommend(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteRecommend(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 活动管理 -->
        <el-tab-pane label="活动管理" name="activity">
          <div class="tab-header">
            <el-button type="primary" :icon="Plus" @click="handleAddActivity">新增活动</el-button>
          </div>
          <el-table :data="activityData" border stripe>
            <el-table-column prop="name" label="活动名称" min-width="180" />
            <el-table-column prop="type" label="活动类型" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="activityTypeMap[row.type]?.type">{{ activityTypeMap[row.type]?.label }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="startTime" label="开始时间" width="180" align="center" />
            <el-table-column prop="endTime" label="结束时间" width="180" align="center" />
            <el-table-column prop="participants" label="参与人数" width="100" align="center" />
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="activityStatusMap[row.status]?.type" effect="dark" round>
                  {{ activityStatusMap[row.status]?.label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditActivity(row)">编辑</el-button>
                <el-button type="warning" link size="small" @click="handleViewActivity(row)">数据</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteActivity(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 优惠券管理 -->
        <el-tab-pane label="优惠券管理" name="coupon">
          <div class="tab-header">
            <el-button type="primary" :icon="Plus" @click="handleAddCoupon">新增优惠券</el-button>
          </div>
          <el-table :data="couponData" border stripe>
            <el-table-column prop="name" label="优惠券名称" min-width="160" />
            <el-table-column label="类型" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="row.type === '满减' ? 'primary' : 'success'">{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="面额" width="120" align="center">
              <template #default="{ row }">
                <span class="coupon-amount">¥{{ row.amount }}</span>
              </template>
            </el-table-column>
            <el-table-column label="使用条件" width="150" align="center">
              <template #default="{ row }">
                <span v-if="row.condition > 0">满{{ row.condition }}可用</span>
                <span v-else>无门槛</span>
              </template>
            </el-table-column>
            <el-table-column label="有效期" width="260" align="center">
              <template #default="{ row }">
                {{ row.startDate }} ~ {{ row.endDate }}
              </template>
            </el-table-column>
            <el-table-column label="发放/使用" width="120" align="center">
              <template #default="{ row }">
                <span>{{ row.usedCount }}/{{ row.totalCount }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="couponStatusMap[row.status]?.type" effect="dark" round>
                  {{ couponStatusMap[row.status]?.label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditCoupon(row)">编辑</el-button>
                <el-button type="success" link size="small" @click="handleDistributeCoupon(row)">发放</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteCoupon(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 公告管理 -->
        <el-tab-pane label="公告管理" name="notice">
          <div class="tab-header">
            <el-button type="primary" :icon="Plus" @click="handleAddNotice">发布公告</el-button>
          </div>
          <el-table :data="noticeData" border stripe>
            <el-table-column prop="title" label="公告标题" min-width="200" />
            <el-table-column prop="type" label="类型" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="noticeTypeMap[row.type]?.type">{{ noticeTypeMap[row.type]?.label }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="publishTime" label="发布时间" width="180" align="center" />
            <el-table-column prop="publisher" label="发布人" width="120" align="center" />
            <el-table-column prop="viewCount" label="阅读量" width="100" align="center" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="row.status === 1 ? 'success' : 'info'" effect="dark" round>
                  {{ row.status === 1 ? '已发布' : '草稿' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditNotice(row)">编辑</el-button>
                <el-button type="warning" link size="small" @click="handlePreviewNotice(row)">预览</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteNotice(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 轮播图编辑弹窗 -->
    <el-dialog v-model="bannerDialogVisible" :title="bannerForm.id ? '编辑轮播图' : '新增轮播图'" width="600px" destroy-on-close>
      <el-form :model="bannerForm" :rules="bannerRules" ref="bannerFormRef" label-width="100px">
        <el-form-item label="轮播图" prop="image">
          <el-upload
            class="banner-uploader"
            action="#"
            :show-file-list="false"
            :auto-upload="false"
          >
            <el-image v-if="bannerForm.image" :src="bannerForm.image" fit="cover" class="uploaded-banner" />
            <el-icon v-else class="upload-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="bannerForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="链接地址" prop="link">
          <el-input v-model="bannerForm.link" placeholder="请输入跳转链接" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="bannerForm.sort" :min="0" :max="999" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="bannerForm.status" :active-value="1" :inactive-value="0" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="bannerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveBanner">保存</el-button>
      </template>
    </el-dialog>

    <!-- 优惠券编辑弹窗 -->
    <el-dialog v-model="couponDialogVisible" :title="couponForm.id ? '编辑优惠券' : '新增优惠券'" width="600px" destroy-on-close>
      <el-form :model="couponForm" :rules="couponRules" ref="couponFormRef" label-width="100px">
        <el-form-item label="优惠券名称" prop="name">
          <el-input v-model="couponForm.name" placeholder="请输入优惠券名称" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="couponForm.type">
            <el-radio label="满减">满减券</el-radio>
            <el-radio label="折扣">折扣券</el-radio>
            <el-radio label="无门槛">无门槛券</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="面额" prop="amount">
          <el-input-number v-model="couponForm.amount" :min="1" :max="10000" :precision="2" />
        </el-form-item>
        <el-form-item label="使用条件" prop="condition">
          <el-input-number v-model="couponForm.condition" :min="0" :max="10000" :precision="2" />
          <span class="form-tip">元，0表示无门槛</span>
        </el-form-item>
        <el-form-item label="有效期" prop="dateRange">
          <el-date-picker
            v-model="couponForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="发放数量" prop="totalCount">
          <el-input-number v-model="couponForm.totalCount" :min="1" :max="100000" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="couponDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCoupon">保存</el-button>
      </template>
    </el-dialog>

    <!-- 公告编辑弹窗 -->
    <el-dialog v-model="noticeDialogVisible" :title="noticeForm.id ? '编辑公告' : '发布公告'" width="700px" destroy-on-close>
      <el-form :model="noticeForm" :rules="noticeRules" ref="noticeFormRef" label-width="100px">
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="noticeForm.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="公告类型" prop="type">
          <el-select v-model="noticeForm.type" placeholder="请选择类型">
            <el-option label="系统公告" value="system" />
            <el-option label="活动公告" value="activity" />
            <el-option label="更新公告" value="update" />
            <el-option label="安全公告" value="security" />
          </el-select>
        </el-form-item>
        <el-form-item label="公告内容" prop="content">
          <el-input v-model="noticeForm.content" type="textarea" :rows="8" placeholder="请输入公告内容" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="noticeForm.status">
            <el-radio :label="1">立即发布</el-radio>
            <el-radio :label="0">存为草稿</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="noticeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveNotice">保存</el-button>
      </template>
    </el-dialog>

    <!-- 公告预览弹窗 -->
    <el-dialog v-model="noticePreviewVisible" title="公告预览" width="600px">
      <div v-if="previewNotice" class="notice-preview">
        <h2>{{ previewNotice.title }}</h2>
        <div class="notice-meta">
          <span>类型：{{ noticeTypeMap[previewNotice.type]?.label }}</span>
          <span>发布时间：{{ previewNotice.publishTime }}</span>
          <span>发布人：{{ previewNotice.publisher }}</span>
        </div>
        <div class="notice-content">{{ previewNotice.content }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

const activeTab = ref('banner')

// 表单引用
const bannerFormRef = ref<FormInstance>()
const couponFormRef = ref<FormInstance>()
const noticeFormRef = ref<FormInstance>()

// 弹窗控制
const bannerDialogVisible = ref(false)
const couponDialogVisible = ref(false)
const noticeDialogVisible = ref(false)
const noticePreviewVisible = ref(false)
const previewNotice = ref<any>(null)

// 类型映射
const activityTypeMap: Record<string, { label: string; type: string }> = {
  discount: { label: '优惠活动', type: 'primary' },
  competition: { label: '比赛活动', type: 'success' },
  promotion: { label: '推广活动', type: 'warning' }
}

const activityStatusMap: Record<string, { label: string; type: string }> = {
  upcoming: { label: '未开始', type: 'info' },
  ongoing: { label: '进行中', type: 'success' },
  ended: { label: '已结束', type: 'danger' }
}

const couponStatusMap: Record<string, { label: string; type: string }> = {
  active: { label: '进行中', type: 'success' },
  upcoming: { label: '未开始', type: 'info' },
  ended: { label: '已结束', type: 'danger' }
}

const noticeTypeMap: Record<string, { label: string; type: string }> = {
  system: { label: '系统公告', type: 'primary' },
  activity: { label: '活动公告', type: 'success' },
  update: { label: '更新公告', type: 'warning' },
  security: { label: '安全公告', type: 'danger' }
}

// 轮播图表单
const bannerForm = reactive({
  id: 0,
  image: '',
  title: '',
  link: '',
  sort: 0,
  status: 1
})

const bannerRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  image: [{ required: true, message: '请上传轮播图', trigger: 'change' }]
}

// 优惠券表单
const couponForm = reactive({
  id: 0,
  name: '',
  type: '满减',
  amount: 50,
  condition: 200,
  dateRange: [] as string[],
  totalCount: 1000
})

const couponRules = {
  name: [{ required: true, message: '请输入优惠券名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  amount: [{ required: true, message: '请输入面额', trigger: 'blur' }]
}

// 公告表单
const noticeForm = reactive({
  id: 0,
  title: '',
  type: 'system',
  content: '',
  status: 1
})

const noticeRules = {
  title: [{ required: true, message: '请输入公告标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择公告类型', trigger: 'change' }],
  content: [{ required: true, message: '请输入公告内容', trigger: 'blur' }]
}

// 轮播图数据
const bannerData = ref([
  {
    id: 1,
    image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
    title: '新用户专享 首单立减50元',
    link: '/pages/activity/newcomer',
    sort: 1,
    status: 1,
    createTime: '2026-06-10 10:00:00'
  },
  {
    id: 2,
    image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
    title: '毕业季特惠 拍照8折起',
    link: '/pages/activity/graduation',
    sort: 2,
    status: 1,
    createTime: '2026-06-08 14:30:00'
  },
  {
    id: 3,
    image: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
    title: '摄影师入驻 享专属流量',
    link: '/pages/recruit/photographer',
    sort: 3,
    status: 0,
    createTime: '2026-06-05 09:00:00'
  }
])

// 推荐位数据
const recommendData = ref([
  { id: 1, title: '热门摄影师推荐', type: '摄影师', targetId: 'P1001', sort: 1, status: 1, createTime: '2026-06-10 10:00:00' },
  { id: 2, title: '精选写真套餐', type: '套餐', targetId: 'T2001', sort: 2, status: 1, createTime: '2026-06-09 14:00:00' },
  { id: 3, title: '人气模特推荐', type: '模特', targetId: 'M3001', sort: 3, status: 1, createTime: '2026-06-08 09:00:00' },
  { id: 4, title: '优质商家推荐', type: '商家', targetId: 'S4001', sort: 4, status: 0, createTime: '2026-06-07 16:00:00' }
])

// 活动数据
const activityData = ref([
  {
    id: 1,
    name: '毕业季摄影特惠',
    type: 'discount',
    startTime: '2026-06-01 00:00:00',
    endTime: '2026-06-30 23:59:59',
    participants: 1256,
    status: 'ongoing'
  },
  {
    id: 2,
    name: '最美证件照评选',
    type: 'competition',
    startTime: '2026-07-01 00:00:00',
    endTime: '2026-07-15 23:59:59',
    participants: 0,
    status: 'upcoming'
  },
  {
    id: 3,
    name: '新用户邀请有礼',
    type: 'promotion',
    startTime: '2026-05-01 00:00:00',
    endTime: '2026-05-31 23:59:59',
    participants: 3420,
    status: 'ended'
  }
])

// 优惠券数据
const couponData = ref([
  {
    id: 1,
    name: '新人专享券',
    type: '满减',
    amount: 50,
    condition: 200,
    startDate: '2026-06-01',
    endDate: '2026-06-30',
    usedCount: 456,
    totalCount: 1000,
    status: 'active'
  },
  {
    id: 2,
    name: '摄影套餐折扣券',
    type: '折扣',
    amount: 20,
    condition: 100,
    startDate: '2026-06-15',
    endDate: '2026-07-15',
    usedCount: 89,
    totalCount: 500,
    status: 'active'
  },
  {
    id: 3,
    name: '无门槛优惠券',
    type: '无门槛',
    amount: 10,
    condition: 0,
    startDate: '2026-07-01',
    endDate: '2026-07-31',
    usedCount: 0,
    totalCount: 2000,
    status: 'upcoming'
  },
  {
    id: 4,
    name: '母亲节特惠券',
    type: '满减',
    amount: 100,
    condition: 500,
    startDate: '2026-05-01',
    endDate: '2026-05-15',
    usedCount: 320,
    totalCount: 300,
    status: 'ended'
  }
])

// 公告数据
const noticeData = ref([
  {
    id: 1,
    title: '关于平台服务费率调整的公告',
    type: 'system',
    content: '尊敬的用户，为提供更优质的服务，平台将于2026年7月1日起调整服务费率...',
    publishTime: '2026-06-15 10:00:00',
    publisher: '管理员',
    viewCount: 1256,
    status: 1
  },
  {
    id: 2,
    title: '毕业季摄影活动火热进行中',
    type: 'activity',
    content: '毕业季来临，91约拍Pro推出毕业季摄影特惠活动，全场8折起...',
    publishTime: '2026-06-10 14:00:00',
    publisher: '运营小王',
    viewCount: 2340,
    status: 1
  },
  {
    id: 3,
    title: 'APP 3.0版本更新说明',
    type: 'update',
    content: '91约拍Pro 3.0版本全新升级，新增AI智能推荐、视频约拍等功能...',
    publishTime: '2026-06-08 09:00:00',
    publisher: '技术小李',
    viewCount: 3456,
    status: 1
  },
  {
    id: 4,
    title: '关于加强用户隐私保护的通知',
    type: 'security',
    content: '为保障用户隐私安全，平台已升级数据加密方案...',
    publishTime: '',
    publisher: '管理员',
    viewCount: 0,
    status: 0
  }
])

// 轮播图操作
const handleAddBanner = () => {
  bannerForm.id = 0
  bannerForm.image = ''
  bannerForm.title = ''
  bannerForm.link = ''
  bannerForm.sort = 0
  bannerForm.status = 1
  bannerDialogVisible.value = true
}

const handleEditBanner = (row: any) => {
  Object.assign(bannerForm, row)
  bannerDialogVisible.value = true
}

const handleDeleteBanner = (row: any) => {
  ElMessageBox.confirm('确认删除该轮播图？', '确认删除', { type: 'warning' }).then(() => {
    const index = bannerData.value.findIndex(item => item.id === row.id)
    if (index !== -1) bannerData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const handleBannerStatusChange = (row: any) => {
  ElMessage.success(row.status === 1 ? '已启用' : '已禁用')
}

const saveBanner = () => {
  bannerDialogVisible.value = false
  ElMessage.success('保存成功')
}

// 推荐位操作
const handleAddRecommend = () => {
  ElMessage.info('新增推荐')
}

const handleEditRecommend = (row: any) => {
  ElMessage.info(`编辑推荐: ${row.title}`)
}

const handleDeleteRecommend = (row: any) => {
  ElMessageBox.confirm('确认删除该推荐位？', '确认删除', { type: 'warning' }).then(() => {
    const index = recommendData.value.findIndex(item => item.id === row.id)
    if (index !== -1) recommendData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 活动操作
const handleAddActivity = () => {
  ElMessage.info('新增活动')
}

const handleEditActivity = (row: any) => {
  ElMessage.info(`编辑活动: ${row.name}`)
}

const handleViewActivity = (row: any) => {
  ElMessage.info(`查看活动数据: ${row.name}`)
}

const handleDeleteActivity = (row: any) => {
  ElMessageBox.confirm('确认删除该活动？', '确认删除', { type: 'warning' }).then(() => {
    const index = activityData.value.findIndex(item => item.id === row.id)
    if (index !== -1) activityData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 优惠券操作
const handleAddCoupon = () => {
  couponForm.id = 0
  couponForm.name = ''
  couponForm.type = '满减'
  couponForm.amount = 50
  couponForm.condition = 200
  couponForm.dateRange = []
  couponForm.totalCount = 1000
  couponDialogVisible.value = true
}

const handleEditCoupon = (row: any) => {
  Object.assign(couponForm, row)
  couponDialogVisible.value = true
}

const handleDistributeCoupon = (row: any) => {
  ElMessageBox.prompt('请输入发放用户ID，多个用逗号分隔', '发放优惠券', {
    inputPlaceholder: '例如: 1001,1002,1003'
  }).then(({ value }) => {
    ElMessage.success(`已发放给 ${value.split(',').length} 位用户`)
  }).catch(() => {})
}

const handleDeleteCoupon = (row: any) => {
  ElMessageBox.confirm('确认删除该优惠券？', '确认删除', { type: 'warning' }).then(() => {
    const index = couponData.value.findIndex(item => item.id === row.id)
    if (index !== -1) couponData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const saveCoupon = () => {
  couponDialogVisible.value = false
  ElMessage.success('保存成功')
}

// 公告操作
const handleAddNotice = () => {
  noticeForm.id = 0
  noticeForm.title = ''
  noticeForm.type = 'system'
  noticeForm.content = ''
  noticeForm.status = 1
  noticeDialogVisible.value = true
}

const handleEditNotice = (row: any) => {
  Object.assign(noticeForm, row)
  noticeDialogVisible.value = true
}

const handlePreviewNotice = (row: any) => {
  previewNotice.value = row
  noticePreviewVisible.value = true
}

const handleDeleteNotice = (row: any) => {
  ElMessageBox.confirm('确认删除该公告？', '确认删除', { type: 'warning' }).then(() => {
    const index = noticeData.value.findIndex(item => item.id === row.id)
    if (index !== -1) noticeData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const saveNotice = () => {
  noticeDialogVisible.value = false
  ElMessage.success('保存成功')
}
</script>

<style scoped>
.operation-container {
  padding: 20px;
}

.tab-header {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-end;
}

.banner-preview {
  width: 120px;
  height: 60px;
  border-radius: 4px;
}

.banner-uploader {
  width: 300px;
  height: 150px;
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
}

.banner-uploader:hover {
  border-color: #6734E8;
}

.uploaded-banner {
  width: 100%;
  height: 100%;
}

.upload-icon {
  font-size: 28px;
  color: #909399;
}

.coupon-amount {
  color: #F56C6C;
  font-weight: 700;
  font-size: 16px;
}

.form-tip {
  margin-left: 8px;
  color: #909399;
  font-size: 13px;
}

.notice-preview {
  padding: 20px;
}

.notice-preview h2 {
  text-align: center;
  margin-bottom: 16px;
  color: #303133;
}

.notice-meta {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
  color: #909399;
  font-size: 14px;
}

.notice-content {
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap;
}

:deep(.el-button--primary) {
  --el-button-bg-color: #6734E8;
  --el-button-border-color: #6734E8;
  --el-button-hover-bg-color: #7c4ddb;
  --el-button-hover-border-color: #7c4ddb;
}

:deep(.el-tabs__item.is-active) {
  color: #6734E8;
}

:deep(.el-tabs__active-bar) {
  background-color: #6734E8;
}
</style>
