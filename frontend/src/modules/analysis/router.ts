import type { RouteRecordRaw } from 'vue-router'

export const analysisRoutes: RouteRecordRaw[] = [
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('./views/Dashboard.vue'),
    meta: {
      requiresAuth: true,
      title: '数据分析'
    }
  },
  {
    path: '/analysis/1rm',
    name: 'OneRMAnalysis',
    component: () => import('./views/Dashboard.vue'), // 占位符
    meta: {
      requiresAuth: true,
      title: '1RM 分析'
    }
  },
  {
    path: '/analysis/volume',
    name: 'VolumeStats',
    component: () => import('./views/Dashboard.vue'), // 占位符
    meta: {
      requiresAuth: true,
      title: '训练量统计'
    }
  },
  {
    path: '/analysis/progress',
    name: 'Progress',
    component: () => import('./views/Dashboard.vue'), // 占位符
    meta: {
      requiresAuth: true,
      title: '进度追踪'
    }
  }
]
