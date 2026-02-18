<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">动作库</h1>
      <p class="mt-1 text-sm text-gray-500">浏览和管理训练动作</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- 筛选栏 -->
      <div class="lg:col-span-1">
        <ExerciseFilter
          v-model:search="filters.search"
          v-model:category="filters.category"
          v-model:muscleGroup="filters.muscleGroup"
          @clear="handleClearFilters"
        />
      </div>

      <!-- 动作列表 -->
      <div class="lg:col-span-3">
        <Loading :loading="loading">
          <div v-if="filteredExercises.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ExerciseCard
              v-for="exercise in filteredExercises"
              :key="exercise.id"
              :exercise="exercise"
              @click="handleExerciseClick"
            />
          </div>

          <div v-else class="text-center py-12">
            <svg
              class="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">没有找到动作</h3>
            <p class="mt-1 text-sm text-gray-500">尝试调整筛选条件</p>
          </div>
        </Loading>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useExerciseStore } from '../stores/exercise'
import { storeToRefs } from 'pinia'
import ExerciseFilter from '../components/ExerciseFilter.vue'
import ExerciseCard from '../components/ExerciseCard.vue'
import Loading from '@/shared/components/ui/Loading.vue'
import type { Exercise, ExerciseQueryParams } from '../types'

const router = useRouter()
const exerciseStore = useExerciseStore()

const { filteredExercises, loading, filters } = storeToRefs(exerciseStore)

// 监听筛选条件变化，重新获取数据
watch(
  filters,
  (newFilters) => {
    exerciseStore.fetchExercises(newFilters)
  },
  { deep: true }
)

function handleExerciseClick(exercise: Exercise) {
  router.push(`/exercises/${exercise.id}`)
}

function handleClearFilters() {
  exerciseStore.clearFilters()
}

onMounted(() => {
  exerciseStore.fetchExercises()
})
</script>
