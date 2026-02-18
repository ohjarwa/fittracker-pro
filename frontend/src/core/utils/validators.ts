import { z } from 'zod'

// 通用验证规则
export const validators = {
  email: z.string().email('请输入有效的邮箱地址'),

  password: z
    .string()
    .min(8, '密码至少8个字符')
    .regex(/[A-Z]/, '密码必须包含大写字母')
    .regex(/[a-z]/, '密码必须包含小写字母')
    .regex(/[0-9]/, '密码必须包含数字'),

  required: (fieldName: string) => z.string().min(1, `${fieldName}不能为空`),

  positiveNumber: (fieldName: string) =>
    z.number().positive(`${fieldName}必须是正数`),

  weight: z.number().min(0, '重量不能为负数').max(1000, '重量超出范围'),

  reps: z.number().int('次数必须是整数').min(1, '次数至少为1').max(100, '次数超出范围'),

  rpe: z.number().min(1, 'RPE至少为1').max(10, 'RPE最大为10').optional()
}

// 验证函数
export function validate<T>(schema: z.ZodSchema<T>, data: unknown): T {
  return schema.parse(data)
}

export function safeValidate<T>(
  schema: z.ZodSchema<T>,
  data: unknown
): { success: true; data: T } | { success: false; errors: string[] } {
  try {
    const result = schema.parse(data)
    return { success: true, data: result }
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors = error.errors.map(e => e.message)
      return { success: false, errors }
    }
    return { success: false, errors: ['验证失败'] }
  }
}

// 表单验证辅助函数
export function getFieldError(
  errors: Record<string, string[]>,
  field: string
): string | undefined {
  return errors[field]?.[0]
}
