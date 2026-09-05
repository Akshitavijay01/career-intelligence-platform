import { useState, useEffect } from 'react'
import { userApi } from '@/api/client'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/common/Card'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { Settings, Save, Bell, Shield, User, Lock, Mail, Eye } from 'lucide-react'
import { toast } from 'sonner'

type SettingsTab = 'profile' | 'notifications' | 'security'

export default function SettingsPage() {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [activeTab, setActiveTab] = useState<SettingsTab>('profile')

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    location: '',
    phone: '',
    linkedin: '',
    github: ''
  })

  const [notifications, setNotifications] = useState({
    email_opportunities: true,
    email_recommendations: true,
    email_applications: true,
    email_interviews: true,
    email_weekly_digest: false,
    push_opportunities: true,
    push_recommendations: false,
    push_applications: true,
    push_interviews: true,
  })

  const [security, setSecurity] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
    two_factor_enabled: false,
  })

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await userApi.getProfile()
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

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setSaving(true)
      await userApi.updateProfile(formData)
      toast.success('Profile updated successfully.')
    } catch (err: any) {
      toast.error('Failed to update profile.')
    } finally {
      setSaving(false)
    }
  }

  const handleNotificationsSave = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setSaving(true)
      await new Promise(r => setTimeout(r, 500))
      toast.success('Notification preferences saved.')
    } catch (err: any) {
      toast.error('Failed to save notification preferences.')
    } finally {
      setSaving(false)
    }
  }

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault()
    if (security.new_password !== security.confirm_password) {
      toast.error('New passwords do not match.')
      return
    }
    if (security.new_password.length < 8) {
      toast.error('Password must be at least 8 characters.')
      return
    }
    try {
      setSaving(true)
      await new Promise(r => setTimeout(r, 500))
      toast.success('Password changed successfully.')
      setSecurity({ ...security, current_password: '', new_password: '', confirm_password: '' })
    } catch (err: any) {
      toast.error('Failed to change password.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner message="Loading account settings..." />

  const tabs: { key: SettingsTab; label: string; icon: React.ReactNode }[] = [
    { key: 'profile', label: 'Public Profile', icon: <User className="w-4 h-4" /> },
    { key: 'notifications', label: 'Notifications', icon: <Bell className="w-4 h-4" /> },
    { key: 'security', label: 'Security', icon: <Shield className="w-4 h-4" /> },
  ]

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <Settings className="w-6 h-6 text-gray-600" /> Account Settings
        </h1>
        <p className="text-gray-500 text-sm">Manage your profile visibility, notifications, and security</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Sidebar tabs */}
        <div className="md:col-span-1 space-y-2">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`w-full flex items-center justify-between p-3 font-medium rounded-lg transition-colors ${
                activeTab === tab.key
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center gap-2">{tab.icon} {tab.label}</div>
            </button>
          ))}
        </div>

        {/* Content panel */}
        {activeTab === 'profile' && (
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>Update your public facing details</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleProfileSave} className="space-y-4">
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
        )}

        {activeTab === 'notifications' && (
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>Choose how and when you want to be notified</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleNotificationsSave} className="space-y-6">
                {/* Email Notifications */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2 mb-3">
                    <Mail className="w-4 h-4" /> Email Notifications
                  </h3>
                  <div className="space-y-3">
                    {[
                      { key: 'email_opportunities', label: 'New job opportunities', desc: 'Get notified when new internships or jobs match your skills' },
                      { key: 'email_recommendations', label: 'Skill recommendations', desc: 'Receive updates on recommended skills to learn' },
                      { key: 'email_applications', label: 'Application updates', desc: 'Status changes on your job applications' },
                      { key: 'email_interviews', label: 'Interview reminders', desc: 'Reminders before scheduled interviews' },
                      { key: 'email_weekly_digest', label: 'Weekly digest', desc: 'A weekly summary of your activity and new opportunities' },
                    ].map((item) => (
                      <label key={item.key} className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={(notifications as any)[item.key]}
                          onChange={(e) => setNotifications({ ...notifications, [item.key]: e.target.checked })}
                          className="mt-0.5 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">{item.label}</div>
                          <div className="text-xs text-gray-500">{item.desc}</div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Push Notifications */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2 mb-3">
                    <Bell className="w-4 h-4" /> Push Notifications
                  </h3>
                  <div className="space-y-3">
                    {[
                      { key: 'push_opportunities', label: 'New job opportunities', desc: 'Real-time alerts for matching jobs' },
                      { key: 'push_recommendations', label: 'Skill recommendations', desc: 'Alerts when new skills are trending in your field' },
                      { key: 'push_applications', label: 'Application updates', desc: 'Instant notification on application status changes' },
                      { key: 'push_interviews', label: 'Interview reminders', desc: 'Push notification 15 minutes before an interview' },
                    ].map((item) => (
                      <label key={item.key} className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={(notifications as any)[item.key]}
                          onChange={(e) => setNotifications({ ...notifications, [item.key]: e.target.checked })}
                          className="mt-0.5 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <div>
                          <div className="text-sm font-medium text-gray-900">{item.label}</div>
                          <div className="text-xs text-gray-500">{item.desc}</div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="pt-4 flex justify-end">
                  <button
                    type="submit"
                    disabled={saving}
                    className="flex items-center gap-2 px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-70"
                  >
                    <Save className="w-4 h-4" />
                    {saving ? 'Saving...' : 'Save Preferences'}
                  </button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {activeTab === 'security' && (
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Security Settings</CardTitle>
              <CardDescription>Manage your password and account security</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Change Password */}
                <form onSubmit={handlePasswordChange} className="space-y-4">
                  <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
                    <Lock className="w-4 h-4" /> Change Password
                  </h3>
                  <div className="space-y-3">
                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-700">Current Password</label>
                      <input
                        type="password"
                        value={security.current_password}
                        onChange={(e) => setSecurity({ ...security, current_password: e.target.value })}
                        className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        required
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-1">
                        <label className="text-sm font-medium text-gray-700">New Password</label>
                        <input
                          type="password"
                          value={security.new_password}
                          onChange={(e) => setSecurity({ ...security, new_password: e.target.value })}
                          className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          required
                          minLength={8}
                        />
                      </div>
                      <div className="space-y-1">
                        <label className="text-sm font-medium text-gray-700">Confirm Password</label>
                        <input
                          type="password"
                          value={security.confirm_password}
                          onChange={(e) => setSecurity({ ...security, confirm_password: e.target.value })}
                          className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          required
                          minLength={8}
                        />
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-end">
                    <button
                      type="submit"
                      disabled={saving}
                      className="flex items-center gap-2 px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-70"
                    >
                      <Lock className="w-4 h-4" />
                      {saving ? 'Updating...' : 'Update Password'}
                    </button>
                  </div>
                </form>

                <hr className="border-gray-200" />

                {/* Two-Factor Authentication */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2 mb-3">
                    <Eye className="w-4 h-4" /> Two-Factor Authentication
                  </h3>
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <div className="text-sm font-medium text-gray-900">Two-factor authentication</div>
                      <div className="text-xs text-gray-500">Add an extra layer of security to your account</div>
                    </div>
                    <button
                      onClick={() => {
                        setSecurity({ ...security, two_factor_enabled: !security.two_factor_enabled })
                        toast.success(
                          security.two_factor_enabled
                            ? 'Two-factor authentication disabled.'
                            : 'Two-factor authentication enabled.'
                        )
                      }}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        security.two_factor_enabled ? 'bg-blue-600' : 'bg-gray-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          security.two_factor_enabled ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                <hr className="border-gray-200" />

                {/* Account Info */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 mb-3">Account Information</h3>
                  <div className="p-4 bg-gray-50 rounded-lg space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Account type</span>
                      <span className="font-medium text-gray-900">Student</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Email verified</span>
                      <span className="font-medium text-green-600">Yes</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Member since</span>
                      <span className="font-medium text-gray-900">September 2026</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
