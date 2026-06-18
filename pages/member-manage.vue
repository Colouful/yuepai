<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
      <el-form-item label="用户昵称" prop="nickname">
        <el-input v-model="queryParams.nickname" placeholder="请输入用户昵称" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="会员等级" prop="level">
        <el-select v-model="queryParams.level" placeholder="请选择等级" clearable style="width: 200px">
          <el-option v-for="item in levelOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="会员状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 200px">
          <el-option label="有效" value="active" />
          <el-option label="已过期" value="expired" />
          <el-option label="已冻结" value="frozen" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- Tab 切换 -->
    <el-tabs v-model="activeTab">
      <!-- 会员列表 -->
      <el-tab-pane label="会员列表" name="list">
        <el-table v-loading="loading" :data="memberList" border>
          <el-table-column label="用户信息" width="200">
            <template slot-scope="scope">
              <div style="display: flex; align-items: center">
                <el-avatar :src="scope.row.avatar" :size="36" style="margin-right: 10px" />
                <div>
                  <div style="font-weight: bold">{{ scope.row.nickname }}</div>
                  <div style="font-size: 12px; color: #909399">ID: {{ scope.row.userId }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="会员等级" width="120" align="center">
            <template slot-scope="scope">
              <el-tag :type="getLevelTagType(scope.row.level)">
                <i class="el-icon-star-on" /> {{ getLevelLabel(scope.row.level) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="会员状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">{{ getStatusLabel(scope.row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="开通方式" prop="openMethod" width="100" align="center">
            <template slot-scope="scope">
              {{ scope.row.openMethod === 'pay' ? '付费开通' : '活动赠送' }}
            </template>
          </el-table-column>
          <el-table-column label="支付金额" width="100" align="center">
            <template slot-scope="scope">
              <span style="color: #f56c6c">¥{{ scope.row.payAmount || '0.00' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="开通时间" prop="openTime" width="160" align="center" />
          <el-table-column label="到期时间" prop="expireTime" width="160" align="center">
            <template slot-scope="scope">
              <span :style="{ color: isExpiringSoon(scope.row.expireTime) ? '#f56c6c' : '#303133' }">
                {{ scope.row.expireTime }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="剩余天数" width="100" align="center">
            <template slot-scope="scope">
              <span :style="{ color: scope.row.remainingDays <= 7 ? '#f56c6c' : '#67c23a', fontWeight: 'bold' }">
                {{ scope.row.remainingDays }}天
              </span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center" fixed="right">
            <template slot-scope="scope">
              <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.row)" v-hasPermi="['yuepai:member:edit']">编辑</el-button>
              <el-button type="text" icon="el-icon-refresh" @click="handleRenew(scope.row)" v-hasPermi="['yuepai:member:edit']" style="color: #e6a23c">续期</el-button>
              <el-button type="text" icon="el-icon-close" @click="handleFreeze(scope.row)" v-hasPermi="['yuepai:member:edit']" style="color: #f56c6c">
                {{ scope.row.status === 'frozen' ? '解冻' : '冻结' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <pagination v-show="total > 0" :total="total" :page.sync="queryParams.pageNum" :limit.sync="queryParams.pageSize" @pagination="getList" />
      </el-tab-pane>

      <!-- 等级配置 -->
      <el-tab-pane label="等级配置" name="level">
        <el-card shadow="hover">
          <div slot="header" class="card-header">
            <span>会员等级配置</span>
            <el-button type="primary" size="mini" icon="el-icon-plus" @click="handleAddLevel" v-hasPermi="['yuepai:member:level']">新增等级</el-button>
          </div>
          <el-table :data="levelList" border>
            <el-table-column label="等级" width="80" align="center">
              <template slot-scope="scope">
                <el-tag :type="getLevelTagType(scope.row.level)">
                  <i class="el-icon-star-on" /> {{ scope.row.level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="等级名称" prop="levelName" width="120" />
            <el-table-column label="月价格" width="100" align="center">
              <template slot-scope="scope">
                <span style="color: #f56c6c">¥{{ scope.row.monthPrice }}</span>
              </template>
            </el-table-column>
            <el-table-column label="年价格" width="100" align="center">
              <template slot-scope="scope">
                <span style="color: #f56c6c">¥{{ scope.row.yearPrice }}</span>
              </template>
            </el-table-column>
            <el-table-column label="权益数量" width="100" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.benefits ? scope.row.benefits.length : 0 }} 项</span>
              </template>
            </el-table-column>
            <el-table-column label="当前会员数" prop="memberCount" width="100" align="center" />
            <el-table-column label="排序" prop="sort" width="80" align="center" />
            <el-table-column label="状态" width="100" align="center">
              <template slot-scope="scope">
                <el-switch v-model="scope.row.enabled" :active-value="true" :inactive-value="false" @change="handleLevelStatusChange(scope.row)" v-hasPermi="['yuepai:member:level']" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" align="center">
              <template slot-scope="scope">
                <el-button type="text" icon="el-icon-edit" @click="handleEditLevel(scope.row)" v-hasPermi="['yuepai:member:level']">编辑</el-button>
                <el-button type="text" icon="el-icon-setting" @click="handleConfigBenefits(scope.row)" v-hasPermi="['yuepai:member:benefit']" style="color: #409eff">配置权益</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <!-- 权益配置 -->
      <el-tab-pane label="权益配置" name="benefit">
        <el-card shadow="hover">
          <div slot="header" class="card-header">
            <span>会员权益管理</span>
            <el-button type="primary" size="mini" icon="el-icon-plus" @click="handleAddBenefit" v-hasPermi="['yuepai:member:benefit']">新增权益</el-button>
          </div>
          <el-table :data="benefitList" border>
            <el-table-column label="权益ID" prop="benefitId" width="80" align="center" />
            <el-table-column label="权益图标" width="80" align="center">
              <template slot-scope="scope">
                <i :class="scope.row.icon" style="font-size: 24px; color: #409eff" />
              </template>
            </el-table-column>
            <el-table-column label="权益名称" prop="benefitName" width="150" />
            <el-table-column label="权益说明" prop="description" min-width="250" show-overflow-tooltip />
            <el-table-column label="权益类型" prop="benefitType" width="120" align="center">
              <template slot-scope="scope">
                <el-tag>{{ getBenefitTypeLabel(scope.row.benefitType) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="权益值" prop="benefitValue" width="120" align="center">
              <template slot-scope="scope">
                {{ scope.row.benefitValue === -1 ? '无限' : scope.row.benefitValue }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template slot-scope="scope">
                <el-button type="text" icon="el-icon-edit" @click="handleEditBenefit(scope.row)" v-hasPermi="['yuepai:member:benefit']">编辑</el-button>
                <el-button type="text" icon="el-icon-delete" @click="handleDeleteBenefit(scope.row)" v-hasPermi="['yuepai:member:benefit']" style="color: #f56c6c">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 等级编辑对话框 -->
    <el-dialog :title="levelDialogTitle" :visible.sync="levelDialogVisible" width="600px" append-to-body>
      <el-form :model="levelForm" ref="levelFormRef" :rules="levelFormRules" label-width="120px">
        <el-form-item label="等级" prop="level">
          <el-input-number v-model="levelForm.level" :min="1" :max="99" />
        </el-form-item>
        <el-form-item label="等级名称" prop="levelName">
          <el-input v-model="levelForm.levelName" placeholder="如：黄金会员" />
        </el-form-item>
        <el-form-item label="月价格" prop="monthPrice">
          <el-input-number v-model="levelForm.monthPrice" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="年价格" prop="yearPrice">
          <el-input-number v-model="levelForm.yearPrice" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="levelForm.sort" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="levelForm.enabled" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="levelDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitLevel">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 权益编辑对话框 -->
    <el-dialog :title="benefitDialogTitle" :visible.sync="benefitDialogVisible" width="600px" append-to-body>
      <el-form :model="benefitForm" ref="benefitFormRef" :rules="benefitFormRules" label-width="120px">
        <el-form-item label="权益名称" prop="benefitName">
          <el-input v-model="benefitForm.benefitName" placeholder="如：免费查看联系方式" />
        </el-form-item>
        <el-form-item label="权益图标" prop="icon">
          <el-input v-model="benefitForm.icon" placeholder="如：el-icon-phone" />
        </el-form-item>
        <el-form-item label="权益类型" prop="benefitType">
          <el-select v-model="benefitForm.benefitType" placeholder="请选择" style="width: 100%">
            <el-option label="功能解锁" value="feature" />
            <el-option label="次数限制" value="count" />
            <el-option label="折扣优惠" value="discount" />
            <el-option label="专属标识" value="badge" />
          </el-select>
        </el-form-item>
        <el-form-item label="权益值" prop="benefitValue">
          <el-input-number v-model="benefitForm.benefitValue" :min="-1" />
          <span style="margin-left: 10px; color: #909399">-1 表示无限</span>
        </el-form-item>
        <el-form-item label="权益说明" prop="description">
          <el-input v-model="benefitForm.description" type="textarea" placeholder="请输入权益说明" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="benefitDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitBenefit">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 会员编辑对话框 -->
    <el-dialog title="编辑会员" :visible.sync="editDialogVisible" width="500px" append-to-body>
      <el-form :model="editForm" ref="editFormRef" label-width="100px">
        <el-form-item label="用户">
          <span>{{ editForm.nickname }}</span>
        </el-form-item>
        <el-form-item label="会员等级">
          <el-select v-model="editForm.level" placeholder="请选择等级" style="width: 100%">
            <el-option v-for="item in levelOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="到期时间">
          <el-date-picker v-model="editForm.expireTime" type="datetime" placeholder="选择到期时间" value-format="yyyy-MM-dd HH:mm:ss" style="width: 100%" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitEdit">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 续期对话框 -->
    <el-dialog title="会员续期" :visible.sync="renewDialogVisible" width="400px" append-to-body>
      <el-form :model="renewForm" label-width="100px">
        <el-form-item label="用户">{{ renewForm.nickname }}</el-form-item>
        <el-form-item label="续期时长">
          <el-radio-group v-model="renewForm.duration">
            <el-radio :label="1">1个月</el-radio>
            <el-radio :label="3">3个月</el-radio>
            <el-radio :label="6">6个月</el-radio>
            <el-radio :label="12">12个月</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="renewDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitRenew">确认续期</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getMemberList, updateMember, freezeMember, renewMember, getLevelList, addLevel, updateLevel, updateLevelStatus, getBenefitList, addBenefit, updateBenefit, deleteBenefit } from '@/api/yuepai/yuepai-admin'
import Pagination from '@/components/Pagination'

export default {
  name: 'YuepaiMemberManage',
  components: { Pagination },
  data() {
    return {
      activeTab: 'list',
      showSearch: true,
      loading: false,
      queryParams: { pageNum: 1, pageSize: 20, nickname: undefined, level: undefined, status: undefined },
      memberList: [],
      total: 0,
      levelOptions: [
        { label: 'VIP1 黄金会员', value: 1 },
        { label: 'VIP2 铂金会员', value: 2 },
        { label: 'VIP3 钻石会员', value: 3 }
      ],
      levelList: [],
      benefitList: [],
      levelDialogVisible: false,
      levelDialogTitle: '新增等级',
      levelForm: { level: 1, levelName: '', monthPrice: 0, yearPrice: 0, sort: 0, enabled: true },
      levelFormRules: {
        level: [{ required: true, message: '请输入等级', trigger: 'blur' }],
        levelName: [{ required: true, message: '请输入等级名称', trigger: 'blur' }]
      },
      benefitDialogVisible: false,
      benefitDialogTitle: '新增权益',
      benefitForm: { benefitId: undefined, benefitName: '', icon: '', benefitType: 'feature', benefitValue: -1, description: '' },
      benefitFormRules: {
        benefitName: [{ required: true, message: '请输入权益名称', trigger: 'blur' }],
        benefitType: [{ required: true, message: '请选择权益类型', trigger: 'change' }]
      },
      editDialogVisible: false,
      editForm: { userId: undefined, nickname: '', level: 1, expireTime: '' },
      renewDialogVisible: false,
      renewForm: { userId: undefined, nickname: '', duration: 1 }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      this.loading = true
      try {
        const res = await getMemberList(this.queryParams)
        this.memberList = res.rows
        this.total = res.total
      } catch (err) {
        this.$modal.msgError('获取会员列表失败：' + err.message)
      } finally {
        this.loading = false
      }
    },
    handleQuery() {
      this.queryParams.pageNum = 1
      this.getList()
    },
    resetQuery() {
      this.resetForm('queryForm')
      this.handleQuery()
    },
    handleEdit(row) {
      this.editForm = { userId: row.userId, nickname: row.nickname, level: row.level, expireTime: row.expireTime }
      this.editDialogVisible = true
    },
    submitEdit() {
      this.$refs.editFormRef.validate(async valid => {
        if (!valid) return
        try {
          await updateMember(this.editForm.userId, this.editForm)
          this.$modal.msgSuccess('修改成功')
          this.editDialogVisible = false
          this.getList()
        } catch (err) {
          this.$modal.msgError('修改失败：' + err.message)
        }
      })
    },
    handleRenew(row) {
      this.renewForm = { userId: row.userId, nickname: row.nickname, duration: 1 }
      this.renewDialogVisible = true
    },
    async submitRenew() {
      try {
        await renewMember(this.renewForm.userId, { duration: this.renewForm.duration })
        this.$modal.msgSuccess('续期成功')
        this.renewDialogVisible = false
        this.getList()
      } catch (err) {
        this.$modal.msgError('续期失败：' + err.message)
      }
    },
    async handleFreeze(row) {
      const action = row.status === 'frozen' ? '解冻' : '冻结'
      try {
        await this.$confirm(`确认${action}该会员吗？`, '提示', { type: 'warning' })
        await freezeMember(row.userId, { frozen: row.status !== 'frozen' })
        this.$modal.msgSuccess(action + '成功')
        this.getList()
      } catch (err) {
        if (err !== 'cancel') this.$modal.msgError(action + '失败：' + err.message)
      }
    },
    async getLevels() {
      try {
        const res = await getLevelList()
        this.levelList = res.data
      } catch (err) {
        this.$modal.msgError('获取等级列表失败')
      }
    },
    handleAddLevel() {
      this.levelDialogTitle = '新增等级'
      this.levelForm = { level: 1, levelName: '', monthPrice: 0, yearPrice: 0, sort: 0, enabled: true }
      this.levelDialogVisible = true
    },
    handleEditLevel(row) {
      this.levelDialogTitle = '编辑等级'
      this.levelForm = { ...row }
      this.levelDialogVisible = true
    },
    submitLevel() {
      this.$refs.levelFormRef.validate(async valid => {
        if (!valid) return
        try {
          if (this.levelForm.levelId) {
            await updateLevel(this.levelForm.levelId, this.levelForm)
          } else {
            await addLevel(this.levelForm)
          }
          this.$modal.msgSuccess('保存成功')
          this.levelDialogVisible = false
          this.getLevels()
        } catch (err) {
          this.$modal.msgError('保存失败：' + err.message)
        }
      })
    },
    async handleLevelStatusChange(row) {
      try {
        await updateLevelStatus(row.levelId, { enabled: row.enabled })
        this.$modal.msgSuccess(row.enabled ? '已启用' : '已禁用')
      } catch (err) {
        row.enabled = !row.enabled
        this.$modal.msgError('操作失败')
      }
    },
    async getBenefits() {
      try {
        const res = await getBenefitList()
        this.benefitList = res.data
      } catch (err) {
        this.$modal.msgError('获取权益列表失败')
      }
    },
    handleAddBenefit() {
      this.benefitDialogTitle = '新增权益'
      this.benefitForm = { benefitId: undefined, benefitName: '', icon: '', benefitType: 'feature', benefitValue: -1, description: '' }
      this.benefitDialogVisible = true
    },
    handleEditBenefit(row) {
      this.benefitDialogTitle = '编辑权益'
      this.benefitForm = { ...row }
      this.benefitDialogVisible = true
    },
    submitBenefit() {
      this.$refs.benefitFormRef.validate(async valid => {
        if (!valid) return
        try {
          if (this.benefitForm.benefitId) {
            await updateBenefit(this.benefitForm.benefitId, this.benefitForm)
          } else {
            await addBenefit(this.benefitForm)
          }
          this.$modal.msgSuccess('保存成功')
          this.benefitDialogVisible = false
          this.getBenefits()
        } catch (err) {
          this.$modal.msgError('保存失败：' + err.message)
        }
      })
    },
    async handleDeleteBenefit(row) {
      try {
        await this.$confirm('确认删除该权益吗？', '警告', { type: 'warning' })
        await deleteBenefit(row.benefitId)
        this.$modal.msgSuccess('删除成功')
        this.getBenefits()
      } catch (err) {
        if (err !== 'cancel') this.$modal.msgError('删除失败')
      }
    },
    handleConfigBenefits(row) {
      this.$router.push({ path: '/yuepai/member/benefits', query: { levelId: row.levelId } })
    },
    getLevelLabel(level) {
      const map = { 1: 'VIP1 黄金', 2: 'VIP2 铂金', 3: 'VIP3 钻石' }
      return map[level] || 'VIP' + level
    },
    getLevelTagType(level) {
      const map = { 1: 'warning', 2: '', 3: 'danger' }
      return map[level] || 'info'
    },
    getStatusLabel(status) {
      const map = { active: '有效', expired: '已过期', frozen: '已冻结' }
      return map[status] || '未知'
    },
    getStatusTagType(status) {
      const map = { active: 'success', expired: 'info', frozen: 'danger' }
      return map[status] || 'info'
    },
    getBenefitTypeLabel(type) {
      const map = { feature: '功能解锁', count: '次数限制', discount: '折扣优惠', badge: '专属标识' }
      return map[type] || type
    },
    isExpiringSoon(expireTime) {
      if (!expireTime) return false
      const diff = new Date(expireTime) - new Date()
      return diff > 0 && diff < 7 * 24 * 60 * 60 * 1000
    }
  },
  watch: {
    activeTab(val) {
      if (val === 'level' && this.levelList.length === 0) this.getLevels()
      if (val === 'benefit' && this.benefitList.length === 0) this.getBenefits()
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
</style>
