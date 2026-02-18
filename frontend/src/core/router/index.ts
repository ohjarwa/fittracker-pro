import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { exerciseRoutes } from '@/modules/exercise/router'
import { workoutRoutes } from '@/modules/workout/router'
import { authRoutes } from '@/modules/auth/router'
import { analysisRoutes } from '@/modules/analysis/router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/modules/auth/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/modules/auth/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/shared/components/layout/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/modules/analysis/views/Dashboard.vue')
      },
      // 添加 Auth 模块路由
      ...authRoutes,
      // 添加 Exercise 模块路由
      ...exerciseRoutes,
      // 添加 Workout 模块路由
      ...workoutRoutes,
      // 添加 Analysis 模块路由
      ...analysisRoutes
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
