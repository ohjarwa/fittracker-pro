import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthApi } from '../services/auth.api'
import type { User, LoginCredentials, RegisterData, UserUpdateData } from '../types'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => {
    return !!localStorage.getItem('token')
  })

  const userDisplayName = computed(() => {
    return user.value?.nickname || user.value?.email || '用户'
  })

  // Actions
  async function login(credentials: LoginCredentials) {
    loading.value = true
    error.value = null

    try {
      const api = useAuthApi()
      const response = await api.login(credentials)

      // 保存 tokens
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)

      // 获取用户信息
      await fetchProfile()

      return response
    } catch (err: any) {
      error.value = err.response?.data?.message || '登录失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function register(data: RegisterData) {
    loading.value = true
    error.value = null

    try {
      const api = useAuthApi()
      const response = await api.register(data)

      // 保存 tokens
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)

      // 获取用户信息
      await fetchProfile()

      return response
    } catch (err: any) {
      error.value = err.response?.data?.message || '注册失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchProfile() {
    loading.value = true
    error.value = null

    try {
      const api = useAuthApi()
      user.value = await api.getProfile()
      return user.value
    } catch (err: any) {
      error.value = err.response?.data?.message || '获取用户信息失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(data: UserUpdateData) {
    loading.value = true
    error.value = null

    try {
      const api = useAuthApi()
      user.value = await api.updateProfile(data)
      return user.value
    } catch (err: any) {
      error.value = err.response?.data?.message || '更新用户信息失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }

  return {
    // State
    user,
    loading,
    error,

    // Getters
    isAuthenticated,
    userDisplayName,

    // Actions
    login,
    register,
    fetchProfile,
    updateProfile,
    logout
  }
})
