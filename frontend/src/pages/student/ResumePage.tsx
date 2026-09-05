import { useState, useEffect } from 'react'
import { resumeApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { FileUp, CheckCircle, AlertTriangle } from 'lucide-react'
import { toast } from 'sonner'

export default function ResumePage() {
  const [resume, setResume] = useState<any>(null)
  const [analysis, setAnalysis] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadResumeData = async () => {
    try {
      setLoading(true)
      setError(null)
      const [resRes, anaRes] = await Promise.allSettled([
        resumeApi.getResume(),
        resumeApi.getAnalysis()
      ])
      if (resRes.status === 'fulfilled') setResume(resRes.value.data)
      if (anaRes.status === 'fulfilled') setAnalysis(anaRes.value.data)
    } catch (err: any) {
      console.error(err)
      setError('Unable to load resume information.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadResumeData()
  }, [])

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      setUploading(true)
      await resumeApi.upload(formData)
      toast.success('Resume uploaded and processed successfully!')
      await loadResumeData()
      try { localStorage.setItem('careerai_profile_refresh', String(Date.now())) } catch {}
      window.dispatchEvent(new CustomEvent('careerai:profile-updated'))
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to upload resume.')
    } finally {
      setUploading(false)
    }
  }

  if (loading) return <LoadingSpinner message="Fetching resume insights..." />
  if (error) return <ErrorState message={error} onRetry={loadResumeData} />

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Resume Intelligence</h1>
        <p className="text-gray-500 text-sm">Upload your resume to extract skills and evaluate ATS readiness</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Upload Resume</CardTitle>
            <CardDescription>Supports PDF and DOCX formats (Max 5MB)</CardDescription>
          </CardHeader>
          <CardContent>
            <label className="border-2 border-dashed border-gray-300 rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 hover:bg-blue-50/50 transition-colors">
              <FileUp className="w-8 h-8 text-blue-500 mb-2" />
              <span className="text-sm font-medium text-gray-700">
                {uploading ? 'Processing...' : 'Click to select resume'}
              </span>
              <span className="text-xs text-gray-400 mt-1">PDF or DOCX</span>
              <input
                type="file"
                className="hidden"
                accept=".pdf,.docx"
                disabled={uploading}
                onChange={handleFileUpload}
              />
            </label>

            {resume && (
              <div className="mt-4 p-3 bg-gray-50 rounded-lg text-xs text-gray-600">
                <span className="font-semibold block">Latest File:</span>
                {resume.file_name}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Resume Analysis & Scores</CardTitle>
            <CardDescription>AI-generated scoring and feedback</CardDescription>
          </CardHeader>
          <CardContent>
            {!analysis ? (
              <div className="text-center py-10 text-gray-500 text-sm">
                No resume analyzed yet. Upload a resume to see full breakdown.
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                  <div>
                    <h3 className="font-bold text-lg text-blue-950">Overall ATS Score</h3>
                    <p className="text-xs text-blue-700">Calculated based on structure, skills, and clarity</p>
                  </div>
                  <span className="text-2xl font-black text-blue-600">{analysis.overall_score || 0}%</span>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-emerald-50 rounded-lg flex items-start gap-2">
                    <CheckCircle className="w-5 h-5 text-emerald-600 mt-0.5 shrink-0" />
                    <div>
                      <h4 className="text-sm font-semibold text-emerald-950">Strengths</h4>
                      <ul className="text-xs text-emerald-800 mt-1 space-y-0.5 list-disc list-inside">
                        {(() => {
                          let vals: string[] = []
                          if (Array.isArray(analysis.strengths)) vals = analysis.strengths
                          else if (typeof analysis.strengths === 'string') try { vals = JSON.parse(analysis.strengths) } catch { if (analysis.strengths) vals = [analysis.strengths] }
                          return vals.length > 0
                            ? vals.map((s: string, i: number) => <li key={i}>{s}</li>)
                            : <li>Strong project experience and technical terminology.</li>
                        })()}
                      </ul>
                    </div>
                  </div>

                  <div className="p-3 bg-amber-50 rounded-lg flex items-start gap-2">
                    <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5 shrink-0" />
                    <div>
                      <h4 className="text-sm font-semibold text-amber-950">Improvements</h4>
                      <ul className="text-xs text-amber-800 mt-1 space-y-0.5 list-disc list-inside">
                        {(() => {
                          let vals: string[] = []
                          if (Array.isArray(analysis.recommendations)) vals = analysis.recommendations
                          else if (typeof analysis.recommendations === 'string') try { vals = JSON.parse(analysis.recommendations) } catch { if (analysis.recommendations) vals = [analysis.recommendations] }
                          return vals.length > 0
                            ? vals.map((s: string, i: number) => <li key={i}>{s}</li>)
                            : <li>Add quantitative impact metrics to project descriptions.</li>
                        })()}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
