<template>
  <div
    class="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-4 cursor-pointer"
    @click="handleClick"
  >
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-900">{{ exercise.name }}</h3>
        <div class="mt-2 flex flex-wrap gap-2">
          <span
            :class="categoryClass"
            class="px-2 py-1 text-xs font-medium rounded-full"
          >
            {{ categoryLabel }}
          </span>
          <span
            v-for="muscle in exercise.muscleGroups.slice(0, 3)"
            :key="muscle"
            class="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-700"
          >
            {{ getMuscleLabel(muscle) }}
          </span>
        </div>
        <p v-if="exercise.description" class="mt-2 text-sm text-gray-600 line-clamp-2">
          {{ exercise.description }}
        </p>
      </div>
      <button
        v-if="showActions"
        @click.stop="handleEdit"
        class="ml-2 p-2 text-gray-400 hover:text-gray-600"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Exercise } from '../types'

interface Props {
  exercise: Exercise
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showActions: false
})

const emit = defineEmits<{
  click: [exercise: Exercise]
  edit: [exercise: Exercise]
}>()

// 兼容字符串和枚举的分类标签
const categoryLabels: Record<string, string> = {
  'barbell': '杠铃',
  'dumbbell': '哑铃',
  'machine': '器械',
  'bodyweight': '自重',
  'cardio': '有氧'
}

const categoryColors: Record<string, string> = {
  'barbell': 'bg-purple-100 text-purple-700',
  'dumbbell': 'bg-indigo-100 text-indigo-700',
  'machine': 'bg-gray-100 text-gray-700',
  'bodyweight': 'bg-green-100 text-green-700',
  'cardio': 'bg-orange-100 text-orange-700'
}

const muscleLabels: Record<string, string> = {
  'chest': '胸部',
  'back': '背部',
  'shoulders': '肩部',
  'biceps': '肱二头肌',
  'triceps': '肱三头肌',
  'legs': '腿部',
  'core': '核心',
  'full_body': '全身'
}

const categoryLabel = computed(() => {
  const cat = String(props.exercise.category)
  return categoryLabels[cat] || props.exercise.category
})

const categoryClass = computed(() => {
  const cat = String(props.exercise.category)
  return categoryColors[cat] || 'bg-gray-100 text-gray-700'
})

function getMuscleLabel(muscle: string) {
  return muscleLabels[muscle] || muscle
}

function handleClick() {
  emit('click', props.exercise)
}

function handleEdit() {
  emit('edit', props.exercise)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
