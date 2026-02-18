import { useApi } from '@/core/composables/useApi'
import type { Exercise, ExerciseQueryParams, ExerciseFormData } from '../types'
import type { PaginatedResponse } from '@/core/api/types'

export const useExerciseApi = () => {
  const { get, post, put, del } = useApi()

  return {
    // 获取动作列表
    getExercises: (params?: ExerciseQueryParams) =>
      get<Exercise[]>('/api/exercises', { params }),

    // 获取分页动作列表
    getExercisesPaginated: (params?: ExerciseQueryParams) =>
      get<PaginatedResponse<Exercise>>('/api/exercises', { params }),

    // 获取单个动作
    getExercise: (id: number) =>
      get<Exercise>(`/api/exercises/${id}`),

    // 创建动作
    createExercise: (data: ExerciseFormData) =>
      post<Exercise>('/api/exercises', data),

    // 更新动作
    updateExercise: (id: number, data: Partial<ExerciseFormData>) =>
      put<Exercise>(`/api/exercises/${id}`, data),

    // 删除动作
    deleteExercise: (id: number) =>
      del<void>(`/api/exercises/${id}`),

    // 搜索动作
    searchExercises: (query: string) =>
      get<Exercise[]>('/api/exercises/search', { params: { q: query } })
  }
}
