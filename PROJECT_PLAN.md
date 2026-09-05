# AI-Powered Internship & Career Intelligence Platform

## Project Architecture & Implementation Plan

---

## 1. SYSTEM ARCHITECTURE OVERVIEW

The platform follows a modern full-stack architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ │
│  │Dashboard│ │ Profile │ │ Resume  │ │Opportun │ │  Admin   │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │ REST API (HTTP)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │  Auth   │ │ Resume  │ │ Match   │ │  Career │ │  Admin  │ │
│  │ Router  │ │ Parser  │ │ Engine  │ │  AI     │ │ Router  │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │  Users   │ │Opportunit│ │ Skills   │ │ Applications     │  │
│  │  Tables  │ │   ies    │ │ Vector   │ │ & Tracking       │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. DATABASE SCHEMA DESIGN

### Core Tables

```sql
-- Users & Authentication
users (id, email, password_hash, role, created_at, updated_at)
user_profiles (user_id, first_name, last_name, phone, location, profile_photo, 
               linkedin, github, portfolio, is_active)

-- Education
education (id, user_id, degree, college, university, semester, cgpa, 
           graduation_year, start_date, end_date)

-- Skills (with vector embeddings for semantic matching)
skills (id, name, category, embedding vector(384))
user_skills (user_id, skill_id, proficiency_level)

-- Projects
projects (id, user_id, title, description, technologies, github_url, 
          live_url, role, start_date, end_date)

-- Certifications
certifications (id, user_id, certificate_name, issuer, issue_date, 
                credential_url)

-- Experience
experiences (id, user_id, company, role, duration, description, 
             start_date, end_date)

-- Resume Management
resumes (id, user_id, file_name, file_path, file_type, uploaded_at)
resume_parsing (resume_id, extracted_data JSONB, parse_status)
resume_analysis (resume_id, overall_score, skills_score, projects_score,
                 experience_score, keywords_score, formatting_score,
                 strengths JSONB, weaknesses JSONB, recommendations JSONB)

-- Opportunities Database
opportunities (id, title, company, description, location, work_type,
               stipend, salary, employment_type, education_requirements,
               experience_requirements, application_deadline, application_url,
               source, posting_date, status, is_verified, created_at)
opportunity_skills (opportunity_id, skill_id, is_required)

-- Recommendations
recommendations (id, user_id, opportunity_id, overall_score, skill_match,
                 semantic_similarity, education_match, experience_match,
                 location_match, project_relevance, matched_skills JSONB,
                 missing_skills JSONB, explanation, created_at)

-- Application Tracking
applications (id, user_id, opportunity_id, status, applied_date,
              notes, interview_date, salary_offered, created_at, updated_at)

-- Career Intelligence
skill_gaps (id, user_id, target_role, current_skills JSONB,
            missing_skills JSONB, priority, created_at)

career_roadmaps (id, user_id, target_role, current_level,
                 target_level, progress_percentage, created_at)
roadmap_items (roadmap_id, skill_name, description, difficulty,
               estimated_hours, prerequisites, resources JSONB,
               is_completed, completed_at)

career_scores (id, user_id, technical_skills_score, projects_score,
               resume_score, certifications_score, experience_score,
               interview_readiness_score, overall_score, calculated_at)

-- Interview Preparation
interview_sessions (id, user_id, opportunity_id, difficulty, interview_type,
                    started_at, completed_at, overall_score)
interview_questions (session_id, question, question_type, user_answer,
                     ai_evaluation, score)

-- AI Chat History
chat_messages (id, user_id, role, content, created_at)

-- Notifications
notifications (id, user_id, type, title, message, is_read, created_at)

-- Admin
admin_analytics (id, date, total_users, active_users, total_opportunities,
                 total_applications, total_interviews, created_at)
```

---

## 3. API STRUCTURE

### Authentication Endpoints
```
POST   /api/auth/register          - User registration
POST   /api/auth/login             - User login (returns JWT)
POST   /api/auth/logout            - User logout
POST   /api/auth/refresh           - Refresh JWT token
GET    /api/auth/me                - Get current user
```

