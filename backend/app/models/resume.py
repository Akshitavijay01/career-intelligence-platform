from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500))
    file_type = Column(String(50))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

class ResumeParsing(Base):
    __tablename__ = "resume_parsing"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, nullable=False)
    extracted_data = Column(Text)  # JSON string
    parse_status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, nullable=False)
    overall_score = Column(Float, default=0)
    skills_score = Column(Float, default=0)
    projects_score = Column(Float, default=0)
    experience_score = Column(Float, default=0)
    keywords_score = Column(Float, default=0)
    formatting_score = Column(Float, default=0)
    strengths = Column(Text)  # JSON string
    weaknesses = Column(Text)  # JSON string
    recommendations = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())