import { useState, useEffect } from 'react'
import { userApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'
import { Mail, MapPin, Award, BookOpen } from 'lucide-react'

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null)
  const [skills, setSkills] = useState<any[]>([])
  const [education, setEducation] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadProfile = async () => {
    try {
      setLoading(true)
      setError(null)
      const [profileRes, skillsRes, eduRes] = await Promise.all([
        userApi.getProfile(),
        userApi.getSkills(),
        userApi.getEducation(),
      ])
      setProfile(profileRes.data)
      setSkills(skillsRes.data || [])
      setEducation(eduRes.data || [])
    } catch (err: any) {
      console.error(err)
      setError('Unable to load profile data.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProfile()
    const refetch = () => loadProfile()
    window.addEventListener('careerai:profile-updated', refetch)
    const onVisibility = () => { if (document.visibilityState === 'visible') loadProfile() }
    document.addEventListener('visibilitychange', onVisibility)
    window.addEventListener('focus', refetch)
    return () => {
      window.removeEventListener('careerai:profile-updated', refetch)
      document.removeEventListener('visibilitychange', onVisibility)
      window.removeEventListener('focus', refetch)
    }
  }, [])

  if (loading) return <LoadingSpinner message="Loading profile..." />
  if (error) return <ErrorState message={error} onRetry={loadProfile} />

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Student Profile</h1>
        <p className="text-gray-500 text-sm">Manage your profile details, skills, and academic history</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Personal Info</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-lg">
                {profile?.first_name?.[0] || 'U'}
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{profile?.first_name} {profile?.last_name}</h3>
                <p className="text-xs text-gray-500">{profile?.user_id}</p>
              </div>
            </div>

            <div className="space-y-2 pt-4 border-t text-sm">
              <div className="flex items-center gap-2 text-gray-600">
                <MapPin className="w-4 h-4 text-gray-400" />
                <span>{profile?.location || 'Not provided'}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Mail className="w-4 h-4 text-gray-400" />
                <span>{profile?.user_id}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="w-5 h-5 text-blue-600" /> Skills
              </CardTitle>
              <CardDescription>Verified technical and soft skills</CardDescription>
            </CardHeader>
            <CardContent>
              {skills.length === 0 ? (
                <p className="text-sm text-gray-500">No skills added yet.</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill, index) => (
                    <span key={index} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-medium">
                      {skill.name || skill.skill_id}
                    </span>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-emerald-600" /> Education
              </CardTitle>
              <CardDescription>Academic background and degrees</CardDescription>
            </CardHeader>
            <CardContent>
              {education.length === 0 ? (
                <p className="text-sm text-gray-500">No education entries found.</p>
              ) : (
                <div className="space-y-3">
                  {education.map((edu, index) => (
                    <div key={index} className="p-3 bg-gray-50 rounded-lg">
                      <h4 className="font-medium text-gray-900">{edu.degree}</h4>
                      <p className="text-sm text-gray-500">{edu.university || edu.college}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
