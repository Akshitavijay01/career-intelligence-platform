import { useState, useEffect } from 'react'
import { recommendationsApi } from '@/api/client'
import { Card } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { EmptyState } from '@/components/common/EmptyState'
import { Sparkles, RefreshCw, CheckCircle2, XCircle } from 'lucide-react'
import { toast } from 'sonner'

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadRecommendations = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await recommendationsApi.getRecommendations()
      setRecommendations(res.data || [])
    } catch (err: any) {
      console.error(err)
      setError('Unable to compute AI recommendations right now.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRecommendations()
  }, [])

  const handleRefresh = async () => {
    try {
      setRefreshing(true)
      await recommendationsApi.refresh()
      toast.success('Recommendations refreshed!')
      await loadRecommendations()
    } catch (err: any) {
      toast.error('Could not refresh recommendations.')
    } finally {
      setRefreshing(false)
    }
  }

  const formatSkills = (skills: any) => {
    if (!skills) return ''
    if (Array.isArray(skills)) return skills.join(', ')
    if (typeof skills === 'string') {
      try {
        const parsed = JSON.parse(skills)
        if (Array.isArray(parsed)) return parsed.join(', ')
      } catch (e) {
        // Not valid JSON, return cleaned up string
        return skills.replace(/[\[\]"']/g, '')
      }
      return skills
    }
    return String(skills)
  }

  if (loading) return <LoadingSpinner message="Calculating career match scores with AI engine..." />
  if (error) return <ErrorState message={error} onRetry={loadRecommendations} />

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-amber-500" />
            AI Career Recommendations
          </h1>
          <p className="text-gray-500 text-sm">Personalized opportunity matches based on your skills and profile</p>
        </div>

        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="flex items-center gap-2 px-4 py-2 border rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 shadow-sm"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh Matches
        </button>
      </div>

      {recommendations.length === 0 ? (
        <EmptyState
          title="No Match Data Available"
          description="Update your skills or upload your resume to generate high-accuracy job recommendations."
          actionLabel="Recalculate Matches"
          onAction={handleRefresh}
        />
      ) : (
        <div className="space-y-4">
          {recommendations.map((rec) => {
            const matched = formatSkills(rec.matched_skills)
            const missing = formatSkills(rec.missing_skills)

            return (
              <Card key={rec.id} className="p-5 hover:border-blue-300 transition-colors">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-bold text-gray-900">{rec.opportunity?.title || 'Matched Position'}</h3>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
                        {Math.round(rec.overall_score || 85)}% Match
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">{rec.explanation || 'Strong correlation with your declared technical skills and background.'}</p>

                    <div className="flex flex-wrap items-center gap-4 text-xs pt-1">
                      {matched && (
                        <div className="flex items-center gap-1 text-emerald-700">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>Matched: {matched}</span>
                        </div>
                      )}
                      {missing && (
                        <div className="flex items-center gap-1 text-amber-700">
                          <XCircle className="w-3.5 h-3.5" />
                          <span>Suggested: {missing}</span>
                        </div>
                      )}
                    </div>
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
