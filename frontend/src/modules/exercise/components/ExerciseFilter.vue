<template>
  <div class="bg-white rounded-lg shadow p-4">
    <div class="space-y-4">
      <!-- 搜索框 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">搜索动作</label>
        <input
          v-model="localSearch"
          type="text"
          placeholder="输入动作名称或描述..."
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          @input="handleSearch"
        />
      </div>

      <!-- 分类筛选 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">动作分类</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="category in categories"
            :key="category.value"
            @click="handleCategoryChange(category.value)"
            :class="
              selectedCategory === category.value
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            "
            class="px-3 py-1.5 text-sm font-medium rounded-full transition-colors"
          >
            {{ category.label }}
          </button>
        </div>
      </div>

      <!-- 肌肉群筛选 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">目标肌肉</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="muscle in muscleGroups"
            :key="muscle.value"
            @click="handleMuscleChange(muscle.value)"
            :class="
              selectedMuscle === muscle.value
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            "
            class="px-3 py-1.5 text-sm font-medium rounded-full transition-colors"
          >
            {{ muscle.label }}
          </button>
        </div>
      </div>

      <!-- 清除筛选 -->
      <button
        v-if="hasFilters"
        @click="handleClearFilters"
        class="w-full py-2 text-sm text-gray-600 hover:text-gray-900 underline"
      >
        清除所有筛选
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ExerciseCategory, MuscleGroup } from '../types'

interface Props {
  search?: string
  category?: ExerciseCategory
  muscleGroup?: MuscleGroup
}

const props = withDefaults(defineProps<Props>(), {
  search: '',
  category: undefined,
  muscleGroup: undefined
})

const emit = defineEmits<{
  'update:search': [value: string]
  'update:category': [value: ExerciseCategory | undefined]
  'update:muscleGroup': [value: MuscleGroup | undefined]
  clear: []
}>()

const localSearch = ref(props.search)
const selectedCategory = ref<ExerciseCategory | undefined>(props.category)
const selectedMuscle = ref<MuscleGroup | undefined>(props.muscleGroup)

const categories = [
  { label: '全部', value: undefined },
  { label: '杠铃', value: ExerciseCategory.BARBELL },
  { label: '哑铃', value: ExerciseCategory.DUMBBELL },
  { label: '器械', value: ExerciseCategory.MACHINE },
  { label: '自重', value: ExerciseCategory.BODYWEIGHT },
  { label: '有氧', value: ExerciseCategory.CARDIO }
]

const muscleGroups = [
  { label: '全部', value: undefined },
  { label: '胸部', value: MuscleGroup.CHEST },
  { label: '背部', value: MuscleGroup.BACK },
  { label: '肩部', value: MuscleGroup.SHOULDERS },
  { label: '腿部', value: MuscleGroup.LEGS },
  { label: '核心', value: MuscleGroup.CORE }
]

const hasFilters = computed(() => {
  return localSearch.value || selectedCategory.value || selectedMuscle.value
})

// 防抖搜索
let searchTimeout: NodeJS.Timeout | null = null

function handleSearch() {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }

  searchTimeout = setTimeout(() => {
    emit('update:search', localSearch.value)
  }, 300)
}

function handleCategoryChange(category: ExerciseCategory | undefined) {
  selectedCategory.value = category
  emit('update:category', category)
}

function handleMuscleChange(muscle: MuscleGroup | undefined) {
  selectedMuscle.value = muscle
  emit('update:muscleGroup', muscle)
}

function handleClearFilters() {
  localSearch.value = ''
  selectedCategory.value = undefined
  selectedMuscle.value = undefined
  emit('clear')
}

// 监听 props 变化
watch(
  () => props.search,
  (newVal) => {
    localSearch.value = newVal
  }
)

watch(
  () => props.category,
  (newVal) => {
    selectedCategory.value = newVal
  }
)

watch(
  () => props.muscleGroup,
  (newVal) => {
    selectedMuscle.value = newVal
  }
)
</script>
