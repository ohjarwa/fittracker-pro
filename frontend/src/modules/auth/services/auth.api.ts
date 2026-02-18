import { useApi } from '@/core/composables/useApi'
import type {
  User,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  UserUpdateData,
  ChangePasswordData
} from '../types'

export const useAuthApi = () => {
  const { get, post, put } = useApi()

  return {
    // 登录
    login: (credentials: LoginCredentials) =>
      post<AuthResponse>('/api/auth/login', credentials),

    // 注册
    register: (data: RegisterData) =>
      post<AuthResponse>('/api/auth/register', data),

    // 刷新 Token
    refreshToken: (refreshToken: string) =>
      post<AuthResponse>('/api/auth/refresh', { refresh_token: refreshToken }),

    // 获取当前用户信息
    getProfile: () =>
      get<User>('/api/auth/me'),

    // 更新用户信息
    updateProfile: (data: UserUpdateData) =>
      put<User>('/api/auth/me', data),

    // 修改密码
    changePassword: (data: ChangePasswordData) =>
      post<void>('/api/auth/change-password', data),

    // 登出
    logout: () =>
      post<void>('/api/auth/logout')
  }
}
