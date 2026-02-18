// 动作分类
export enum ExerciseCategory {
  BARBELL = 'barbell',
  DUMBBELL = 'dumbbell',
  MACHINE = 'machine',
  BODYWEIGHT = 'bodyweight',
  CARDIO = 'cardio'
}

// 肌肉群
export enum MuscleGroup {
  CHEST = 'chest',
  BACK = 'back',
  SHOULDERS = 'shoulders',
  BICEPS = 'biceps',
  TRICEPS = 'triceps',
  LEGS = 'legs',
  CORE = 'core',
  FULL_BODY = 'full_body'
}

// 动作接口
export interface Exercise {
  id: number
  name: string
  category: ExerciseCategory
  muscleGroups: MuscleGroup[]
  description?: string
  imageUrl?: string
  videoUrl?: string
  instructions?: string[]
  tips?: string[]
  createdAt?: string
  updatedAt?: string
}

// 动作列表查询参数
export interface ExerciseQueryParams {
  category?: ExerciseCategory
  muscleGroup?: MuscleGroup
  search?: string
  page?: number
  pageSize?: number
}

// 动作创建/更新数据
export interface ExerciseFormData {
  name: string
  category: ExerciseCategory
  muscleGroups: MuscleGroup[]
  description?: string
  imageUrl?: string
  videoUrl?: string
  instructions?: string[]
  tips?: string[]
}
