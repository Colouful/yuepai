<template>
  <div class="risk-control-container">
    <!-- 风险概览 -->
    <el-row :gutter="16" class="stat-row">
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-high">
          <div class="stat-value">8</div>
          <div class="stat-label">高风险</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-medium">
          <div class="stat-value">23</div>
          <div class="stat-label">中风险</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-low">
          <div class="stat-value">56</div>
          <div class="stat-label">低风险</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card stat-blocked">
          <div class="stat-value">156</div>
          <div class="stat-label">已封禁账号</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never">
      <el-tabs v-model="activeTab">
        <!-- 风险交易监控 -->
        <el-tab-pane label="风险交易监控" name="transaction">
          <el-form :model="searchForm" inline class="search-form">
            <el-form-item label="风险等级">
              <el-select v-model="searchForm.level" placeholder="全部" clearable style="width: 150px">
                <el-option label="高风险" value="high" />
                <el-option label="中风险" value="medium" />
                <el-option label="低风险" value="low" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="全部" clearable style="width: 150px">
                <el-option label="待处理" value="pending" />
                <el-option label="处理中" value="processing" />
                <el-option label="已处理" value="resolved" />
                <el-option label="已忽略" value="ignored" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
              <el-button :icon="Refresh" @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>

          <el-table v-loading="loading" :data="transactionData" border stripe>
            <el-table-column prop="orderNo" label="订单号" width="180" />
            <el-table-column label="用户" width="140">
              <template #default="{ row }">
                <div class="user-cell">
                  <el-avatar :size="28" :src="row.userAvatar" />
                  <span>{{ row.userName }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" width="120" align="center">
              <template #default="{ row }">
                <span class="amount">¥{{ row.amount }}</span>
              </template>
            </el-table-column>
            <el-table-column label="风险等级" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="riskLevelMap[row.level].type" effect="dark" round>
                  {{ riskLevelMap[row.level].label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="reason" label="风险原因" min-width="200" show-overflow-tooltip />
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="transactionStatusMap[row.status].type" effect="plain">
                  {{ transactionStatusMap[row.status].label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="triggerTime" label="触发时间" width="180" align="center" />
            <el-table-column label="操作" width="220" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleViewTransaction(row)">详情</el-button>
                <template v-if="row.status === 'pending'">
                  <el-button type="success" link size="small" @click="handleProcessTransaction(row, 'resolved')">确认正常</el-button>
                  <el-button type="danger" link size="small" @click="handleProcessTransaction(row, 'blocked')">封禁处理</el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 用户行为分析 -->
        <el-tab-pane label="用户行为分析" name="behavior">
          <el-form :model="behaviorSearchForm" inline class="search-form">
            <el-form-item label="用户ID">
              <el-input v-model="behaviorSearchForm.userId" placeholder="请输入用户ID" clearable style="width: 200px" />
            </el-form-item>
            <el-form-item label="风险标签">
              <el-select v-model="behaviorSearchForm.tag" placeholder="全部" clearable style="width: 180px">
                <el-option label="频繁取消" value="cancel" />
                <el-option label="恶意评价" value="review" />
                <el-option label="虚假交易" value="fake" />
                <el-option label="账号异常" value="abnormal" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :icon="Search" @click="handleBehaviorSearch">搜索</el-button>
            </el-form-item>
          </el-form>

          <el-table :data="behaviorData" border stripe>
            <el-table-column label="用户" width="160">
              <template #default="{ row }">
                <div class="user-cell">
                  <el-avatar :size="32" :src="row.avatar" />
                  <div class="user-detail">
                    <div class="user-name">{{ row.userName }}</div>
                    <div class="user-id">ID: {{ row.userId }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="orderCount" label="订单数" width="100" align="center" />
            <el-table-column prop="cancelRate" label="取消率" width="100" align="center">
              <template #default="{ row }">
                <span :class="{ 'text-danger': row.cancelRate > 30 }">{{ row.cancelRate }}%</span>
              </template>
            </el-table-column>
            <el-table-column prop="complaintCount" label="被投诉次数" width="120" align="center" />
            <el-table-column prop="refundRate" label="退款率" width="100" align="center">
              <template #default="{ row }">
                <span :class="{ 'text-danger': row.refundRate > 20 }">{{ row.refundRate }}%</span>
              </template>
            </el-table-column>
            <el-table-column label="风险标签" min-width="200">
              <template #default="{ row }">
                <el-tag
                  v-for="tag in row.riskTags"
                  :key="tag"
                  :type="tagTypeMap[tag]"
                  effect="plain"
                  class="risk-tag"
                >
                  {{ tagLabelMap[tag] }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="风险评分" width="120" align="center">
              <template #default="{ row }">
                <el-progress
                  :percentage="row.riskScore"
                  :color="row.riskScore >= 70 ? '#F56C6C' : row.riskScore >= 40 ? '#E6A23C' : '#67C23A'"
                  :stroke-width="10"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleViewBehavior(row)">详情</el-button>
                <el-button type="danger" link size="small" @click="handleBlockUser(row)">封禁</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 封禁管理 -->
        <el-tab-pane label="封禁管理" name="blocked">
          <div class="tab-header">
            <el-button type="danger" :icon="Plus" @click="handleAddBlock">手动封禁</el-button>
            <el-button type="warning" plain @click="handleExportBlock">导出封禁列表</el-button>
          </div>

          <el-table :data="blockedData" border stripe>
            <el-table-column label="用户" width="160">
              <template #default="{ row }">
                <div class="user-cell">
                  <el-avatar :size="32" :src="row.avatar" />
                  <div class="user-detail">
                    <div class="user-name">{{ row.userName }}</div>
                    <div class="user-phone">{{ row.phone }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="blockType" label="封禁类型" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="row.blockType === 'permanent' ? 'danger' : 'warning'" effect="dark">
                  {{ row.blockType === 'permanent' ? '永久封禁' : '临时封禁' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="reason" label="封禁原因" min-width="200" show-overflow-tooltip />
            <el-table-column prop="blockTime" label="封禁时间" width="180" align="center" />
            <el-table-column prop="expireTime" label="解封时间" width="180" align="center">
              <template #default="{ row }">
                <span>{{ row.expireTime || '永久' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="operator" label="操作人" width="120" align="center" />
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'danger' : 'info'" effect="dark" round>
                  {{ row.status === 'active' ? '封禁中' : '已解封' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center" fixed="right">
              <template #default="{ row }">
                <el-button v-if="row.status === 'active'" type="warning" link size="small" @click="handleUnblock(row)">解封</el-button>
                <el-button type="primary" link size="small" @click="handleViewBlockDetail(row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 风控规则 -->
        <el-tab-pane label="风控规则" name="rules">
          <div class="tab-header">
            <el-button type="primary" :icon="Plus" @click="handleAddRule">新增规则</el-button>
          </div>

          <el-table :data="ruleData" border stripe>
            <el-table-column prop="name" label="规则名称" min-width="180" />
            <el-table-column prop="type" label="规则类型" width="120" align="center">
              <template #default="{ row }">
                <el-tag effect="plain">{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="规则描述" min-width="250" show-overflow-tooltip />
            <el-table-column prop="triggerCount" label="触发次数" width="100" align="center" />
            <el-table-column label="状态" width="120" align="center">
              <template #default="{ row }">
                <el-switch
                  v-model="row.status"
                  :active-value="1"
                  :inactive-value="0"
                  active-text="启用"
                  inactive-text="禁用"
                  @change="handleRuleStatusChange(row)"
                />
              </template>
            </el-table-column>
            <el-table-column prop="updateTime" label="更新时间" width="180" align="center" />
            <el-table-column label="操作" width="180" align="center" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditRule(row)">编辑</el-button>
                <el-button type="warning" link size="small" @click="handleTestRule(row)">测试</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteRule(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 操作日志 -->
        <el-tab-pane label="操作日志" name="log">
          <el-form :model="logSearchForm" inline class="search-form">
            <el-form-item label="操作类型">
              <el-select v-model="logSearchForm.type" placeholder="全部" clearable style="width: 150px">
                <el-option label="封禁" value="block" />
                <el-option label="解封" value="unblock" />
                <el-option label="退款" value="refund" />
                <el-option label="规则变更" value="rule" />
              </el-select>
            </el-form-item>
            <el-form-item label="操作人">
              <el-input v-model="logSearchForm.operator" placeholder="请输入操作人" clearable style="width: 150px" />
            </el-form-item>
            <el-form-item label="时间范围">
              <el-date-picker
                v-model="logSearchForm.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :icon="Search" @click="handleLogSearch">搜索</el-button>
            </el-form-item>
          </el-form>

          <el-table :data="logData" border stripe>
            <el-table-column prop="id" label="日志ID" width="100" align="center" />
            <el-table-column prop="type" label="操作类型" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="logTypeMap[row.type]?.type">{{ logTypeMap[row.type]?.label }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="target" label="操作对象" width="160" />
            <el-table-column prop="description" label="操作描述" min-width="250" show-overflow-tooltip />
            <el-table-column prop="operator" label="操作人" width="120" align="center" />
            <el-table-column prop="ip" label="IP地址" width="140" align="center" />
            <el-table-column prop="operateTime" label="操作时间" width="180" align="center" />
          </el-table>

          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="logPagination.page"
              v-model:page-size="logPagination.size"
              :page-sizes="[20, 50, 100]"
              :total="logPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              background
            />
          </div>
        </el-tab-pane>
      </el-tabs>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          background
        />
      </div>
    </el-card>

    <!-- 手动封禁弹窗 -->
    <el-dialog v-model="blockDialogVisible" title="手动封禁" width="500px" destroy-on-close>
      <el-form :model="blockForm" :rules="blockRules" ref="blockFormRef" label-width="100px">
        <el-form-item label="用户ID" prop="userId">
          <el-input v-model="blockForm.userId" placeholder="请输入用户ID" />
        </el-form-item>
        <el-form-item label="封禁类型" prop="blockType">
          <el-radio-group v-model="blockForm.blockType">
            <el-radio label="temporary">临时封禁</el-radio>
            <el-radio label="permanent">永久封禁</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="blockForm.blockType === 'temporary'" label="封禁时长" prop="duration">
          <el-select v-model="blockForm.duration" placeholder="请选择">
            <el-option label="1天" :value="1" />
            <el-option label="3天" :value="3" />
            <el-option label="7天" :value="7" />
            <el-option label="30天" :value="30" />
            <el-option label="90天" :value="90" />
          </el-select>
        </el-form-item>
        <el-form-item label="封禁原因" prop="reason">
          <el-input v-model="blockForm.reason" type="textarea" :rows="3" placeholder="请输入封禁原因" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="blockDialogVisible = false">取消</el-button>
        <el-button type="danger" :loading="blockLoading" @click="confirmBlock">确认封禁</el-button>
      </template>
    </el-dialog>

    <!-- 风控规则编辑弹窗 -->
    <el-dialog v-model="ruleDialogVisible" :title="ruleForm.id ? '编辑规则' : '新增规则'" width="600px" destroy-on-close>
      <el-form :model="ruleForm" :rules="ruleRules" ref="ruleFormRef" label-width="100px">
        <el-form-item label="规则名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="规则类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择">
            <el-option label="交易风控" value="交易风控" />
            <el-option label="账号风控" value="账号风控" />
            <el-option label="内容风控" value="内容风控" />
            <el-option label="行为风控" value="行为风控" />
          </el-select>
        </el-form-item>
        <el-form-item label="规则描述" prop="description">
          <el-input v-model="ruleForm.description" type="textarea" :rows="3" placeholder="请输入规则描述" />
        </el-form-item>
        <el-form-item label="触发条件" prop="condition">
          <el-input v-model="ruleForm.condition" type="textarea" :rows="4" placeholder="请输入触发条件（JSON格式）" />
        </el-form-item>
        <el-form-item label="处理动作" prop="action">
          <el-checkbox-group v-model="ruleForm.actions">
            <el-checkbox label="alert">告警通知</el-checkbox>
            <el-checkbox label="block">自动封禁</el-checkbox>
            <el-checkbox label="freeze">冻结资金</el-checkbox>
            <el-checkbox label="review">人工审核</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ruleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRule">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

const activeTab = ref('transaction')
const loading = ref(false)
const blockLoading = ref(false)

// 表单引用
const blockFormRef = ref<FormInstance>()
const ruleFormRef = ref<FormInstance>()

// 弹窗控制
const blockDialogVisible = ref(false)
const ruleDialogVisible = ref(false)

// 搜索表单
const searchForm = reactive({ level: '', status: '' })
const behaviorSearchForm = reactive({ userId: '', tag: '' })
const logSearchForm = reactive({ type: '', operator: '', dateRange: [] })

// 分页
const pagination = reactive({ page: 1, size: 10, total: 50 })
const logPagination = reactive({ page: 1, size: 20, total: 100 })

// 类型映射
const riskLevelMap: Record<string, { label: string; type: string }> = {
  high: { label: '高风险', type: 'danger' },
  medium: { label: '中风险', type: 'warning' },
  low: { label: '低风险', type: 'info' }
}

const transactionStatusMap: Record<string, { label: string; type: string }> = {
  pending: { label: '待处理', type: 'warning' },
  processing: { label: '处理中', type: 'primary' },
  resolved: { label: '已处理', type: 'success' },
  ignored: { label: '已忽略', type: 'info' }
}

const tagTypeMap: Record<string, string> = {
  cancel: 'warning',
  review: 'danger',
  fake: 'danger',
  abnormal: 'warning'
}

const tagLabelMap: Record<string, string> = {
  cancel: '频繁取消',
  review: '恶意评价',
  fake: '虚假交易',
  abnormal: '账号异常'
}

const logTypeMap: Record<string, { label: string; type: string }> = {
  block: { label: '封禁', type: 'danger' },
  unblock: { label: '解封', type: 'success' },
  refund: { label: '退款', type: 'warning' },
  rule: { label: '规则变更', type: 'primary' }
}

// 手动封禁表单
const blockForm = reactive({
  userId: '',
  blockType: 'temporary',
  duration: 7,
  reason: ''
})

const blockRules = {
  userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  blockType: [{ required: true, message: '请选择封禁类型', trigger: 'change' }],
  reason: [{ required: true, message: '请输入封禁原因', trigger: 'blur' }]
}

// 风控规则表单
const ruleForm = reactive({
  id: 0,
  name: '',
  type: '',
  description: '',
  condition: '',
  actions: [] as string[]
})

const ruleRules = {
  name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择规则类型', trigger: 'change' }],
  description: [{ required: true, message: '请输入规则描述', trigger: 'blur' }]
}

// 风险交易数据
const transactionData = ref([
  {
    id: 1,
    orderNo: 'YP20260615001',
    userName: '张三',
    userAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 9999,
    level: 'high',
    reason: '单笔金额异常，超出正常范围3倍',
    status: 'pending',
    triggerTime: '2026-06-15 14:30:00'
  },
  {
    id: 2,
    orderNo: 'YP20260615002',
    userName: '李四',
    userAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 5000,
    level: 'medium',
    reason: '同一用户1小时内下单5次，疑似刷单',
    status: 'pending',
    triggerTime: '2026-06-15 13:20:00'
  },
  {
    id: 3,
    orderNo: 'YP20260615003',
    userName: '王五',
    userAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 2000,
    level: 'low',
    reason: '新用户首单大额交易',
    status: 'resolved',
    triggerTime: '2026-06-15 11:45:00'
  },
  {
    id: 4,
    orderNo: 'YP20260614004',
    userName: '赵六',
    userAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 8000,
    level: 'high',
    reason: '关联账号多次异常退款，疑似套现',
    status: 'processing',
    triggerTime: '2026-06-14 22:10:00'
  },
  {
    id: 5,
    orderNo: 'YP20260614005',
    userName: '孙七',
    userAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    amount: 1500,
    level: 'medium',
    reason: '异地登录后立即大额交易',
    status: 'ignored',
    triggerTime: '2026-06-14 18:30:00'
  }
])

// 用户行为数据
const behaviorData = ref([
  {
    userId: 'U1001',
    userName: '张三',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    orderCount: 15,
    cancelRate: 40,
    complaintCount: 3,
    refundRate: 25,
    riskTags: ['cancel', 'fake'],
    riskScore: 85
  },
  {
    userId: 'U1002',
    userName: '李四',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    orderCount: 28,
    cancelRate: 15,
    complaintCount: 5,
    refundRate: 10,
    riskTags: ['review'],
    riskScore: 62
  },
  {
    userId: 'U1003',
    userName: '王五',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    orderCount: 50,
    cancelRate: 8,
    complaintCount: 1,
    refundRate: 5,
    riskTags: [],
    riskScore: 25
  },
  {
    userId: 'U1004',
    userName: '赵六',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    orderCount: 8,
    cancelRate: 60,
    complaintCount: 7,
    refundRate: 50,
    riskTags: ['cancel', 'review', 'fake', 'abnormal'],
    riskScore: 95
  }
])

// 封禁数据
const blockedData = ref([
  {
    id: 1,
    userName: '赵六',
    phone: '138****1234',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    blockType: 'permanent',
    reason: '虚假交易、恶意套现，累计违规5次',
    blockTime: '2026-06-14 22:30:00',
    expireTime: '',
    operator: '管理员A',
    status: 'active'
  },
  {
    id: 2,
    userName: '钱八',
    phone: '139****5678',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    blockType: 'temporary',
    reason: '发布违规内容，首次违规',
    blockTime: '2026-06-13 10:00:00',
    expireTime: '2026-06-20 10:00:00',
    operator: '管理员B',
    status: 'active'
  },
  {
    id: 3,
    userName: '周九',
    phone: '137****9012',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    blockType: 'temporary',
    reason: '多次恶意差评',
    blockTime: '2026-06-10 14:00:00',
    expireTime: '2026-06-17 14:00:00',
    operator: '管理员A',
    status: 'unblocked'
  }
])

// 风控规则数据
const ruleData = ref([
  {
    id: 1,
    name: '大额交易预警',
    type: '交易风控',
    description: '单笔交易金额超过设定阈值时触发预警',
    triggerCount: 156,
    status: 1,
    updateTime: '2026-06-10 10:00:00'
  },
  {
    id: 2,
    name: '高频交易拦截',
    type: '交易风控',
    description: '同一用户短时间内多次下单时触发拦截',
    triggerCount: 89,
    status: 1,
    updateTime: '2026-06-08 14:30:00'
  },
  {
    id: 3,
    name: '异常登录检测',
    type: '账号风控',
    description: '检测异地登录、频繁密码错误等异常行为',
    triggerCount: 234,
    status: 1,
    updateTime: '2026-06-05 09:00:00'
  },
  {
    id: 4,
    name: '恶意评价识别',
    type: '行为风控',
    description: '识别恶意差评、刷好评等异常评价行为',
    triggerCount: 67,
    status: 1,
    updateTime: '2026-06-03 16:00:00'
  },
  {
    id: 5,
    name: '敏感词过滤',
    type: '内容风控',
    description: '对用户发布的文字内容进行敏感词检测',
    triggerCount: 456,
    status: 0,
    updateTime: '2026-06-01 11:00:00'
  }
])

// 操作日志数据
const logData = ref([
  { id: 1001, type: 'block', target: '赵六 (U1004)', description: '永久封禁用户账号，原因：虚假交易、恶意套现', operator: '管理员A', ip: '192.168.1.100', operateTime: '2026-06-14 22:30:00' },
  { id: 1002, type: 'refund', target: '订单YP20260614003', description: '人工确认退款¥299.00', operator: '管理员B', ip: '192.168.1.101', operateTime: '2026-06-14 20:15:00' },
  { id: 1003, type: 'block', target: '钱八 (U1005)', description: '临时封禁7天，原因：发布违规内容', operator: '管理员B', ip: '192.168.1.101', operateTime: '2026-06-13 10:00:00' },
  { id: 1004, type: 'unblock', target: '周九 (U1006)', description: '提前解封用户账号', operator: '管理员A', ip: '192.168.1.100', operateTime: '2026-06-12 15:30:00' },
  { id: 1005, type: 'rule', target: '大额交易预警', description: '修改预警阈值从5000元调整为8000元', operator: '管理员A', ip: '192.168.1.100', operateTime: '2026-06-10 10:00:00' }
])

// 搜索
const handleSearch = () => {
  loading.value = true
  setTimeout(() => { loading.value = false }, 500)
}

const handleReset = () => {
  searchForm.level = ''
  searchForm.status = ''
  handleSearch()
}

const handleBehaviorSearch = () => {
  loading.value = true
  setTimeout(() => { loading.value = false }, 500)
}

const handleLogSearch = () => {
  loading.value = true
  setTimeout(() => { loading.value = false }, 500)
}

// 交易详情
const handleViewTransaction = (row: any) => {
  ElMessage.info(`查看交易详情: ${row.orderNo}`)
}

// 处理交易
const handleProcessTransaction = (row: any, action: string) => {
  if (action === 'resolved') {
    ElMessageBox.confirm('确认该交易为正常交易？', '确认操作', { type: 'warning' }).then(() => {
      row.status = 'resolved'
      ElMessage.success('已确认正常')
    }).catch(() => {})
  } else {
    ElMessageBox.confirm('确认封禁该用户？', '封禁处理', { type: 'error' }).then(() => {
      row.status = 'resolved'
      ElMessage.success('已封禁处理')
    }).catch(() => {})
  }
}

// 用户行为
const handleViewBehavior = (row: any) => {
  ElMessage.info(`查看用户行为详情: ${row.userName}`)
}

const handleBlockUser = (row: any) => {
  ElMessageBox.confirm(`确认封禁用户 ${row.userName}？`, '封禁用户', { type: 'error' }).then(() => {
    ElMessage.success('已封禁')
  }).catch(() => {})
}

// 封禁管理
const handleAddBlock = () => {
  blockForm.userId = ''
  blockForm.blockType = 'temporary'
  blockForm.duration = 7
  blockForm.reason = ''
  blockDialogVisible.value = true
}

const confirmBlock = () => {
  blockLoading.value = true
  setTimeout(() => {
    blockLoading.value = false
    blockDialogVisible.value = false
    ElMessage.success('封禁成功')
  }, 800)
}

const handleUnblock = (row: any) => {
  ElMessageBox.confirm(`确认解封用户 ${row.userName}？`, '解封确认', { type: 'warning' }).then(() => {
    row.status = 'unblocked'
    ElMessage.success('已解封')
  }).catch(() => {})
}

const handleViewBlockDetail = (row: any) => {
  ElMessage.info(`查看封禁详情: ${row.userName}`)
}

const handleExportBlock = () => {
  ElMessage.success('导出成功')
}

// 风控规则
const handleAddRule = () => {
  ruleForm.id = 0
  ruleForm.name = ''
  ruleForm.type = ''
  ruleForm.description = ''
  ruleForm.condition = ''
  ruleForm.actions = []
  ruleDialogVisible.value = true
}

const handleEditRule = (row: any) => {
  Object.assign(ruleForm, row)
  ruleDialogVisible.value = true
}

const handleTestRule = (row: any) => {
  ElMessage.info(`测试规则: ${row.name}`)
}

const handleDeleteRule = (row: any) => {
  ElMessageBox.confirm(`确认删除规则 "${row.name}"？`, '确认删除', { type: 'warning' }).then(() => {
    const index = ruleData.value.findIndex(item => item.id === row.id)
    if (index !== -1) ruleData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const handleRuleStatusChange = (row: any) => {
  ElMessage.success(row.status === 1 ? '规则已启用' : '规则已禁用')
}

const saveRule = () => {
  ruleDialogVisible.value = false
  ElMessage.success('保存成功')
}
</script>

<style scoped>
.risk-control-container {
  padding: 20px;
}

.stat-row {
  margin-bottom: 16px;
}

.stat-card {
  text-align: center;
  padding: 10px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-high .stat-value { color: #F56C6C; }
.stat-medium .stat-value { color: #E6A23C; }
.stat-low .stat-value { color: #909399; }
.stat-blocked .stat-value { color: #6734E8; }

.search-form {
  margin-bottom: 16px;
}

.tab-header {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-detail {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #303133;
  font-size: 13px;
}

.user-id,
.user-phone {
  font-size: 12px;
  color: #909399;
}

.amount {
  color: #F56C6C;
  font-weight: 600;
}

.risk-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}

.text-danger {
  color: #F56C6C;
  font-weight: 600;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
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
