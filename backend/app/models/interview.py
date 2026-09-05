from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class InterviewDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class InterviewType(str, enum.Enum):
    TECHNICAL = "technical"
    HR = "hr"
    MIXED = "mixed"

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    opportunity_id = Column(Integer)
    difficulty = Column(SQLEnum(InterviewDifficulty), default=InterviewDifficulty.MEDIUM)
    interview_type = Column(SQLEnum(InterviewType), default=InterviewType.MIXED)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    overall_score = Column(Float)

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    question_type = Column(String(20))
    user_answer = Column(Text)
    ai_evaluation = Column(Text)
    score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    type = Column(String(50))
    title = Column(String(200))
    message = Column(Text)
    is_read = Column(String(10), default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AdminAnalytics(Base):
    __tablename__ = "admin_analytics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(10))
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_opportunities = Column(Integer, default=0)
    total_applications = Column(Integer, default=0)
    total_interviews = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())