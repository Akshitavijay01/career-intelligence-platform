from fastapi import Header, APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.recommendation import Recommendation
from app.models.opportunity import Opportunity
from app.models.user import User, UserProfile, Skill, UserSkill, Education, Experience, Project
from app.services.matching_engine import MatchingEngine
from app.core.security import decode_token
from datetime import datetime

router = APIRouter()
matching_engine = MatchingEngine()

@router.get("/", response_model=List[dict])
async def get_recommendations(
    limit: int = 10,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    # Get user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user profile and data
    user_profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    # Get user skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    user_skill_ids = [us.skill_id for us in user_skills]
    user_skill_names = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            user_skill_names.append(skill.name)

    # Get user education
    education = db.query(Education).filter(Education.user_id == user.id).all()

    # Get user experience
    experience = db.query(Experience).filter(Experience.user_id == user.id).all()

    # Get user projects
    projects = db.query(Project).filter(Project.user_id == user.id).all()

    # Build user profile for matching
    user_data = {
        "skills": user_skill_names,
        "education": [{"degree": e.degree, "college": e.college, "university": e.university, "graduation_year": e.graduation_year} for e in education],
        "experience": [{"company": exp.company, "role": exp.role, "duration": exp.duration} for exp in experience],
        "projects": [{"title": proj.title, "technologies": proj.technologies.split(", ") if proj.technologies else [], "description": proj.description} for proj in projects]
    }

    # Get active opportunities
    opportunities = db.query(Opportunity).filter(Opportunity.status == "active").all()

    # Generate recommendations
    import json as _json
    recommendations = []
    for opp in opportunities:
        match_result = matching_engine.calculate_match(user_data, opp)
        if match_result["overall_score"] >= 30:  # Only show reasonable matches
            serialized = {
                k: (_json.dumps(v) if k in ("matched_skills", "missing_skills") and isinstance(v, list) else v)
                for k, v in match_result.items()
            }
            # Check if recommendation already exists
            existing_rec = db.query(Recommendation).filter(
                Recommendation.user_id == user.id,
                Recommendation.opportunity_id == opp.id
            ).first()

            if existing_rec:
                # Update existing recommendation
                for key, value in serialized.items():
                    setattr(existing_rec, key, value)
                existing_rec.explanation = matching_engine.generate_explanation(user_data, opp, match_result)
                db.commit()
                recommendations.append(existing_rec)
            else:
                # Create new recommendation
                explanation = matching_engine.generate_explanation(user_data, opp, match_result)
                recommendation = Recommendation(
                    user_id=user.id,
                    opportunity_id=opp.id,
                    explanation=explanation,
                    **serialized
                )
                db.add(recommendation)
                db.commit()
                db.refresh(recommendation)
                recommendations.append(recommendation)

    # Sort by overall score descending and limit
    recommendations.sort(key=lambda x: x.overall_score, reverse=True)
    limited = recommendations[:limit]

    # Convert SQLAlchemy objects to dicts for JSON serialization
    result = []
    for rec in limited:
        opp = db.query(Opportunity).filter(Opportunity.id == rec.opportunity_id).first()
        result.append({
            "id": rec.id,
            "overall_score": rec.overall_score,
            "skill_match": rec.skill_match,
            "semantic_similarity": rec.semantic_similarity,
            "education_match": rec.education_match,
            "experience_match": rec.experience_match,
            "location_match": rec.location_match,
            "project_relevance": rec.project_relevance,
            "matched_skills": rec.matched_skills,
            "missing_skills": rec.missing_skills,
            "explanation": rec.explanation,
            "opportunity": {
                "id": opp.id if opp else None,
                "title": opp.title if opp else None,
                "company": opp.company if opp else None,
                "location": opp.location if opp else None,
            } if opp else None,
        })

    return result

@router.get("/{recommendation_id}")
async def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == user.id
    ).first()

    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    # Get opportunity details
    opportunity = db.query(Opportunity).filter(Opportunity.id == recommendation.opportunity_id).first()
    return {
        "recommendation": recommendation,
        "opportunity": opportunity
    }

@router.post("/refresh")
async def refresh_recommendations(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Clear existing recommendations for user
    db.query(Recommendation).filter(Recommendation.user_id == user.id).delete()

    # Generate fresh recommendations (this will be handled by the GET endpoint when called)
    return {"message": "Recommendations refreshed successfully"}

@router.get("/explain/{recommendation_id}")
async def get_recommendation_explanation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == user.id
    ).first()

    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return {
        "explanation": recommendation.explanation,
        "matched_skills": recommendation.matched_skills,
        "missing_skills": recommendation.missing_skills
    }