import { ref } from 'vue'

interface Notification {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
}

const notifications = ref<Notification[]>([])
let idCounter = 0

export function useNotification() {
  function show(type: Notification['type'], message: string, duration = 3000) {
    const id = idCounter++
    notifications.value.push({ id, type, message })

    setTimeout(() => {
      const index = notifications.value.findIndex(n => n.id === id)
      if (index !== -1) {
        notifications.value.splice(index, 1)
      }
    }, duration)
  }

  return {
    notifications,
    success: (message: string) => show('success', message),
    error: (message: string) => show('error', message),
    warning: (message: string) => show('warning', message),
    info: (message: string) => show('info', message)
  }
}
