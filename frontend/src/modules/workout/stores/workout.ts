import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useWorkoutApi } from '../services/workout.api'
import type { WorkoutSession, WorkoutTemplate, WorkoutSessionFormData, WorkoutQueryParams } from '../types'

export const useWorkoutStore = defineStore('workout', () => {
  // State
  const workouts = ref<WorkoutSession[]>([])
  const currentWorkout = ref<WorkoutSession | null>(null)
  const templates = ref<WorkoutTemplate[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 筛选条件
  const filters = ref<WorkoutQueryParams>({
    startDate: undefined,
    endDate: undefined,
    page: 1,
    pageSize: 20
  })

  // Getters
  const workoutCount = computed(() => workouts.value.length)

  const recentWorkouts = computed(() => {
    return workouts.value
      .slice()
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
      .slice(0, 5)
  })

  // Actions
  async function fetchWorkouts(params?: WorkoutQueryParams) {
    loading.value = true
    error.value = null

    try {
      const api = useWorkoutApi()
      const queryParams = { ...filters.value, ...params }
      const response = await api.getWorkoutsPaginated(queryParams)
      workouts.value = response.items
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取训练记录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchWorkout(id: number) {
    loading.value = true
    error.value = null

    try {
      const api = useWorkoutApi()
      currentWorkout.value = await api.getWorkout(id)
      return currentWorkout.value
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取训练详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createWorkout(data: WorkoutSessionFormData) {
    loading.value = true
    error.value = null

    try {
      const api = useWorkoutApi()
      const workout = await api.createWorkout(data)
      workouts.value.unshift(workout)
      return workout
    } catch (err: any) {
      error.value = err.response?.data?.message || '创建训练记录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateWorkout(id: number, data: Partial<WorkoutSessionFormData>) {
    loading.value = true
    error.value = null

    try {
      const api = useWorkoutApi()
      const workout = await api.updateWorkout(id, data)

      // 更新列表中的项
      const index = workouts.value.findIndex(w => w.id === id)
      if (index !== -1) {
        workouts.value[index] = workout
      }

      // 更新当前项
      if (currentWorkout.value?.id === id) {
        currentWorkout.value = workout
      }

      return workout
    } catch (err: any) {
      error.value = err.response?.data?.message || '更新训练记录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteWorkout(id: number) {
    loading.value = true
    error.value = null

    try {
      const api = useWorkoutApi()
      await api.deleteWorkout(id)

      // 从列表中移除
      workouts.value = workouts.value.filter(w => w.id !== id)

      // 清空当前项
      if (currentWorkout.value?.id === id) {
        currentWorkout.value = null
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || '删除训练记录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchTemplates() {
    loading.value = true
    error.value = null

    try {
      const api = useWorkoutApi()
      templates.value = await api.getTemplates()
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取训练模板失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setFilters(newFilters: Partial<WorkoutQueryParams>) {
    filters.value = { ...filters.value, ...newFilters }
  }

  function clearFilters() {
    filters.value = {
      startDate: undefined,
      endDate: undefined,
      page: 1,
      pageSize: 20
    }
  }

  return {
    // State
    workouts,
    currentWorkout,
    templates,
    loading,
    error,
    filters,

    // Getters
    workoutCount,
    recentWorkouts,

    // Actions
    fetchWorkouts,
    fetchWorkout,
    createWorkout,
    updateWorkout,
    deleteWorkout,
    fetchTemplates,
    setFilters,
    clearFilters
  }
})
