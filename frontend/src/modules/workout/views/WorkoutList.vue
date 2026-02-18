<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">训练记录</h1>
        <p class="mt-1 text-sm text-gray-500">记录和管理你的训练</p>
      </div>
      <Button @click="handleCreate">新建训练</Button>
    </div>

    <Loading :loading="loading">
      <div v-if="recentWorkouts.length > 0" class="space-y-4">
        <Card
          v-for="workout in recentWorkouts"
          :key="workout.id"
          :hover="true"
          class="cursor-pointer"
          @click="handleWorkoutClick(workout)"
        >
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">
                {{ workout.notes || workout.template_name || '训练' }}
              </h3>
              <p class="text-sm text-gray-500 mt-1">
                {{ formatDate(workout.date) }}
                <span v-if="workout.duration_min"> · {{ workout.duration_min }} 分钟</span>
                <span v-if="workout.overall_rpe"> · RPE {{ workout.overall_rpe }}</span>
              </p>
            </div>
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </Card>
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
        <h3 class="mt-2 text-sm font-medium text-gray-900">还没有训练记录</h3>
        <p class="mt-1 text-sm text-gray-500">开始记录你的第一次训练吧</p>
        <div class="mt-6">
          <Button @click="handleCreate">创建训练</Button>
        </div>
      </div>
    </Loading>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWorkoutStore } from '../stores/workout'
import { storeToRefs } from 'pinia'
import Button from '@/shared/components/ui/Button.vue'
import Card from '@/shared/components/ui/Card.vue'
import Loading from '@/shared/components/ui/Loading.vue'
import { formatDate } from '@/core/utils/format'
import type { WorkoutSession } from '../types'

const router = useRouter()
const workoutStore = useWorkoutStore()

const { recentWorkouts, loading } = storeToRefs(workoutStore)

function handleCreate() {
  router.push('/workouts/create')
}

function handleWorkoutClick(workout: WorkoutSession) {
  router.push(`/workouts/${workout.id}`)
}

onMounted(() => {
  workoutStore.fetchWorkouts()
})
</script>
