from fastapi import Header, APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.user import Skill, UserSkill
from app.core.security import decode_token

router = APIRouter()

@router.get("/")
async def get_all_skills(db: Session = Depends(get_db)):
    """Get all skills in the system."""
    skills = db.query(Skill).all()
    return skills

@router.post("/")
async def create_skill(
    name: str,
    category: str = "technical",
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """Create a new skill (admin only)."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Check if skill already exists
    existing = db.query(Skill).filter(Skill.name == name.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")

    skill = Skill(name=name.lower(), category=category)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

@router.get("/categories")
async def get_skill_categories(db: Session = Depends(get_db)):
    """Get all skill categories."""
    categories = db.query(Skill.category).distinct().all()
    return [c[0] for c in categories]

@router.get("/user/{user_id}")
async def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    """Get skills for a specific user."""
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    return user_skills

@router.get("/most-demanding")
async def get_most_demanding_skills(limit: int = 10, db: Session = Depends(get_db)):
    """Get most in-demand skills."""
    # This would typically use opportunity_skills join
    # Simplified version for now
    demanding_skills = [
        {"name": "python", "category": "technical", "demand": "high"},
        {"name": "javascript", "category": "technical", "demand": "high"},
        {"name": "sql", "category": "technical", "demand": "high"},
        {"name": "aws", "category": "cloud", "demand": "high"},
        {"name": "docker", "category": "tools", "demand": "high"},
        {"name": "machine learning", "category": "technical", "demand": "high"},
        {"name": "react", "category": "frontend", "demand": "high"},
        {"name": "node", "category": "backend", "demand": "high"}
    ]

    return demanding_skills[:limit]

@router.get("/trending")
async def get_trending_skills(limit: int = 10, db: Session = Depends(get_db)):
    """Get trending skills based on job postings."""
    # Simplified trending skills list
    trending_skills = [
        {"name": "ai/machine learning", "category": "technical", "growth": "125%"},
        {"name": " cybersecurity", "category": "security", "growth": "95%"},
        {"name": "cloud computing", "category": "cloud", "growth": "85%"},
        {"name": "data engineering", "category": "technical", "growth": "78%"},
        {"name": "devops", "category": "tools", "growth": "65%"}
    ]

    return trending_skills[:limit]