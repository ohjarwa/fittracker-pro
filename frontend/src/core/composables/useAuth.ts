import { useAuthStore } from '@/core/stores/auth'
import { useRouter } from 'vue-router'
import { useNotification } from './useNotification'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()
  const notification = useNotification()

  async function login(email: string, password: string) {
    try {
      // 这里会在 auth 模块中实现具体的 API 调用
      // const response = await authApi.login({ email, password })
      // authStore.setTokens(response.access_token, response.refresh_token)
      notification.success('登录成功')
      await router.push('/')
    } catch (error: any) {
      notification.error(error.response?.data?.message || '登录失败')
      throw error
    }
  }

  async function logout() {
    authStore.logout()
    await router.push('/login')
    notification.success('已退出登录')
  }

  return {
    login,
    logout,
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.user
  }
}
