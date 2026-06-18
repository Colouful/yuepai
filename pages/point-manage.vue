<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
      <el-form-item label="用户昵称" prop="nickname">
        <el-input v-model="queryParams.nickname" placeholder="请输入用户昵称" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="积分范围" prop="pointRange">
        <el-input v-model="queryParams.pointMin" placeholder="最小值" style="width: 100px" />
        <span style="margin: 0 5px">-</span>
        <el-input v-model="queryParams.pointMax" placeholder="最大值" style="width: 100px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- Tab 切换 -->
    <el-tabs v-model="activeTab" @tab-click="handleTabChange">
      <!-- 积分规则配置 -->
      <el-tab-pane label="积分规则配置" name="rules">
        <el-card shadow="hover">
          <div slot="header" class="card-header">
            <span>积分获取规则</span>
            <el-button type="primary" size="mini" icon="el-icon-plus" @click="handleAddRule" v-hasPermi="['yuepai:point:config']">新增规则</el-button>
          </div>
          <el-table :data="ruleList" border>
            <el-table-column label="规则ID" prop="ruleId" width="80" align="center" />
            <el-table-column label="规则名称" prop="ruleName" width="180" />
            <el-table-column label="业务类型" prop="bizType" width="150" align="center">
              <template slot-scope="scope">
                <el-tag>{{ getBizTypeLabel(scope.row.bizType) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="积分数量" prop="points" width="120" align="center">
              <template slot-scope="scope">
                <span style="color: #67c23a; font-weight: bold">+{{ scope.row.points }}</span>
              </template>
            </el-table-column>
            <el-table-column label="每日上限" prop="dailyLimit" width="120" align="center">
              <template slot-scope="scope">
                {{ scope.row.dailyLimit > 0 ? scope.row.dailyLimit : '无限制' }}
              </template>
            </el-table-column>
            <el-table-column label="总上限" prop="totalLimit" width="120" align="center">
              <template slot-scope="scope">
                {{ scope.row.totalLimit > 0 ? scope.row.totalLimit : '无限制' }}
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100" align="center">
              <template slot-scope="scope">
                <el-switch v-model="scope.row.enabled" :active-value="true" :inactive-value="false" @change="handleRuleStatusChange(scope.row)" v-hasPermi="['yuepai:point:config']" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" align="center">
              <template slot-scope="scope">
                <el-button type="text" icon="el-icon-edit" @click="handleEditRule(scope.row)" v-hasPermi="['yuepai:point:config']">编辑</el-button>
                <el-button type="text" icon="el-icon-delete" @click="handleDeleteRule(scope.row)" v-hasPermi="['yuepai:point:config']" style="color: #f56c6c">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <!-- 用户积分查询 -->
      <el-tab-pane label="用户积分查询" name="users">
        <el-row :gutter="10" class="mb8">
          <el-col :span="1.5">
            <el-button type="warning" plain icon="el-icon-gift" @click="handleBatchGrant" v-hasPermi="['yuepai:point:grant']">批量发放</el-button>
          </el-col>
        </el-row>

        <el-table v-loading="loading" :data="userPointList" border @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55" align="center" />
          <el-table-column label="用户信息" width="200">
            <template slot-scope="scope">
              <div style="display: flex; align-items: center">
                <el-avatar :src="scope.row.avatar" :size="32" style="margin-right: 10px" />
                <div>
                  <div style="font-weight: bold">{{ scope.row.nickname }}</div>
                  <div style="font-size: 12px; color: #909399">ID: {{ scope.row.userId }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="当前积分" prop="currentPoints" width="120" align="center">
            <template slot-scope="scope">
              <span style="color: #e6a23c; font-weight: bold; font-size: 16px">{{ scope.row.currentPoints }}</span>
            </template>
          </el-table-column>
          <el-table-column label="累计获得" prop="totalEarned" width="120" align="center">
            <template slot-scope="scope">
              <span style="color: #67c23a">+{{ scope.row.totalEarned }}</span>
            </template>
          </el-table-column>
          <el-table-column label="累计消费" prop="totalSpent" width="120" align="center">
            <template slot-scope="scope">
              <span style="color: #f56c6c">-{{ scope.row.totalSpent }}</span>
            </template>
          </el-table-column>
          <el-table-column label="本月获得" prop="monthEarned" width="120" align="center" />
          <el-table-column label="最后变动" prop="lastChangeTime" width="160" align="center" />
          <el-table-column label="操作" width="250" align="center">
            <template slot-scope="scope">
              <el-button type="text" icon="el-icon-view" @click="handlePointDetail(scope.row)">明细</el-button>
              <el-button type="text" icon="el-icon-gift" @click="handleGrant(scope.row)" v-hasPermi="['yuepai:point:grant']" style="color: #e6a23c">发放</el-button>
              <el-button type="text" icon="el-icon-minus" @click="handleDeduct(scope.row)" v-hasPermi="['yuepai:point:deduct']" style="color: #f56c6c">扣减</el-button>
            </template>
          </el-table-column>
        </el-table>

        <pagination v-show="userPointTotal > 0" :total="userPointTotal" :page.sync="queryParams.pageNum" :limit.sync="queryParams.pageSize" @pagination="getUserPoints" />
      </el-tab-pane>
    </el-tabs>

    <!-- 积分规则编辑对话框 -->
    <el-dialog :title="ruleDialogTitle" :visible.sync="ruleDialogVisible" width="600px" append-to-body>
      <el-form :model="ruleForm" ref="ruleFormRef" :rules="ruleFormRules" label-width="120px">
        <el-form-item label="规则名称" prop="ruleName">
          <el-input v-model="ruleForm.ruleName" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="业务类型" prop="bizType">
          <el-select v-model="ruleForm.bizType" placeholder="请选择业务类型" style="width: 100%">
            <el-option label="每日签到" value="daily_checkin" />
            <el-option label="完成约拍" value="complete_appointment" />
            <el-option label="发布约拍" value="publish_appointment" />
            <el-option label="邀请注册" value="invite_register" />
            <el-option label="完善资料" value="complete_profile" />
            <el-option label="实名认证" value="real_name_certify" />
            <el-option label="发布作品" value="publish_work" />
            <el-option label="获得好评" value="receive_good_review" />
            <el-option label="系统奖励" value="system_reward" />
          </el-select>
        </el-form-item>
        <el-form-item label="积分数量" prop="points">
          <el-input-number v-model="ruleForm.points" :min="1" :max="99999" />
        </el-form-item>
        <el-form-item label="每日上限">
          <el-input-number v-model="ruleForm.dailyLimit" :min="0" :max="99999" />
          <span style="margin-left: 10px; color: #909399">0 表示无限制</span>
        </el-form-item>
        <el-form-item label="总上限">
          <el-input-number v-model="ruleForm.totalLimit" :min="0" :max="9999999" />
          <span style="margin-left: 10px; color: #909399">0 表示无限制</span>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="ruleForm.enabled" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="ruleForm.remark" type="textarea" placeholder="请输入备注" :rows="2" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="ruleDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitRule">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 积分发放对话框 -->
    <el-dialog title="积分发放" :visible.sync="grantDialogVisible" width="500px" append-to-body>
      <el-form :model="grantForm" ref="grantFormRef" :rules="grantFormRules" label-width="100px">
        <el-form-item label="发放对象">
          <span v-if="grantForm.userId">{{ grantForm.nickname }}（ID: {{ grantForm.userId }}）</span>
          <span v-else>批量发放（{{ selectedUsers.length }} 人）</span>
        </el-form-item>
        <el-form-item label="发放积分" prop="points">
          <el-input-number v-model="grantForm.points" :min="1" :max="99999" />
        </el-form-item>
        <el-form-item label="发放原因" prop="reason">
          <el-input v-model="grantForm.reason" type="textarea" placeholder="请输入发放原因" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="grantDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitGrant">确认发放</el-button>
      </div>
    </el-dialog>

    <!-- 积分扣减对话框 -->
    <el-dialog title="积分扣减" :visible.sync="deductDialogVisible" width="500px" append-to-body>
      <el-form :model="deductForm" ref="deductFormRef" :rules="deductFormRules" label-width="100px">
        <el-form-item label="扣减对象">
          <span>{{ deductForm.nickname }}（ID: {{ deductForm.userId }}，当前积分: {{ deductForm.currentPoints }}）</span>
        </el-form-item>
        <el-form-item label="扣减积分" prop="points">
          <el-input-number v-model="deductForm.points" :min="1" :max="deductForm.currentPoints" />
        </el-form-item>
        <el-form-item label="扣减原因" prop="reason">
          <el-input v-model="deductForm.reason" type="textarea" placeholder="请输入扣减原因" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="deductDialogVisible = false">取 消</el-button>
        <el-button type="danger" @click="submitDeduct">确认扣减</el-button>
      </div>
    </el-dialog>

    <!-- 积分明细对话框 -->
    <el-dialog title="积分明细" :visible.sync="detailDialogVisible" width="800px" append-to-body>
      <div class="point-summary">
        <div class="summary-item">
          <div class="label">当前积分</div>
          <div class="value" style="color: #e6a23c">{{ detailUser.currentPoints }}</div>
        </div>
        <div class="summary-item">
          <div class="label">累计获得</div>
          <div class="value" style="color: #67c23a">+{{ detailUser.totalEarned }}</div>
        </div>
        <div class="summary-item">
          <div class="label">累计消费</div>
          <div class="value" style="color: #f56c6c">-{{ detailUser.totalSpent }}</div>
        </div>
      </div>
      <el-table :data="pointDetailList" border>
        <el-table-column label="时间" prop="createTime" width="160" align="center" />
        <el-table-column label="类型" prop="type" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 'earn' ? 'success' : 'danger'">
              {{ scope.row.type === 'earn' ? '获得' : '消费' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="积分变动" width="120" align="center">
          <template slot-scope="scope">
            <span :style="{ color: scope.row.type === 'earn' ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
              {{ scope.row.type === 'earn' ? '+' : '-' }}{{ scope.row.points }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="变动后余额" prop="balanceAfter" width="120" align="center" />
        <el-table-column label="说明" prop="description" min-width="200" show-overflow-tooltip />
      </el-table>
      <pagination v-show="detailTotal > 0" :total="detailTotal" :page.sync="detailQuery.pageNum" :limit.sync="detailQuery.pageSize" @pagination="getPointDetail" />
    </el-dialog>
  </div>
</template>

<script>
import { getPointRules, addPointRule, updatePointRule, deletePointRule, getUserPoints, getPointDetail, grantPoints, deductPoints, batchGrantPoints } from '@/api/yuepai/yuepai-admin'
import Pagination from '@/components/Pagination'

export default {
  name: 'YuepaiPointManage',
  components: { Pagination },
  data() {
    return {
      activeTab: 'rules',
      showSearch: true,
      loading: false,
      queryParams: { pageNum: 1, pageSize: 20, nickname: undefined, pointMin: undefined, pointMax: undefined },
      ruleList: [],
      userPointList: [],
      userPointTotal: 0,
      selectedUsers: [],
      ruleDialogVisible: false,
      ruleDialogTitle: '新增积分规则',
      ruleForm: { ruleId: undefined, ruleName: '', bizType: '', points: 10, dailyLimit: 0, totalLimit: 0, enabled: true, remark: '' },
      ruleFormRules: {
        ruleName: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
        bizType: [{ required: true, message: '请选择业务类型', trigger: 'change' }],
        points: [{ required: true, message: '请输入积分数量', trigger: 'blur' }]
      },
      grantDialogVisible: false,
      grantForm: { userId: undefined, nickname: '', points: 100, reason: '' },
      grantFormRules: {
        points: [{ required: true, message: '请输入发放积分', trigger: 'blur' }],
        reason: [{ required: true, message: '请输入发放原因', trigger: 'blur' }]
      },
      deductDialogVisible: false,
      deductForm: { userId: undefined, nickname: '', currentPoints: 0, points: 10, reason: '' },
      deductFormRules: {
        points: [{ required: true, message: '请输入扣减积分', trigger: 'blur' }],
        reason: [{ required: true, message: '请输入扣减原因', trigger: 'blur' }]
      },
      detailDialogVisible: false,
      detailUser: {},
      pointDetailList: [],
      detailTotal: 0,
      detailQuery: { pageNum: 1, pageSize: 10, userId: undefined }
    }
  },
  created() {
    this.getRules()
  },
  methods: {
    handleTabChange(tab) {
      if (tab.name === 'users' && this.userPointList.length === 0) {
        this.getUserPoints()
      }
    },
    async getRules() {
      try {
        const res = await getPointRules()
        this.ruleList = res.data
      } catch (err) {
        this.$modal.msgError('获取积分规则失败：' + err.message)
      }
    },
    async getUserPoints() {
      this.loading = true
      try {
        const res = await getUserPoints(this.queryParams)
        this.userPointList = res.rows
        this.userPointTotal = res.total
      } catch (err) {
        this.$modal.msgError('获取用户积分失败：' + err.message)
      } finally {
        this.loading = false
      }
    },
    handleQuery() {
      this.queryParams.pageNum = 1
      this.getUserPoints()
    },
    resetQuery() {
      this.resetForm('queryForm')
      this.handleQuery()
    },
    handleSelectionChange(selection) {
      this.selectedUsers = selection
    },
    handleAddRule() {
      this.ruleDialogTitle = '新增积分规则'
      this.ruleForm = { ruleId: undefined, ruleName: '', bizType: '', points: 10, dailyLimit: 0, totalLimit: 0, enabled: true, remark: '' }
      this.ruleDialogVisible = true
    },
    handleEditRule(row) {
      this.ruleDialogTitle = '编辑积分规则'
      this.ruleForm = { ...row }
      this.ruleDialogVisible = true
    },
    submitRule() {
      this.$refs.ruleFormRef.validate(async valid => {
        if (!valid) return
        try {
          if (this.ruleForm.ruleId) {
            await updatePointRule(this.ruleForm.ruleId, this.ruleForm)
          } else {
            await addPointRule(this.ruleForm)
          }
          this.$modal.msgSuccess('保存成功')
          this.ruleDialogVisible = false
          this.getRules()
        } catch (err) {
          this.$modal.msgError('保存失败：' + err.message)
        }
      })
    },
    async handleDeleteRule(row) {
      try {
        await this.$confirm('确认删除该积分规则吗？', '警告', { type: 'warning' })
        await deletePointRule(row.ruleId)
        this.$modal.msgSuccess('删除成功')
        this.getRules()
      } catch (err) {
        if (err !== 'cancel') this.$modal.msgError('删除失败：' + err.message)
      }
    },
    async handleRuleStatusChange(row) {
      try {
        await updatePointRule(row.ruleId, { enabled: row.enabled })
        this.$modal.msgSuccess(row.enabled ? '已启用' : '已禁用')
      } catch (err) {
        row.enabled = !row.enabled
        this.$modal.msgError('操作失败：' + err.message)
      }
    },
    handleGrant(row) {
      this.grantForm = { userId: row.userId, nickname: row.nickname, points: 100, reason: '' }
      this.grantDialogVisible = true
    },
    handleBatchGrant() {
      if (this.selectedUsers.length === 0) return this.$modal.msgWarning('请先选择用户')
      this.grantForm = { userId: undefined, nickname: '', points: 100, reason: '' }
      this.grantDialogVisible = true
    },
    submitGrant() {
      this.$refs.grantFormRef.validate(async valid => {
        if (!valid) return
        try {
          if (this.grantForm.userId) {
            await grantPoints(this.grantForm.userId, this.grantForm)
          } else {
            const userIds = this.selectedUsers.map(u => u.userId)
            await batchGrantPoints(userIds, this.grantForm)
          }
          this.$modal.msgSuccess('发放成功')
          this.grantDialogVisible = false
          this.getUserPoints()
        } catch (err) {
          this.$modal.msgError('发放失败：' + err.message)
        }
      })
    },
    handleDeduct(row) {
      this.deductForm = { userId: row.userId, nickname: row.nickname, currentPoints: row.currentPoints, points: 10, reason: '' }
      this.deductDialogVisible = true
    },
    submitDeduct() {
      this.$refs.deductFormRef.validate(async valid => {
        if (!valid) return
        try {
          await deductPoints(this.deductForm.userId, this.deductForm)
          this.$modal.msgSuccess('扣减成功')
          this.deductDialogVisible = false
          this.getUserPoints()
        } catch (err) {
          this.$modal.msgError('扣减失败：' + err.message)
        }
      })
    },
    async handlePointDetail(row) {
      this.detailUser = row
      this.detailQuery = { pageNum: 1, pageSize: 10, userId: row.userId }
      await this.getPointDetail()
      this.detailDialogVisible = true
    },
    async getPointDetail() {
      try {
        const res = await getPointDetail(this.detailQuery)
        this.pointDetailList = res.rows
        this.detailTotal = res.total
      } catch (err) {
        this.$modal.msgError('获取积分明细失败：' + err.message)
      }
    },
    getBizTypeLabel(type) {
      const map = {
        daily_checkin: '每日签到',
        complete_appointment: '完成约拍',
        publish_appointment: '发布约拍',
        invite_register: '邀请注册',
        complete_profile: '完善资料',
        real_name_certify: '实名认证',
        publish_work: '发布作品',
        receive_good_review: '获得好评',
        system_reward: '系统奖励'
      }
      return map[type] || type
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.point-summary {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}
.summary-item {
  text-align: center;
}
.summary-item .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}
.summary-item .value {
  font-size: 24px;
  font-weight: bold;
}
</style>
