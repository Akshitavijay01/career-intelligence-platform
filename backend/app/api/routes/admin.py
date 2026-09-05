from fastapi import Header, APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.user import User, UserProfile, UserRole
from app.models.opportunity import Opportunity, OpportunityStatus
from app.models.application import Application
from app.models.interview import InterviewSession
from app.core.security import decode_token

router = APIRouter()


def _require_admin(db: Session, authorization: Optional[str]) -> User:
    """Decode JWT and return user only if admin role. Raises 401/403."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/dashboard")
async def get_admin_dashboard(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    """Get admin dashboard statistics."""
    _require_admin(db, authorization)

    # Get statistics
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()

    total_opportunities = db.query(Opportunity).count()
    active_opportunities = db.query(Opportunity).filter(Opportunity.status == "active").count()

    total_applications = db.query(Application).count()
    total_interviews = db.query(InterviewSession).count()

    # Most requested skills (simplified)
    most_requested_skills = [
        {"skill_name": "python", "count": 150},
        {"skill_name": "javascript", "count": 120},
        {"skill_name": "sql", "count": 100},
        {"skill_name": "aws", "count": 85},
        {"skill_name": "docker", "count": 75}
    ]

    # Popular job roles
    popular_roles = [
        {"role": "Software Developer", "count": 85},
        {"role": "Data Scientist", "count": 45},
        {"role": "DevOps Engineer", "count": 30},
        {"role": "Full Stack Developer", "count": 60}
    ]

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_opportunities": total_opportunities,
        "active_opportunities": active_opportunities,
        "total_applications": total_applications,
        "total_interviews": total_interviews,
        "most_requested_skills": most_requested_skills[:5],
        "popular_job_roles": popular_roles
    }

@router.get("/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """Get all users for admin management."""
    _require_admin(db, authorization)

    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    is_active: bool = None,
    role: str = None,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """Update user status or role (admin only)."""
    _require_admin(db, authorization)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if is_active is not None:
        user.is_active = is_active
    if role:
        user.role = role

    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """Delete a user (admin only)."""
    _require_admin(db, authorization)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.get("/opportunities")
async def get_all_opportunities(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """Get all opportunities for admin management."""
    _require_admin(db, authorization)

    query = db.query(Opportunity)

    if status:
        query = query.filter(Opportunity.status == status)

    opportunities = query.offset(skip).limit(limit).all()
    return opportunities

@router.post("/opportunities")
async def create_opportunity_admin(
    title: str,
    company: str,
    description: str,
    location: str,
    work_type: str,
    employment_type: str,
    education_requirements: str,
    experience_requirements: str,
    application_deadline: str,
    application_url: str,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """Create a new opportunity (admin only)."""
    _require_admin(db, authorization)

    from app.models.opportunity import Opportunity, WorkType, EmploymentType, OpportunityStatus

    opportunity = Opportunity(
        title=title,
        company=company,
        description=description,
        location=location,
        work_type=WorkType(work_type),
        employment_type=EmploymentType(employment_type),
        education_requirements=education_requirements,
        experience_requirements=experience_requirements,
        application_deadline=application_deadline,
        application_url=application_url,
        source="admin",
        posting_date="today",
        status=OpportunityStatus.ACTIVE,
        is_verified=True
    )

    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity

@router.get("/analytics")
async def get_analytics(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    """Get platform analytics."""
    _require_admin(db, authorization)

    from app.models.user import User
    from app.models.application import Application
    from app.models.interview import InterviewSession

    # User growth (simplified - would normally use date-based query)
    total_users = db.query(User).count()

    # Application status distribution
    status_counts = {}
    for status in ["saved", "applied", "assessment", "interview", "offer", "rejected", "withdrawn"]:
        count = db.query(Application).filter(Application.status == status).count()
        status_counts[status] = count

    # Interview success rate
    total_interviews = db.query(InterviewSession).count()
    successful_interviews = db.query(InterviewSession).filter(InterviewSession.overall_score >= 70).count()

    success_rate = (successful_interviews / total_interviews * 100) if total_interviews > 0 else 0

    return {
        "total_users": total_users,
        "application_status_distribution": status_counts,
        "total_interviews": total_interviews,
        "success_rate": round(success_rate, 1)
    }