### Profile Management
```
GET    /api/users/me               - Get current user profile
PUT    /api/users/me               - Update profile
GET    /api/users/me/education     - Get education details
POST   /api/users/me/education     - Add education
PUT    /api/users/me/education/{id} - Update education
DELETE /api/users/me/education/{id} - Delete education
GET    /api/users/me/skills        - Get user skills
POST   /api/users/me/skills        - Add skill
DELETE /api/users/me/skills/{id}   - Remove skill
GET    /api/users/me/projects      - Get projects
POST   /api/users/me/projects      - Add project
PUT    /api/users/me/projects/{id} - Update project
DELETE /api/users/me/projects/{id} - Delete project
GET    /api/users/me/certifications - Get certifications
POST   /api/users/me/certifications - Add certification
DELETE /api/users/me/certifications/{id} - Delete certification
GET    /api/users/me/experiences   - Get experience
POST   /api/users/me/experiences   - Add experience
DELETE /api/users/me/experiences/{id} - Delete experience
```

### Resume Management
```
POST   /api/resume/upload          - Upload resume (PDF/DOCX)
GET    /api/resume                 - Get user's resume
DELETE /api/resume                 - Delete resume
POST   /api/resume/analyze         - Analyze resume
GET    /api/resume/analysis        - Get resume analysis
GET    /api/resume/extracted       - Get extracted data
```

### Opportunities
```
GET    /api/opportunities          - List opportunities (with filters)
GET    /api/opportunities/{id}     - Get opportunity details
GET    /api/opportunities/search   - Search opportunities
GET    /api/opportunities/featured - Get featured opportunities
```

### Recommendations
```
GET    /api/recommendations        - Get personalized recommendations
GET    /api/recommendations/{id}   - Get recommendation details
GET    /api/recommendations/explain/{id} - Get explanation
```

### Career Intelligence
```
GET    /api/skills/gaps            - Get skill gaps for target role
POST   /api/skills/gaps/analyze    - Analyze skill gaps
GET    /api/career/roadmap         - Get career roadmap
POST   /api/career/roadmap/generate - Generate roadmap
PUT    /api/career/roadmap/items/{id} - Mark item complete
GET    /api/career/readiness       - Get career readiness score
GET    /api/career/analytics       - Get career analytics
```

### Applications
```
GET    /api/applications           - List applications
POST   /api/applications           - Apply to opportunity
PUT    /api/applications/{id}      - Update application status
DELETE /api/applications/{id}      - Withdraw application
GET    /api/applications/stats     - Get application statistics
```

### Interview Preparation
```
POST   /api/interview/start        - Start interview session
POST   /api/interview/answer       - Submit answer
GET    /api/interview/history      - Get interview history
GET    /api/interview/session/{id} - Get session details
GET    /api/interview/questions    - Get AI-generated questions
```

### AI Chat
```
POST   /api/ai/chat                - Send message to AI assistant
GET    /api/ai/chat/history        - Get chat history
DELETE /api/ai/chat/history        - Clear chat history
```

### Admin Endpoints
```
GET    /api/admin/dashboard        - Admin dashboard stats
GET    /api/admin/users            - Manage users
PUT    /api/admin/users/{id}       - Update user
GET    /api/admin/opportunities    - Manage opportunities
POST   /api/admin/opportunities    - Create opportunity
PUT    /api/admin/opportunities/{id} - Update opportunity
DELETE /api/admin/opportunities/{id} - Delete opportunity
GET    /api/admin/skills           - Manage skills
POST   /api/admin/skills           - Create skill
GET    /api/admin/analytics        - Platform analytics
GET    /api/admin/reports          - Generate reports
```

---

## 4. AI/ML METHODOLOGY

### Resume Parsing
- **Libraries**: PyMuPDF (PDF), python-docx (DOCX)
- **Process**:
  1. Extract raw text from document
  2. Use spaCy NER for entity extraction (names, emails, phones)
  3. Rule-based section detection (Education, Experience, Skills, Projects)
  4. Regex patterns for学历 details, dates, URLs
  5. Store structured JSON output

### Resume Analysis (Scoring)
- **Scoring Criteria**:
  - Skills (20%): Number of technical skills, relevance to target roles
  - Projects (20%): Quantity, description quality, technologies used, URLs
  - Experience (20%): Relevance, duration, measurable achievements
  - Keywords (20%): Industry keywords, action verbs, ATS optimization
  - Formatting (20%): Structure, consistency, readability

