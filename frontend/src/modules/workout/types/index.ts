import type { Exercise } from '@/modules/exercise/types'

// 训练组
export interface WorkoutSet {
  id?: number
  exerciseId: number
  exercise?: Exercise
  weight: number
  reps: number
  rpe?: number
  restTime?: number
  notes?: string
  order?: number
}

// 训练session
export interface WorkoutSession {
  id?: number
  date: string
  name?: string
  notes?: string
  sets: WorkoutSet[]
  duration?: number
  createdAt?: string
  updatedAt?: string
}

// 训练模板
export interface WorkoutTemplate {
  id: number
  name: string
  description?: string
  exercises: TemplateExercise[]
  createdAt?: string
  updatedAt?: string
}

// 模板中的动作
export interface TemplateExercise {
  exerciseId: number
  exercise?: Exercise
  sets: number
  reps: number
  weight?: number
  rpe?: number
  restTime?: number
  notes?: string
}

// 训练创建/更新数据
export interface WorkoutSessionFormData {
  date: string
  name?: string
  notes?: string
  sets: Omit<WorkoutSet, 'id' | 'exercise'>[]
  duration?: number
}

// 训练模板创建/更新数据
export interface WorkoutTemplateFormData {
  name: string
  description?: string
  exercises: TemplateExercise[]
}

// 训练查询参数
export interface WorkoutQueryParams {
  startDate?: string
  endDate?: string
  page?: number
  pageSize?: number
}
