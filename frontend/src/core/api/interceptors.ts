import client from './client'
import axios from 'axios'

// 请求拦截器 - 自动注入 Token
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 统一错误处理
client.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  async (error) => {
    const originalRequest = error.config

    // Token 过期，尝试刷新
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (refreshToken) {
          // 使用独立的 axios 实例刷新 token，避免循环调用拦截器
          const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/auth/refresh`,
            { refresh_token: refreshToken },
            { headers: { 'Content-Type': 'application/json' } }
          )

          const { access_token, refresh_token } = response.data
          localStorage.setItem('token', access_token)
          localStorage.setItem('refreshToken', refresh_token)

          // 重试原始请求
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return client(originalRequest)
        }
      } catch (refreshError) {
        // 刷新失败，清除登录状态
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    // 其他错误直接抛出
    return Promise.reject(error)
  }
)

export { client }
