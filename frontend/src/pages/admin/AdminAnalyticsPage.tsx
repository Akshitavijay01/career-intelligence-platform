import { useEffect, useState } from 'react'
import {
  Users,
  CheckCircle,
  ArrowUpRight,
  TrendingUp
} from 'lucide-react'
import { adminApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import {
  BarChart,
  PieChart,
  Pie,
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  Line,
  Bar
} from 'recharts'

interface AnalyticsData {
  total_users: number
  application_status_distribution: Record<string, number>
  total_interviews: number
  success_rate: number
  application_success_rate: number
  average_career_readiness: number
  most_requested_skills: { skill_name: string; count: number }[]
  popular_job_roles: { role: string; count: number }[]
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#8dd1e1', '#a4de6c', '#d0ed57', '#ffc658']

export default function AdminAnalyticsPage() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d' | 'all'>('30d')
  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await adminApi.getAnalytics()
      setAnalytics(response.data)
    } catch (err: any) {
      console.error('Error fetching analytics:', err)
      setError('Unable to load analytics data.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <LoadingSpinner message="Loading analytics..." />
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchAnalytics} />
  }

  // Transform data for charts
  const skillsData = (analytics?.most_requested_skills || []).map(skill => ({
    name: skill.skill_name,
    count: skill.count
  }))

  const rolesData = (analytics?.popular_job_roles || []).map(role => ({
    name: role.role,
    count: role.count
  }))

  const applicationData = Object.entries(analytics?.application_status_distribution || {}).map(([status, count]) => ({
    name: status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
    value: count,
    fill: COLORS[Object.keys(analytics?.application_status_distribution || {}).indexOf(status) % COLORS.length]
  }))

  // Mock trend data for demonstration
  const trendData = Array.from({ length: 30 }, (_, i) => ({
    day: `Day ${i + 1}`,
    users: Math.floor(Math.random() * 100) + 50,
    applications: Math.floor(Math.random() * 200) + 100,
    interviews: Math.floor(Math.random() * 50) + 20
  }))

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Platform Analytics</h1>
          <p className="text-gray-600 mt-1">Insights and metrics for the career intelligence platform</p>
        </div>
        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-gray-700">Time Range:</label>
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as any)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="all">All time</option>
          </select>
          <button
            onClick={fetchAnalytics}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
          >
            Refresh Data
          </button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Users</CardTitle>
            <CardDescription>All registered users</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">{analytics?.total_users}</div>
            <div className="text-sm text-gray-500 mt-1">
              <Users className="w-4 h-4 inline-block mr-1" />
              +{Math.floor(Math.random() * 50)} this month
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Applications</CardTitle>
            <CardDescription>Total applications submitted</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {Object.values(analytics?.application_status_distribution || {}).reduce((a, b) => a + b, 0)}
            </div>
            <div className="text-sm text-gray-500 mt-1">
              <CheckCircle className="w-4 h-4 inline-block mr-1" />
              {analytics?.application_success_rate || 0}% success rate
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Interviews</CardTitle>
            <CardDescription>Conducted interviews</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">{analytics?.total_interviews}</div>
            <div className="text-sm text-gray-500 mt-1">
              <ArrowUpRight className="w-4 h-4 inline-block mr-1" />
              {analytics?.success_rate || 0}% success rate
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Career Readiness</CardTitle>
            <CardDescription>Average career preparedness score</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="text-3xl font-bold text-gray-900">{analytics?.average_career_readiness || 0}%</div>
            <div className="text-sm text-gray-500 mt-1">
              <TrendingUp className="w-4 h-4 inline-block mr-1" />
              Across all active users
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Application Status Distribution</CardTitle>
            <CardDescription>Current status of all applications</CardDescription>
          </CardHeader>
          <CardContent>
            {applicationData.length > 0 ? (
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={120}
                      data={applicationData}
                      dataKey="value"
                      nameKey="name"
                      label={({ name, value }) => `${name}: ${value}`}
                      labelLine={{ stroke: '#666', strokeWidth: 1 }}
                      stroke="none"
                    >
                      {applicationData.map((entry, i) => (
                        <Cell key={`cell-${i}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="h-80 flex items-center justify-center">
                <p className="text-gray-500">No application data available</p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Most Requested Skills</CardTitle>
            <CardDescription>Top skills demanded by employers</CardDescription>
          </CardHeader>
          <CardContent>
            {skillsData.length > 0 ? (
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={skillsData.slice(0, 10)} layout="vertical" margin={{ left: 20, right: 30, top: 20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis type="category" dataKey="name" tick={{ fontSize: 12 }} width={100} />
                    <Tooltip />
                    <Bar dataKey="count" fill="#0088FE" barSize={15} radius={[0, 4, 4, 0]}>
                      {skillsData.slice(0, 10).map((_entry, i) => (
                        <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="h-80 flex items-center justify-center">
                <p className="text-gray-500">No skills data available</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Popular Job Roles</CardTitle>
            <CardDescription>Most common positions posted</CardDescription>
          </CardHeader>
          <CardContent>
            {rolesData.length > 0 ? (
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={rolesData} margin={{ left: 20, right: 30, top: 20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#00C49F" barSize={20} radius={[4, 4, 0, 0]}>
                      {rolesData.map((_entry, i) => (
                        <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="h-80 flex items-center justify-center">
                <p className="text-gray-500">No job role data available</p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>User Growth Trend</CardTitle>
            <CardDescription>New users over the last {timeRange === '7d' ? '7' : timeRange === '30d' ? '30' : timeRange === '90d' ? '90' : 'all'} days</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData} margin={{ left: 20, right: 30, top: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" tick={{ fontSize: 10 }} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="users" stroke="#0088FE" strokeWidth={2} dot={false} name="Users" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}