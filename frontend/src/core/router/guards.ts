import type { Router } from 'vue-router'

export function setupRouterGuards(router: Router) {
  router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    const isAuthenticated = !!token

    // 需要认证但未登录
    if (to.meta.requiresAuth && !isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }

    // 已登录但访问登录页
    if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
      next('/')
      return
    }

    next()
  })
}
