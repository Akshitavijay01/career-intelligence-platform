import { cn } from '@/utils/cn'
import * as React from 'react'

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'default' | 'sm' | 'lg'
  className?: string
  disabled?: boolean
  asChild?: boolean
  children: React.ReactNode
}

const variants = {
  primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
  outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
  ghost: 'hover:bg-accent hover:text-accent-foreground',
}

const sizes = {
  default: 'h-10 px-4 py-2',
  sm: 'h-9 px-3 rounded-md',
  lg: 'h-11 px-8 rounded-md',
}

export function Button({
  variant = 'primary',
  size = 'default',
  className,
  disabled = false,
  asChild = false,
  children,
}: ButtonProps) {
  const Component = asChild ? React.Fragment : 'button'
  return (
    <Component
      className={cn(
        'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled}
    >
      {children}
    </Component>
  )
}