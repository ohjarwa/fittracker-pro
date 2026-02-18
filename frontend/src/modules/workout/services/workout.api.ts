import { useApi } from '@/core/composables/useApi'
import type {
  WorkoutSession,
  WorkoutTemplate,
  WorkoutSessionFormData,
  WorkoutTemplateFormData,
  WorkoutQueryParams
} from '../types'
import type { PaginatedResponse } from '@/core/api/types'

export const useWorkoutApi = () => {
  const { get, post, put, del } = useApi()

  return {
    // ===== 训练记录 =====

    // 获取训练列表
    getWorkouts: (params?: WorkoutQueryParams) =>
      get<WorkoutSession[]>('/api/workouts', { params }),

    // 获取分页训练列表
    getWorkoutsPaginated: (params?: WorkoutQueryParams) =>
      get<PaginatedResponse<WorkoutSession>>('/api/workouts', { params }),

    // 获取单个训练
    getWorkout: (id: number) =>
      get<WorkoutSession>(`/api/workouts/${id}`),

    // 创建训练
    createWorkout: (data: WorkoutSessionFormData) =>
      post<WorkoutSession>('/api/workouts', data),

    // 更新训练
    updateWorkout: (id: number, data: Partial<WorkoutSessionFormData>) =>
      put<WorkoutSession>(`/api/workouts/${id}`, data),

    // 删除训练
    deleteWorkout: (id: number) =>
      del<void>(`/api/workouts/${id}`),

    // ===== 训练模板 =====

    // 获取模板列表
    getTemplates: () =>
      get<WorkoutTemplate[]>('/api/workouts/templates'),

    // 获取单个模板
    getTemplate: (id: number) =>
      get<WorkoutTemplate>(`/api/workouts/templates/${id}`),

    // 创建模板
    createTemplate: (data: WorkoutTemplateFormData) =>
      post<WorkoutTemplate>('/api/workouts/templates', data),

    // 更新模板
    updateTemplate: (id: number, data: Partial<WorkoutTemplateFormData>) =>
      put<WorkoutTemplate>(`/api/workouts/templates/${id}`, data),

    // 删除模板
    deleteTemplate: (id: number) =>
      del<void>(`/api/workouts/templates/${id}`),

    // 从模板创建训练
    createWorkoutFromTemplate: (templateId: number, date: string) =>
      post<WorkoutSession>(`/api/workouts/templates/${templateId}/start`, { date })
  }
}
