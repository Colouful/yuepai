<template>
  <div class="app-container">
    <!-- 日期范围选择 -->
    <el-form :inline="true" class="mb8">
      <el-form-item label="日期范围">
        <el-date-picker v-model="dateRange" type="daterange" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd" style="width: 280px" @change="handleDateChange" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="fetchData">查询</el-button>
        <el-button icon="el-icon-download" @click="handleExport" v-hasPermi="['yuepai:stats:export']">导出</el-button>
      </el-form-item>
    </el-form>

    <!-- 核心指标 -->
    <el-row :gutter="16" class="mb8">
      <el-col :span="4" v-for="item in coreMetrics" :key="item.label">
        <el-card shadow="hover">
          <div class="core-metric">
            <div class="core-label">{{ item.label }}</div>
            <div class="core-value" :style="{ color: item.color }">{{ item.value }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="mb8">
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header"><span>DAU趋势</span></div>
          <div ref="dauChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header"><span>新增用户趋势</span></div>
          <div ref="newUserChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="mb8">
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header"><span>约拍数趋势</span></div>
          <div ref="appointmentChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header"><span>GMV趋势</span></div>
          <div ref="gmvChart" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 留存率表格 -->
    <el-card shadow="hover" class="mb8">
      <div slot="header"><span>留存率分析</span></div>
      <el-table v-loading="retentionLoading" :data="retentionData" border>
        <el-table-column label="日期" prop="date" width="120" align="center" />
        <el-table-column label="新增用户" prop="newUsers" width="100" align="center" />
        <el-table-column :label="'第' + col + '天'" v-for="col in retentionColumns" :key="col" width="90" align="center">
          <template slot-scope="scope">
            <span :style="{ backgroundColor: getHeatColor(scope.row['day' + col]), color: '#fff', padding: '2px 8px', borderRadius: '4px', fontSize: '12px' }">
              {{ scope.row['day' + col] !== undefined && scope.row['day' + col] !== null ? scope.row['day' + col] + '%' : '-' }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 漏斗分析 -->
    <el-card shadow="hover">
      <div slot="header"><span>转化漏斗分析</span></div>
      <el-row :gutter="20">
        <el-col :span="12">
          <div ref="funnelChart" style="width: 100%; height: 400px"></div>
        </el-col>
        <el-col :span="12">
          <el-table :data="funnelTableData" border>
            <el-table-column label="环节" prop="name" width="150" />
            <el-table-column label="人数" prop="value" width="100" align="center" />
            <el-table-column label="转化率" width="100" align="center">
              <template slot-scope="scope">
                <span style="color: #409eff; font-weight: bold">{{ scope.row.rate }}%</span>
              </template>
            </el-table-column>
            <el-table-column label="流失率" width="100" align="center">
              <template slot-scope="scope">
                <span style="color: #f56c6c">{{ scope.row.dropRate }}%</span>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getCoreMetrics, getDauTrend, getNewUserTrend, getAppointmentTrend, getGmvTrend, getRetentionData, getFunnelData, exportStats } from '@/api/yuepai/yuepai-admin'

export default {
  name: 'YuepaiStatsDashboard',
  data() {
    return {
      dateRange: [],
      coreMetrics: [
        { label: 'DAU', value: '0', color: '#409eff' },
        { label: '新增用户', value: '0', color: '#67c23a' },
        { label: '约拍数', value: '0', color: '#e6a23c' },
        { label: 'GMV', value: '¥0', color: '#f56c6c' },
        { label: '订单数', value: '0', color: '#909399' },
        { label: '转化率', value: '0%', color: '#00b894' }
      ],
      dauChart: null,
      newUserChart: null,
      appointmentChart: null,
      gmvChart: null,
      funnelChart: null,
      retentionLoading: false,
      retentionData: [],
      retentionColumns: [1, 2, 3, 4, 5, 6, 7],
      funnelTableData: []
    }
  },
  mounted() {
    this.fetchData()
  },
  beforeDestroy() {
    [this.dauChart, this.newUserChart, this.appointmentChart, this.gmvChart, this.funnelChart].forEach(chart => {
      if (chart) chart.dispose()
    })
  },
  methods: {
    handleDateChange() {
      this.fetchData()
    },
    getParams() {
      const params = {}
      if (this.dateRange && this.dateRange.length === 2) {
        params.beginTime = this.dateRange[0]
        params.endTime = this.dateRange[1]
      }
      return params
    },
    async fetchData() {
      const params = this.getParams()
      await Promise.all([
        this.getCore(params),
        this.renderDauChart(params),
        this.renderNewUserChart(params),
        this.renderAppointmentChart(params),
        this.renderGmvChart(params),
        this.getRetention(params),
        this.renderFunnelChart(params)
      ])
    },
    async getCore(params) {
      try {
        const res = await getCoreMetrics(params)
        const d = res.data
        this.coreMetrics = [
          { label: 'DAU', value: d.dau || '0', color: '#409eff' },
          { label: '新增用户', value: d.newUsers || '0', color: '#67c23a' },
          { label: '约拍数', value: d.appointments || '0', color: '#e6a23c' },
          { label: 'GMV', value: '¥' + (d.gmv || '0'), color: '#f56c6c' },
          { label: '订单数', value: d.orders || '0', color: '#909399' },
          { label: '转化率', value: (d.conversion || '0') + '%', color: '#00b894' }
        ]
      } catch (err) {
        console.error('获取核心指标失败', err)
      }
    },
    initLineChart(refName, chartInstance, option) {
      if (!this[chartInstance]) {
        this[chartInstance] = echarts.init(this.$refs[refName])
      }
      this[chartInstance].setOption(option)
    },
    async renderDauChart(params) {
      try {
        const res = await getDauTrend(params)
        const d = res.data
        this.initLineChart('dauChart', 'dauChart', {
          tooltip: { trigger: 'axis' },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: { type: 'category', data: d.dates || [] },
          yAxis: { type: 'value', name: '人数' },
          series: [{ name: 'DAU', type: 'bar', data: d.values || [], itemStyle: { color: '#409eff' }, barMaxWidth: 30 }]
        })
      } catch (err) {
        console.error('获取DAU趋势失败', err)
      }
    },
    async renderNewUserChart(params) {
      try {
        const res = await getNewUserTrend(params)
        const d = res.data
        this.initLineChart('newUserChart', 'newUserChart', {
          tooltip: { trigger: 'axis' },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: { type: 'category', data: d.dates || [] },
          yAxis: { type: 'value', name: '人数' },
          series: [{ name: '新增用户', type: 'line', smooth: true, areaStyle: {}, data: d.values || [], itemStyle: { color: '#67c23a' } }]
        })
      } catch (err) {
        console.error('获取新增用户趋势失败', err)
      }
    },
    async renderAppointmentChart(params) {
      try {
        const res = await getAppointmentTrend(params)
        const d = res.data
        this.initLineChart('appointmentChart', 'appointmentChart', {
          tooltip: { trigger: 'axis' },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: { type: 'category', data: d.dates || [] },
          yAxis: { type: 'value', name: '次数' },
          series: [{ name: '约拍数', type: 'line', smooth: true, areaStyle: {}, data: d.values || [], itemStyle: { color: '#e6a23c' } }]
        })
      } catch (err) {
        console.error('获取约拍趋势失败', err)
      }
    },
    async renderGmvChart(params) {
      try {
        const res = await getGmvTrend(params)
        const d = res.data
        this.initLineChart('gmvChart', 'gmvChart', {
          tooltip: { trigger: 'axis', formatter: '{b}<br/>{a}: ¥{c}' },
          grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
          xAxis: { type: 'category', data: d.dates || [] },
          yAxis: { type: 'value', name: '金额(元)' },
          series: [{ name: 'GMV', type: 'bar', data: d.values || [], itemStyle: { color: '#f56c6c' }, barMaxWidth: 30 }]
        })
      } catch (err) {
        console.error('获取GMV趋势失败', err)
      }
    },
    async getRetention(params) {
      this.retentionLoading = true
      try {
        const res = await getRetentionData(params)
        this.retentionData = res.data || []
      } catch (err) {
        console.error('获取留存数据失败', err)
      } finally {
        this.retentionLoading = false
      }
    },
    getHeatColor(value) {
      if (value === undefined || value === null) return '#ebeef5'
      if (value >= 60) return '#67c23a'
      if (value >= 40) return '#95d475'
      if (value >= 25) return '#e6a23c'
      if (value >= 15) return '#f89898'
      return '#f56c6c'
    },
    async renderFunnelChart(params) {
      try {
        const res = await getFunnelData(params)
        const d = res.data
        const items = d.items || []
        this.funnelTableData = items.map((item, index) => ({
          name: item.name,
          value: item.value,
          rate: index === 0 ? '100.00' : items[0].value > 0 ? ((item.value / items[0].value) * 100).toFixed(2) : '0.00',
          dropRate: index === 0 ? '0.00' : items[index - 1].value > 0 ? (((items[index - 1].value - item.value) / items[index - 1].value) * 100).toFixed(2) : '0.00'
        }))
        if (!this.funnelChart) {
          this.funnelChart = echarts.init(this.$refs.funnelChart)
        }
        this.funnelChart.setOption({
          tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c}' },
          series: [{
            name: '转化漏斗',
            type: 'funnel',
            left: '10%',
            width: '80%',
            sort: 'descending',
            gap: 2,
            label: { show: true, position: 'inside', formatter: '{b}\n{c}' },
            data: items
          }]
        })
      } catch (err) {
        console.error('获取漏斗数据失败', err)
      }
    },
    async handleExport() {
      try {
        const res = await exportStats(this.getParams())
        const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = '统计数据.xlsx'
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
.core-metric {
  text-align: center;
  padding: 8px 0;
}
.core-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}
.core-value {
  font-size: 24px;
  font-weight: bold;
}
</style>
