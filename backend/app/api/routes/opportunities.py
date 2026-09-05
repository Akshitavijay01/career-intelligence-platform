from fastapi import Header, APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.opportunity import Opportunity, OpportunitySkill
from app.models.user import Skill
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunityResponse
from app.core.security import decode_token
from datetime import datetime
import re

router = APIRouter()

@router.post("/", response_model=OpportunityResponse)
async def create_opportunity(
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    # Admin-only check (simplified)
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    # In a real app, check if user is admin

    db_opportunity = Opportunity(**opportunity.dict())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)

    # Add skills if provided
    if opportunity.skills:
        for skill_data in opportunity.skills:
            # Get or create skill
            skill_name = skill_data["name"].lower()
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                skill = Skill(name=skill_name, category=skill_data.get("category", "technical"))
                db.add(skill)
                db.commit()
                db.refresh(skill)

            opp_skill = OpportunitySkill(
                opportunity_id=db_opportunity.id,
                skill_id=skill.id,
                is_required=skill_data.get("is_required", True)
            )
            db.add(opp_skill)

    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

@router.get("/", response_model=List[OpportunityResponse])
async def get_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    location: Optional[str] = None,
    work_type: Optional[str] = None,
    employment_type: Optional[str] = None,
    min_stipend: Optional[float] = None,
    max_stipend: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Opportunity).filter(Opportunity.status == "active")

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            (Opportunity.title.ilike(search_term)) |
            (Opportunity.company.ilike(search_term)) |
            (Opportunity.description.ilike(search_term))
        )

    if location:
        query = query.filter(Opportunity.location.ilike(f"%{location}%"))

    if work_type:
        query = query.filter(Opportunity.work_type == work_type)

    if employment_type:
        query = query.filter(Opportunity.employment_type == employment_type)

    if min_stipend is not None:
        query = query.filter(Opportunity.stipend >= min_stipend)

    if max_stipend is not None:
        query = query.filter(Opportunity.stipend <= max_stipend)

    opportunities = query.offset(skip).limit(limit).all()
    return opportunities

@router.get("/search/", response_model=List[OpportunityResponse])
async def search_opportunities(
    q: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    search_term = f"%{q.lower()}%"
    opportunities = db.query(Opportunity).filter(
        Opportunity.status == "active",
        (Opportunity.title.ilike(search_term)) |
        (Opportunity.company.ilike(search_term)) |
        (Opportunity.description.ilike(search_term))
    ).limit(limit).all()
    return opportunities

@router.get("/stats/summary")
async def get_opportunity_stats(db: Session = Depends(get_db)):
    total = db.query(Opportunity).filter(Opportunity.status == "active").count()
    remote_count = db.query(Opportunity).filter(
        Opportunity.status == "active",
        Opportunity.work_type == "remote"
    ).count()
    internship_count = db.query(Opportunity).filter(
        Opportunity.status == "active",
        Opportunity.employment_type == "internship"
    ).count()

    return {
        "total_active": total,
        "remote_opportunities": remote_count,
        "internship_opportunities": internship_count
    }

@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity