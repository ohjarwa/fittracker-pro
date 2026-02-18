// 1RM 数据
export interface OneRMData {
  exerciseId: number
  exerciseName: string
  estimated1RM: number
  date: string
  formula?: string
}

// 训练量统计
export interface VolumeStats {
  date: string
  totalVolume: number
  muscleGroup?: string
  exerciseCount: number
  setCount: number
}

// 肌肉平衡分析
export interface MuscleBalance {
  muscleGroup: string
  totalVolume: number
  percentage: number
  exerciseCount: number
}

// 进度数据
export interface ProgressData {
  date: string
  value: number
  exerciseId?: number
  exerciseName?: string
}

// 分析查询参数
export interface AnalysisQueryParams {
  startDate?: string
  endDate?: string
  exerciseId?: number
  muscleGroup?: string
}

// 仪表盘统计数据
export interface DashboardStats {
  totalWorkouts: number
  totalVolume: number
  totalSets: number
  averageRPE: number
  mostFrequentExercise: string
  currentStreak: number
}
