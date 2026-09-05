from fastapi import Header, APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.application import Application, ApplicationStatus
from app.models.opportunity import Opportunity
from app.models.user import User
from app.core.security import decode_token
from datetime import datetime

router = APIRouter()

def _get_user_id(db: Session, email: str) -> int:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.id

@router.get("/")
async def get_applications(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    applications = db.query(Application).filter(Application.user_id == user_id).all()

    # Get opportunity details for each application
    results = []
    for app in applications:
        opportunity = db.query(Opportunity).filter(Opportunity.id == app.opportunity_id).first()
        results.append({
            "application": app,
            "opportunity": opportunity
        })

    return results

@router.post("/")
async def create_application(
    opportunity_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    # Check if opportunity exists
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Check if already applied
    existing = db.query(Application).filter(
        Application.user_id == user_id,
        Application.opportunity_id == opportunity_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this opportunity")

    # Create application
    application = Application(
        user_id=user_id,
        opportunity_id=opportunity_id,
        status=ApplicationStatus.APPLIED,
        applied_date=datetime.utcnow().strftime("%Y-%m-%d")
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    return application

@router.get("/stats")
async def get_application_stats(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    total = db.query(Application).filter(Application.user_id == user_id).count()

    stats_by_status = {}
    for status in ApplicationStatus:
        count = db.query(Application).filter(
            Application.user_id == user_id,
            Application.status == status
        ).count()
        stats_by_status[status.value] = count

    return {
        "total": total,
        "by_status": stats_by_status
    }

@router.put("/{application_id}")
async def update_application(
    application_id: int,
    status: str,
    notes: str = None,
    interview_date: str = None,
    salary_offered: float = None,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Update fields
    if status:
        application.status = ApplicationStatus(status)
    if notes:
        application.notes = notes
    if interview_date:
        application.interview_date = interview_date
    if salary_offered:
        application.salary_offered = salary_offered

    db.commit()
    db.refresh(application)
    return application

@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()
    return {"message": "Application deleted"}