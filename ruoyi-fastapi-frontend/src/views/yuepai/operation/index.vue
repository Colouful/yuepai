<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="轮播图" name="banner" />
      <el-tab-pane label="活动" name="activity" />
      <el-tab-pane label="优惠券" name="coupon" />
      <el-tab-pane label="公告" name="notice" />
    </el-tabs>

    <el-row style="margin-bottom: 16px">
      <el-button type="primary" icon="Plus" @click="handleAdd">新增{{ tabLabels[activeTab] }}</el-button>
    </el-row>

    <el-table v-loading="loading" :data="list" border stripe>
      <el-table-column label="ID" prop="id" width="70" align="center" />
      <el-table-column label="标题" prop="title" min-width="200" show-overflow-tooltip />
      <el-table-column v-if="activeTab==='banner'" label="图片" width="140" align="center">
        <template #default="{ row }"><el-image v-if="row.image" :src="row.image" style="width:100px;height:50px;border-radius:4px" fit="cover" /></template>
      </el-table-column>
      <el-table-column v-if="activeTab==='banner'||activeTab==='activity'" label="链接" prop="link" width="200" show-overflow-tooltip />
      <el-table-column label="排序" prop="sort_order" width="80" align="center" />
      <el-table-column label="状态" width="90" align="center">
        <template #default="{ row }"><el-tag :type="row.status==='1'?'success':'info'">{{ row.status==='1'?'启用':'禁用' }}</el-tag></template>
      </el-table-column>
      <el-table-column label="浏览量" prop="view_count" width="90" align="center" />
      <el-table-column label="创建时间" prop="create_time" width="170" />
      <el-table-column label="操作" width="160" fixed="right" align="center">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.page_num" v-model:limit="queryParams.page_size" @pagination="getList" />

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑' : '新增'" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px">
        <el-form-item label="标题" prop="title"><el-input v-model="form.title" placeholder="请输入标题" /></el-form-item>
        <el-form-item v-if="activeTab==='banner'" label="图片"><el-input v-model="form.image" placeholder="图片URL" /></el-form-item>
        <el-form-item v-if="activeTab==='banner'||activeTab==='activity'" label="链接"><el-input v-model="form.link" placeholder="跳转链接" /></el-form-item>
        <el-form-item v-if="activeTab==='notice'" label="内容" prop="content"><el-input v-model="form.content" type="textarea" :rows="6" placeholder="请输入内容" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" :max="999" /></el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status"><el-radio value="1">启用</el-radio><el-radio value="0">禁用</el-radio></el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { getOperationList, saveOperation, deleteOperation } from '@/api/yuepai/admin'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeTab = ref('banner')
const loading = ref(false); const list = ref([]); const total = ref(0)
const queryParams = reactive({ type: 'banner', status: '', page_num: 1, page_size: 50 })
const dialogVisible = ref(false); const formRef = ref(null)
const form = reactive({ id: null, type: 'banner', title: '', content: '', image: '', link: '', sort_order: 0, status: '1' })
const rules = { title: [{ required: true, message: '请输入标题', trigger: 'blur' }] }
const tabLabels = { banner: '轮播图', activity: '活动', coupon: '优惠券', notice: '公告' }

async function getList() {
  loading.value = true
  try { const res = await getOperationList(queryParams); list.value = res.data?.rows || []; total.value = res.data?.total || 0 } finally { loading.value = false }
}
function handleTabChange(tab) { queryParams.type = tab; queryParams.page_num = 1; form.type = tab; getList() }
function handleAdd() { Object.assign(form, { id: null, type: activeTab.value, title: '', content: '', image: '', link: '', sort_order: 0, status: '1' }); dialogVisible.value = true }
function handleEdit(row) { Object.assign(form, row); dialogVisible.value = true }
async function handleDelete(row) {
  await ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' })
  await deleteOperation(row.id); ElMessage.success('删除成功'); getList()
}
async function confirmSave() {
  await saveOperation(form); ElMessage.success('保存成功'); dialogVisible.value = false; getList()
}
getList()
</script>
