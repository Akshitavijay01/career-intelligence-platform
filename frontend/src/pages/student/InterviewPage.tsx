import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { interviewApi } from '@/api/client'
import { Card, CardContent } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { EmptyState } from '@/components/common/EmptyState'
import { MessageSquare, Play, RefreshCcw } from 'lucide-react'
import { toast } from 'sonner'

export default function InterviewPage() {
  const navigate = useNavigate()
  const [history, setHistory] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadHistory = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await interviewApi.getHistory()
      setHistory(res.data || [])
    } catch (err: any) {
      console.error(err)
      setError('Unable to load mock interview history.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  const startSession = async () => {
    try {
      setStarting(true)
      const res = await interviewApi.startSession('medium', 'mixed')
      toast.success('Interview session created!')
      navigate(`/interview/${res.data.session_id}`)
    } catch (err: any) {
      toast.error('Could not generate interview questions at this time.')
    } finally {
      setStarting(false)
    }
  }

  if (loading) return <LoadingSpinner message="Fetching interview preparation materials..." />
  if (error) return <ErrorState message={error} onRetry={loadHistory} />

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <MessageSquare className="w-6 h-6 text-green-600" /> Interview Preparation
          </h1>
          <p className="text-gray-500 text-sm">Practice with AI-generated technical and HR questions tailored to your resume</p>
        </div>

        <button
          onClick={startSession}
          disabled={starting}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors shadow-sm"
        >
          {starting ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
          Start New Practice
        </button>
      </div>

      {history.length === 0 ? (
        <EmptyState
          title="No Mock Interviews Yet"
          description="Ready to test your knowledge? Start a new practice session and get instant AI feedback on your answers."
          actionLabel="Start Interview"
          onAction={startSession}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {history.map((session) => (
            <Card key={session.id} className="hover:border-green-300 transition-colors">
              <CardContent className="p-5">
                <div className="flex justify-between items-start mb-4">
                  <div className="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wide bg-green-100 text-green-800">
                    {session.interview_type || 'Mixed'}
                  </div>
                  <div className="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wide bg-gray-100 text-gray-800">
                    {session.difficulty || 'Medium'}
                  </div>
                </div>

                <h3 className="font-semibold text-gray-900">Practice Session #{session.id}</h3>
                <p className="text-xs text-gray-500 mt-1">Status: {session.completed_at ? 'Completed' : 'In Progress'}</p>

                <div className="mt-4 pt-4 border-t flex justify-between items-center">
                  <span className="text-sm font-bold text-gray-800">Score: {session.overall_score || 0}/100</span>
                  <button
                    onClick={() => navigate(`/interview/${session.id}`)}
                    className="text-sm text-green-600 hover:underline font-medium"
                  >
                    {session.completed_at ? 'View Feedback' : 'Continue'}
                  </button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
