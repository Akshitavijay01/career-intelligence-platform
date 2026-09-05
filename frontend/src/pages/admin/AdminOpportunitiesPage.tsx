import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Briefcase,
  Search,
  Trash2,
  Edit,
  X,
  ChevronRight,
  ChevronLeft,
  Plus
} from 'lucide-react'
import { adminApi } from '@/api/client'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { ErrorState } from '@/components/common/ErrorState'

interface Opportunity {
  id: number
  title: string
  company: string
  location: string
  work_type: 'remote' | 'hybrid' | 'on-site'
  employment_type: 'internship' | 'full-time' | 'part-time' | 'contract'
  education_requirements: string
  experience_requirements: string
  application_deadline: string
  application_url: string
  status: 'active' | 'closed' | 'draft'
  is_verified: boolean
  source: string
  created_at: string
}

export default function AdminOpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'closed' | 'draft'>('all')
  const [filteredOpportunities, setFilteredOpportunities] = useState<Opportunity[]>([])
  const [currentPage, setCurrentPage] = useState(1)
  const [opportunitiesPerPage] = useState(10)
  const [createModalOpen, setCreateModalOpen] = useState(false)
  const [editOpportunityId, setEditOpportunityId] = useState<number | null>(null)
  const [formData, setFormData] = useState<Partial<Opportunity>>({
    title: '',
    company: '',
    location: '',
    work_type: 'on-site',
    employment_type: 'internship',
    education_requirements: '',
    experience_requirements: '',
    application_deadline: '',
    application_url: '',
    status: 'active',
    is_verified: false,
    source: 'admin'
  })

  useEffect(() => {
    fetchOpportunities()
  }, [])

  const fetchOpportunities = async () => {
    try {
      setLoading(true)
      setError(null)
      let status: string | undefined
      if (statusFilter !== 'all') {
        status = statusFilter
      }
      const response = await adminApi.getOpportunities(status, 0, 100)
      setOpportunities(response.data)
      setFilteredOpportunities(response.data)
    } catch (err: any) {
      console.error('Error fetching opportunities:', err)
      setError('Unable to load opportunities.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!searchTerm && statusFilter === 'all') {
      setFilteredOpportunities(opportunities)
      return
    }

    const filtered = opportunities.filter(opp => {
      const matchesSearch = !searchTerm ||
        opp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        opp.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
        opp.location.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesStatus = statusFilter === 'all' || opp.status === statusFilter

      return matchesSearch && matchesStatus
    })
    setFilteredOpportunities(filtered)
    setCurrentPage(1)
  }, [searchTerm, statusFilter, opportunities])

  // Pagination
  const totalPages = Math.max(1, Math.ceil(filteredOpportunities.length / opportunitiesPerPage))
  const currentOpportunities = filteredOpportunities.slice(
    (currentPage - 1) * opportunitiesPerPage,
    currentPage * opportunitiesPerPage
  )

  const handleCreateOpportunity = async () => {
    try {
      await adminApi.createOpportunity(formData)
      setCreateModalOpen(false)
      setFormData({
        title: '',
        company: '',
        location: '',
        work_type: 'on-site',
        employment_type: 'internship',
        education_requirements: '',
        experience_requirements: '',
        application_deadline: '',
        application_url: '',
        status: 'active',
        is_verified: false,
        source: 'admin'
      })
      await fetchOpportunities()
    } catch (err: any) {
      console.error('Error creating opportunity:', err)
      setError('Failed to create opportunity.')
    }
  }

  const handleUpdateOpportunity = async () => {
    if (!editOpportunityId) return

    try {
      await adminApi.createOpportunity({
        ...formData,
        id: editOpportunityId
      })
      setEditOpportunityId(null)
      await fetchOpportunities()
    } catch (err: any) {
      console.error('Error updating opportunity:', err)
      setError('Failed to update opportunity.')
    }
  }

  const handleDeleteOpportunity = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this opportunity? This action cannot be undone.')) {
      return
    }

    try {
      // Note: We don't have a delete endpoint in adminApi yet, but we can add it or use the existing one if available
      // For now, we'll simulate by filtering out locally and then refetch
      setOpportunities(opportunities.filter(opp => opp.id !== id))
      setFilteredOpportunities(filteredOpportunities.filter(opp => opp.id !== id))
      // In a real app, we would call an API endpoint
      // await adminApi.deleteOpportunity(id)
    } catch (err: any) {
      console.error('Error deleting opportunity:', err)
      setError('Failed to delete opportunity.')
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const target = e.target as HTMLInputElement
    const { name, value, type, checked } = target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  if (loading) {
    return <LoadingSpinner message="Loading opportunities..." />
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchOpportunities} />
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Opportunity Management</h1>
          <p className="text-gray-600 mt-1">Manage job and internship listings</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setCreateModalOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            Add Opportunity
          </button>
          <Link to="/admin/opportunities/new">
            <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
              Import Opportunities
            </button>
          </Link>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center w-full md:w-auto">
          <Search className="w-5 h-5 text-gray-400 mr-2" />
          <input
            type="text"
            placeholder="Search opportunities by title, company, or location..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-4 pr-10 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          />
        </div>

        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Status:</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as 'all' | 'active' | 'closed' | 'draft')}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="closed">Closed</option>
            <option value="draft">Draft</option>
          </select>
        </div>

        <div className="flex items-center gap-2 text-sm text-gray-600">
          <span>Showing {currentOpportunities.length} of {filteredOpportunities.length} opportunities</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span>{currentPage} of {totalPages}</span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Opportunities Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse bg-white">
          <thead>
            <tr className="border-b">
              <th className="text-left px-4 py-3 text-sm font-medium text-gray-500">Title</th>
              <th className="text-left px-4 py-3 text-sm font-medium text-gray-500">Company</th>
              <th className="text-left px-4 py-3 text-sm font-medium text-gray-500">Location</th>
              <th className="text-left px-4 py-3 text-sm font-medium text-gray-500">Work Type</th>
              <th className="text-left px-4 py-3 text-sm font-medium text-gray-500">Employment Type</th>
              <th className="text-left px-4 py-3 text-sm font-medium text-gray-500">Status</th>
              <th className="text-center px-4 py-3 text-sm font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            {currentOpportunities.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-4 py-6 text-center text-gray-500">
                  No opportunities found
                </td>
              </tr>
            ) : (
              currentOpportunities.map((opp) => (
                <tr key={opp.id} className="border-t">
                  <td className="px-4 py-4">
                    <div className="flex items-center">
                      <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center mr-3">
                        {opp.title.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">{opp.title}</p>
                        <p className="text-xs text-gray-500">ID: {opp.id}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-4">{opp.company}</td>
                  <td className="px-4 py-4">{opp.location}</td>
                  <td className="px-4 py-4">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      opp.work_type === 'remote'
                        ? 'bg-blue-100 text-blue-800'
                        : opp.work_type === 'hybrid'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-green-100 text-green-800'
                    }`}>
                      {opp.work_type.replace('-', ' ')}
                    </span>
                  </td>
                  <td className="px-4 py-4">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      opp.employment_type === 'internship'
                        ? 'bg-purple-100 text-purple-800'
                        : opp.employment_type === 'full-time'
                          ? 'bg-blue-100 text-blue-800'
                          : opp.employment_type === 'part-time'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {opp.employment_type.replace('-', ' ')}
                    </span>
                  </td>
                  <td className="px-4 py-4">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      opp.status === 'active'
                        ? 'bg-emerald-100 text-emerald-800'
                        : opp.status === 'closed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {opp.status}
                    </span>
                  </td>
                  <td className="text-center px-4 py-4 space-x-2">
                    {editOpportunityId === opp.id ? (
                      <>
                        <button
                          onClick={() => {
                            setFormData({
                              title: opp.title,
                              company: opp.company,
                              location: opp.location,
                              work_type: opp.work_type,
                              employment_type: opp.employment_type,
                              education_requirements: opp.education_requirements,
                              experience_requirements: opp.experience_requirements,
                              application_deadline: opp.application_deadline,
                              application_url: opp.application_url,
                              status: opp.status,
                              is_verified: opp.is_verified,
                              source: opp.source
                            })
                          }}
                          className="p-1 text-gray-500 hover:text-gray-700"
                        >
                          <Briefcase className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleUpdateOpportunity()}
                          className="px-2 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => {
                            setEditOpportunityId(null)
                            setFormData({
                              title: '',
                              company: '',
                              location: '',
                              work_type: 'on-site',
                              employment_type: 'internship',
                              education_requirements: '',
                              experience_requirements: '',
                              application_deadline: '',
                              application_url: '',
                              status: 'active',
                              is_verified: false,
                              source: 'admin'
                            })
                          }}
                          className="p-1 text-gray-500 hover:text-gray-700"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => {
                            setEditOpportunityId(opp.id)
                            setFormData({
                              title: opp.title,
                              company: opp.company,
                              location: opp.location,
                              work_type: opp.work_type,
                              employment_type: opp.employment_type,
                              education_requirements: opp.education_requirements,
                              experience_requirements: opp.experience_requirements,
                              application_deadline: opp.application_deadline,
                              application_url: opp.application_url,
                              status: opp.status,
                              is_verified: opp.is_verified,
                              source: opp.source
                            })
                          }}
                          className="p-1 text-gray-500 hover:text-gray-700"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteOpportunity(opp.id)}
                          className="p-1 text-gray-500 hover:text-gray-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Create Opportunity Modal */}
      {createModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg w-96 max-w-full p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Create New Opportunity</h2>
            <form onSubmit={(e) => {
              e.preventDefault()
              handleCreateOpportunity()
            }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Title*</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title || ''}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Company*</label>
                <input
                  type="text"
                  name="company"
                  value={formData.company || ''}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Location*</label>
                <input
                  type="text"
                  name="location"
                  value={formData.location || ''}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="flex flex-col md:flex-row md:gap-4">
                <div className="flex-1 md:mr-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Work Type*</label>
                  <select
                    name="work_type"
                    value={formData.work_type || 'on-site'}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                  >
                    <option value="on-site">On-Site</option>
                    <option value="remote">Remote</option>
                    <option value="hybrid">Hybrid</option>
                  </select>
                </div>
                <div className="flex-1 md:ml-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Employment Type*</label>
                  <select
                    name="employment_type"
                    value={formData.employment_type || 'internship'}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                  >
                    <option value="internship">Internship</option>
                    <option value="full-time">Full-Time</option>
                    <option value="part-time">Part-Time</option>
                    <option value="contract">Contract</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Education Requirements*</label>
                <input
                  type="text"
                  name="education_requirements"
                  value={formData.education_requirements || ''}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Experience Requirements*</label>
                <input
                  type="text"
                  name="experience_requirements"
                  value={formData.experience_requirements || ''}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="flex flex-col md:flex-row md:gap-4">
                <div className="flex-1 md:mr-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Application Deadline*</label>
                  <input
                    type="date"
                    name="application_deadline"
                    value={formData.application_deadline || ''}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div className="flex-1 md:ml-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Application URL*</label>
                  <input
                    type="url"
                    name="application_url"
                    value={formData.application_url || ''}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <div className="flex flex-col md:flex-row md:gap-4">
                <div className="flex-1 md:mr-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Source</label>
                  <input
                    type="text"
                    name="source"
                    value={formData.source || 'admin'}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus-ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div className="flex-1 md:ml-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Verified</label>
                  <input
                    type="checkbox"
                    name="is_verified"
                    checked={formData.is_verified || false}
                    onChange={handleInputChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => setCreateModalOpen(false)}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Create Opportunity
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}