from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine, Base, init_db
from app.api.routes import auth, dashboard, users, resume, opportunities, recommendations, skills, career, applications, interview, ai, admin
import os

# Initialize database and create tables
init_db()

# Mount uploads directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="Career Intelligence Platform API",
    description="AI-Powered Internship & Career Intelligence Platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["Opportunities"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(career.router, prefix="/api/career", tags=["Career Intelligence"])
app.include_router(applications.router, prefix="/api/applications", tags=["Applications"])
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Assistant"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "Career Intelligence Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "OK",
        "database": "SQLite (local development)"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "SQLite"}

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    from app.core.database import SessionLocal
    from app.core.seed import seed_database

    print("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    print("Database initialized successfully!")
    print(f"Database file: {settings.DATABASE_URL}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)