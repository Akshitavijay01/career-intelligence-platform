import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Briefcase,
  MessageSquare,
  Target,
  ChevronRight,
  ArrowUpRight,
  FileText
} from 'lucide-react'
import { dashboardApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'

interface DashboardStats {
  career_readiness: number
  resume_score: number
  technical_skill_score: number
  recommended_jobs: number
  applications: number
  interviews: number
  skill_gaps: number
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardData()
    const refetch = () => fetchDashboardData()
    window.addEventListener('careerai:profile-updated', refetch)
    const onVisibility = () => { if (document.visibilityState === 'visible') fetchDashboardData() }
    document.addEventListener('visibilitychange', onVisibility)
    window.addEventListener('focus', refetch)
    return () => {
      window.removeEventListener('careerai:profile-updated', refetch)
      document.removeEventListener('visibilitychange', onVisibility)
      window.removeEventListener('focus', refetch)
    }
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await dashboardApi.getStats()
      setStats(response.data)
    } catch (err: any) {
      console.error('Error fetching dashboard data:', err)
      setError('Unable to load dashboard data right now.')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-emerald-600 bg-emerald-100'
    if (score >= 60) return 'text-blue-600 bg-blue-100'
    if (score >= 40) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  if (loading) {
    return <LoadingSpinner message="Loading your career intelligence dashboard..." />
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchDashboardData} />
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Welcome back!</h1>
          <p className="text-gray-600 mt-1">Here's your career intelligence overview</p>
        </div>
        <div className="flex gap-3">
          <Link to="/resume">
            <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50">
              <FileText className="w-4 h-4" />
              Update Resume
            </button>
          </Link>
          <Link to="/career-roadmap">
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700">
              <Target className="w-4 h-4" />
              Build Roadmap
            </button>
          </Link>
        </div>
      </div>

      {/* Career Readiness Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Career Readiness</CardTitle>
            <CardDescription>Your overall career preparedness score</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {stats && (
              <>
                <div className="flex items-center gap-8">
                  <div className="relative w-32 h-32">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="12"
                        className="text-gray-200"
                      />
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="12"
                        strokeDasharray={351.86}
                        strokeDashoffset={351.86 - (351.86 * stats.career_readiness) / 100}
                        className="text-blue-600 transition-all duration-1000 ease-out"
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className={`text-3xl font-bold ${getScoreColor(stats.career_readiness)}`}>
                        {stats.career_readiness}%
                      </span>
                      <span className="text-xs text-gray-500">Overall</span>
                    </div>
                  </div>
                  <div className="flex-1 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Technical Skills</span>
                      <span className="font-medium">{stats.technical_skill_score}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${stats.technical_skill_score}%` }} />
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Resume Score</span>
                      <span className="font-medium">{stats.resume_score}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${stats.resume_score}%` }} />
                    </div>
                  </div>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4">
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-lg font-bold text-gray-900">{stats.applications}</div>
                    <div className="text-xs text-gray-600">Applications</div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-lg font-bold text-gray-900">{stats.interviews}</div>
                    <div className="text-xs text-gray-600">Interviews</div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-lg font-bold text-gray-900">{stats.skill_gaps}</div>
                    <div className="text-xs text-gray-600">Skill Gaps</div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-lg font-bold text-gray-900">{stats.recommended_jobs}</div>
                    <div className="text-xs text-gray-600">Matches</div>
                  </div>
                </div>
              </>
            )}
          </CardContent>
          <CardFooter>
            <Link to="/career-readiness" className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center">
              View detailed analysis <ChevronRight className="w-4 h-4 ml-1" />
            </Link>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Recommended next steps</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link to="/resume/analyze" className="flex items-center p-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white">
                <FileText className="w-5 h-5" />
              </div>
              <div className="ml-3">
                <div className="font-medium text-sm">Analyze Resume</div>
                <div className="text-xs text-gray-500">Get AI feedback</div>
              </div>
            </Link>
            <Link to="/skill-gap" className="flex items-center p-3 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors">
              <div className="w-10 h-10 bg-purple-600 rounded-lg flex items-center justify-center text-white">
                <Target className="w-5 h-5" />
              </div>
              <div className="ml-3">
                <div className="font-medium text-sm">Skill Gap Analysis</div>
                <div className="text-xs text-gray-500">Find missing skills</div>
              </div>
            </Link>
            <Link to="/interview" className="flex items-center p-3 bg-green-50 hover:bg-green-100 rounded-lg transition-colors">
              <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center text-white">
                <MessageSquare className="w-5 h-5" />
              </div>
              <div className="ml-3">
                <div className="font-medium text-sm">Interview Prep</div>
                <div className="text-xs text-gray-500">Practice questions</div>
              </div>
            </Link>
            <Link to="/opportunities" className="flex items-center p-3 bg-orange-50 hover:bg-orange-100 rounded-lg transition-colors">
              <div className="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center text-white">
                <Briefcase className="w-5 h-5" />
              </div>
              <div className="ml-3">
                <div className="font-medium text-sm">Find Jobs</div>
                <div className="text-xs text-gray-500">Explore opportunities</div>
              </div>
            </Link>
          </CardContent>
        </Card>
      </div>

      {/* Top Recommended Opportunities */}
      <Card>
        <CardHeader>
          <CardTitle>Top Recommended Opportunities</CardTitle>
          <CardDescription>Jobs matched for your profile based on AI analysis</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {stats?.recommended_jobs === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Briefcase className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900">No recommendations yet</h3>
              <p className="text-gray-500 mt-2">Upload your resume to get personalized matches</p>
              <Link to="/resume" className="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700">
                Upload Resume
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[1, 2, 3].map((item) => (
                <div key={item} className="border border-gray-200 rounded-xl p-4 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="font-medium text-gray-900">Python Developer Intern</h3>
                      <p className="text-sm text-gray-500">Tech Solutions India</p>
                    </div>
                    <span className="px-2 py-1 text-xs font-medium bg-emerald-100 text-emerald-700 rounded-full">
                      Remote
                    </span>
                  </div>
                  <div className="flex items-center gap-1 text-sm text-gray-600 mb-3">
                    <span className="w-2 h-2 bg-emerald-500 rounded-full" />
                    91% Match
                  </div>
                  <div className="space-y-2">
                    <div className="text-xs text-gray-500">
                      <span className="font-medium text-gray-700">Matched:</span> Python, SQL, React
                    </div>
                    <div className="text-xs text-gray-500">
                      <span className="font-medium text-gray-700">Missing:</span> Docker, AWS
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
        <CardFooter>
          <Link to="/recommendations" className="w-full flex items-center justify-center gap-2 text-sm text-blue-600 hover:text-blue-700 font-medium">
            View All Recommendations <ArrowUpRight className="w-4 h-4" />
          </Link>
        </CardFooter>
      </Card>
    </div>
  )
}