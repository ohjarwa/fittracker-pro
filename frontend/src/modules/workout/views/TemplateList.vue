<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/core/composables/useApi'

interface Template {
  name: string
  usage_count: number
}

const templates = ref<Template[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchTemplates() {
  loading.value = true
  error.value = null
  try {
    const { get } = useApi()
    const response = await get<{ templates: Template[] }>('/api/workouts/templates/list')
    templates.value = response.templates
  } catch (err: any) {
    error.value = err.response?.data?.message || '获取训练模板失败'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTemplates()
})
</script>

<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">训练模板</h1>
        <p class="text-gray-600 mt-1">管理你的训练模板</p>
      </div>
      <button
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        新建模板
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <p class="text-gray-600 mt-2">加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-600">{{ error }}</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="templates.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">还没有训练模板</h3>
      <p class="mt-1 text-sm text-gray-500">创建训练时保存为模板，或者从历史训练中创建模板</p>
    </div>

    <!-- 模板列表 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="template in templates"
        :key="template.name"
        class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
      >
        <h3 class="text-lg font-semibold text-gray-900">{{ template.name }}</h3>
        <div class="mt-3 text-sm text-gray-500">
          已使用 {{ template.usage_count }} 次
        </div>
        <div class="mt-4 flex gap-2">
          <button class="flex-1 px-3 py-1.5 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            使用模板
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
