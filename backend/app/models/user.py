from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Text
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    location = Column(String(255))
    profile_photo = Column(String(500))
    linkedin = Column(String(255))
    github = Column(String(255))
    portfolio = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    degree = Column(String(100), nullable=False)
    college = Column(String(200))
    university = Column(String(200))
    semester = Column(Integer)
    cgpa = Column(String(10))
    graduation_year = Column(Integer)
    start_date = Column(String(10))
    end_date = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    skill_id = Column(Integer, nullable=False)
    proficiency_level = Column(String(20), default="beginner")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    technologies = Column(Text)  # Comma-separated list
    github_url = Column(String(500))
    live_url = Column(String(500))
    role = Column(String(100))
    start_date = Column(String(10))
    end_date = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    certificate_name = Column(String(200), nullable=False)
    issuer = Column(String(200))
    issue_date = Column(String(10))
    credential_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    company = Column(String(200), nullable=False)
    role = Column(String(200))
    duration = Column(String(100))
    description = Column(Text)
    start_date = Column(String(10))
    end_date = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())