import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAnalysisApi } from '../services/analysis.api'
import type {
  OneRMData,
  VolumeStats,
  MuscleBalance,
  DashboardStats,
  AnalysisQueryParams
} from '../types'

export const useAnalysisStore = defineStore('analysis', () => {
  // State
  const dashboardStats = ref<DashboardStats | null>(null)
  const oneRMData = ref<OneRMData[]>([])
  const volumeStats = ref<VolumeStats[]>([])
  const muscleBalance = ref<MuscleBalance[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 时间范围
  const dateRange = ref<AnalysisQueryParams>({
    startDate: undefined,
    endDate: undefined
  })

  // Actions
  async function fetchDashboardStats(params?: AnalysisQueryParams) {
    loading.value = true
    error.value = null

    try {
      const api = useAnalysisApi()
      const queryParams = { ...dateRange.value, ...params }
      dashboardStats.value = await api.getDashboardStats(queryParams)
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取统计数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchOneRMData(params?: AnalysisQueryParams) {
    loading.value = true
    error.value = null

    try {
      const api = useAnalysisApi()
      const queryParams = { ...dateRange.value, ...params }
      oneRMData.value = await api.getOneRMData(queryParams)
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取1RM数据失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchVolumeStats(params?: AnalysisQueryParams) {
    loading.value = true
    error.value = null

    try {
      const api = useAnalysisApi()
      const queryParams = { ...dateRange.value, ...params }
      volumeStats.value = await api.getVolumeStats(queryParams)
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取训练量统计失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchMuscleBalance(params?: AnalysisQueryParams) {
    loading.value = true
    error.value = null

    try {
      const api = useAnalysisApi()
      const queryParams = { ...dateRange.value, ...params }
      muscleBalance.value = await api.getMuscleBalance(queryParams)
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取肌肉平衡分析失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setDateRange(range: Partial<AnalysisQueryParams>) {
    dateRange.value = { ...dateRange.value, ...range }
  }

  function clearDateRange() {
    dateRange.value = {
      startDate: undefined,
      endDate: undefined
    }
  }

  return {
    // State
    dashboardStats,
    oneRMData,
    volumeStats,
    muscleBalance,
    loading,
    error,
    dateRange,

    // Actions
    fetchDashboardStats,
    fetchOneRMData,
    fetchVolumeStats,
    fetchMuscleBalance,
    setDateRange,
    clearDateRange
  }
})
