<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">仪表盘</h1>

    <Loading :loading="loading">
      <div v-if="stats" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- 训练次数 -->
        <Card>
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">总训练次数</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalWorkouts }}</p>
            </div>
          </div>
        </Card>

        <!-- 训练量 -->
        <Card>
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">总训练量</p>
              <p class="text-2xl font-semibold text-gray-900">{{ formatVolume(stats.totalVolume) }}</p>
            </div>
          </div>
        </Card>

        <!-- 连续训练天数 -->
        <Card>
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">连续训练</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.currentStreak }} 天</p>
            </div>
          </div>
        </Card>

        <!-- 最常训练动作 -->
        <Card class="md:col-span-2 lg:col-span-3">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">最常训练动作</h3>
          <p class="text-gray-600">{{ stats.mostFrequentExercise }}</p>
        </Card>
      </div>

      <div v-else class="text-center py-12">
        <p class="text-gray-500">暂无训练数据</p>
      </div>
    </Loading>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAnalysisStore } from '../stores/analysis'
import { storeToRefs } from 'pinia'
import Card from '@/shared/components/ui/Card.vue'
import Loading from '@/shared/components/ui/Loading.vue'
import { formatVolume } from '@/core/utils/format'

const analysisStore = useAnalysisStore()
const { dashboardStats, loading } = storeToRefs(analysisStore)

const stats = computed(() => dashboardStats.value)

onMounted(() => {
  analysisStore.fetchDashboardStats()
})
</script>
