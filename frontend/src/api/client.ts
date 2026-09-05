import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post('/auth/login', { email, password }),
  register: (data: any) => apiClient.post('/auth/register', data),
  getMe: () => apiClient.get('/auth/me'),
}

// Dashboard API
export const dashboardApi = {
  getStats: () => apiClient.get('/dashboard'),
}

// Profile / Users API
export const userApi = {
  getProfile: () => apiClient.get('/users/me'),
  updateProfile: (data: any) => apiClient.put('/users/me', data),
  getEducation: () => apiClient.get('/users/me/education'),
  addEducation: (data: any) => apiClient.post('/users/me/education', data),
  getSkills: () => apiClient.get('/users/me/skills'),
  addSkill: (data: any) => apiClient.post('/users/me/skills', data),
  getProjects: () => apiClient.get('/users/me/projects'),
  addProject: (data: any) => apiClient.post('/users/me/projects', data),
}

// Resume API
export const resumeApi = {
  upload: (formData: FormData) =>
    apiClient.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getResume: () => apiClient.get('/resume'),
  getAnalysis: () => apiClient.get('/resume/analysis'),
}

// Opportunities API
export const opportunitiesApi = {
  getOpportunities: (params?: any) => apiClient.get('/opportunities', { params }),
  getOpportunity: (id: number) => apiClient.get(`/opportunities/${id}`),
}

// Recommendations API
export const recommendationsApi = {
  getRecommendations: () => apiClient.get('/recommendations'),
  refresh: () => apiClient.post('/recommendations/refresh'),
}

// Skills API
export const skillsApi = {
  getSkills: () => apiClient.get('/skills'),
  getTrending: () => apiClient.get('/skills/trending'),
}

// Career / Skill Gap / Roadmap API
export const careerApi = {
  getGaps: () => apiClient.get('/career/gaps'),
  analyzeGaps: (targetRole: string) => apiClient.post(`/career/gaps/analyze?target_role=${targetRole}`),
  getRoadmap: () => apiClient.get('/career/roadmap'),
  generateRoadmap: (targetRole: string) => apiClient.post(`/career/roadmap/generate?target_role=${targetRole}`),
  toggleRoadmapItem: (itemId: number) => apiClient.put(`/career/roadmap/items/${itemId}`),
  getReadiness: () => apiClient.get('/career/readiness'),
}

// Applications API
export const applicationsApi = {
  getApplications: () => apiClient.get('/applications'),
  createApplication: (opportunityId: number) => apiClient.post(`/applications/?opportunity_id=${opportunityId}`),
  updateApplication: (id: number, status: string) => apiClient.put(`/applications/${id}?status=${status}`),
  getStats: () => apiClient.get('/applications/stats'),
}

// Interview API
export const interviewApi = {
  startSession: (difficulty: string, type: string) =>
    apiClient.post(`/interview/start?difficulty=${difficulty}&interview_type=${type}`),
  submitAnswer: (sessionId: number, questionId: number, answer: string) =>
    apiClient.post(`/interview/answer?session_id=${sessionId}&question_id=${questionId}&answer=${encodeURIComponent(answer)}`),
  getHistory: () => apiClient.get('/interview/history'),
  getSession: (sessionId: number) => apiClient.get(`/interview/session/${sessionId}`),
}

// AI Assistant API
export const aiApi = {
  chat: (message: string) => apiClient.post(`/ai/chat?message=${message}`),
  getChatHistory: () => apiClient.get('/ai/chat/history'),
}

// Admin API
export const adminApi = {
  getDashboardStats: () => apiClient.get('/admin/dashboard'),
  getUsers: (skip: number = 0, limit: number = 100) =>
    apiClient.get('/admin/users', { params: { skip, limit } }),
  updateUser: (userId: number, updates: { is_active?: boolean; role?: string }) =>
    apiClient.put(`/admin/users/${userId}`, updates),
  deleteUser: (userId: number) =>
    apiClient.delete(`/admin/users/${userId}`),
  getOpportunities: (status?: string, skip: number = 0, limit: number = 100) =>
    apiClient.get('/admin/opportunities', { params: { status, skip, limit } }),
  createOpportunity: (data: any) => apiClient.post('/admin/opportunities', data),
  getAnalytics: () => apiClient.get('/admin/analytics'),
}

export default apiClient