### Semantic Matching (Vector Similarity)
- **Model**: sentence-transformers (all-MiniLM-L6-v2, 384 dimensions)
- **Process**:
  1. Generate embeddings for student profile (skills + projects + description)
  2. Generate embeddings for job descriptions
  3. Calculate cosine similarity between vectors
  4. Combine with rule-based scoring

### Skill Gap Analysis
- **Algorithm**:
  1. Define skill ontologies for common roles (Full Stack, Data Science, etc.)
  2. Compare user's current skills against required skills
  3. Categorize gaps by priority (HIGH/MEDIUM/LOW)
  4. Generate personalized learning recommendations

### Career Roadmap Generation
- **Approach**:
  1. Identify current skill level from profile
  2. Define skill prerequisites and learning path
  3. Estimate learning time for each skill
  4. Provide curated resources (free courses, tutorials)

---

## 5. MATCHING ALGORITHM

### Weighted Score Calculation

```
Overall Match = (Skill × 0.35) + (Semantic × 0.25) + 
                (Education × 0.10) + (Experience × 0.10) + 
                (Location × 0.10) + (Project Relevance × 0.10)
```

### Skill Matching Algorithm
```
1. Extract user skills from profile
2. Extract job required/preferred skills
3. Calculate:
   - required_skill_match = (matched_required / total_required) × 100
   - preferred_skill_match = (matched_preferred / total_preferred) × 100
4. Weighted average based on required vs preferred
```

### Explainability
For each recommendation, provide:
- List of matched skills (✓)
- List of missing skills (⚠)
- Specific recommendations to improve

---

## 6. DEVELOPMENT PHASES

### Phase 1: Foundation (Week 1-2)
- Project setup (React + Vite + FastAPI)
- Database setup (PostgreSQL + pgvector)
- Authentication system (JWT)
- Basic UI layout (Sidebar, Navigation)

### Phase 2: Profile Management (Week 2-3)
- User profile CRUD
- Education, Skills, Projects, Certifications, Experience
- Profile photo upload

### Phase 3: Resume Intelligence (Week 3-4)
- Resume upload (PDF/DOCX)
- Text extraction
- Section parsing
- Resume scoring & analysis

### Phase 4: Opportunity Engine (Week 4-5)
- Opportunity CRUD (Admin)
- Search & filters
- Pagination
- Seed data with 50+ realistic opportunities

### Phase 5: AI Matching (Week 5-6)
- Skill matching algorithm
- Semantic similarity (vector embeddings)
- Hybrid recommendation engine
- Explainable match scores

### Phase 6: Career Intelligence (Week 6-7)
- Skill gap analyzer
- Career roadmap generator
- Career readiness calculator

### Phase 7: Application Tracking (Week 7-8)
- Application management
- Status tracking
- Kanban board UI

### Phase 8: Interview AI (Week 8-9)
- Question generation
- Resume-based questions
- Answer evaluation

### Phase 9: AI Assistant (Week 9)
- Chat interface
- Profile-aware responses

### Phase 10: Admin Panel (Week 9-10)
- User management
- Opportunity management
- Analytics dashboard

### Phase 11: Testing & Polish (Week 10-11)
- API testing
- Frontend testing
- Responsive testing
- Bug fixes

### Phase 12: Documentation (Week 11-12)
- README
- API docs
- Project report material

---

## 7. TECHNOLOGY STACK DETAILS

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type safety |
| Vite | 5.x | Build tool |
| Tailwind CSS | 3.x | Styling |
| React Router | 6.x | Navigation |
| Recharts | 2.x | Charts/Analytics |
| Lucide React | latest | Icons |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Runtime |
| FastAPI | 0.109 | Web Framework |
| Pydantic | 2.x | Validation |
| SQLAlchemy | 2.x | ORM |
| JWT | - | Authentication |
| Passlib | - | Password hashing |

### Database
| Technology | Version | Purpose |
|------------|---------|---------|
| PostgreSQL | 15 | Primary DB |
| pgvector | latest | Vector similarity |

