<template>
  <div class="app-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb8">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">待审核</div>
            <div class="stat-value" style="color: #e6a23c">{{ stats.pending }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">今日通过</div>
            <div class="stat-value" style="color: #67c23a">{{ stats.todayApproved }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">今日拒绝</div>
            <div class="stat-value" style="color: #f56c6c">{{ stats.todayRejected }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-title">累计审核</div>
            <div class="stat-value">{{ stats.totalReviewed }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索区域 -->
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="100px">
      <el-form-item label="内容类型" prop="contentType">
        <el-select v-model="queryParams.contentType" placeholder="请选择" clearable style="width: 200px">
          <el-option label="动态" value="post" />
          <el-option label="作品" value="work" />
          <el-option label="评论" value="comment" />
        </el-select>
      </el-form-item>
      <el-form-item label="审核状态" prop="reviewStatus">
        <el-select v-model="queryParams.reviewStatus" placeholder="请选择" clearable style="width: 200px">
          <el-option label="待审核" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已拒绝" value="rejected" />
        </el-select>
      </el-form-item>
      <el-form-item label="发布人" prop="publisher">
        <el-input v-model="queryParams.publisher" placeholder="请输入发布人" clearable style="width: 200px" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="发布时间" prop="dateRange">
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
        <el-button type="success" icon="el-icon-check" :disabled="multipleSelection.length === 0" @click="handleBatchApprove" v-hasPermi="['yuepai:content:review']">批量通过</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" icon="el-icon-close" :disabled="multipleSelection.length === 0" @click="handleBatchReject" v-hasPermi="['yuepai:content:review']">批量拒绝</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" />
    </el-row>

    <!-- 内容列表 -->
    <el-table v-loading="loading" :data="contentList" border @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="内容预览" min-width="300">
        <template slot-scope="scope">
          <div class="content-preview">
            <el-image v-if="scope.row.coverImage" :src="scope.row.coverImage" style="width: 60px; height: 60px; border-radius: 4px; margin-right: 10px" fit="cover" />
            <div class="content-info">
              <div class="content-title">{{ scope.row.title || '无标题' }}</div>
              <div class="content-text" v-if="scope.row.content">{{ scope.row.content | contentFilter }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="内容类型" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getContentTypeTagType(scope.row.contentType)">{{ getContentTypeLabel(scope.row.contentType) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="发布人" width="120" align="center">
        <template slot-scope="scope">
          <div style="display: flex; align-items: center; justify-content: center">
            <el-avatar :src="scope.row.publisherAvatar" :size="24" style="margin-right: 6px" />
            <span>{{ scope.row.publisherName }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="审核状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getReviewTagType(scope.row.reviewStatus)">{{ getReviewLabel(scope.row.reviewStatus) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="发布时间" prop="createTime" width="160" align="center" />
      <el-table-column label="操作" width="240" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button type="text" icon="el-icon-view" @click="handlePreview(scope.row)">预览</el-button>
          <template v-if="scope.row.reviewStatus === 'pending'">
            <el-button type="text" icon="el-icon-check" @click="handleApprove(scope.row)" v-hasPermi="['yuepai:content:review']" style="color: #67c23a">通过</el-button>
            <el-button type="text" icon="el-icon-close" @click="handleReject(scope.row)" v-hasPermi="['yuepai:content:review']" style="color: #f56c6c">拒绝</el-button>
          </template>
          <el-button type="text" icon="el-icon-delete" @click="handleDelete(scope.row)" v-hasPermi="['yuepai:content:delete']" style="color: #f56c6c">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" :page.sync="queryParams.pageNum" :limit.sync="queryParams.pageSize" @pagination="getList" />

    <!-- 内容预览对话框 -->
    <el-dialog title="内容预览" :visible.sync="previewDialogVisible" width="700px" append-to-body>
      <div class="preview-container">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="内容类型">{{ getContentTypeLabel(previewForm.contentType) }}</el-descriptions-item>
          <el-descriptions-item label="发布人">{{ previewForm.publisherName }}</el-descriptions-item>
          <el-descriptions-item label="发布时间" :span="2">{{ previewForm.createTime }}</el-descriptions-item>
        </el-descriptions>
        <el-divider content-position="left">内容详情</el-divider>
        <h3 v-if="previewForm.title">{{ previewForm.title }}</h3>
        <p style="line-height: 1.8; white-space: pre-wrap;">{{ previewForm.content }}</p>
        <div v-if="previewForm.images && previewForm.images.length" style="margin-top: 15px">
          <el-image v-for="(img, index) in previewForm.images" :key="index" :src="img" style="width: 120px; height: 120px; margin-right: 10px; margin-bottom: 10px; border-radius: 4px" fit="cover" :preview-src-list="previewForm.images" />
        </div>
      </div>
      <div slot="footer">
        <el-button @click="previewDialogVisible = false">关 闭</el-button>
        <template v-if="previewForm.reviewStatus === 'pending'">
          <el-button type="success" @click="handleApprove(previewForm); previewDialogVisible = false" v-hasPermi="['yuepai:content:review']">通 过</el-button>
          <el-button type="danger" @click="handleReject(previewForm)" v-hasPermi="['yuepai:content:review']">拒 绝</el-button>
        </template>
      </div>
    </el-dialog>

    <!-- 批量拒绝对话框 -->
    <el-dialog title="批量拒绝" :visible.sync="batchRejectDialogVisible" width="500px" append-to-body>
      <el-form :model="batchRejectForm" ref="batchRejectFormRef" :rules="batchRejectFormRules" label-width="100px">
        <el-form-item label="拒绝数量">
          <span style="font-weight: bold">{{ multipleSelection.length }}</span> 条内容
        </el-form-item>
        <el-form-item label="拒绝原因" prop="reason">
          <el-select v-model="batchRejectForm.reason" placeholder="请选择拒绝原因" style="width: 100%">
            <el-option label="内容违规" value="violation" />
            <el-option label="信息虚假" value="false_info" />
            <el-option label="涉及广告" value="advertising" />
            <el-option label="低俗内容" value="vulgar" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="详细说明" prop="detail">
          <el-input v-model="batchRejectForm.detail" type="textarea" placeholder="请输入详细说明（选填）" :rows="3" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="batchRejectDialogVisible = false">取 消</el-button>
        <el-button type="danger" @click="submitBatchReject">确认拒绝</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getContentList, approveContent, rejectContent, batchApproveContent, batchRejectContent, deleteContent, getContentStats } from '@/api/yuepai/yuepai-admin'
import Pagination from '@/components/Pagination'
import RightToolbar from '@/components/RightToolbar'

export default {
  name: 'YuepaiContentReview',
  components: { Pagination, RightToolbar },
  filters: {
    contentFilter(val) {
      if (!val) return ''
      return val.length > 80 ? val.substring(0, 80) + '...' : val
    }
  },
  data() {
    return {
      showSearch: true,
      loading: false,
      stats: {
        pending: 0,
        todayApproved: 0,
        todayRejected: 0,
        totalReviewed: 0
      },
      queryParams: {
        pageNum: 1,
        pageSize: 20,
        contentType: undefined,
        reviewStatus: undefined,
        publisher: undefined,
        dateRange: []
      },
      contentList: [],
      total: 0,
      multipleSelection: [],
      previewDialogVisible: false,
      previewForm: {},
      batchRejectDialogVisible: false,
      batchRejectForm: {
        reason: undefined,
        detail: ''
      },
      batchRejectFormRules: {
        reason: [{ required: true, message: '请选择拒绝原因', trigger: 'change' }]
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
        const res = await getContentStats()
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
        const res = await getContentList(params)
        this.contentList = res.rows
        this.total = res.total
      } catch (err) {
        this.$modal.msgError('获取内容列表失败：' + err.message)
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
    handleSelectionChange(selection) {
      this.multipleSelection = selection
    },
    handlePreview(row) {
      this.previewForm = { ...row }
      this.previewDialogVisible = true
    },
    async handleApprove(row) {
      try {
        await this.$confirm('确认通过该内容审核？', '提示', { type: 'success' })
        await approveContent(row.contentId, {})
        this.$modal.msgSuccess('审核通过')
        this.getList()
        this.getStats()
      } catch (err) {
        if (err !== 'cancel') this.$modal.msgError('操作失败：' + err.message)
      }
    },
    async handleReject(row) {
      this.batchRejectForm = { reason: undefined, detail: '' }
      this.batchRejectDialogVisible = true
      this.$nextTick(() => {
        this._rejectSingle = row.contentId
      })
    },
    async handleBatchApprove() {
      try {
        await this.$confirm(`确认通过选中的 ${this.multipleSelection.length} 条内容？`, '提示', { type: 'success' })
        const ids = this.multipleSelection.map(item => item.contentId)
        await batchApproveContent(ids)
        this.$modal.msgSuccess('批量通过成功')
        this.getList()
        this.getStats()
      } catch (err) {
        if (err !== 'cancel') this.$modal.msgError('操作失败：' + err.message)
      }
    },
    handleBatchReject() {
      this.batchRejectForm = { reason: undefined, detail: '' }
      this._rejectSingle = null
      this.batchRejectDialogVisible = true
    },
    submitBatchReject() {
      this.$refs.batchRejectFormRef.validate(async valid => {
        if (!valid) return
        try {
          if (this._rejectSingle) {
            await rejectContent(this._rejectSingle, {
              reason: this.batchRejectForm.reason,
              detail: this.batchRejectForm.detail
            })
          } else {
            const ids = this.multipleSelection.map(item => item.contentId)
            await batchRejectContent(ids, {
              reason: this.batchRejectForm.reason,
              detail: this.batchRejectForm.detail
            })
          }
          this.$modal.msgSuccess('拒绝成功')
          this.batchRejectDialogVisible = false
          this.getList()
          this.getStats()
        } catch (err) {
          this.$modal.msgError('操作失败：' + err.message)
        }
      })
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该内容吗？此操作不可恢复。', '警告', { type: 'warning' })
        await deleteContent(row.contentId)
        this.$modal.msgSuccess('删除成功')
        this.getList()
      } catch (err) {
        if (err !== 'cancel') this.$modal.msgError('删除失败')
      }
    },
    getContentTypeLabel(type) {
      const map = { post: '动态', work: '作品', comment: '评论' }
      return map[type] || type
    },
    getContentTypeTagType(type) {
      const map = { post: '', work: 'success', comment: 'warning' }
      return map[type] || 'info'
    },
    getReviewLabel(status) {
      const map = { pending: '待审核', approved: '已通过', rejected: '已拒绝' }
      return map[status] || status
    },
    getReviewTagType(status) {
      const map = { pending: 'warning', approved: 'success', rejected: 'danger' }
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
.content-preview {
  display: flex;
  align-items: center;
}
.content-info {
  flex: 1;
  overflow: hidden;
}
.content-title {
  font-weight: bold;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.content-text {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}
.preview-container h3 {
  margin: 10px 0;
  color: #303133;
}
</style>
