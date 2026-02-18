<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900">个人中心</h1>
    <p class="mt-1 text-sm text-gray-500">管理你的个人信息</p>

    <div class="mt-6">
      <Card title="个人信息">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">邮箱</label>
            <p class="mt-1 text-gray-900">{{ user?.email }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">昵称</label>
            <p class="mt-1 text-gray-900">{{ user?.nickname || '未设置' }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">训练年限</label>
            <p class="mt-1 text-gray-900">{{ user?.trainingAge || 0 }} 年</p>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { storeToRefs } from 'pinia'
import Card from '@/shared/components/ui/Card.vue'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

onMounted(() => {
  if (!user.value) {
    userStore.fetchProfile()
  }
})
</script>
