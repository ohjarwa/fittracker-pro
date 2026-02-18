<template>
  <div :class="cardClasses">
    <div v-if="title || $slots.header" class="px-6 py-4 border-b border-gray-200">
      <slot name="header">
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
      </slot>
    </div>
    <div :class="bodyClasses">
      <slot />
    </div>
    <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-200 bg-gray-50">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  padding?: boolean
  shadow?: boolean
  hover?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  padding: true,
  shadow: true,
  hover: false
})

const cardClasses = computed(() => {
  const base = 'bg-white rounded-lg overflow-hidden'
  const shadowClass = props.shadow ? 'shadow' : ''
  const hoverClass = props.hover ? 'transition-shadow hover:shadow-lg' : ''

  return [base, shadowClass, hoverClass]
})

const bodyClasses = computed(() => {
  return props.padding ? 'p-6' : ''
})
</script>
