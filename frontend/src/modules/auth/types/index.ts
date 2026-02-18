// 用户信息
export interface User {
  id: number
  email: string
  nickname?: string
  bodyWeight?: number
  height?: number
  trainingAge?: number
  unitPreference?: 'kg' | 'lb'
  createdAt?: string
  updatedAt?: string
}

// 登录凭证
export interface LoginCredentials {
  email: string
  password: string
}

// 注册数据
export interface RegisterData extends LoginCredentials {
  nickname?: string
}

// 认证响应
export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

// 用户更新数据
export interface UserUpdateData {
  nickname?: string
  bodyWeight?: number
  height?: number
  trainingAge?: number
  unitPreference?: 'kg' | 'lb'
}

// 修改密码数据
export interface ChangePasswordData {
  old_password: string
  new_password: string
}
