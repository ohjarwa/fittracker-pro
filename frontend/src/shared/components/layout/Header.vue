<template>
  <header class="bg-white border-b border-gray-200 px-6 py-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <h1 class="text-xl font-bold text-primary-600">FitTracker Pro</h1>
      </div>

      <div class="flex items-center space-x-4">
        <!-- 用户菜单 -->
        <div class="relative" ref="menuRef">
          <button
            @click="showMenu = !showMenu"
            class="flex items-center space-x-2 text-gray-700 hover:text-gray-900 focus:outline-none"
          >
            <div
              class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center"
            >
              <span class="text-sm font-medium text-primary-600">
                {{ userInitials }}
              </span>
            </div>
            <span class="text-sm font-medium">{{ authStore.user?.nickname || '用户' }}</span>
          </button>

          <!-- 下拉菜单 -->
          <div
            v-if="showMenu"
            class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-50"
          >
            <router-link
              to="/profile"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              @click="showMenu = false"
            >
              个人中心
            </router-link>
            <router-link
              to="/settings"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              @click="showMenu = false"
            >
              设置
            </router-link>
            <hr class="my-1" />
            <button
              @click="handleLogout"
              class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/core/stores/auth'
import { useAuth } from '@/core/composables/useAuth'

const authStore = useAuthStore()
const { logout } = useAuth()

const showMenu = ref(false)
const menuRef = ref<HTMLElement | null>(null)

const userInitials = computed(() => {
  const nickname = authStore.user?.nickname
  if (nickname) {
    return nickname.substring(0, 2).toUpperCase()
  }
  return 'U'
})

async function handleLogout() {
  showMenu.value = false
  await logout()
}

// 点击外部关闭菜单
function handleClickOutside(event: MouseEvent) {
  if (menuRef.value && !menuRef.value.contains(event.target as Node)) {
    showMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
