// User Types
export interface User {
  id: number
  email: string
  role: 'student' | 'admin'
  created_at: string
}

export interface UserProfile {
  id: number
  user_id: number
  first_name: string
  last_name: string
  phone?: string
  location?: string
  profile_photo?: string
  linkedin?: string
  github?: string
  portfolio?: string
  is_active: boolean
}

export interface Education {
  id: number
  user_id: number
  degree: string
  college: string
  university: string
  semester?: number
  cgpa?: number
  graduation_year: number
  start_date?: string
  end_date?: string
}

export interface Skill {
  id: number
  name: string
  category: string
}

export interface UserSkill {
  id: number
  user_id: number
  skill_id: number
  proficiency_level: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  skill?: Skill
}

export interface Project {
  id: number
  user_id: number
  title: string
  description: string
  technologies: string[]
  github_url?: string
  live_url?: string
  role?: string
  start_date?: string
  end_date?: string
}

export interface Certification {
  id: number
  user_id: number
  certificate_name: string
  issuer: string
  issue_date: string
  credential_url?: string
}

export interface Experience {
  id: number
  user_id: number
  company: string
  role: string
  duration: string
  description: string
  start_date?: string
  end_date?: string
}

// Resume Types
export interface Resume {
  id: number
  user_id: number
  file_name: string
  file_path: string
  file_type: string
  uploaded_at: string
}

export interface ResumeAnalysis {
  id: number
  resume_id: number
  overall_score: number
  skills_score: number
  projects_score: number
  experience_score: number
  keywords_score: number
  formatting_score: number
  strengths: string[]
  weaknesses: string[]
  recommendations: string[]
}

// Opportunity Types
export interface Opportunity {
  id: number
  title: string
  company: string
  description: string
  location: string
  work_type: 'remote' | 'hybrid' | 'on-site'
  stipend?: number
  salary?: number
  employment_type: 'internship' | 'full-time' | 'part-time' | 'contract'
  education_requirements: string
  experience_requirements: string
  application_deadline: string
  application_url: string
  source: string
  posting_date: string
  status: 'active' | 'closed' | 'draft'
  is_verified: boolean
  created_at: string
  skills?: Skill[]
}

// Application Types
export type ApplicationStatus = 'saved' | 'applied' | 'assessment' | 'interview' | 'offer' | 'rejected' | 'withdrawn'

export interface Application {
  id: number
  user_id: number
  opportunity_id: number
  status: ApplicationStatus
  applied_date: string
  notes?: string
  interview_date?: string
  salary_offered?: number
  created_at: string
  updated_at: string
  opportunity?: Opportunity
}

// Recommendation Types
export interface Recommendation {
  id: number
  user_id: number
  opportunity_id: number
  overall_score: number
  skill_match: number
  semantic_similarity: number
  education_match: number
  experience_match: number
  location_match: number
  project_relevance: number
  matched_skills: string[]
  missing_skills: string[]
  explanation: string
  created_at: string
  opportunity?: Opportunity
}

// Career Intelligence Types
export interface SkillGap {
  id: number
  user_id: number
  target_role: string
  current_skills: string[]
  missing_skills: string[]
  priority: 'high' | 'medium' | 'low'
  created_at: string
}

export interface RoadmapItem {
  id: number
  roadmap_id: number
  skill_name: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  estimated_hours: number
  prerequisites: string[]
  resources: { name: string; url: string }[]
  is_completed: boolean
  completed_at?: string
}

export interface CareerRoadmap {
  id: number
  user_id: number
  target_role: string
  current_level: string
  target_level: string
  progress_percentage: number
  created_at: string
  items?: RoadmapItem[]
}

export interface CareerScore {
  id: number
  user_id: number
  technical_skills_score: number
  projects_score: number
  resume_score: number
  certifications_score: number
  experience_score: number
  interview_readiness_score: number
  overall_score: number
  calculated_at: string
}

// Interview Types
export interface InterviewSession {
  id: number
  user_id: number
  opportunity_id?: number
  difficulty: 'easy' | 'medium' | 'hard'
  interview_type: 'technical' | 'hr' | 'mixed'
  started_at: string
  completed_at?: string
  overall_score?: number
}

export interface InterviewQuestion {
  id: number
  session_id: number
  question: string
  question_type: 'technical' | 'hr' | 'resume-based'
  user_answer?: string
  ai_evaluation?: string
  score?: number
}

// Chat Types
export interface ChatMessage {
  id: number
  user_id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

// Notification Types
export interface Notification {
  id: number
  user_id: number
  type: 'application' | 'interview' | 'deadline' | 'recommendation' | 'milestone'
  title: string
  message: string
  is_read: boolean
  created_at: string
}

// Admin Types
export interface AdminAnalytics {
  total_users: number
  active_users: number
  total_opportunities: number
  total_applications: number
  total_interviews: number
  most_requested_skills: { skill_name: string; count: number }[]
  popular_job_roles: { role: string; count: number }[]
  application_success_rate: number
  average_career_readiness: number
}

// API Response Types
export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}