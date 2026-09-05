from fastapi import Header, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_token

router = APIRouter()

@router.get("/")
async def get_dashboard(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """Get user dashboard statistics."""
    if not authorization:
        # Return default values for unauthenticated users
        return {
            "career_readiness": 0,
            "resume_score": 0,
            "technical_skill_score": 0,
            "recommended_jobs": 0,
            "applications": 0,
            "interviews": 0,
            "skill_gaps": 0
        }

    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        email = payload.get("sub")

        # Get user by email
        from app.models.user import User
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return {
                "career_readiness": 0,
                "resume_score": 0,
                "technical_skill_score": 0,
                "recommended_jobs": 0,
                "applications": 0,
                "interviews": 0,
                "skill_gaps": 0
            }

        # Get user stats
        from app.models.user import UserSkill, Project, Certification, Experience
        from app.models.application import Application
        from app.models.recommendation import Recommendation

        # Count skills
        skills_count = db.query(UserSkill).filter(UserSkill.user_id == user.id).count()

        # Count projects
        projects_count = db.query(Project).filter(Project.user_id == user.id).count()

        # Count certifications
        certs_count = db.query(Certification).filter(Certification.user_id == user.id).count()

        # Count experience
        exp_count = db.query(Experience).filter(Experience.user_id == user.id).count()

        # Count applications
        applications_count = db.query(Application).filter(Application.user_id == user.id).count()

        # Count recommendations (active job matches)
        recommendations_count = db.query(Recommendation).filter(
            Recommendation.user_id == user.id,
            Recommendation.overall_score >= 30
        ).count()

        # Calculate career readiness
        career_readiness = calculate_career_readiness(
            skills_count, projects_count, certs_count, exp_count
        )

        # Calculate resume score (simplified)
        resume_score = min(100, (skills_count * 3) + (projects_count * 5) + (certs_count * 3) + 20)

        # Technical skill score
        technical_skill_score = min(100, skills_count * 5)

        # Estimate skill gaps (based on common missing skills)
        skill_gaps = max(0, 10 - skills_count)

        # Count interviews (approximate)
        interviews = int(applications_count * 0.3)

        return {
            "career_readiness": career_readiness,
            "resume_score": resume_score,
            "technical_skill_score": technical_skill_score,
            "recommended_jobs": recommendations_count,
            "applications": applications_count,
            "interviews": interviews,
            "skill_gaps": skill_gaps
        }

    except Exception as e:
        print(f"Dashboard error: {e}")
        return {
            "career_readiness": 0,
            "resume_score": 0,
            "technical_skill_score": 0,
            "recommended_jobs": 0,
            "applications": 0,
            "interviews": 0,
            "skill_gaps": 0
        }

def calculate_career_readiness(skills: int, projects: int, certs: int, experience: int) -> int:
    """Calculate career readiness score (0-100)."""
    score = 0

    # Technical skills (25%)
    score += min(25, skills * 3)

    # Projects (25%)
    score += min(25, projects * 8)

    # Certifications (15%)
    score += min(15, certs * 5)

    # Experience (20%)
    score += min(20, experience * 10)

    # Other factors (15%)
    score += 15  # Base score for platform usage

    return min(100, score)