### AI/ML
| Technology | Purpose |
|------------|---------|
| sentence-transformers | Semantic embeddings |
| scikit-learn | ML algorithms |
| spaCy | NLP/NER |
| PyMuPDF | PDF extraction |
| python-docx | DOCX extraction |

---

## 8. FILE STRUCTURE

```
career-intelligence-platform/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/        (Button, Input, Card, Modal, etc.)
│   │   │   ├── layout/        (Sidebar, Navbar, Layout)
│   │   │   ├── dashboard/     (Stats, Charts)
│   │   │   ├── profile/       (ProfileForm, EducationCard)
│   │   │   ├── resume/        (Upload, Analysis)
│   │   │   ├── opportunities/ (Card, Filters, List)
│   │   │   ├── matching/      (MatchScore, SkillGap)
│   │   │   ├── career/        (Roadmap, Readiness)
│   │   │   ├── applications/  (Kanban, ApplicationCard)
│   │   │   ├── interview/     (Question, Practice)
│   │   │   └── admin/         (Dashboard, Tables)
│   │   ├── pages/
│   │   │   ├── auth/          (Login, Register)
│   │   │   ├── student/       (All student pages)
│   │   │   └── admin/         (All admin pages)
│   │   ├── contexts/
│   │   │   ├── AuthContext.tsx
│   │   │   └── AppContext.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useApi.ts
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.service.ts
│   │   │   └── ...
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── utils/
│   │   │   ├── helpers.ts
│   │   │   └── constants.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── resume.py
│   │   │   │   ├── opportunities.py
│   │   │   │   ├── recommendations.py
│   │   │   │   ├── skills.py
│   │   │   │   ├── career.py
│   │   │   │   ├── applications.py
│   │   │   │   ├── interview.py
│   │   │   │   ├── ai.py
│   │   │   │   └── admin.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── profile.py
│   │   │   ├── resume.py
│   │   │   ├── opportunity.py
│   │   │   ├── application.py
│   │   │   └── ...
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── resume_parser.py
│   │   │   ├── resume_analyzer.py
│   │   │   ├── matching_engine.py
│   │   │   ├── skill_gap.py
│   │   │   ├── roadmap.py
│   │   │   └── career_score.py
│   │   ├── ml/
│   │   │   ├── embeddings.py
│   │   │   └── similarity.py
│   │   ├── utils/
│   │   │   └── helpers.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_resume.py
│   │   ├── test_matching.py
│   │   └── test_api.py
│   ├── requirements.txt
│   ├── .env.example
│   └── alembic.ini
│
├── database/
│   ├── migrations/
│   └── seed/
│       └── seed_data.sql
│
├── docker-compose.yml
├── Dockerfile.frontend
├── Dockerfile.backend
├── README.md
└── .gitignore
```

---

## 9. ENVIRONMENT VARIABLES

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/career_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=career_db

# JWT
SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# File Upload
MAX_FILE_SIZE_MB=5
UPLOAD_DIR=./uploads

# AI/ML (optional)
SENTENCE_TRANSFORMERS_MODEL=all-MiniLM-L6-v2

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:8000

# Environment
DEBUG=true
```

---

## 10. RUNNING THE APPLICATION

### Using Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python -m uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 11. KEY IMPLEMENTATION NOTES

1. **Real AI, Not Fake**: All AI features use actual libraries (sentence-transformers, spaCy)
2. **Vector Similarity**: Uses pgvector for efficient similarity search
3. **Semantic Matching**: Generates real embeddings for job matching
4. **No Hardcoded Data**: All statistics come from actual database queries
5. **Production Patterns**: JWT auth, password hashing, input validation
6. **Responsive UI**: Works on mobile, tablet, and desktop

---

## 12. SUCCESS CRITERIA

The completed application demonstrates:
- ✓ Complete user flow from registration to job application
- ✓ Real AI-powered resume parsing and analysis
- ✓ Semantic job matching with explainable scores
- ✓ Personalized career roadmaps and skill gaps
- ✓ Interview preparation with AI evaluation
- ✓ Admin dashboard with platform analytics
- ✓ Professional SaaS-quality UI
- ✓ Production-ready security patterns