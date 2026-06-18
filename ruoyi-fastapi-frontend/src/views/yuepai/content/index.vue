<template>
  <div class="app-container">
    <el-form :inline="true" :model="queryParams">
      <el-form-item label="审核"><el-select v-model="queryParams.audit_status" clearable><el-option label="待审核" value="0" /><el-option label="已通过" value="1" /><el-option label="已拒绝" value="2" /></el-select></el-form-item>
      <el-form-item><el-button type="primary" @click="handleQuery">搜索</el-button></el-form-item>
    </el-form>
    <el-table v-loading="loading" :data="list" border>
      <el-table-column label="ID" prop="id" width="70" />
      <el-table-column label="类型" width="80"><template #default="{row}"><el-tag>{{ row.type==="work"?"作品":"动态" }}</el-tag></template></el-table-column>
      <el-table-column label="标题" prop="title" show-overflow-tooltip />
      <el-table-column label="图片数" width="80" align="center"><template #default="{row}">{{ row.images?.length||0 }}</template></el-table-column>
      <el-table-column label="点赞" prop="like_count" width="70" align="center" />
      <el-table-column label="审核" width="90" align="center"><template #default="{row}"><el-tag :type="auditTag(row.audit_status)">{{ auditText[row.audit_status] }}</el-tag></template></el-table-column>
      <el-table-column label="时间" prop="create_time" width="160" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{row}">
          <el-button v-if="row.audit_status==='0'" size="small" type="success" @click="handleAudit(row.id,'1')">通过</el-button>
          <el-button v-if="row.audit_status==='0'" size="small" type="danger" @click="handleAudit(row.id,'2')">拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="queryParams.page_num" :total="total" :page-size="20" layout="total, prev, pager, next" @current-change="handleQuery" />
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { getYuepaiPostList, auditYuepaiPost } from "@/api/yuepai/post";
import { ElMessage } from "element-plus";
const auditText={"0":"待审核","1":"已通过","2":"已拒绝"};
const auditTag=(s)=>({"0":"warning","1":"success","2":"danger"}[s]);
const loading=ref(false);const list=ref([]);const total=ref(0);
const queryParams=ref({audit_status:"0",page_num:1,page_size:20});
async function handleQuery(){loading.value=true;try{const res=await getYuepaiPostList(queryParams.value);list.value=res.rows||[];total.value=res.total||0;}finally{loading.value=false;}}
async function handleAudit(id,status){await auditYuepaiPost(id,status);ElMessage.success("审核成功");handleQuery();}
onMounted(()=>handleQuery());
</script>
