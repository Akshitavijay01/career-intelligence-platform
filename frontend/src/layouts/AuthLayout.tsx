import { Outlet } from 'react-router-dom'

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Career Intelligence
          </h1>
          <p className="text-gray-600">AI-Powered Internship & Career Platform</p>
        </div>
        <div className="bg-white rounded-xl shadow-lg p-8">
          <Outlet />
        </div>
        <p className="text-center mt-6 text-sm text-gray-500">
          Your journey to the perfect career starts here
        </p>
      </div>
    </div>
  )
}