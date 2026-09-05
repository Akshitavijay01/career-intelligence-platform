import { useState, useEffect } from 'react'
import { userApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { Settings, Save, Bell, Shield, User } from 'lucide-react'
import { toast } from 'sonner'

export default function SettingsPage() {
  const [profile] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    location: '',
    phone: '',
    linkedin: '',
    github: ''
  })

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await userApi.getProfile()
        console.log(profile)
        if (res.data) {
          setFormData({
            first_name: res.data.first_name || '',
            last_name: res.data.last_name || '',
            location: res.data.location || '',
            phone: res.data.phone || '',
            linkedin: res.data.linkedin || '',
            github: res.data.github || ''
          })
        }
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setSaving(true)
      await userApi.updateProfile(formData)
      toast.success('Your preferences have been saved.')
    } catch (err: any) {
      toast.error('Failed to update settings.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner message="Loading account settings..." />

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Settings className="w-6 h-6 text-gray-600" /> Account Settings
        </h1>
        <p className="text-gray-500 text-sm">Manage your profile visibility, notifications, and security</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 space-y-2">
          <button className="w-full flex items-center justify-between p-3 bg-blue-50 text-blue-700 font-medium rounded-lg">
            <div className="flex items-center gap-2"><User className="w-4 h-4" /> Public Profile</div>
          </button>
          <button className="w-full flex items-center justify-between p-3 text-gray-600 hover:bg-gray-50 font-medium rounded-lg transition-colors">
            <div className="flex items-center gap-2"><Bell className="w-4 h-4" /> Notifications</div>
          </button>
          <button className="w-full flex items-center justify-between p-3 text-gray-600 hover:bg-gray-50 font-medium rounded-lg transition-colors">
            <div className="flex items-center gap-2"><Shield className="w-4 h-4" /> Security</div>
          </button>
        </div>

        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
            <CardDescription>Update your public facing details</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-gray-700">First Name</label>
                  <input
                    type="text"
                    value={formData.first_name}
                    onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-sm font-medium text-gray-700">Last Name</label>
                  <input
                    type="text"
                    value={formData.last_name}
                    onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-700">Location</label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({...formData, location: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g. San Francisco, CA or Remote"
                />
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-gray-700">LinkedIn URL</label>
                  <input
                    type="url"
                    value={formData.linkedin}
                    onChange={(e) => setFormData({...formData, linkedin: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-sm font-medium text-gray-700">GitHub URL</label>
                  <input
                    type="url"
                    value={formData.github}
                    onChange={(e) => setFormData({...formData, github: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="pt-4 flex justify-end">
                <button
                  type="submit"
                  disabled={saving}
                  className="flex items-center gap-2 px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-70"
                >
                  <Save className="w-4 h-4" />
                  {saving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
