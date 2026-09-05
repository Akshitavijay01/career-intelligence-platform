import { useState, useEffect } from 'react'
import { careerApi } from '@/api/client'
import { Card } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { Map, CheckCircle2, Circle, Sparkles } from 'lucide-react'
import { toast } from 'sonner'

export default function RoadmapPage() {
  const [roadmapData, setRoadmapData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadRoadmap = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await careerApi.getRoadmap()
      setRoadmapData(res.data)
    } catch (err: any) {
      console.log('No existing roadmap found')
      setRoadmapData(null)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateRoadmap = async (role: string) => {
    try {
      setError(null)
      setGenerating(true)
      const res = await careerApi.generateRoadmap(role)
      setRoadmapData(res.data)
      toast.success(`Generated roadmap for ${role}!`)
    } catch (err: any) {
      console.error(err)
      setError('Unable to construct career roadmap.')
    } finally {
      setGenerating(false)
    }
  }

  useEffect(() => {
    loadRoadmap()
  }, [])

  if (loading) return <LoadingSpinner message="Generating your personalized learning roadmap..." />
  if (error) return <ErrorState message={error} onRetry={loadRoadmap} />

  const items = roadmapData?.items || [
    { skill_name: 'Core Algorithms & Data Structures', description: 'Master Trees, Graphs, Dynamic Programming on LeetCode', estimated_hours: 40, is_completed: 'true' },
    { skill_name: 'Advanced Backend Frameworks', description: 'Build asynchronous APIs using FastAPI and SQLModel', estimated_hours: 30, is_completed: 'false' },
    { skill_name: 'System Architecture & Caching', description: 'Learn Redis caching, message queues, and horizontal scaling', estimated_hours: 25, is_completed: 'false' },
    { skill_name: 'CI/CD & Cloud Deployment', description: 'Containerize apps with Docker and deploy on AWS / GCP', estimated_hours: 20, is_completed: 'false' }
  ]

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Map className="w-6 h-6 text-blue-600" /> Career Learning Roadmap
          </h1>
          <p className="text-gray-500 text-sm">Step-by-step milestones to land your target software engineering position</p>
        </div>

        <button
          onClick={() => handleGenerateRoadmap('Full Stack Engineer')}
          disabled={generating}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 shadow-sm"
        >
          <Sparkles className="w-4 h-4" />
          {generating ? 'Regenerating...' : 'Regenerate Roadmap'}
        </button>
      </div>

      <div className="space-y-4">
        {items.map((item: any, idx: number) => {
          const isDone = item.is_completed === 'true' || item.is_completed === true
          return (
            <Card key={idx} className={`p-5 transition-all ${isDone ? 'bg-emerald-50/40 border-emerald-200' : 'bg-white'}`}>
              <div className="flex items-start gap-4">
                <button
                  type="button"
                  onClick={async () => {
                    try {
                      const res = await careerApi.toggleRoadmapItem(item.id)
                      const updated = res.data
                      setRoadmapData((prev: any) => {
                        if (!prev) return prev
                        return {
                          ...prev,
                          items: prev.items.map((it: any) =>
                            it.id === item.id ? { ...it, is_completed: updated.is_completed } : it
                          ),
                          roadmap: { ...prev.roadmap, progress_percentage: updated.progress }
                        }
                      })
                    } catch (err: any) {
                      console.error('Failed to toggle roadmap item', err)
                      toast.error('Could not update milestone.')
                    }
                  }}
                  className="mt-0.5 p-0 focus:outline-none"
                  aria-label={isDone ? 'Mark as incomplete' : 'Mark as complete'}
                >
                  {isDone ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-600" />
                  ) : (
                    <Circle className="w-6 h-6 text-gray-300 hover:text-blue-500 transition-colors" />
                  )}
                </button>

                <div className="flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <h3 className={`text-base font-bold ${isDone ? 'text-emerald-950 line-through' : 'text-gray-900'}`}>
                      {idx + 1}. {item.skill_name}
                    </h3>
                    <span className="text-xs px-2.5 py-0.5 rounded-full font-medium bg-gray-100 text-gray-600">
                      Est. {item.estimated_hours} hrs
                    </span>
                  </div>

                  <p className="text-xs text-gray-600 mt-1">{item.description}</p>
                </div>
              </div>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
