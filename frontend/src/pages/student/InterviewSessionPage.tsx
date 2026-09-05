import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { interviewApi } from '@/api/client'
import { Card, CardContent } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { ArrowLeft, CheckCircle, Send, AlertCircle } from 'lucide-react'
import { toast } from 'sonner'

export default function InterviewSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>()
  const navigate = useNavigate()

  const [session, setSession] = useState<any>(null)
  const [questions, setQuestions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentIdx, setCurrentIdx] = useState(0)
  const [answer, setAnswer] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [scores, setScores] = useState<Record<number, { score: number; evaluation: string }>>({})
  const [sessionComplete, setSessionComplete] = useState(false)

  const loadSession = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await interviewApi.getSession(Number(sessionId))
      setSession(res.data.session)
      setQuestions(res.data.questions || [])

      // Hydrate scores for already-answered questions
      const existing: Record<number, { score: number; evaluation: string }> = {}
      let firstUnanswered = -1
      for (let i = 0; i < res.data.questions.length; i++) {
        const q = res.data.questions[i]
        if (q.score != null) {
          existing[q.id] = { score: q.score, evaluation: q.ai_evaluation || '' }
        } else if (firstUnanswered === -1) {
          firstUnanswered = i
        }
      }
      setScores(existing)
      setCurrentIdx(firstUnanswered >= 0 ? firstUnanswered : 0)

      if (res.data.questions.every((q: any) => q.score != null) && res.data.questions.length > 0) {
        setSessionComplete(true)
      }
    } catch {
      setError('Unable to load interview session.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSession()
  }, [sessionId])

  const submitAnswer = async () => {
    if (!answer.trim()) {
      toast.error('Please enter an answer before submitting.')
      return
    }

    const q = questions[currentIdx]
    try {
      setSubmitting(true)
      const res = await interviewApi.submitAnswer(session.id, q.id, answer.trim())
      setScores((prev) => ({
        ...prev,
        [q.id]: { score: res.data.score, evaluation: res.data.evaluation },
      }))
      setAnswer('')

      // Check if all questions are now answered
      const allAnswered = questions.every((qu) => qu.id === q.id || scores[qu.id] != null)
      if (allAnswered || currentIdx === questions.length - 1) {
        setSessionComplete(true)
        toast.success('All questions answered!')
      } else {
        setCurrentIdx((i) => i + 1)
      }
    } catch {
      toast.error('Failed to submit answer. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <LoadingSpinner message="Loading interview session..." />
  if (error) return <ErrorState message={error} onRetry={loadSession} />

  const currentQ = questions[currentIdx]
  const answeredCount = Object.keys(scores).length
  const totalScore = Object.values(scores).reduce((sum, s) => sum + s.score, 0)
  const avgScore = answeredCount > 0 ? Math.round(totalScore / answeredCount) : 0

  return (
    <div className="space-y-6">
      <button
        onClick={() => navigate('/interview')}
        className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Interview Prep
      </button>

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Interview Session #{sessionId}</h1>
          <p className="text-gray-500 text-sm">
            {session.interview_type} · {session.difficulty} · {answeredCount}/{questions.length} answered
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{avgScore}</div>
            <div className="text-xs text-gray-500">avg score</div>
          </div>
        </div>
      </div>

      {sessionComplete ? (
        <Card>
          <CardContent className="p-8 text-center space-y-4">
            <CheckCircle className="w-12 h-12 text-green-500 mx-auto" />
            <h2 className="text-xl font-bold text-gray-900">Session Complete</h2>
            <p className="text-gray-600">Overall score: <span className="font-bold text-green-600">{avgScore}/100</span></p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6 text-left max-w-2xl mx-auto">
              {questions.map((q, i) => {
                const s = scores[q.id]
                return (
                  <div key={q.id} className="bg-gray-50 rounded-lg p-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold uppercase text-gray-500">Q{i + 1} · {q.question_type}</span>
                      <span className={`text-sm font-bold ${s.score >= 60 ? 'text-green-600' : s.score >= 40 ? 'text-amber-600' : 'text-red-600'}`}>
                        {s.score}/100
                      </span>
                    </div>
                    <p className="text-sm text-gray-800">{q.question}</p>
                    <p className="text-xs text-gray-500 italic">{s.evaluation}</p>
                  </div>
                )
              })}
            </div>
            <button
              onClick={() => navigate('/interview')}
              className="mt-4 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors"
            >
              Back to Interview Prep
            </button>
          </CardContent>
        </Card>
      ) : currentQ ? (
        <div className="space-y-4">
          <Card>
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Question {currentIdx + 1} of {questions.length} · {currentQ.question_type}
                </span>
                <span className="text-xs font-semibold uppercase px-2 py-0.5 rounded bg-gray-100 text-gray-700">
                  {session.difficulty}
                </span>
              </div>
              <p className="text-lg font-medium text-gray-900">{currentQ.question}</p>

              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Type your answer here..."
                rows={6}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-800 placeholder:text-gray-400 focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-y transition-colors"
                disabled={submitting || !!scores[currentQ.id]}
              />

              {scores[currentQ.id] && (
                <div className={`rounded-lg p-4 space-y-2 ${
                  scores[currentQ.id].score >= 60 ? 'bg-green-50 border border-green-200' :
                  scores[currentQ.id].score >= 40 ? 'bg-amber-50 border border-amber-200' :
                  'bg-red-50 border border-red-200'
                }`}>
                  <div className="flex items-center gap-2">
                    {scores[currentQ.id].score >= 60
                      ? <CheckCircle className="w-5 h-5 text-green-600" />
                      : <AlertCircle className="w-5 h-5 text-amber-600" />}
                    <span className="font-bold text-gray-900">Score: {scores[currentQ.id].score}/100</span>
                  </div>
                  <p className="text-sm text-gray-700">{scores[currentQ.id].evaluation}</p>
                </div>
              )}
            </CardContent>
          </Card>

          <div className="flex justify-end">
            <button
              onClick={submitAnswer}
              disabled={submitting || !answer.trim() || !!scores[currentQ.id]}
              className="flex items-center gap-2 px-5 py-2.5 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              Submit Answer
            </button>
          </div>
        </div>
      ) : (
        <Card>
          <CardContent className="p-6 text-center text-gray-500">No questions found for this session.</CardContent>
        </Card>
      )}
    </div>
  )
}
