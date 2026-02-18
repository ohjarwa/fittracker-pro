import { useApi } from '@/core/composables/useApi'
import type {
  OneRMData,
  VolumeStats,
  MuscleBalance,
  ProgressData,
  AnalysisQueryParams,
  DashboardStats
} from '../types'

export const useAnalysisApi = () => {
  const { get } = useApi()

  return {
    // 获取仪表盘统计
    getDashboardStats: (params?: AnalysisQueryParams) =>
      get<DashboardStats>('/api/analysis/dashboard', { params }),

    // 获取 1RM 数据
    getOneRMData: (params?: AnalysisQueryParams) =>
      get<OneRMData[]>('/api/analysis/1rm', { params }),

    // 获取训练量统计
    getVolumeStats: (params?: AnalysisQueryParams) =>
      get<VolumeStats[]>('/api/analysis/volume', { params }),

    // 获取肌肉平衡分析
    getMuscleBalance: (params?: AnalysisQueryParams) =>
      get<MuscleBalance[]>('/api/analysis/muscle-balance', { params }),

    // 获取进度数据
    getProgressData: (exerciseId: number, params?: AnalysisQueryParams) =>
      get<ProgressData[]>(`/api/analysis/progress/${exerciseId}`, { params })
  }
}
