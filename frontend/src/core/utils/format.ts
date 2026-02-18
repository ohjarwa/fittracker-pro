import { format, parseISO, differenceInDays } from 'date-fns'
import { zhCN } from 'date-fns/locale'

export function formatDate(date: string | Date, pattern = 'yyyy-MM-dd'): string {
  try {
    const d = typeof date === 'string' ? parseISO(date) : date
    return format(d, pattern, { locale: zhCN })
  } catch {
    return ''
  }
}

export function formatDateTime(date: string | Date): string {
  return formatDate(date, 'yyyy-MM-dd HH:mm:ss')
}

export function formatRelativeTime(date: string | Date): string {
  try {
    const d = typeof date === 'string' ? parseISO(date) : date
    const days = differenceInDays(new Date(), d)

    if (days === 0) return '今天'
    if (days === 1) return '昨天'
    if (days < 7) return `${days}天前`
    if (days < 30) return `${Math.floor(days / 7)}周前`
    if (days < 365) return `${Math.floor(days / 30)}个月前`
    return `${Math.floor(days / 365)}年前`
  } catch {
    return ''
  }
}

export function formatNumber(num: number, decimals = 2): string {
  return num.toFixed(decimals)
}

export function formatWeight(weight: number, unit = 'kg'): string {
  return `${formatNumber(weight, 1)}${unit}`
}

export function formatVolume(volume: number): string {
  if (volume >= 1000) {
    return `${formatNumber(volume / 1000, 1)}t`
  }
  return `${formatNumber(volume, 0)}kg`
}

export function formatPercentage(value: number, decimals = 1): string {
  return `${formatNumber(value, decimals)}%`
}

export function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  if (hours > 0) {
    return `${hours}小时${minutes}分钟`
  }
  if (minutes > 0) {
    return `${minutes}分钟${secs}秒`
  }
  return `${secs}秒`
}
