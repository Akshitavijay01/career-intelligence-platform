from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class WorkType(str, enum.Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on-site"

class EmploymentType(str, enum.Enum):
    INTERNSHIP = "internship"
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"

class OpportunityStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    description = Column(Text)
    location = Column(String(100))
    work_type = Column(SQLEnum(WorkType), default=WorkType.ON_SITE)
    stipend = Column(Float)
    salary = Column(Float)
    employment_type = Column(SQLEnum(EmploymentType), nullable=False)
    education_requirements = Column(Text)
    experience_requirements = Column(Text)
    application_deadline = Column(String(10))
    application_url = Column(String(500))
    source = Column(String(100))
    posting_date = Column(String(10))
    status = Column(SQLEnum(OpportunityStatus), default=OpportunityStatus.ACTIVE)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OpportunitySkill(Base):
    __tablename__ = "opportunity_skills"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, nullable=False)
    skill_id = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())