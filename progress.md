# FitTracker Pro 开发进度与核心知识

> 记录开发过程中遇到的问题、解决方案和核心知识点

---

## 2026-02-18: 注册功能修复

### 问题描述
用户注册功能无法使用，点击注册按钮后没有任何反应。

### 根本原因

#### 1. bcrypt 版本不兼容
- **现象**: 后端日志显示 `AttributeError: module 'bcrypt' has no attribute '__about__'`
- **原因**: bcrypt 5.0.0 移除了 `__about__` 属性，与 passlib 1.7.4 不兼容
- **解决方案**: 降级 bcrypt 到 4.1.2
  ```bash
  pip install 'bcrypt==4.1.2'
  ```

#### 2. 注册接口返回格式错误
- **现象**: 前端期望注册后获得 Token，但后端只返回 UserResponse
- **原因**: 后端注册接口 `response_model=UserResponse`，但前端需要 Token 进行后续认证
- **解决方案**: 修改 [backend/app/routers/auth.py:21](backend/app/routers/auth.py#L21)
  ```python
  # 修改前
  @router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)

  # 修改后
  @router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)

  # 并在函数最后返回 tokens
  return create_tokens(user.id)
  ```

### 核心知识点

1. **Python 依赖版本兼容性**
   - bcrypt 5.x 与 passlib 1.7.4 不兼容
   - 使用 bcrypt 4.x 版本可避免此问题
   - 建议在 requirements.txt 中明确版本号

2. **JWT 认证流程**
   - 注册/登录成功后应返回 access_token 和 refresh_token
   - 前端保存 Token 到 localStorage
   - 后续请求在 Header 中携带: `Authorization: Bearer <token>`

3. **前后端接口契约**
   - 确保后端返回的数据格式与前端期望一致
   - 使用 Pydantic 的 response_model 明确接口返回格式
   - 前端使用 TypeScript 类型定义确保类型安全

### 测试验证

#### 后端 API 测试
```bash
# 测试注册
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","nickname":"test","password":"password123"}'

# 预期返回
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### 相关文件
- [backend/requirements.txt](backend/requirements.txt) - Python 依赖
- [backend/app/routers/auth.py](backend/app/routers/auth.py) - 认证路由
- [frontend/src/modules/auth/stores/user.ts](frontend/src/modules/auth/stores/user.ts) - 前端认证逻辑

---

## 2026-02-18: 401 Token 刷新无限循环修复

### 问题描述
登录后页面一直 loading，浏览器控制台显示大量 401 错误，网络面板有数万个失败的 `/api/auth/refresh` 请求。

### 根本原因

**前端 Axios 拦截器的递归调用问题**

- 当任何请求返回 401 时，拦截器会尝试刷新 token
- 刷新 token 的请求使用了**同一个 axios client**（有相同的拦截器）
- 如果 refresh_token 无效，刷新请求本身也返回 401
- 401 又触发拦截器尝试刷新，导致**无限递归循环**

```typescript
// ❌ 错误代码（第32行）
const response = await client.post('/api/auth/refresh', {
  refresh_token: refreshToken
})
// client 有拦截器，如果 /refresh 返回 401，会再次触发刷新逻辑
```

### 解决方案

修改 [frontend/src/core/api/interceptors.ts:32](frontend/src/core/api/interceptors.ts#L32)

```typescript
// ✅ 正确代码 - 使用独立的 axios 实例
import axios from 'axios'

const response = await axios.post(
  `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/auth/refresh`,
  { refresh_token: refreshToken },
  { headers: { 'Content-Type': 'application/json' } }
)
```

**关键点**：使用 `axios` 而不是 `client`，这样刷新请求不会经过拦截器，避免递归。

### 核心知识点

1. **Axios 拦截器的陷阱**
   - 拦截器中的请求会再次触发拦截器
   - 避免在拦截器中使用同一个 axios 实例发请求
   - 使用独立的 axios 实例或原生 fetch

2. **Token 刷新的最佳实践**
   - 刷新 token 的请求应该绕过拦截器
   - 使用标志位（如 `_retry`）防止重复刷新
   - 刷新失败后清除 token 并跳转登录页

3. **调试技巧**
   - Network 面板查看是否有大量重复请求
   - Console 面板查看错误日志
   - 使用 `_retry` 标志位避免无限循环

### 测试验证

1. **清除浏览器缓存和 localStorage**
   ```
   浏览器开发者工具 > Application > Storage > Clear site data
   或者在控制台执行：localStorage.clear()
   ```

2. **重新登录测试**
   - 访问 http://localhost:5173/login
   - 输入账号密码登录
   - 页面应该正常跳转，不再一直 loading

3. **验证 Network 面板**
   - 应该只有一个 `/api/auth/refresh` 请求（如果需要刷新）
   - 不应该有大量 401 错误

### 相关文件
- [frontend/src/core/api/interceptors.ts](frontend/src/core/api/interceptors.ts) - Axios 拦截器
- [frontend/src/core/api/client.ts](frontend/src/core/api/client.ts) - Axios 实例

---

## 2026-02-18: 动作库和训练记录页面加载修复

### 问题描述

1. **动作库页面**显示"没有找到动作"，持续 loading 状态
2. **训练记录页面**持续 loading 状态，无法显示内容

### 根本原因

**后端和前端数据格式不匹配**

#### 动作库问题

1. **API 返回格式错误**
   - Store 调用 `getExercises()` 期望返回数组
   - 但后端实际返回分页格式：`{ total: number, items: Exercise[] }`

2. **数据字段不兼容**
   - 后端返回：`primary_muscle`, `secondary_muscles[]`, `equipment`
   - 前端期望：`muscleGroups[]`, `category` (枚举类型)

3. **组件类型过于严格**
   - ExerciseCard 组件使用 `Record<ExerciseCategory, string>`
   - 实际接收到的是字符串，导致渲染错误

#### 训练记录问题

1. **API 返回格式错误**（与动作库相同）
   - Store 调用 `getWorkouts()` 期望返回数组
   - 后端返回分页格式：`{ total: number, items: WorkoutSession[] }`

### 解决方案

#### 1. 修复动作库 Store

修改 [frontend/src/modules/exercise/stores/exercise.ts](frontend/src/modules/exercise/stores/exercise.ts)

```typescript
// 添加设备到分类的映射
const equipmentToCategory: Record<string, string> = {
  'barbell': 'barbell',
  'dumbbell': 'dumbbell',
  'machine': 'machine',
  'bodyweight': 'bodyweight',
  'cable': 'machine',
  'cardio': 'cardio'
}

// 添加肌肉群映射
const muscleGroupMapping: Record<string, string> = {
  'chest': 'chest',
  'back': 'back',
  'shoulders': 'shoulders',
  'biceps': 'biceps',
  'triceps': 'triceps',
  'legs': 'legs',
  'core': 'core',
  'glutes': 'legs',
  'hamstrings': 'legs',
  'full_body': 'full_body'
}

// 数据转换函数
function transformExercise(data: any): Exercise {
  const category = equipmentToCategory[data.equipment] || 'barbell' as any
  const muscleGroups: any[] = [
    muscleGroupMapping[data.primary_muscle] || 'chest',
    ...(data.secondary_muscles || []).map((m: string) => muscleGroupMapping[m] || 'chest')
  ]
  return {
    id: data.id,
    name: data.name,
    category,
    muscleGroups,
    description: data.description || undefined,
    createdAt: data.created_at,
    updatedAt: data.updated_at
  }
}

// 修改 fetchExercises 使用分页 API
async function fetchExercises(params?: ExerciseQueryParams) {
  loading.value = true
  error.value = null
  try {
    const api = useExerciseApi()
    const queryParams = { ...filters.value, ...params }
    const response = await api.getExercisesPaginated(queryParams)
    exercises.value = response.items.map(transformExercise)
  } catch (err: any) {
    error.value = err.response?.data?.message || '获取动作列表失败'
    throw err
  } finally {
    loading.value = false
  }
}
```

#### 2. 修复 ExerciseCard 组件

修改 [frontend/src/modules/exercise/components/ExerciseCard.vue](frontend/src/modules/exercise/components/ExerciseCard.vue)

```typescript
// 改为使用字符串作为 key
const categoryLabels: Record<string, string> = {
  'barbell': '杠铃',
  'dumbbell': '哑铃',
  'machine': '器械',
  'bodyweight': '自重',
  'cardio': '有氧'
}

const categoryColors: Record<string, string> = {
  'barbell': 'bg-purple-100 text-purple-700',
  'dumbbell': 'bg-indigo-100 text-indigo-700',
  'machine': 'bg-gray-100 text-gray-700',
  'bodyweight': 'bg-green-100 text-green-700',
  'cardio': 'bg-orange-100 text-orange-700'
}

const muscleLabels: Record<string, string> = {
  'chest': '胸部',
  'back': '背部',
  'shoulders': '肩部',
  'biceps': '肱二头肌',
  'triceps': '肱三头肌',
  'legs': '腿部',
  'core': '核心',
  'full_body': '全身'
}

const categoryLabel = computed(() => {
  const cat = String(props.exercise.category)
  return categoryLabels[cat] || props.exercise.category
})

function getMuscleLabel(muscle: string) {
  return muscleLabels[muscle] || muscle
}
```

#### 3. 修复训练记录 Store

修改 [frontend/src/modules/workout/stores/workout.ts](frontend/src/modules/workout/stores/workout.ts)

```typescript
async function fetchWorkouts(params?: WorkoutQueryParams) {
  loading.value = true
  error.value = null
  try {
    const api = useWorkoutApi()
    const queryParams = { ...filters.value, ...params }
    const response = await api.getWorkoutsPaginated(queryParams)
    workouts.value = response.items
  } catch (err: any) {
    error.value = err.response?.data?.message || '获取训练记录失败'
    throw err
  } finally {
    loading.value = false
  }
}
```

### 核心知识点

1. **分页 API 的统一处理**
   - 后端应统一使用 `{ total, items }` 格式返回分页数据
   - 前端 Store 应使用 `getXxxPaginated()` 方法而不是 `getXxx()`
   - 在 Store 中访问 `response.items` 获取数据数组

2. **数据转换层的重要性**
   - 后端和前端的数据格式可能不同
   - 在 Store 层添加 `transformXxx()` 函数转换数据
   - 使用映射表（Record）处理字段名称和枚举值的差异

3. **组件类型设计的灵活性**
   - 避免使用严格的枚举类型作为 Record 的 key
   - 使用 `string` 类型作为 key 可以兼容枚举和字符串
   - 使用 `String()` 转换确保类型安全

4. **Vue 渲染错误的调试**
   - Console 面板查看 Vue 的渲染错误
   - 使用 `<Loading>` 组件的 `loading` 属性排查状态
   - 检查 Store 中的数据是否正确获取

### 测试验证

1. **动作库页面**
   - 访问 http://localhost:5173/exercises
   - 应该能看到 20 个默认动作
   - 搜索和筛选功能正常工作

2. **训练记录页面**
   - 访问 http://localhost:5173/workouts
   - 应该显示"还没有训练记录"的空状态
   - 不再持续 loading

3. **其他页面**
   - 仪表盘页面正常加载
   - 数据分析页面正常加载

### 相关文件
- [frontend/src/modules/exercise/stores/exercise.ts](frontend/src/modules/exercise/stores/exercise.ts) - 动作库 Store
- [frontend/src/modules/exercise/components/ExerciseCard.vue](frontend/src/modules/exercise/components/ExerciseCard.vue) - 动作卡片组件
- [frontend/src/modules/workout/stores/workout.ts](frontend/src/modules/workout/stores/workout.ts) - 训练记录 Store
- [frontend/src/modules/exercise/services/exercise.api.ts](frontend/src/modules/exercise/services/exercise.api.ts) - 动作库 API
- [frontend/src/modules/workout/services/workout.api.ts](frontend/src/modules/workout/services/workout.api.ts) - 训练记录 API

---

## Chrome DevTools MCP 卡顿问题 ✅ 已解决

### 问题描述
使用 Chrome DevTools MCP 工具时经常超时或卡住。

### 根本原因
- **主要问题**: 页面存在 401 刷新循环，导致数万个网络请求
- **次要原因**: Chrome DevTools MCP 处理大量数据时响应慢

### 解决方案

**根本解决**: 修复 401 刷新循环（见上一章节）

**临时方案**（如果仍然卡顿）:
1. 清理页面状态并刷新
2. 使用替代测试方法（curl、Postman）
3. 重启 Chrome 远程调试模式

### 最佳实践
- 修复所有导致大量网络请求的 bug
- 优先使用 API 测试验证后端功能
- 只在页面状态正常时使用浏览器自动化

---

## 待解决问题

无！所有已知问题已解决 🎉

---

## 2026-02-18: 训练模板页面路由修复

### 问题描述
访问 `/templates` 路由时显示的是训练记录页面的内容，而不是训练模板页面。

### 根本原因

1. **缺少模板页面组件**
   - workout 模块只有 `WorkoutList.vue` 组件
   - 路由配置中 `/templates` 指向了 `WorkoutList.vue`（作为占位符）

2. **前后端 API 不匹配**
   - 前端定义了完整的模板 CRUD API (`/api/workouts/templates`)
   - 后端只实现了 `/api/workouts/templates/list` 用于统计已使用过的模板名称

### 解决方案

#### 1. 创建模板列表页面

创建新文件 [frontend/src/modules/workout/views/TemplateList.vue](frontend/src/modules/workout/views/TemplateList.vue)

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/core/composables/useApi'

interface Template {
  name: string
  usage_count: number
}

const templates = ref<Template[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function fetchTemplates() {
  loading.value = true
  error.value = null
  try {
    const { get } = useApi()
    const response = await get<{ templates: Template[] }>('/api/workouts/templates/list')
    templates.value = response.templates
  } catch (err: any) {
    error.value = err.response?.data?.message || '获取训练模板失败'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTemplates()
})
</script>

<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">训练模板</h1>
        <p class="text-gray-600 mt-1">管理你的训练模板</p>
      </div>
      <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        新建模板
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <p class="text-gray-600 mt-2">加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-600">{{ error }}</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="templates.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">还没有训练模板</h3>
      <p class="mt-1 text-sm text-gray-500">创建训练时保存为模板，或者从历史训练中创建模板</p>
    </div>

    <!-- 模板列表 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="template in templates"
        :key="template.name"
        class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
      >
        <h3 class="text-lg font-semibold text-gray-900">{{ template.name }}</h3>
        <div class="mt-3 text-sm text-gray-500">
          已使用 {{ template.usage_count }} 次
        </div>
        <div class="mt-4 flex gap-2">
          <button class="flex-1 px-3 py-1.5 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            使用模板
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
```

#### 2. 更新路由配置

修改 [frontend/src/modules/workout/router.ts](frontend/src/modules/workout/router.ts:32)

```typescript
// 修改前
{
  path: '/templates',
  name: 'Templates',
  component: () => import('./views/WorkoutList.vue'), // 占位符，后续实现
  meta: { requiresAuth: true, title: '训练模板' }
}

// 修改后
{
  path: '/templates',
  name: 'Templates',
  component: () => import('./views/TemplateList.vue'),
  meta: { requiresAuth: true, title: '训练模板' }
}
```

### 核心知识点

1. **路由占位符的最佳实践**
   - 开发初期可以使用占位符组件，但应该显示明确的"待开发"状态
   - 避免让多个路由指向同一个功能组件，容易造成混淆
   - 完成功能后及时更新路由配置

2. **前后端 API 契约一致性**
   - 前端定义的 API 应该与后端实现保持一致
   - 如果后端只实现了部分功能，前端应该相应调整
   - 使用 TypeScript 类型定义确保接口契约清晰

3. **渐进式功能实现**
   - 当前后端只实现了基于 `template_name` 的简单统计
   - 前端页面已创建好，后续可以扩展为完整的模板管理系统
   - 空状态提示应该引导用户如何创建模板

### 测试验证

访问 http://localhost:5173/templates
- 应该显示"训练模板"标题
- 显示空状态提示"还没有训练模板"
- 不再显示训练记录的内容

### 相关文件
- [frontend/src/modules/workout/views/TemplateList.vue](frontend/src/modules/workout/views/TemplateList.vue) - 新建的模板列表页面
- [frontend/src/modules/workout/router.ts](frontend/src/modules/workout/router.ts) - 更新的路由配置
- [backend/app/routers/workouts.py](backend/app/routers/workouts.py:400) - 后端模板统计接口

---

## 开发环境配置

### 数据库查看方法

#### 方法 1: 命令行
```bash
cd backend
sqlite3 fittracker.db
.tables
SELECT * FROM users;
```

#### 方法 2: 图形化工具
- **DB Browser for SQLite**: https://sqlitebrowser.org/
- **TablePlus**: https://tableplus.com/
- 打开 [backend/fittracker.db](backend/fittracker.db) 文件即可

### 启动服务

#### 后端
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

#### 前端
```bash
cd frontend
npm run dev
```

### 访问地址
- 前端: http://localhost:5173
- 后端 API 文档: http://localhost:8000/docs
- 后端健康检查: http://localhost:8000/health

---

## 技术栈速查

### 后端
- FastAPI - Web 框架
- SQLAlchemy 2.0 - ORM（异步）
- SQLite - 数据库（开发环境）
- Pydantic v2 - 数据验证
- python-jose - JWT 认证
- passlib + bcrypt - 密码加密

### 前端
- Vue 3 - 前端框架
- TypeScript - 类型安全
- Vite - 构建工具
- Pinia - 状态管理
- Vue Router - 路由
- Axios - HTTP 客户端
- Tailwind CSS - 样式

---

## 最佳实践

### 1. 依赖版本管理
- 使用 `pip freeze > requirements.txt` 固定版本
- 定期更新依赖但要注意兼容性
- 使用虚拟环境隔离项目依赖

### 2. 前后端联调
- 使用 FastAPI 的 `/docs` 接口测试后端功能
- 浏览器开发者工具查看网络请求和错误
- 确保 CORS 配置正确

### 3. 数据库操作
- 使用 Alembic 管理数据库迁移
- 开发环境使用 SQLite，生产环境切换到 PostgreSQL
- 定期备份数据库文件

---

*最后更新: 2026-02-18*
