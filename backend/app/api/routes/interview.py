from fastapi import Header, APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.interview import InterviewSession, InterviewQuestion, InterviewDifficulty, InterviewType
from app.models.user import User, Project, UserSkill, Skill
from app.services.interview_generator import InterviewGenerator
from app.core.security import decode_token
from datetime import datetime

router = APIRouter()
interview_generator = InterviewGenerator()

def _get_user_id(db: Session, email: str) -> int:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.id

@router.post("/start")
async def start_interview_session(
    difficulty: str,
    interview_type: str,
    opportunity_id: int = None,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    # Create interview session
    session = InterviewSession(
        user_id=user_id,
        opportunity_id=opportunity_id,
        difficulty=InterviewDifficulty(difficulty),
        interview_type=InterviewType(interview_type),
        started_at=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Get user's skills and projects for context
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    skills_list = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            skills_list.append(skill.name)

    projects = db.query(Project).filter(Project.user_id == user_id).all()
    projects_list = [{"title": p.title, "technologies": p.technologies, "description": p.description} for p in projects]

    # Generate questions
    questions_data = interview_generator.generate_questions(
        difficulty=difficulty,
        interview_type=interview_type,
        skills=skills_list,
        projects=projects_list
    )

    # Store questions
    for q_data in questions_data:
        question = InterviewQuestion(
            session_id=session.id,
            question=q_data["question"],
            question_type=q_data["type"]
        )
        db.add(question)

    db.commit()

    # Get all questions for this session
    questions = db.query(InterviewQuestion).filter(InterviewQuestion.session_id == session.id).all()

    return {
        "session_id": session.id,
        "questions": questions
    }

@router.post("/answer")
async def submit_answer(
    session_id: int,
    question_id: int,
    answer: str,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    # Verify session belongs to user
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == user_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get question
    question = db.query(InterviewQuestion).filter(
        InterviewQuestion.id == question_id,
        InterviewQuestion.session_id == session_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Evaluate answer
    evaluation = interview_generator.evaluate_answer(question.question, answer, question.question_type)

    # Update question with answer and evaluation
    question.user_answer = answer
    question.ai_evaluation = evaluation["feedback"]
    question.score = evaluation["score"]

    db.commit()
    db.refresh(question)

    return {
        "evaluation": evaluation["feedback"],
        "score": evaluation["score"]
    }

@router.get("/history")
async def get_interview_history(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    sessions = db.query(InterviewSession).filter(InterviewSession.user_id == user_id).all()
    return sessions

@router.get("/session/{session_id}")
async def get_interview_session(
    session_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == user_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get questions for this session
    questions = db.query(InterviewQuestion).filter(InterviewQuestion.session_id == session_id).all()

    # Calculate overall score if all questions are answered
    answered_questions = [q for q in questions if q.score is not None]
    if len(answered_questions) == len(questions) and questions:
        overall_score = sum(q.score for q in answered_questions) / len(answered_questions)
        session.overall_score = overall_score
        session.completed_at = datetime.utcnow()
        db.commit()

    return {
        "session": session,
        "questions": questions
    }

@router.get("/questions")
async def generate_interview_questions(
    role: str = "Software Developer",
    difficulty: str = "medium",
    count: int = 5,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    email = payload.get("sub")

    user_id = _get_user_id(db, email)

    # Get user's skills and projects for context
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    skills_list = []
    for us in user_skills:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if skill:
            skills_list.append(skill.name)

    projects = db.query(Project).filter(Project.user_id == user_id).all()
    projects_list = [{"title": p.title, "technologies": p.technologies} for p in projects]

    # Generate questions
    questions = interview_generator.generate_questions(
        difficulty=difficulty,
        interview_type="mixed",
        skills=skills_list,
        projects=projects_list,
        count=count
    )

    return questions
