from fastapi import Header, APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.interview import ChatMessage
from app.models.user import User, UserProfile, Education, UserSkill, Skill, Project, Experience
from app.services.ai_assistant import AIAssistant
from app.core.security import decode_token
from datetime import datetime

router = APIRouter()
ai_assistant = AIAssistant()

@router.post("/chat")
async def chat_with_ai(
    message: str,
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

    # Get user profile for context
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    user_context = {}

    if profile:
        user_context["first_name"] = profile.first_name
        user_context["last_name"] = profile.last_name
        user_context["location"] = profile.location

    # Get user skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    skills = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            skills.append(skill.name)
    user_context["skills"] = skills

    # Get user education
    education = db.query(Education).filter(Education.user_id == user.id).all()
    user_context["education"] = [{"degree": e.degree, "college": e.college} for e in education]

    # Get user projects
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    user_context["projects"] = [{"title": p.title, "technologies": p.technologies} for p in projects]

    # Get user experience
    experience = db.query(Experience).filter(Experience.user_id == user.id).all()
    user_context["experience"] = [{"company": exp.company, "role": exp.role, "duration": exp.duration} for exp in experience]

    # Store user message
    user_msg = ChatMessage(
        user_id=user.id,
        role="user",
        content=message,
        created_at=datetime.utcnow()
    )
    db.add(user_msg)

    # Get AI response
    ai_response = ai_assistant.get_response(message, user_context)

    # Store AI response
    ai_msg = ChatMessage(
        user_id=user.id,
        role="assistant",
        content=ai_response,
        created_at=datetime.utcnow()
    )
    db.add(ai_msg)
    db.commit()

    return {"response": ai_response}

@router.get("/chat/history")
async def get_chat_history(
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

    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user.id).order_by(ChatMessage.created_at.desc()).limit(50).all()
    messages.reverse()  # Show oldest first
    return messages

@router.delete("/chat/history")
async def clear_chat_history(
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

    db.query(ChatMessage).filter(ChatMessage.user_id == user.id).delete()
    db.commit()
    return {"message": "Chat history cleared"}

@router.post("/analyze-resume-feedback")
async def analyze_resume_and_give_feedback(
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

    # Get user context for resume feedback
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    skills = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            skills.append(skill.name)

    education = db.query(Education).filter(Education.user_id == user.id).all()
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    experience = db.query(Experience).filter(Experience.user_id == user.id).all()

    # Generate resume feedback
    feedback = ai_assistant.provide_resume_feedback(
        skills=skills,
        education=education,
        projects=projects,
        experience=experience
    )

    return {"feedback": feedback}

@router.post("/generate-interview-questions")
async def generate_resume_based_questions(
    count: int = 5,
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

    # Get user's projects for context
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    projects_list = [{"title": p.title, "technologies": p.technologies, "description": p.description} for p in projects]

    # Generate resume-based questions
    questions = ai_assistant.generate_resume_based_questions(projects_list, count)

    return {"questions": questions}