import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './core/router'
import { setupRouterGuards } from './core/router/guards'
import App from './App.vue'
import './assets/styles/main.css'

// 导入 API 拦截器
import './core/api/interceptors'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 设置路由守卫
setupRouterGuards(router)

app.mount('#app')

