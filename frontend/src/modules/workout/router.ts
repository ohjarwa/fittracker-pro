import type { RouteRecordRaw } from 'vue-router'

export const workoutRoutes: RouteRecordRaw[] = [
  {
    path: '/workouts',
    name: 'Workouts',
    component: () => import('./views/WorkoutList.vue'),
    meta: {
      requiresAuth: true,
      title: '训练记录'
    }
  },
  {
    path: '/workouts/create',
    name: 'WorkoutCreate',
    component: () => import('./views/WorkoutList.vue'), // 占位符，后续实现
    meta: {
      requiresAuth: true,
      title: '创建训练'
    }
  },
  {
    path: '/workouts/:id',
    name: 'WorkoutDetail',
    component: () => import('./views/WorkoutList.vue'), // 占位符，后续实现
    meta: {
      requiresAuth: true,
      title: '训练详情'
    }
  },
  {
    path: '/templates',
    name: 'Templates',
    component: () => import('./views/TemplateList.vue'),
    meta: {
      requiresAuth: true,
      title: '训练模板'
    }
  }
]
