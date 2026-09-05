import { useState, useEffect } from 'react'
import { applicationsApi } from '@/api/client'
import { Card } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { EmptyState } from '@/components/common/EmptyState'
import { Briefcase, Building, Calendar } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadApplications = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await applicationsApi.getApplications()
      setApplications(res.data || [])
    } catch (err: any) {
      console.error(err)
      setError('Unable to fetch application history.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadApplications()
  }, [])

  if (loading) return <LoadingSpinner message="Fetching your submitted applications..." />
  if (error) return <ErrorState message={error} onRetry={loadApplications} />

  const getStatusBadge = (status: string) => {
    const s = status?.toLowerCase()
    if (s === 'applied') return 'bg-blue-100 text-blue-800'
    if (s === 'interview') return 'bg-purple-100 text-purple-800'
    if (s === 'offer') return 'bg-emerald-100 text-emerald-800'
    if (s === 'rejected') return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Application Tracker</h1>
          <p className="text-gray-500 text-sm">Track status and timelines for all opportunities you've applied for</p>
        </div>

        <Link
          to="/opportunities"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-sm inline-flex items-center gap-1.5"
        >
          <Briefcase className="w-4 h-4" /> Apply for More
        </Link>
      </div>

      {applications.length === 0 ? (
        <EmptyState
          title="No Applications Submitted"
          description="You haven't applied to any roles yet. Explore current openings to get started!"
          actionLabel="Browse Opportunities"
          onAction={() => window.location.href = '/opportunities'}
        />
      ) : (
        <div className="space-y-4">
          {applications.map((item) => {
            const app = item.application || item
            const opp = item.opportunity || {}
            return (
              <Card key={app.id} className="p-5 hover:border-gray-300 transition-colors">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <h3 className="font-bold text-gray-900 text-base">{opp.title || 'Software Engineering Position'}</h3>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Building className="w-4 h-4 text-gray-400" />
                      <span>{opp.company || 'Tech Partner Inc.'}</span>
                      <span>•</span>
                      <span>{opp.location || 'Remote'}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1 text-xs text-gray-500">
                      <Calendar className="w-3.5 h-3.5" />
                      <span>Applied: {app.applied_date || 'Recently'}</span>
                    </div>

                    <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${getStatusBadge(app.status)}`}>
                      {app.status || 'APPLIED'}
                    </span>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
