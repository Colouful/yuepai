<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
      <el-form-item label="用户昵称" prop="nickname">
        <el-input v-model="queryParams.nickname" placeholder="请输入用户昵称" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="queryParams.phone" placeholder="请输入手机号" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="用户状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 200px">
          <el-option label="正常" value="0" />
          <el-option label="禁用" value="1" />
        </el-select>
      </el-form-item>
      <el-form-item label="认证状态" prop="certifyStatus">
        <el-select v-model="queryParams.certifyStatus" placeholder="请选择" clearable style="width: 200px">
          <el-option label="未认证" value="0" />
          <el-option label="认证中" value="1" />
          <el-option label="已认证" value="2" />
          <el-option label="认证失败" value="3" />
        </el-select>
      </el-form-item>
      <el-form-item label="用户角色" prop="role">
        <el-select v-model="queryParams.role" placeholder="请选择角色" clearable style="width: 200px">
          <el-option label="摄影师" value="photographer" />
          <el-option label="模特" value="model" />
          <el-option label="化妆师" value="makeup" />
          <el-option label="普通用户" value="user" />
        </el-select>
      </el-form-item>
      <el-form-item label="注册时间" prop="dateRange">
        <el-date-picker v-model="queryParams.dateRange" type="daterange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd" style="width: 240px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作栏 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="warning" icon="el-icon-download" @click="handleExport" v-hasPermi="['yuepai:user:export']">导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" />
    </el-row>

    <!-- 用户列表 -->
    <el-table v-loading="loading" :data="userList" border>
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
      <el-table-column label="手机号" prop="phone" width="120" align="center" />
      <el-table-column label="角色" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getRoleTagType(scope.row.role)">{{ getRoleLabel(scope.row.role) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="认证状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getCertifyTagType(scope.row.certifyStatus)">{{ getCertifyLabel(scope.row.certifyStatus) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="积分" prop="points" width="80" align="center" />
      <el-table-column label="会员等级" width="120" align="center">
        <template slot-scope="scope">
          <el-tag :type="getLevelTagType(scope.row.memberLevel)" v-if="scope.row.memberLevel">
            <i class="el-icon-star-on" /> {{ getLevelLabel(scope.row.memberLevel) }}
          </el-tag>
          <span v-else style="color: #909399">普通用户</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.status" active-value="0" inactive-value="1" @change="handleStatusChange(scope.row)" v-hasPermi="['yuepai:user:edit']" />
        </template>
      </el-table-column>
      <el-table-column label="注册时间" prop="createTime" width="160" align="center" />
      <el-table-column label="操作" width="240" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button type="text" icon="el-icon-view" @click="handleDetail(scope.row)" v-hasPermi="['yuepai:user:query']">详情</el-button>
          <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.row)" v-hasPermi="['yuepai:user:edit']">编辑</el-button>
          <el-button v-if="scope.row.certifyStatus === '1'" type="text" icon="el-icon-check" @click="handleCertifyReview(scope.row)" v-hasPermi="['yuepai:user:certify']" style="color: #e6a23c">认证审核</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" :page.sync="queryParams.pageNum" :limit.sync="queryParams.pageSize" @pagination="getList" />

    <!-- 用户详情对话框 -->
    <el-dialog title="用户详情" :visible.sync="detailDialogVisible" width="700px" append-to-body>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户ID">{{ detailForm.userId }}</el-descriptions-item>
        <el-descriptions-item label="昵称">{{ detailForm.nickname }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ detailForm.phone }}</el-descriptions-item>
        <el-descriptions-item label="角色">
          <el-tag :type="getRoleTagType(detailForm.role)">{{ getRoleLabel(detailForm.role) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="积分">{{ detailForm.points }}</el-descriptions-item>
        <el-descriptions-item label="会员等级">{{ getLevelLabel(detailForm.memberLevel) || '普通用户' }}</el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ detailForm.createTime }}</el-descriptions-item>
        <el-descriptions-item label="最近登录">{{ detailForm.lastLoginTime }}</el-descriptions-item>
      </el-descriptions>
      <el-divider content-position="left">认证信息</el-divider>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="认证状态">
          <el-tag :type="getCertifyTagType(detailForm.certifyStatus)">{{ getCertifyLabel(detailForm.certifyStatus) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{ detailForm.realName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ detailForm.idCard || '-' }}</el-descriptions-item>
        <el-descriptions-item label="认证照片">
          <el-image v-if="detailForm.certifyPhoto" :src="detailForm.certifyPhoto" style="width: 100px; height: 100px" fit="cover" :preview-src-list="[detailForm.certifyPhoto]" />
          <span v-else>-</span>
        </el-descriptions-item>
      </el-descriptions>
      <div slot="footer">
        <el-button @click="detailDialogVisible = false">关 闭</el-button>
      </div>
    </el-dialog>

    <!-- 认证审核对话框 -->
    <el-dialog title="认证审核" :visible.sync="certifyDialogVisible" width="500px" append-to-body>
      <el-form :model="certifyForm" ref="certifyFormRef" :rules="certifyFormRules" label-width="100px">
        <el-form-item label="用户">
          <span>{{ certifyForm.nickname }}</span>
        </el-form-item>
        <el-form-item label="真实姓名">{{ certifyForm.realName }}</el-form-item>
        <el-form-item label="身份证号">{{ certifyForm.idCard }}</el-form-item>
        <el-form-item label="认证照片">
          <el-image v-if="certifyForm.certifyPhoto" :src="certifyForm.certifyPhoto" style="width: 150px; height: 150px" fit="cover" :preview-src-list="[certifyForm.certifyPhoto]" />
        </el-form-item>
        <el-form-item label="审核结果" prop="result">
          <el-radio-group v-model="certifyForm.result">
            <el-radio label="2">通过</el-radio>
            <el-radio label="3">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="拒绝原因" prop="reason" v-if="certifyForm.result === '3'">
          <el-input v-model="certifyForm.reason" type="textarea" placeholder="请输入拒绝原因" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="certifyDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitCertifyReview">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getUserList, getUserDetail, updateUserStatus, reviewCertification, exportUser } from '@/api/yuepai/yuepai-admin'
