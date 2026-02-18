<template>
  <div>
    <Loading :loading="loading">
      <div v-if="exercise">
        <!-- 头部 -->
        <div class="mb-6">
          <button
            @click="handleBack"
            class="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            返回列表
          </button>

          <div class="flex items-start justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">{{ exercise.name }}</h1>
              <div class="mt-2 flex flex-wrap gap-2">
                <span
                  :class="categoryClass"
                  class="px-3 py-1 text-sm font-medium rounded-full"
                >
                  {{ categoryLabel }}
                </span>
                <span
                  v-for="muscle in exercise.muscleGroups"
                  :key="muscle"
                  class="px-3 py-1 text-sm font-medium rounded-full bg-blue-100 text-blue-700"
                >
                  {{ getMuscleLabel(muscle) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 内容 -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- 左侧：图片/视频 -->
          <div class="lg:col-span-1">
            <Card>
              <div v-if="exercise.imageUrl" class="aspect-w-16 aspect-h-9">
                <img
                  :src="exercise.imageUrl"
                  :alt="exercise.name"
                  class="object-cover w-full h-full rounded-lg"
                />
              </div>
              <div v-else class="aspect-w-16 aspect-h-9 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-16 h-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </Card>
          </div>

          <!-- 右侧：详情 -->
          <div class="lg:col-span-2 space-y-6">
            <!-- 描述 -->
            <Card v-if="exercise.description" title="动作描述">
              <p class="text-gray-700">{{ exercise.description }}</p>
            </Card>

            <!-- 动作说明 -->
            <Card v-if="exercise.instructions && exercise.instructions.length > 0" title="动作步骤">
              <ol class="list-decimal list-inside space-y-2">
                <li v-for="(instruction, index) in exercise.instructions" :key="index" class="text-gray-700">
                  {{ instruction }}
                </li>
              </ol>
            </Card>

            <!-- 注意事项 -->
            <Card v-if="exercise.tips && exercise.tips.length > 0" title="注意事项">
              <ul class="list-disc list-inside space-y-2">
                <li v-for="(tip, index) in exercise.tips" :key="index" class="text-gray-700">
                  {{ tip }}
                </li>
              </ul>
            </Card>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12">
        <p class="text-gray-500">动作不存在</p>
      </div>
    </Loading>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useExerciseStore } from '../stores/exercise'
import { storeToRefs } from 'pinia'
import Card from '@/shared/components/ui/Card.vue'
import Loading from '@/shared/components/ui/Loading.vue'
import { ExerciseCategory, MuscleGroup } from '../types'

const route = useRoute()
const router = useRouter()
const exerciseStore = useExerciseStore()

const { currentExercise: exercise, loading } = storeToRefs(exerciseStore)

const categoryLabels: Record<ExerciseCategory, string> = {
  [ExerciseCategory.BARBELL]: '杠铃',
  [ExerciseCategory.DUMBBELL]: '哑铃',
  [ExerciseCategory.MACHINE]: '器械',
  [ExerciseCategory.BODYWEIGHT]: '自重',
  [ExerciseCategory.CARDIO]: '有氧'
}

const categoryColors: Record<ExerciseCategory, string> = {
  [ExerciseCategory.BARBELL]: 'bg-purple-100 text-purple-700',
  [ExerciseCategory.DUMBBELL]: 'bg-indigo-100 text-indigo-700',
  [ExerciseCategory.MACHINE]: 'bg-gray-100 text-gray-700',
  [ExerciseCategory.BODYWEIGHT]: 'bg-green-100 text-green-700',
  [ExerciseCategory.CARDIO]: 'bg-orange-100 text-orange-700'
}

const muscleLabels: Record<MuscleGroup, string> = {
  [MuscleGroup.CHEST]: '胸部',
  [MuscleGroup.BACK]: '背部',
  [MuscleGroup.SHOULDERS]: '肩部',
  [MuscleGroup.BICEPS]: '肱二头肌',
  [MuscleGroup.TRICEPS]: '肱三头肌',
  [MuscleGroup.LEGS]: '腿部',
  [MuscleGroup.CORE]: '核心',
  [MuscleGroup.FULL_BODY]: '全身'
}

const categoryLabel = computed(() => {
  return exercise.value ? categoryLabels[exercise.value.category] : ''
})

const categoryClass = computed(() => {
  return exercise.value ? categoryColors[exercise.value.category] : ''
})

function getMuscleLabel(muscle: MuscleGroup) {
  return muscleLabels[muscle] || muscle
}

function handleBack() {
  router.push('/exercises')
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    exerciseStore.fetchExercise(id)
  }
})
</script>
