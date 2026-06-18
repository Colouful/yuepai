<template>
  <div class="app-container">
    <!-- 日期范围选择 -->
    <el-form :inline="true" class="mb8">
      <el-form-item label="日期范围">
        <el-date-picker v-model="dateRange" type="daterange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd" style="width: 280px" @change="handleDateChange" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="fetchData">查询</el-button>
        <el-button icon="el-icon-download" @click="handleExport" v-hasPermi="['yuepai:finance:export']">导出</el-button>
      </el-form-item>
    </el-form>

    <!-- 指标卡片 -->
    <el-row :gutter="20" class="mb8">
      <el-col :span="6" v-for="item in metricCards" :key="item.label">
        <el-card shadow="hover">
          <div class="metric-card">
            <div class="metric-label">{{ item.label }}</div>
            <div class="metric-value" :style="{ color: item.color }">{{ item.prefix }}{{ item.value }}</div>
            <div class="metric-trend" :style="{ color: item.trend >= 0 ? '#67c23a' : '#f56c6c' }">
              <i :class="item.trend >= 0 ? 'el-icon-top' : 'el-icon-bottom'" />
              {{ Math.abs(item.trend) }}% 较昨日
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="mb8">
      <el-col :span="16">
        <el-card shadow="hover">
          <div slot="header"><span>收入趋势</span></div>
          <div ref="trendChart" style="width: 100%; height: 400px"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div slot="header"><span>收入构成</span></div>
          <div ref="pieChart" style="width: 100%; height: 400px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 提现审批 -->
    <el-card shadow="hover" class="mb8">
      <div slot="header">
        <span>待审批提现</span>
      </div>
      <el-table v-loading="withdrawLoading" :data="withdrawList" border>
        <el-table-column label="用户" width="150">
          <template slot-scope="scope">
            <div style="display: flex; align-items: center">
              <el-avatar :src="scope.row.userAvatar" :size="24" style="margin-right: 6px" />
              <span>{{ scope.row.userName }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="提现金额" width="120" align="right">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: bold">¥{{ scope.row.amount }}</span>
          </template>
        </el-table-column>
        <el-table-column label="提现方式" prop="withdrawMethod" width="100" align="center" />
        <el-table-column label="收款账号" prop="accountNo" width="180" />
        <el-table-column label="申请时间" prop="createTime" width="160" align="center" />
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'pending' ? 'warning' : scope.row.status === 'approved' ? 'success' : 'danger'">
              {{ { pending: '待审批', approved: '已通过', rejected: '已拒绝' }[scope.row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <template v-if="scope.row.status === 'pending'">
              <el-button type="text" icon="el-icon-check" @click="handleApproveWithdraw(scope.row)" v-hasPermi="['yuepai:finance:withdraw']" style="color: #67c23a">通过</el-button>
              <el-button type="text" icon="el-icon-close" @click="handleRejectWithdraw(scope.row)" v-hasPermi="['yuepai:finance:withdraw']" style="color: #f56c6c">拒绝</el-button>
            </template>
            <span v-else style="color: #909399">已处理</span>
          </template>
        </el-table-column>
      </el-table>
      <pagination v-show="withdrawTotal > 0" :total="withdrawTotal" :page.sync="withdrawQuery.pageNum" :limit.sync="withdrawQuery.pageSize" @pagination="getWithdrawList" />
    </el-card>

    <!-- 交易记录 -->
    <el-card shadow="hover">
      <div slot="header"><span>交易记录</span></div>
      <el-table v-loading="transactionLoading" :data="transactionList" border>
        <el-table-column label="交易编号" prop="transactionNo" width="180" />
        <el-table-column label="交易类型" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 'income' ? 'success' : 'danger'">{{ scope.row.type === 'income' ? '收入' : '支出' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="交易金额" width="120" align="right">
          <template slot-scope="scope">
            <span :style="{ color: scope.row.type === 'income' ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
              {{ scope.row.type === 'income' ? '+' : '-' }}¥{{ scope.row.amount }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="交易描述" prop="description" min-width="200" show-overflow-tooltip />
        <el-table-column label="关联用户" prop="userName" width="120" align="center" />
        <el-table-column label="交易时间" prop="createTime" width="160" align="center" />
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : scope.row.status === 'pending' ? 'warning' : 'danger'">
              {{ { success: '成功', pending: '处理中', failed: '失败' }[scope.row.status] }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <pagination v-show="transactionTotal > 0" :total="transactionTotal" :page.sync="transactionQuery.pageNum" :limit.sync="transactionQuery.pageSize" @pagination="getTransactionList" />
    </el-card>

    <!-- 拒绝对话框 -->
    <el-dialog title="拒绝提现" :visible.sync="rejectDialogVisible" width="500px" append-to-body>
      <el-form :model="rejectForm" ref="rejectFormRef" :rules="rejectFormRules" label-width="100px">
        <el-form-item label="用户">
          <span>{{ rejectForm.userName }}</span>
        </el-form-item>
        <el-form-item label="提现金额">
          <span style="color: #f56c6c; font-weight: bold">¥{{ rejectForm.amount }}</span>
        </el-form-item>
        <el-form-item label="拒绝原因" prop="reason">
          <el-input v-model="rejectForm.reason" type="textarea" placeholder="请输入拒绝原因" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="rejectDialogVisible = false">取 消</el-button>
        <el-button type="danger" @click="submitRejectWithdraw">确认拒绝</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getFinanceMetrics, getTrendData, getPieData, getWithdrawList, approveWithdraw, rejectWithdraw, getTransactions, exportFinance } from '@/api/yuepai/yuepai-admin'
import Pagination from '@/components/Pagination'

export default {
  name: 'YuepaiFinanceDashboard',
  components: { Pagination },
  data() {
    return {
      dateRange: [],
      metricCards: [
        { label: '总交易额', value: '0.00', prefix: '¥', color: '#303133', trend: 0 },
        { label: '今日收入', value: '0.00', prefix: '¥', color: '#67c23a', trend: 0 },
        { label: '今日佣金', value: '0.00', prefix: '¥', color: '#e6a23c', trend: 0 },
        { label: '待提现金额', value: '0.00', prefix: '¥', color: '#f56c6c', trend: 0 }
      ],
      trendChart: null,
      pieChart: null,
      withdrawLoading: false,
      withdrawList: [],
      withdrawTotal: 0,
      withdrawQuery: { pageNum: 1, pageSize: 10 },
      transactionLoading: false,
      transactionList: [],
      transactionTotal: 0,
      transactionQuery: { pageNum: 1, pageSize: 20 },
      rejectDialogVisible: false,
      rejectForm: {
        withdrawId: undefined,
        userName: '',
        amount: '',
        reason: ''
      },
      rejectFormRules: {
        reason: [{ required: true, message: '请输入拒绝原因', trigger: 'blur' }]
      }
    }
  },
  mounted() {
    this.fetchData()
    this.getWithdrawList()
    this.getTransactionList()
  },
  beforeDestroy() {
    if (this.trendChart) this.trendChart.dispose()
    if (this.pieChart) this.pieChart.dispose()
  },
  methods: {
    handleDateChange() {
      this.fetchData()
    },
    async fetchData() {
      const params = {}
      if (this.dateRange && this.dateRange.length === 2) {
        params.beginTime = this.dateRange[0]
        params.endTime = this.dateRange[1]
      }
      await Promise.all([
        this.getMetrics(params),
        this.getTrendChart(params),
        this.getPieChart(params)
      ])
    },
    async getMetrics(params) {
      try {
        const res = await getFinanceMetrics(params)
        const data = res.data
        this.metricCards = [
          { label: '总交易额', value: data.totalAmount || '0.00', prefix: '¥', color: '#303133', trend: data.totalAmountTrend || 0 },
          { label: '今日收入', value: data.todayIncome || '0.00', prefix: '¥', color: '#67c23a', trend: data.todayIncomeTrend || 0 },
          { label: '今日佣金', value: data.todayCommission || '0.00', prefix: '¥', color: '#e6a23c', trend: data.todayCommissionTrend || 0 },
          { label: '待提现金额', value: data.pendingWithdraw || '0.00', prefix: '¥', color: '#f56c6c', trend: data.pendingWithdrawTrend || 0 }
        ]
      } catch (err) {
        console.error('获取指标失败', err)
      }
    },
    async getTrendChart(params) {
      try {
        const res = await getTrendData(params)
        const data = res.data
        if (!this.trendChart) {
          this.trendChart = echarts.init(this.$refs.trendChart)
        }
        this.trendChart.setOption({
          tooltip: { trigger: 'axis' },
          legend: { data: ['收入', '佣金', '提现'] },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: { type: 'category', boundaryGap: false, data: data.dates || [] },
          yAxis: { type: 'value', name: '金额(元)' },
          series: [
            { name: '收入', type: 'line', smooth: true, data: data.income || [], itemStyle: { color: '#67c23a' } },
            { name: '佣金', type: 'line', smooth: true, data: data.commission || [], itemStyle: { color: '#e6a23c' } },
            { name: '提现', type: 'line', smooth: true, data: data.withdraw || [], itemStyle: { color: '#f56c6c' } }
          ]
        })
      } catch (err) {
        console.error('获取趋势数据失败', err)
      }
    },
    async getPieChart(params) {
      try {
        const res = await getPieData(params)
        const data = res.data
        if (!this.pieChart) {
          this.pieChart = echarts.init(this.$refs.pieChart)
        }
        this.pieChart.setOption({
          tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
          legend: { orient: 'vertical', left: 'left', data: (data.items || []).map(i => i.name) },
          series: [{
            name: '收入构成',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: { show: true, formatter: '{b}: {d}%' },
            data: data.items || []
          }]
        })
      } catch (err) {
        console.error('获取饼图数据失败', err)
      }
    },
    async getWithdrawList() {
      this.withdrawLoading = true
      try {
        const res = await getWithdrawList(this.withdrawQuery)
        this.withdrawList = res.rows
        this.withdrawTotal = res.total
      } catch (err) {
        this.$modal.msgError('获取提现列表失败')
      } finally {
        this.withdrawLoading = false
      }
    },
    async handleApproveWithdraw(row) {
      try {
        await this.$confirm(`确认通过用户 ${row.userName} 的提现申请（¥${row.amount}）？`, '提示', { type: 'success' })
        await approveWithdraw(row.withdrawId)
        this.$modal.msgSuccess('审批通过')
        this.getWithdrawList()
        this.fetchData()
      } catch (err) {
        if (err !== 'cancel') this.$modal.msgError('操作失败')
      }
    },
    handleRejectWithdraw(row) {
      this.rejectForm = {
        withdrawId: row.withdrawId,
        userName: row.userName,
        amount: row.amount,
        reason: ''
      }
      this.rejectDialogVisible = true
    },
    submitRejectWithdraw() {
      this.$refs.rejectFormRef.validate(async valid => {
        if (!valid) return
        try {
          await rejectWithdraw(this.rejectForm.withdrawId, { reason: this.rejectForm.reason })
          this.$modal.msgSuccess('已拒绝')
          this.rejectDialogVisible = false
          this.getWithdrawList()
        } catch (err) {
          this.$modal.msgError('操作失败')
        }
      })
    },
    async getTransactionList() {
      this.transactionLoading = true
      try {
        const params = { ...this.transactionQuery }
        if (this.dateRange && this.dateRange.length === 2) {
          params.beginTime = this.dateRange[0]
          params.endTime = this.dateRange[1]
        }
        const res = await getTransactions(params)
        this.transactionList = res.rows
        this.transactionTotal = res.total
      } catch (err) {
        this.$modal.msgError('获取交易记录失败')
      } finally {
        this.transactionLoading = false
      }
    },
    async handleExport() {
      try {
        const params = {}
        if (this.dateRange && this.dateRange.length === 2) {
          params.beginTime = this.dateRange[0]
          params.endTime = this.dateRange[1]
        }
        const res = await exportFinance(params)
        const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = '财务数据.xlsx'
        link.click()
        URL.revokeObjectURL(link.href)
      } catch (err) {
        this.$modal.msgError('导出失败')
      }
    }
  }
}
</script>

<style scoped>
.metric-card {
  text-align: center;
  padding: 10px 0;
}
.metric-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}
.metric-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 6px;
}
.metric-trend {
  font-size: 12px;
}
</style>
