import { useState, useEffect } from 'react'
import { careerApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { Target } from 'lucide-react'
import { toast } from 'sonner'

export default function SkillGapPage() {
  const [targetRole, setTargetRole] = useState('Full Stack Developer')
  const [analysis, setAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [switching, setSwitching] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const roles = [
    'Full Stack Developer',
    'Frontend Developer',
    'Backend Developer',
    'Data Scientist',
    'Machine Learning Engineer',
    'DevOps Engineer',
  ]

  const runAnalysis = async (role: string) => {
    try {
      const isInitial = !analysis
      if (isInitial) setLoading(true)
      else setSwitching(true)
      setError(null)
      const res = await careerApi.analyzeGaps(role)
      setAnalysis(res.data)
    } catch (err: any) {
      console.error(err)
      setError('Failed to run skill gap analysis.')
      toast.error('Failed to run skill gap analysis.')
    } finally {
      setLoading(false)
      setSwitching(false)
    }
  }

  useEffect(() => {
    runAnalysis(targetRole)
  }, [])

  if (loading) return <LoadingSpinner message="Evaluating skill gaps against market demand..." />
  if (error) return <ErrorState message={error} onRetry={() => runAnalysis(targetRole)} />

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Target className="w-6 h-6 text-purple-600" /> Skill Gap Analysis
        </h1>
        <p className="text-gray-500 text-sm">Benchmark your current skill profile against standard requirements for your target role</p>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-semibold text-gray-600 uppercase">Target Role:</span>
        {roles.map((r) => (
          <button
            key={r}
            onClick={() => {
              setTargetRole(r)
              runAnalysis(r)
            }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              targetRole === r
                ? 'bg-purple-600 text-white shadow-sm'
                : 'bg-white border text-gray-700 hover:bg-gray-50'
            }`}
          >
            {r}
          </button>
        ))}
      </div>

      {switching && (
        <div className="text-xs text-purple-600 animate-pulse">Refreshing analysis for {targetRole}...</div>
      )}
      <div className={`grid grid-cols-1 md:grid-cols-2 gap-6 ${switching ? 'opacity-60' : ''}`}>
        <Card>
          <CardHeader>
            <CardTitle>Missing Core Competencies</CardTitle>
            <CardDescription>High priority skills to acquire for {targetRole}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {(analysis?.all_missing_skills?.length > 0 || analysis?.missing_required_skills?.length > 0) ? (
              (analysis.all_missing_skills || analysis.missing_required_skills || []).map((skill: string, idx: number) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-red-50 text-red-900 rounded-lg text-sm">
                  <span className="font-medium">{skill.trim()}</span>
                  <span className="px-2 py-0.5 text-xs bg-red-200 text-red-800 rounded font-semibold">Priority High</span>
                </div>
              ))
            ) : analysis ? (
              <p className="text-sm text-gray-500">No major gaps — you cover the core requirements for {targetRole}.</p>
            ) : (
              <div className="space-y-2">
                <div className="flex items-center justify-between p-3 bg-purple-50 text-purple-900 rounded-lg text-sm">
                  <span className="font-medium">Docker & Containerization</span>
                  <span className="px-2 py-0.5 text-xs bg-purple-200 text-purple-800 rounded font-semibold">Recommended</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-purple-50 text-purple-900 rounded-lg text-sm">
                  <span className="font-medium">System Design & Scalability</span>
                  <span className="px-2 py-0.5 text-xs bg-purple-200 text-purple-800 rounded font-semibold">Recommended</span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recommended Action Plan</CardTitle>
            <CardDescription>Step-by-step guidance to bridge your gap</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 text-sm text-gray-600">
            {analysis?.priority_skills?.length > 0 ? (
              analysis.priority_skills.slice(0, 3).map((item: any, idx: number) => (
                <div key={idx} className="p-4 border border-purple-100 bg-purple-50/50 rounded-lg space-y-1">
                  <h4 className="font-semibold text-gray-900">{idx + 1}. Learn {item.skill}</h4>
                  <p className="text-xs capitalize">{item.priority} priority for {targetRole}</p>
                </div>
              ))
            ) : (
              <>
                <div className="p-4 border border-gray-100 bg-gray-50 rounded-lg space-y-2">
                  <h4 className="font-semibold text-gray-900">1. Hands-on Project</h4>
                  <p className="text-xs">Build a microservices application utilizing your target stack to demonstrate practical mastery.</p>
                </div>
                <div className="p-4 border border-gray-100 bg-gray-50 rounded-lg space-y-2">
                  <h4 className="font-semibold text-gray-900">2. Certification Milestone</h4>
                  <p className="text-xs">Prepare for an industry-standard credential (e.g. AWS Certified Cloud Practitioner) within 30 days.</p>
                </div>
              </>
            )}
            {analysis?.match_percentage !== undefined && (
              <p className="text-xs text-purple-700 font-medium">Current match: {analysis.match_percentage}%</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
