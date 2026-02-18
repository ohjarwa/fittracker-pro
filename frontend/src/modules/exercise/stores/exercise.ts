import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useExerciseApi } from '../services/exercise.api'
import type { Exercise, ExerciseQueryParams, ExerciseFormData } from '../types'
import { ExerciseCategory, MuscleGroup } from '../types'

export const useExerciseStore = defineStore('exercise', () => {
  // State
  const exercises = ref<Exercise[]>([])
  const currentExercise = ref<Exercise | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 筛选条件
  const filters = ref<ExerciseQueryParams>({
    category: undefined,
    muscleGroup: undefined,
    search: '',
    page: 1,
    pageSize: 20
  })

  // Getters
  const filteredExercises = computed(() => {
    let result = exercises.value

    // 按名称搜索
    if (filters.value.search) {
      const query = filters.value.search.toLowerCase()
      result = result.filter(e =>
        e.name.toLowerCase().includes(query) ||
        e.description?.toLowerCase().includes(query)
      )
    }

    // 按分类筛选
    if (filters.value.category) {
      result = result.filter(e => e.category === filters.value.category)
    }

    // 按肌肉群筛选
    if (filters.value.muscleGroup) {
      result = result.filter(e =>
        e.muscleGroups.includes(filters.value.muscleGroup as MuscleGroup)
      )
    }

    return result
  })

  const exerciseCount = computed(() => exercises.value.length)

  // 设备类型映射
  const equipmentToCategory: Record<string, string> = {
    'barbell': 'barbell',
    'dumbbell': 'dumbbell',
    'machine': 'machine',
    'bodyweight': 'bodyweight',
    'cable': 'machine',
    'cardio': 'cardio'
  }

  // 肌肉群映射
  const muscleGroupMapping: Record<string, string> = {
    'chest': 'chest',
    'back': 'back',
    'shoulders': 'shoulders',
    'biceps': 'biceps',
    'triceps': 'triceps',
    'legs': 'legs',
    'core': 'core',
    'glutes': 'legs',
    'hamstrings': 'legs',
    'full_body': 'full_body'
  }

  // 数据转换：后端格式 -> 前端格式
  function transformExercise(data: any): Exercise {
    // 根据设备类型确定分类
    const category = equipmentToCategory[data.equipment] || 'barbell' as any

    // 构建肌肉群数组
    const muscleGroups: any[] = [
      muscleGroupMapping[data.primary_muscle] || 'chest',
      ...(data.secondary_muscles || []).map((m: string) => muscleGroupMapping[m] || 'chest')
    ]

    return {
      id: data.id,
      name: data.name,
      category,
      muscleGroups,
      description: data.description || undefined,
      createdAt: data.created_at,
      updatedAt: data.updated_at
    }
  }

  // Actions
  async function fetchExercises(params?: ExerciseQueryParams) {
    loading.value = true
    error.value = null

    try {
      const api = useExerciseApi()
      const queryParams = { ...filters.value, ...params }
      const response = await api.getExercisesPaginated(queryParams)
      exercises.value = response.items.map(transformExercise)
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取动作列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchExercise(id: number) {
    loading.value = true
    error.value = null

    try {
      const api = useExerciseApi()
      currentExercise.value = await api.getExercise(id)
      return currentExercise.value
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取动作详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createExercise(data: ExerciseFormData) {
    loading.value = true
    error.value = null

    try {
      const api = useExerciseApi()
      const exercise = await api.createExercise(data)
      exercises.value.push(exercise)
      return exercise
    } catch (err: any) {
      error.value = err.response?.data?.message || '创建动作失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateExercise(id: number, data: Partial<ExerciseFormData>) {
    loading.value = true
    error.value = null

    try {
      const api = useExerciseApi()
      const exercise = await api.updateExercise(id, data)

      // 更新列表中的项
      const index = exercises.value.findIndex(e => e.id === id)
      if (index !== -1) {
        exercises.value[index] = exercise
      }

      // 更新当前项
      if (currentExercise.value?.id === id) {
        currentExercise.value = exercise
      }

      return exercise
    } catch (err: any) {
      error.value = err.response?.data?.message || '更新动作失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteExercise(id: number) {
    loading.value = true
    error.value = null

    try {
      const api = useExerciseApi()
      await api.deleteExercise(id)

      // 从列表中移除
      exercises.value = exercises.value.filter(e => e.id !== id)

      // 清空当前项
      if (currentExercise.value?.id === id) {
        currentExercise.value = null
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || '删除动作失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setFilters(newFilters: Partial<ExerciseQueryParams>) {
    filters.value = { ...filters.value, ...newFilters }
  }

  function clearFilters() {
    filters.value = {
      category: undefined,
      muscleGroup: undefined,
      search: '',
      page: 1,
      pageSize: 20
    }
  }

  return {
    // State
    exercises,
    currentExercise,
    loading,
    error,
    filters,

    // Getters
    filteredExercises,
    exerciseCount,

    // Actions
    fetchExercises,
    fetchExercise,
    createExercise,
    updateExercise,
    deleteExercise,
    setFilters,
    clearFilters
  }
})
