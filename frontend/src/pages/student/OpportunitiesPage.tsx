import { useState, useEffect } from 'react'
import { opportunitiesApi, applicationsApi } from '@/api/client'
import { Card, CardContent } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { EmptyState } from '@/components/common/EmptyState'
import { Search, MapPin, Briefcase, Building, Check } from 'lucide-react'
import { toast } from 'sonner'

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [appliedIds, setAppliedIds] = useState<number[]>([])

  const loadOpportunities = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await opportunitiesApi.getOpportunities({ search: search || undefined })
      setOpportunities(res.data || [])
    } catch (err: any) {
      console.error(err)
      setError('Unable to load job opportunities.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadOpportunities()
  }, [search])

  const handleApply = async (oppId: number) => {
    try {
      await applicationsApi.createApplication(oppId)
      setAppliedIds((prev) => [...prev, oppId])
      toast.success('Application submitted successfully!')
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to submit application.')
    }
  }

  if (loading && !search) return <LoadingSpinner message="Finding job & internship matches..." />
  if (error) return <ErrorState message={error} onRetry={loadOpportunities} />

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Explore Opportunities</h1>
          <p className="text-gray-500 text-sm">Discover verified internships and job roles matching your profile</p>
        </div>

        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search role, company..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 border rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {opportunities.length === 0 ? (
        <EmptyState
          title="No Opportunities Found"
          description="Try broadening your search term or check back later."
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {opportunities.map((opp) => {
            const isApplied = appliedIds.includes(opp.id)
            return (
              <Card key={opp.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-5 flex flex-col justify-between h-full">
                  <div>
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <div>
                        <h3 className="font-semibold text-gray-900 text-base">{opp.title}</h3>
                        <div className="flex items-center gap-1 text-sm text-gray-600 mt-0.5">
                          <Building className="w-4 h-4 text-gray-400" />
                          <span>{opp.company}</span>
                        </div>
                      </div>
                      <span className="px-2.5 py-0.5 text-xs font-semibold bg-blue-50 text-blue-700 rounded-full capitalize">
                        {opp.employment_type || 'Internship'}
                      </span>
                    </div>

                    <p className="text-xs text-gray-500 line-clamp-2 my-3">{opp.description}</p>

                    <div className="flex items-center gap-4 text-xs text-gray-500 pt-2 border-t">
                      <div className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5" />
                        <span>{opp.location || 'Remote'}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Briefcase className="w-3.5 h-3.5" />
                        <span className="capitalize">{opp.work_type || 'Hybrid'}</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t flex justify-end">
                    <button
                      onClick={() => handleApply(opp.id)}
                      disabled={isApplied}
                      className={`px-4 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1 transition-colors ${
                        isApplied
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-blue-600 hover:bg-blue-700 text-white'
                      }`}
                    >
                      {isApplied ? (
                        <>
                          <Check className="w-3.5 h-3.5" /> Applied
                        </>
                      ) : (
                        'Apply Now'
                      )}
                    </button>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
