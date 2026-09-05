from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    opportunity_id = Column(Integer, nullable=False)
    overall_score = Column(Float, default=0)
    skill_match = Column(Float, default=0)
    semantic_similarity = Column(Float, default=0)
    education_match = Column(Float, default=0)
    experience_match = Column(Float, default=0)
    location_match = Column(Float, default=0)
    project_relevance = Column(Float, default=0)
    matched_skills = Column(Text)  # JSON string
    missing_skills = Column(Text)  # JSON string
    explanation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    target_role = Column(String(100), nullable=False)
    current_skills = Column(Text)  # JSON string
    missing_skills = Column(Text)  # JSON string
    priority = Column(String(20), default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CareerRoadmap(Base):
    __tablename__ = "career_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    target_role = Column(String(100), nullable=False)
    current_level = Column(String(50))
    target_level = Column(String(50))
    progress_percentage = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, nullable=False)
    skill_name = Column(String(100), nullable=False)
    description = Column(Text)
    difficulty = Column(String(20), default="beginner")
    estimated_hours = Column(Integer, default=0)
    prerequisites = Column(Text)  # JSON string
    resources = Column(Text)  # JSON string
    is_completed = Column(String(10), default="false")
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CareerScore(Base):
    __tablename__ = "career_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    technical_skills_score = Column(Float, default=0)
    projects_score = Column(Float, default=0)
    resume_score = Column(Float, default=0)
    certifications_score = Column(Float, default=0)
    experience_score = Column(Float, default=0)
    interview_readiness_score = Column(Float, default=0)
    overall_score = Column(Float, default=0)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())