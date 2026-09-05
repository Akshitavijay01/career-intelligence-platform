import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Users,
  Briefcase,
  BarChart3,
} from 'lucide-react'
import { adminApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts'

interface AdminStats {
  total_users: number
  active_users: number
  total_opportunities: number
  active_opportunities: number
  total_applications: number
  total_interviews: number
  most_requested_skills: Array<{ skill_name: string; count: number }>
  popular_job_roles: Array<{ role: string; count: number }>
  application_success_rate: number
  average_career_readiness: number
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await adminApi.getDashboardStats()
      setStats(response.data)
    } catch (err: any) {
      console.error('Error fetching admin dashboard data:', err)
      setError('Unable to load dashboard data right now.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <LoadingSpinner message="Loading admin dashboard..." />
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchDashboardData} />;
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-1">Platform overview and management</p>
        </div>
        <div className="flex gap-3">
          <Link to="/admin/users">
            <button className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-medium hover:bg-red-100">
              <Users className="w-4 h-4" />
              Manage Users
            </button>
          </Link>
          <Link to="/admin/opportunities">
            <button className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-medium hover:bg-red-100">
              <Briefcase className="w-4 h-4" />
              Manage Opportunities
            </button>
          </Link>
          <Link to="/admin/analytics">
            <button className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-medium hover:bg-red-100">
              <BarChart3 className="w-4 h-4" />
              View Analytics
            </button>
          </Link>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Users</CardTitle>
            <CardDescription>Registered users on the platform</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">{stats?.total_users}</div>
            <div className="text-sm text-gray-500">
              {stats?.active_users} active
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Opportunities</CardTitle>
            <CardDescription>Job and internship listings</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">{stats?.total_opportunities}</div>
            <div className="text-sm text-gray-500">
              {stats?.active_opportunities} active
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Applications</CardTitle>
            <CardDescription>Total applications submitted</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">{stats?.total_applications}</div>
            <div className="text-sm text-gray-500">
              {stats?.application_success_rate}% success rate
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Interviews</CardTitle>
            <CardDescription>Conducted interviews</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">{stats?.total_interviews}</div>
            <div className="text-sm text-gray-500">
              {stats?.average_career_readiness}% avg readiness
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Most Requested Skills</CardTitle>
            <CardDescription>Top skills demanded by employers</CardDescription>
          </CardHeader>
          <CardContent>
            {stats?.most_requested_skills && stats.most_requested_skills.length > 0 ? (
              <BarChart
                width={600}
                height={300}
                data={stats.most_requested_skills.slice(0, 5)}
                margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
              >
                <defs>
                  <linearGradient id="colorSkill1" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stopColor="#0088FE" />
                    <stop offset="1" stopColor="#00C49F" />
                  </linearGradient>
                  <linearGradient id="colorSkill2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0" stopColor="#FFBB28" />
                    <stop offset="1" stopColor="#FF8042" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="skill_name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend verticalAlign="top" height={36} />
                <Bar dataKey="count" fill="url(#colorSkill1)" barSize={20} radius={[4, 4, 0, 0]} />
              </BarChart>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500">No skill data available</p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Popular Job Roles</CardTitle>
            <CardDescription>Most common positions posted</CardDescription>
          </CardHeader>
          <CardContent>
            {stats?.popular_job_roles && stats.popular_job_roles.length > 0 ? (
              <PieChart
                width={600}
                height={300}
                data={stats.popular_job_roles}
                margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
              >
                <defs>
                  {stats.popular_job_roles.map((_, i) => (
                    <linearGradient
                      key={`grad${i}`}
                      id={`colorRole${i}`}
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="0" stopColor={COLORS[i % COLORS.length]} />
                      <stop offset="1" stopColor={COLORS[(i + 1) % COLORS.length]} />
                    </linearGradient>
                  ))}
                </defs>
                <Tooltip />
                <Legend verticalAlign="top" height={36} />
                <Pie
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={120}
                  dataKey="count"
                  labelLine={{}}
                  label={({ role, count }) => `${role}: ${count}`}
                >
                  {stats.popular_job_roles.map((_, i) => (
                    <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500">No job role data available</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}