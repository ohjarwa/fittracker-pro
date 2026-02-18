import type { RouteRecordRaw } from 'vue-router'

export const exerciseRoutes: RouteRecordRaw[] = [
  {
    path: '/exercises',
    name: 'Exercises',
    component: () => import('./views/ExerciseList.vue'),
    meta: {
      requiresAuth: true,
      title: '动作库'
    }
  },
  {
    path: '/exercises/:id',
    name: 'ExerciseDetail',
    component: () => import('./views/ExerciseDetail.vue'),
    meta: {
      requiresAuth: true,
      title: '动作详情'
    }
  }
]
