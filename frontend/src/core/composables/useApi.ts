import client from '@/core/api/client'
import type { AxiosRequestConfig } from 'axios'

export function useApi() {
  async function get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return client.get(url, config)
  }

  async function post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return client.post(url, data, config)
  }

  async function put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return client.put(url, data, config)
  }

  async function patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return client.patch(url, data, config)
  }

  async function del<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return client.delete(url, config)
  }

  return {
    get,
    post,
    put,
    patch,
    del
  }
}