import Pagination from '@/components/Pagination'
import RightToolbar from '@/components/RightToolbar'

export default {
  name: 'YuepaiUserList',
  components: { Pagination, RightToolbar },
  data() {
    return {
      showSearch: true,
      loading: false,
      queryParams: {
        pageNum: 1,
        pageSize: 20,
        nickname: undefined,
        phone: undefined,
        status: undefined,
        certifyStatus: undefined,
        role: undefined,
        dateRange: []
      },
      userList: [],
      total: 0,
      detailDialogVisible: false,
      detailForm: {},
      certifyDialogVisible: false,
      certifyForm: {
        userId: undefined,
        nickname: '',
        realName: '',
        idCard: '',
        certifyPhoto: '',
        result: '2',
        reason: ''
      },
      certifyFormRules: {
        result: [{ required: true, message: '请选择审核结果', trigger: 'change' }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      this.loading = true
      try {
        const params = { ...this.queryParams }
        if (params.dateRange && params.dateRange.length === 2) {
          params.beginTime = params.dateRange[0]
          params.endTime = params.dateRange[1]
        }
        delete params.dateRange
        const res = await getUserList(params)
        this.userList = res.rows
        this.total = res.total
      } catch (err) {
        this.$modal.msgError('获取用户列表失败：' + err.message)
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
    async handleDetail(row) {
      try {
        const res = await getUserDetail(row.userId)
        this.detailForm = res.data
        this.detailDialogVisible = true
      } catch (err) {
        this.$modal.msgError('获取详情失败')
      }
    },
    handleEdit(row) {
      this.$router.push({ path: '/yuepai/user/edit/' + row.userId })
    },
    async handleStatusChange(row) {
      try {
        await updateUserStatus(row.userId, row.status)
        this.$modal.msgSuccess('状态修改成功')
      } catch (err) {
        row.status = row.status === '0' ? '1' : '0'
        this.$modal.msgError('操作失败：' + err.message)
      }
    },
    async handleCertifyReview(row) {
      this.certifyForm = {
        userId: row.userId,
        nickname: row.nickname,
        realName: row.realName || '',
        idCard: row.idCard || '',
        certifyPhoto: row.certifyPhoto || '',
        result: '2',
        reason: ''
      }
      this.certifyDialogVisible = true
    },
    submitCertifyReview() {
      this.$refs.certifyFormRef.validate(async valid => {
        if (!valid) return
        try {
          await reviewCertification({
            userId: this.certifyForm.userId,
            result: this.certifyForm.result,
            reason: this.certifyForm.reason
          })
          this.$modal.msgSuccess('审核完成')
          this.certifyDialogVisible = false
          this.getList()
        } catch (err) {
          this.$modal.msgError('审核失败：' + err.message)
        }
      })
    },
    async handleExport() {
      try {
        const res = await exportUser(this.queryParams)
        const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = '用户数据.xlsx'
        link.click()
        URL.revokeObjectURL(link.href)
      } catch (err) {
        this.$modal.msgError('导出失败')
      }
    },
    getRoleLabel(role) {
      const map = { photographer: '摄影师', model: '模特', makeup: '化妆师', user: '普通用户' }
      return map[role] || role
    },
    getRoleTagType(role) {
      const map = { photographer: 'danger', model: '', makeup: 'warning', user: 'info' }
      return map[role] || 'info'
    },
    getCertifyLabel(status) {
      const map = { '0': '未认证', '1': '认证中', '2': '已认证', '3': '认证失败' }
      return map[status] || '未知'
    },
    getCertifyTagType(status) {
      const map = { '0': 'info', '1': 'warning', '2': 'success', '3': 'danger' }
      return map[status] || 'info'
    },
    getLevelLabel(level) {
      const map = { 1: 'VIP1 黄金', 2: 'VIP2 铂金', 3: 'VIP3 钻石' }
      return map[level] || ''
    },
    getLevelTagType(level) {
      const map = { 1: 'warning', 2: '', 3: 'danger' }
      return map[level] || 'info'
    }
  }
}
</script>
