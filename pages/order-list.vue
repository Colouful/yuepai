<template>
  <div class="app-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb8">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">今日订单数</div>
            <div class="stat-value">{{ stats.todayOrders }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">今日交易额</div>
            <div class="stat-value" style="color: #f56c6c">¥{{ stats.todayAmount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">今日佣金</div>
            <div class="stat-value" style="color: #e6a23c">¥{{ stats.todayCommission }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">待退款订单</div>
            <div class="stat-value" style="color: #909399">{{ stats.pendingRefunds }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索区域 -->
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
      <el-form-item label="订单编号" prop="orderNo">
        <el-input v-model="queryParams.orderNo" placeholder="请输入订单编号" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="发起人" prop="initiator">
        <el-input v-model="queryParams.initiator" placeholder="请输入发起人" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="接收人" prop="receiver">
        <el-input v-model="queryParams.receiver" placeholder="请输入接收人" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="订单状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择" clearable style="width: 200px">
          <el-option label="待支付" value="pending" />
          <el-option label="进行中" value="processing" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
          <el-option label="已退款" value="refunded" />
        </el-select>
      </el-form-item>
      <el-form-item label="支付状态" prop="payStatus">
        <el-select v-model="queryParams.payStatus" placeholder="请选择" clearable style="width: 200px">
          <el-option label="未支付" value="unpaid" />
          <el-option label="已支付" value="paid" />
          <el-option label="退款中" value="refunding" />
          <el-option label="已退款" value="refunded" />
        </el-select>
      </el-form-item>
      <el-form-item label="下单时间" prop="dateRange">
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
        <el-button type="warning" icon="el-icon-download" @click="handleExport" v-hasPermi="['yuepai:order:export']">导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" />
    </el-row>

    <!-- 订单列表 -->
    <el-table v-loading="loading" :data="orderList" border>
      <el-table-column label="订单编号" prop="orderNo" width="180" />
      <el-table-column label="发起人" width="120">
        <template slot-scope="scope">
          <div style="display: flex; align-items: center">
            <el-avatar :src="scope.row.initiatorAvatar" :size="24" style="margin-right: 6px" />
            <span>{{ scope.row.initiatorName }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="接收人" width="120">
        <template slot-scope="scope">
          <div style="display: flex; align-items: center">
            <el-avatar :src="scope.row.receiverAvatar" :size="24" style="margin-right: 6px" />
            <span>{{ scope.row.receiverName }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="订单类型" prop="orderType" width="100" align="center">
        <template slot-scope="scope">
          <el-tag>{{ getOrderTypeLabel(scope.row.orderType) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="订单金额" width="100" align="right">
        <template slot-scope="scope">
          <span style="color: #f56c6c; font-weight: bold">¥{{ scope.row.amount }}</span>
        </template>
      </el-table-column>
      <el-table-column label="佣金" width="90" align="right">
        <template slot-scope="scope">
          <span style="color: #e6a23c">¥{{ scope.row.commission }}</span>
        </template>
      </el-table-column>
      <el-table-column label="订单状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getStatusTagType(scope.row.status)">{{ getStatusLabel(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="支付状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getPayStatusTagType(scope.row.payStatus)">{{ getPayStatusLabel(scope.row.payStatus) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="下单时间" prop="createTime" width="160" align="center" />
      <el-table-column label="操作" width="200" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button type="text" icon="el-icon-view" @click="handleDetail(scope.row)" v-hasPermi="['yuepai:order:query']">详情</el-button>
          <el-button v-if="scope.row.payStatus === 'refunding'" type="text" icon="el-icon-check" @click="handleRefundReview(scope.row)" v-hasPermi="['yuepai:order:refund']" style="color: #e6a23c">退款审核</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" :page.sync="queryParams.pageNum" :limit.sync="queryParams.pageSize" @pagination="getList" />

    <!-- 订单详情对话框 -->
    <el-dialog title="订单详情" :visible.sync="detailDialogVisible" width="700px" append-to-body>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单编号">{{ detailForm.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="订单类型">{{ getOrderTypeLabel(detailForm.orderType) }}</el-descriptions-item>
        <el-descriptions-item label="发起人">{{ detailForm.initiatorName }}</el-descriptions-item>
        <el-descriptions-item label="接收人">{{ detailForm.receiverName }}</el-descriptions-item>
        <el-descriptions-item label="订单金额">¥{{ detailForm.amount }}</el-descriptions-item>
        <el-descriptions-item label="佣金">¥{{ detailForm.commission }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusTagType(detailForm.status)">{{ getStatusLabel(detailForm.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="支付状态">
          <el-tag :type="getPayStatusTagType(detailForm.payStatus)">{{ getPayStatusLabel(detailForm.payStatus) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ detailForm.createTime }}</el-descriptions-item>
        <el-descriptions-item label="支付时间">{{ detailForm.payTime || '-' }}</el-descriptions-item>
        <el-descriptions-item label="完成时间">{{ detailForm.completeTime || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailForm.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer">
        <el-button @click="detailDialogVisible = false">关 闭</el-button>
      </div>
    </el-dialog>

    <!-- 退款审核对话框 -->
    <el-dialog title="退款审核" :visible.sync="refundDialogVisible" width="500px" append-to-body>
      <el-form :model="refundForm" ref="refundFormRef" :rules="refundFormRules" label-width="100px">
        <el-form-item label="订单编号">
          <span>{{ refundForm.orderNo }}</span>
        </el-form-item>
        <el-form-item label="退款金额">
          <span style="color: #f56c6c; font-weight: bold">¥{{ refundForm.refundAmount }}</span>
        </el-form-item>
        <el-form-item label="退款原因">
          <span>{{ refundForm.refundReason || '-' }}</span>
        </el-form-item>
        <el-form-item label="审核结果" prop="result">
          <el-radio-group v-model="refundForm.result">
            <el-radio label="approved">同意退款</el-radio>
            <el-radio label="rejected">拒绝退款</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="审核备注" prop="remark" v-if="refundForm.result === 'rejected'">
          <el-input v-model="refundForm.remark" type="textarea" placeholder="请输入拒绝原因" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="refundDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitRefundReview">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getOrderList, getOrderDetail, reviewRefund, getOrderStats, exportOrder } from '@/api/yuepai/yuepai-admin'
import Pagination from '@/components/Pagination'
import RightToolbar from '@/components/RightToolbar'

export default {
  name: 'YuepaiOrderList',
  components: { Pagination, RightToolbar },
  data() {
    return {
      showSearch: true,
      loading: false,
      stats: {
        todayOrders: 0,
        todayAmount: '0.00',
        todayCommission: '0.00',
        pendingRefunds: 0
      },
      queryParams: {
        pageNum: 1,
        pageSize: 20,
        orderNo: undefined,
        initiator: undefined,
        receiver: undefined,
        status: undefined,
        payStatus: undefined,
        dateRange: []
      },
      orderList: [],
      total: 0,
      detailDialogVisible: false,
      detailForm: {},
      refundDialogVisible: false,
      refundForm: {
        orderId: undefined,
        orderNo: '',
        refundAmount: '',
        refundReason: '',
        result: 'approved',
        remark: ''
      },
      refundFormRules: {
        result: [{ required: true, message: '请选择审核结果', trigger: 'change' }]
      }
    }
  },
  created() {
    this.getList()
    this.getStats()
  },
  methods: {
    async getStats() {
      try {
        const res = await getOrderStats()
        this.stats = res.data
      } catch (err) {
        console.error('获取统计失败', err)
      }
    },
    async getList() {
      this.loading = true
      try {
        const params = { ...this.queryParams }
        if (params.dateRange && params.dateRange.length === 2) {
          params.beginTime = params.dateRange[0]
          params.endTime = params.dateRange[1]
        }
        delete params.dateRange
        const res = await getOrderList(params)
        this.orderList = res.rows
        this.total = res.total
      } catch (err) {
        this.$modal.msgError('获取订单列表失败：' + err.message)
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
        const res = await getOrderDetail(row.orderId)
        this.detailForm = res.data
        this.detailDialogVisible = true
      } catch (err) {
        this.$modal.msgError('获取详情失败')
      }
    },
    handleRefundReview(row) {
      this.refundForm = {
        orderId: row.orderId,
        orderNo: row.orderNo,
        refundAmount: row.amount,
        refundReason: row.refundReason || '',
        result: 'approved',
        remark: ''
      }
      this.refundDialogVisible = true
    },
    submitRefundReview() {
      this.$refs.refundFormRef.validate(async valid => {
        if (!valid) return
        try {
          await reviewRefund({
            orderId: this.refundForm.orderId,
            result: this.refundForm.result,
            remark: this.refundForm.remark
          })
          this.$modal.msgSuccess('审核完成')
          this.refundDialogVisible = false
          this.getList()
          this.getStats()
        } catch (err) {
          this.$modal.msgError('审核失败：' + err.message)
        }
      })
    },
    async handleExport() {
      try {
        const res = await exportOrder(this.queryParams)
        const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = '订单数据.xlsx'
        link.click()
        URL.revokeObjectURL(link.href)
      } catch (err) {
        this.$modal.msgError('导出失败')
      }
    },
    getOrderTypeLabel(type) {
      const map = { photo: '摄影约拍', makeup: '化妆服务', video: '视频拍摄' }
      return map[type] || type
    },
    getStatusLabel(status) {
      const map = { pending: '待支付', processing: '进行中', completed: '已完成', cancelled: '已取消', refunded: '已退款' }
      return map[status] || status
    },
    getStatusTagType(status) {
      const map = { pending: 'warning', processing: '', completed: 'success', cancelled: 'info', refunded: 'danger' }
      return map[status] || 'info'
    },
    getPayStatusLabel(status) {
      const map = { unpaid: '未支付', paid: '已支付', refunding: '退款中', refunded: '已退款' }
      return map[status] || status
    },
    getPayStatusTagType(status) {
      const map = { unpaid: 'warning', paid: 'success', refunding: '', refunded: 'danger' }
      return map[status] || 'info'
    }
  }
}
</script>

<style scoped>
.stat-card {
  text-align: center;
  padding: 10px 0;
}
.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}
.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}
</style>
