import { lazy, Suspense } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'sonner'
import { LoadingSpinner } from './components/common/LoadingSpinner'

// Layouts — small, load eagerly
import AuthLayout from './layouts/AuthLayout'
import AppLayout from './layouts/AppLayout'
import AdminLayout from './layouts/AdminLayout'

// Pages — lazy loaded (each becomes its own chunk)
const LoginPage = lazy(() => import('./pages/auth/LoginPage'))
const RegisterPage = lazy(() => import('./pages/auth/RegisterPage'))
const DashboardPage = lazy(() => import('./pages/student/DashboardPage'))
const ProfilePage = lazy(() => import('./pages/student/ProfilePage'))
const ResumePage = lazy(() => import('./pages/student/ResumePage'))
const OpportunitiesPage = lazy(() => import('./pages/student/OpportunitiesPage'))
const RecommendationsPage = lazy(() => import('./pages/student/RecommendationsPage'))
const SkillGapPage = lazy(() => import('./pages/student/SkillGapPage'))
const RoadmapPage = lazy(() => import('./pages/student/RoadmapPage'))
const ApplicationsPage = lazy(() => import('./pages/student/ApplicationsPage'))
const InterviewPage = lazy(() => import('./pages/student/InterviewPage'))
const InterviewSessionPage = lazy(() => import('./pages/student/InterviewSessionPage'))
const SettingsPage = lazy(() => import('./pages/student/SettingsPage'))
const AdminDashboardPage = lazy(() => import('./pages/admin/AdminDashboardPage'))
const AdminUsersPage = lazy(() => import('./pages/admin/AdminUsersPage'))
const AdminOpportunitiesPage = lazy(() => import('./pages/admin/AdminOpportunitiesPage'))
const AdminAnalyticsPage = lazy(() => import('./pages/admin/AdminAnalyticsPage'))

function App() {
  return (
    <>
      <Router>
        <Suspense fallback={<LoadingSpinner message="Loading..." />}>
          <Routes>
            <Route element={<AuthLayout />}>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
            </Route>
            <Route element={<AppLayout />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/resume" element={<ResumePage />} />
              <Route path="/opportunities" element={<OpportunitiesPage />} />
              <Route path="/recommendations" element={<RecommendationsPage />} />
              <Route path="/skill-gap" element={<SkillGapPage />} />
              <Route path="/roadmap" element={<RoadmapPage />} />
              <Route path="/applications" element={<ApplicationsPage />} />
              <Route path="/interview" element={<InterviewPage />} />
              <Route path="/interview/:sessionId" element={<InterviewSessionPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
            <Route element={<AdminLayout />}>
              <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
              <Route path="/admin/dashboard" element={<AdminDashboardPage />} />
              <Route path="/admin/users" element={<AdminUsersPage />} />
              <Route path="/admin/opportunities" element={<AdminOpportunitiesPage />} />
              <Route path="/admin/analytics" element={<AdminAnalyticsPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </Router>
      <Toaster richColors position="top-right" />
    </>
  )
}

export default App
