import { cn } from '@/utils/cn'

interface CardProps {
  className?: string
  children: React.ReactNode
}

export function Card({ className, children }: CardProps) {
  return (
    <div className={cn('bg-white rounded-xl border border-gray-200 shadow-sm', className)}>
      {children}
    </div>
  )
}

interface CardHeaderProps {
  className?: string
  title?: React.ReactNode
  description?: React.ReactNode
  children?: React.ReactNode
}

export function CardHeader({ className, title, description, children }: CardHeaderProps) {
  return (
    <div className={cn('p-6 pb-4', className)}>
      {children}
      {title && <CardTitle>{title}</CardTitle>}
      {description && <CardDescription>{description}</CardDescription>}
    </div>
  )
}

export function CardTitle({ className, children }: { className?: string; children: React.ReactNode }) {
  return <h3 className={cn('text-lg font-semibold text-gray-900', className)}>{children}</h3>
}

export function CardDescription({ className, children }: { className?: string; children: React.ReactNode }) {
  return <p className={cn('text-sm text-gray-500 mt-1', className)}>{children}</p>
}

interface CardContentProps {
  className?: string
  children: React.ReactNode
}

export function CardContent({ className, children }: CardContentProps) {
  return <div className={cn('p-6 pt-4', className)}>{children}</div>
}

interface CardFooterProps {
  className?: string
  children: React.ReactNode
}

export function CardFooter({ className, children }: CardFooterProps) {
  return <div className={cn('p-6 pt-4 border-t border-gray-100', className)}>{children}</div>
}