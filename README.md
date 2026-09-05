# AI-Powered Career Intelligence Platform

## 🚀 Quick Start (Windows Local Development)

This platform runs locally on your Windows laptop with **NO external database required**. Uses SQLite for easy setup.

### Prerequisites
- **Python 3.10 or higher** - [Download here](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download here](https://nodejs.org/)
- **Git** (optional) - [Download here](https://git-scm.com/downloads)

### Installation & Running

#### Step 1: Download the Project
If you have the project folder, open PowerShell and navigate to it:
```powershell
cd C:\Users\hp\OneDrive\Desktop\career-intelligence-platform
```

#### Step 2: Start the Backend (FastAPI + SQLite)
```powershell
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies (this will take a few minutes)
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

**Backend will run at:** http://localhost:8000

**API Documentation:** http://localhost:8000/docs

#### Step 3: Start the Frontend (React)
Open a **NEW PowerShell window** and run:
```powershell
# Navigate to frontend folder
cd C:\Users\hp\OneDrive\Desktop\career-intelligence-platform\frontend

# Install dependencies (this will take a few minutes)
npm install

# Start the development server
npm run dev
```

**Frontend will run at:** http://localhost:5173

### Access the Application
Open your browser and go to: **http://localhost:5173**

---

## 🎯 Features

### For Students
- **AI Resume Analysis** - Upload PDF/DOCX and get instant 0-100 scoring
- **Smart Job Matching** - AI-powered matching with explainable scores
- **Skill Gap Analysis** - Identify missing skills for your target role
- **Career Roadmap** - Personalized learning paths
- **Interview Preparation** - AI-generated questions
- **Application Tracking** - Kanban-style board
- **Career Readiness Score** - Comprehensive analysis

### For Admins
- **Dashboard Analytics** - Platform statistics
- **User Management** - Manage accounts
- **Opportunity Management** - Add job/internship listings

---

## 🛠️ Technology Stack

### Frontend
- React 18 with TypeScript
- Vite (Build tool)
- Tailwind CSS
- React Router
- Recharts (Analytics)

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy 2.0
- SQLite (No server needed!)
- JWT Authentication

### AI/ML
- spaCy (NLP)
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)
- scikit-learn
- Custom algorithms for matching

---

## 📊 How It Works

### Resume Analysis
1. Upload your resume (PDF/DOCX)
2. AI extracts: skills, education, projects, experience
3. Get scored on 5 criteria (20 points each):
   - Skills breadth & relevance
   - Projects quality & documentation
   - Experience & achievements
   - Keywords & ATS optimization
   - Formatting & structure

### Job Matching Algorithm
Hybrid scoring with 6 components:
- **Skill Match (35%)** - Required vs preferred skills
- **Semantic Similarity (25%)** - Word-based relevance
- **Education Match (10%)** - Degree alignment
- **Experience Match (10%)** - Experience level
- **Location Match (10%)** - Remote/on-site preferences
- **Project Relevance (10%)** - Project-job alignment

Every recommendation explains:
- ✓ Skills you match
- ⚠ Skills you're missing
- 📈 How to improve your score

---

## 📁 Project Structure

```
career-intelligence-platform/
├── backend/
│   ├── app/
│   │   ├── api/routes/        # 11 API modules
│   │   ├── core/              # Config, database, security
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # AI/ML services
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── career_intelligence.db # SQLite database (auto-created)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   └── main.tsx
│   ├── package.json
│   └── index.html
│
└── README.md
```

---

## 🔐 Default Accounts

### Create Your Account
On first run, register through the UI:
1. Go to http://localhost:5173
2. Click "Sign up"
3. Fill in your details
4. Start using the platform!

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `execution policy` error when activating venv
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Problem:** `pip install` fails
- Make sure you're in the virtual environment (you should see `(venv)` in your prompt)
- Update pip: `python -m pip install --upgrade pip`

**Problem:** Backend won't start
- Check if port 8000 is in use
- Try a different port: `uvicorn app.main:app --reload --port 8001`

**Problem:** Database errors
- Delete `career_intelligence.db` file and restart the backend
- Database will be recreated automatically

### Frontend Issues

**Problem:** `npm install` fails
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

**Problem:** Frontend won't start
- Check if port 5173 is in use
- The Vite dev server will automatically try the next available port

**Problem:** Can't connect to backend
- Make sure backend is running on http://localhost:8000
- Check browser console for errors

---

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (returns JWT)
- `GET /api/auth/me` - Get current user

### Profile
- `GET/PUT /api/users/me` - User profile
- `POST /api/users/me/skills` - Add skills
- `POST /api/users/me/projects` - Add projects
- `POST /api/users/me/education` - Add education

### Resume
- `POST /api/resume/upload` - Upload resume
- `GET /api/resume/analysis` - Get analysis

### Opportunities
- `GET /api/opportunities` - List internships/jobs
- `GET /api/opportunities/{id}` - Details

### Recommendations
- `GET /api/recommendations` - AI-powered matches
- `GET /api/recommendations/explain/{id}` - Explanation

### Career Intelligence
- `POST /api/skills/gaps/analyze` - Skill gap analysis
- `POST /api/career/roadmap/generate` - Generate roadmap
- `GET /api/career/readiness` - Career readiness score

### Applications
- `GET /api/applications` - Your applications
- `POST /api/applications` - Apply to opportunity

### Interview
- `POST /api/interview/start` - Start practice session
- `GET /api/interview/questions` - Generate questions

---

## 🎓 For BCA Final Year Students

This project demonstrates:

### Technical Skills
- ✅ Full-stack development
- ✅ REST API design
- ✅ Database design & ORM
- ✅ Authentication & security
- ✅ File upload & processing
- ✅ Frontend state management

### AI/ML Skills
- ✅ Resume parsing (PDF/DOCX)
- ✅ NLP text extraction
- ✅ Scoring algorithms
- ✅ Matching algorithms
- ✅ Recommendation systems
- ✅ Skill gap analysis

### Software Engineering
- ✅ Clean architecture
- ✅ Modular design
- ✅ Error handling
- ✅ Input validation
- ✅ API documentation
- ✅ Responsive UI/UX

---

## 🔄 Adding Sample Data

To test with sample opportunities:

1. Go to http://localhost:8000/docs
2. Navigate to "Admin" section
3. Use `POST /api/admin/opportunities` to add opportunities
4. Or use the admin panel in the frontend

---

## 📈 Performance

- **Backend startup:** ~2-3 seconds
- **Resume parsing:** ~1-2 seconds per file
- **Job matching:** ~100-200ms per opportunity
- **Database:** SQLite handles 1000+ opportunities easily

---

## 🚀 Deployment

### Deploy on Render (Free) — One-Click Blueprint

This repo includes a `render.yaml` Blueprint that deploys **PostgreSQL + FastAPI backend + React frontend** all at once.

1. Push this repo to GitHub (already done at `https://github.com/Akshitavijay01/career-intelligence-platform`).
2. Go to [render.com](https://render.com) and **Sign in with GitHub** (free account).
3. Click **New** → **Blueprint** → connect your GitHub repo `career-intelligence-platform`.
4. Render reads `render.yaml` and shows all 3 services — click **Apply**.
5. Wait ~5-10 minutes. You'll get URLs:
   - Frontend: `https://career-intelligence-frontend.onrender.com`
   - Backend API: `https://career-intelligence-api.onrender.com`
   - Swagger docs: `https://career-intelligence-api.onrender.com/docs`

> **Note:** Free-tier services "sleep" after ~15 min of inactivity and wake on the next request (first load may take ~30s).

### Manual Deployment (instead of Blueprint)

- **Database:** Create a free PostgreSQL instance on Render. Copy its *Internal Database URL*.
- **Backend web service:**
  - Root directory: `backend`
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Env vars: `DATABASE_URL` (from Render Postgres), `SECRET_KEY` (random), `CORS_ORIGINS` → your frontend URL
- **Frontend static site:**
  - Root directory: `frontend`
  - Build: `npm install && npm run build`
  - Publish directory: `dist`
  - Env var: `VITE_API_URL` → `https://your-backend.onrender.com/api`

### Older instructions (SQLite/local only)

For simple local production:
1. Set `DEBUG=false`
2. Use proper secret keys
3. Note: SQLite does **not** persist on cloud platforms — use PostgreSQL instead.

---

## 🤝 Support

If you encounter issues:
1. Check this README's troubleshooting section
2. Check backend logs in the terminal
3. Check browser console (F12) for frontend errors
4. Verify Python and Node.js versions

---

## 📝 License

MIT License - Free for academic and personal use

---

**Built with ❤️ for Students**

*Empowering careers through AI-powered intelligence*

**No Docker. No PostgreSQL. No Complexity. Just Works!™**