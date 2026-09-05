interface LoadingSpinnerProps {
  message?: string
  size?: 'sm' | 'md' | 'lg'
}

export function LoadingSpinner({ message = 'Loading...', size = 'md' }: LoadingSpinnerProps) {
  const sizes = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }

  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className={`${sizes[size]} border-4 border-blue-600 border-t-transparent rounded-full animate-spin`} />
      <p className="mt-4 text-gray-500 font-medium text-sm">{message}</p>
    </div>
  )
}
