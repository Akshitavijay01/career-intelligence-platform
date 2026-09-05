from fastapi import Header, APIRouter, HTTPException, status, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.user import UserProfile, User, Education, Skill, UserSkill, Project, Experience
from app.models.resume import Resume, ResumeParsing, ResumeAnalysis
from app.core.config import settings
from app.core.security import decode_token
from app.services.resume_parser import ResumeParser
from app.services.resume_analyzer import ResumeAnalyzer
import os
import shutil
import uuid
import json
from datetime import datetime

router = APIRouter()

# Initialize services
resume_parser = ResumeParser()
resume_analyzer = ResumeAnalyzer()

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
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

    user_id = user.id

    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed"
        )

    # Validate file size
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {settings.MAX_FILE_SIZE_MB}MB limit"
        )

    # Create upload directory if not exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    file_extension = ".pdf" if file.content_type == "application/pdf" else ".docx"
    unique_filename = f"{email}_{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    # Create resume record
    resume = Resume(
        user_id=user_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file_extension.lstrip('.')
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    # Parse resume asynchronously (in background)
    try:
        extracted_data = resume_parser.parse_resume(file_path, file_extension.lstrip('.'))

        # Store parsed data
        parsing_record = ResumeParsing(
            resume_id=resume.id,
            extracted_data=str(extracted_data),  # Store as JSON string
            parse_status="completed"
        )
        db.add(parsing_record)
        db.commit()

        # Analyze resume
        analysis_result = resume_analyzer.analyze_resume(extracted_data)
        # Serialize list fields to JSON strings for TEXT columns
        if isinstance(analysis_result.get('strengths'), list):
            analysis_result['strengths'] = json.dumps(analysis_result['strengths'])
        if isinstance(analysis_result.get('weaknesses'), list):
            analysis_result['weaknesses'] = json.dumps(analysis_result['weaknesses'])
        if isinstance(analysis_result.get('recommendations'), list):
            analysis_result['recommendations'] = json.dumps(analysis_result['recommendations'])

        analysis_record = ResumeAnalysis(
            resume_id=resume.id,
            **analysis_result
        )
        db.add(analysis_record)
        db.commit()

        # Update user profile with extracted data
        await update_profile_from_resume(user_id, extracted_data, db)

        return {
            "message": "Resume uploaded and processed successfully",
            "resume_id": resume.id,
            "extracted_data": extracted_data,
            "analysis": analysis_result
        }
    except Exception as e:
        # Update parsing status to failed
        parsing_record = ResumeParsing(
            resume_id=resume.id,
            extracted_data="{}",
            parse_status="failed"
        )
        db.add(parsing_record)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process resume: {str(e)}"
        )

@router.get("/")
async def get_resume(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resume = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")

    return resume

@router.get("/analysis")
async def get_resume_analysis(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resume = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")

    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id == resume.id).order_by(ResumeAnalysis.created_at.desc()).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found")

    return analysis

@router.delete("/")
async def delete_resume(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resume = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")

    # Delete file
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    # Delete related records
    db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id == resume.id).delete()
    db.query(ResumeParsing).filter(ResumeParsing.resume_id == resume.id).delete()
    db.delete(resume)
    db.commit()

    return {"message": "Resume deleted successfully"}

async def update_profile_from_resume(user_id: int, extracted_data: dict, db: Session):
    """Update user profile with data extracted from resume"""
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            # Create profile if it doesn't exist
            profile = UserProfile(user_id=user_id)
            db.add(profile)

        # Update personal info
        if extracted_data.get("personal_info"):
            personal = extracted_data["personal_info"]
            if personal.get("name"):
                name_parts = personal["name"].split(" ", 1)
                profile.first_name = name_parts[0]
                profile.last_name = name_parts[1] if len(name_parts) > 1 else ""
            if personal.get("phone"):
                profile.phone = personal["phone"]
            if personal.get("location"):
                profile.location = personal["location"]
            if personal.get("linkedin"):
                profile.linkedin = personal["linkedin"]
            if personal.get("github"):
                profile.github = personal["github"]

        # Update education
        if extracted_data.get("education"):
            # Clear existing education
            db.query(Education).filter(Education.user_id == user_id).delete()

            for edu in extracted_data["education"]:
                db_education = Education(
                    user_id=user_id,
                    degree=edu.get("degree", ""),
                    college=edu.get("college", ""),
                    university=edu.get("university", ""),
                    graduation_year=edu.get("graduation_year"),
                    cgpa=edu.get("cgpa"),
                    start_date=edu.get("start_date"),
                    end_date=edu.get("end_date")
                )
                db.add(db_education)

        # Update skills
        if extracted_data.get("skills"):
            # Clear existing skills
            db.query(UserSkill).filter(UserSkill.user_id == user_id).delete()

            for skill_name in extracted_data["skills"]:
                # Get or create skill
                skill = db.query(Skill).filter(Skill.name == skill_name.lower()).first()
                if not skill:
                    skill = Skill(name=skill_name.lower(), category="technical")
                    db.add(skill)
                    db.commit()
                    db.refresh(skill)

                # Add user skill
                user_skill = UserSkill(
                    user_id=user_id,
                    skill_id=skill.id,
                    proficiency_level="intermediate"  # Default from resume
                )
                db.add(user_skill)

        # Update projects
        if extracted_data.get("projects"):
            # Clear existing projects
            db.query(Project).filter(Project.user_id == user_id).delete()

            for proj in extracted_data["projects"]:
                db_project = Project(
                    user_id=user_id,
                    title=proj.get("title", ""),
                    description=proj.get("description", ""),
                    technologies=", ".join(proj.get("technologies", [])),
                    github_url=proj.get("github_url"),
                    live_url=proj.get("live_url"),
                    role=proj.get("role"),
                    start_date=proj.get("start_date"),
                    end_date=proj.get("end_date")
                )
                db.add(db_project)

        # Update experience
        if extracted_data.get("experience"):
            # Clear existing experience
            db.query(Experience).filter(Experience.user_id == user_id).delete()

            for exp in extracted_data["experience"]:
                db_experience = Experience(
                    user_id=user_id,
                    company=exp.get("company", ""),
                    role=exp.get("role", ""),
                    duration=exp.get("duration", ""),
                    description=exp.get("description", ""),
                    start_date=exp.get("start_date"),
                    end_date=exp.get("end_date")
                )
                db.add(db_experience)

        db.commit()
    except Exception as e:
        print(f"Error updating profile from resume: {e}")
        # Don't fail the resume upload if profile update fails