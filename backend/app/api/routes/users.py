from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User, UserProfile, Education, Skill, UserSkill, Project, Certification, Experience
from app.schemas.user import UserProfileCreate, UserProfileUpdate, EducationCreate, EducationUpdate
from app.schemas.user import SkillCreate, ProjectCreate, ProjectUpdate, CertificationCreate
from app.schemas.user import ExperienceCreate, ExperienceUpdate, UserSkillCreate
from app.core.security import decode_token
from datetime import datetime
import os

router = APIRouter()

@router.get("/me")
async def get_profile(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user profile
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not profile:
        return {"message": "Profile not found"}

    return profile

@router.put("/me")
async def update_profile(
    profile_data: UserProfileUpdate,
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

    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

@router.post("/me/education")
async def add_education(
    education: EducationCreate,
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

    db_education = Education(user_id=user.id, **education.dict())
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education

@router.get("/me/education")
async def get_education(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    education = db.query(Education).filter(Education.user_id == user.id).all()
    return education

@router.put("/me/education/{edu_id}")
async def update_education(
    edu_id: int,
    education: EducationUpdate,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    db_education = db.query(Education).filter(Education.id == edu_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="Education not found")

    update_data = education.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_education, field, value)

    db.commit()
    db.refresh(db_education)
    return db_education

@router.delete("/me/education/{edu_id}")
async def delete_education(
    edu_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    db_education = db.query(Education).filter(Education.id == edu_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="Education not found")

    db.delete(db_education)
    db.commit()
    return {"message": "Education deleted"}

@router.post("/me/skills")
async def add_skill(
    skill: UserSkillCreate,
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

    # Get or create skill
    db_skill = db.query(Skill).filter(Skill.name == skill.skill_name.lower()).first()
    if not db_skill:
        db_skill = Skill(name=skill.skill_name.lower(), category=skill.category or "technical")
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)

    # Check if user already has this skill
    existing = db.query(UserSkill).filter(UserSkill.user_id == user.id, UserSkill.skill_id == db_skill.id).first()
    if existing:
        existing.proficiency_level = skill.proficiency_level
        db.commit()
        return existing

    user_skill = UserSkill(
        user_id=user.id,
        skill_id=db_skill.id,
        proficiency_level=skill.proficiency_level
    )
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)
    return user_skill

@router.get("/me/skills")
async def get_skills(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    result = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        result.append({
            "id": us.id,
            "skill_id": us.skill_id,
            "name": skill.name if skill else str(us.skill_id),
            "category": skill.category if skill else "technical",
            "proficiency_level": us.proficiency_level,
            "created_at": us.created_at
        })
    return result

@router.delete("/me/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_skill = db.query(UserSkill).filter(UserSkill.id == skill_id).first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(user_skill)
    db.commit()
    return {"message": "Skill removed"}

@router.post("/me/projects")
async def add_project(
    project: ProjectCreate,
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

    db_project = Project(user_id=user.id, **project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/me/projects")
async def get_projects(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    projects = db.query(Project).filter(Project.user_id == user.id).all()
    return projects

@router.put("/me/projects/{proj_id}")
async def update_project(
    proj_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    db_project = db.query(Project).filter(Project.id == proj_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/me/projects/{proj_id}")
async def delete_project(
    proj_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    db_project = db.query(Project).filter(Project.id == proj_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}

@router.post("/me/certifications")
async def add_certification(
    certification: CertificationCreate,
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

    db_cert = Certification(user_id=user.id, **certification.dict())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

@router.get("/me/certifications")
async def get_certifications(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    certifications = db.query(Certification).filter(Certification.user_id == user.id).all()
    return certifications

@router.delete("/me/certifications/{cert_id}")
async def delete_certification(
    cert_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    db_cert = db.query(Certification).filter(Certification.id == cert_id).first()
    if not db_cert:
        raise HTTPException(status_code=404, detail="Certification not found")

    db.delete(db_cert)
    db.commit()
    return {"message": "Certification deleted"}

@router.post("/me/experiences")
async def add_experience(
    experience: ExperienceCreate,
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

    db_exp = Experience(user_id=user.id, **experience.dict())
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

@router.get("/me/experiences")
async def get_experiences(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    experiences = db.query(Experience).filter(Experience.user_id == user.id).all()
    return experiences

@router.delete("/me/experiences/{exp_id}")
async def delete_experience(
    exp_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    db_exp = db.query(Experience).filter(Experience.id == exp_id).first()
    if not db_exp:
        raise HTTPException(status_code=404, detail="Experience not found")

    db.delete(db_exp)
    db.commit()
    return {"message": "Experience deleted"}