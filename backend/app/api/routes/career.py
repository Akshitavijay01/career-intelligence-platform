from fastapi import Header, APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.recommendation import SkillGap, CareerRoadmap, RoadmapItem, CareerScore
from app.models.user import User, UserSkill, Skill
from app.services.skill_gap_analyzer import SkillGapAnalyzer
from app.services.roadmap_generator import RoadmapGenerator
from app.services.career_score_calculator import CareerScoreCalculator
from app.core.security import decode_token

router = APIRouter()

skill_gap_analyzer = SkillGapAnalyzer()
roadmap_generator = RoadmapGenerator()
career_score_calculator = CareerScoreCalculator()

@router.get("/gaps")
async def get_skill_gaps(
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

    # Get user's current skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    current_skills = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            current_skills.append(skill.name)

    # Get recent skill gaps
    skill_gaps = db.query(SkillGap).filter(SkillGap.user_id == user.id).all()
    return skill_gaps

@router.post("/gaps/analyze")
async def analyze_skill_gaps(
    target_role: str,
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

    # Get user's current skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    current_skills = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            current_skills.append(skill.name)

    # Analyze skill gaps
    gap_analysis = skill_gap_analyzer.analyze_gaps(current_skills, target_role)

    # Store skill gap record
    skill_gap = SkillGap(
        user_id=user.id,
        target_role=target_role,
        current_skills=str(current_skills),
        missing_skills=str(gap_analysis.get("all_missing_skills", [])),
        priority=gap_analysis.get("priority", "medium")
    )
    db.add(skill_gap)
    db.commit()
    db.refresh(skill_gap)

    return gap_analysis

@router.get("/roadmap")
async def get_career_roadmap(
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

    roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.user_id == user.id).order_by(CareerRoadmap.created_at.desc()).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="No roadmap found")

    # Get roadmap items
    items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == roadmap.id).all()

    return {
        "roadmap": roadmap,
        "items": items
    }

@router.post("/roadmap/generate")
async def generate_career_roadmap(
    target_role: str,
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

    # Get user's current skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    current_skills = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            current_skills.append(skill.name)

    # Generate roadmap
    roadmap_data = roadmap_generator.generate_roadmap(current_skills, target_role)

    # Create roadmap record
    roadmap = CareerRoadmap(
        user_id=user.id,
        target_role=target_role,
        current_level=roadmap_data.get("current_level", "beginner"),
        target_level=roadmap_data.get("target_level", "intermediate"),
        progress_percentage=0
    )
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)

    # Add roadmap items
    for item_data in roadmap_data.get("items", []):
        item = RoadmapItem(
            roadmap_id=roadmap.id,
            skill_name=item_data["skill_name"],
            description=item_data["description"],
            difficulty=item_data["difficulty"],
            estimated_hours=item_data["estimated_hours"],
            prerequisites=str(item_data.get("prerequisites", [])),
            resources=str(item_data.get("resources", [])),
            is_completed="false"
        )
        db.add(item)

    db.commit()

    # Get all items
    items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == roadmap.id).all()

    return {
        "roadmap": roadmap,
        "items": items
    }

@router.put("/roadmap/items/{item_id}")
async def mark_roadmap_item_complete(
    item_id: int,
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

    item = db.query(RoadmapItem).filter(RoadmapItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap item not found")

    # Get roadmap
    roadmap = db.query(CareerRoadmap).filter(CareerRoadmap.id == item.roadmap_id).first()
    if not roadmap or roadmap.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Toggle completion
    if item.is_completed == "true":
        item.is_completed = "false"
        item.completed_at = None
    else:
        item.is_completed = "true"
        from datetime import datetime
        item.completed_at = datetime.utcnow()
    db.commit()

    # Update roadmap progress
    all_items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == roadmap.id).all()
    completed_items = [i for i in all_items if i.is_completed == "true"]
    roadmap.progress_percentage = (len(completed_items) / len(all_items)) * 100 if all_items else 0
    db.commit()

    return {"message": "Item toggled", "is_completed": item.is_completed, "progress": roadmap.progress_percentage}

@router.get("/readiness")
async def get_career_readiness(
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

    # Get latest career score
    career_score = db.query(CareerScore).filter(CareerScore.user_id == user.id).order_by(CareerScore.calculated_at.desc()).first()

    if not career_score:
        # Calculate career score
        score_data = await career_score_calculator.calculate_score(user.id, db)
        career_score = CareerScore(user_id=user.id, **score_data)
        db.add(career_score)
        db.commit()
        db.refresh(career_score)

    return career_score

@router.get("/analytics")
async def get_career_analytics(
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

    # Get various analytics data
    from app.models.application import Application
    from app.models.interview import InterviewSession

    total_applications = db.query(Application).filter(Application.user_id == user.id).count()
    total_interviews = db.query(InterviewSession).filter(InterviewSession.user_id == user.id).count()

    # Get skill count
    total_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).count()

    # Get career score
    career_score = db.query(CareerScore).filter(CareerScore.user_id == user.id).order_by(CareerScore.calculated_at.desc()).first()

    return {
        "total_applications": total_applications,
        "total_interviews": total_interviews,
        "total_skills": total_skills,
        "career_readiness": career_score.overall_score if career_score else 0,
        "technical_skills_score": career_score.technical_skills_score if career_score else 0,
        "resume_score": career_score.resume_score if career_score else 0
    }