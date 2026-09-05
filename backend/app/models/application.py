from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ApplicationStatus(str, enum.Enum):
    SAVED = "saved"
    APPLIED = "applied"
    ASSESSMENT = "assessment"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    opportunity_id = Column(Integer, nullable=False)
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_date = Column(String(10))
    notes = Column(Text)
    interview_date = Column(String(10))
    salary_offered = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())