import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'sonner'
import AuthLayout from './layouts/AuthLayout'
import AppLayout from './layouts/AppLayout'
import AdminLayout from './layouts/AdminLayout'

import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'

import DashboardPage from './pages/student/DashboardPage'
import ProfilePage from './pages/student/ProfilePage'
import ResumePage from './pages/student/ResumePage'
import OpportunitiesPage from './pages/student/OpportunitiesPage'
import RecommendationsPage from './pages/student/RecommendationsPage'
import SkillGapPage from './pages/student/SkillGapPage'
import RoadmapPage from './pages/student/RoadmapPage'
import ApplicationsPage from './pages/student/ApplicationsPage'
import InterviewPage from './pages/student/InterviewPage'
import InterviewSessionPage from './pages/student/InterviewSessionPage'
import SettingsPage from './pages/student/SettingsPage'

import AdminDashboardPage from './pages/admin/AdminDashboardPage'
import AdminUsersPage from './pages/admin/AdminUsersPage'
import AdminOpportunitiesPage from './pages/admin/AdminOpportunitiesPage'
import AdminAnalyticsPage from './pages/admin/AdminAnalyticsPage'

function App() {
  return (
    <>
      <Router>
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
      </Router>
      <Toaster richColors position="top-right" />
    </>
  )
}

export default App
