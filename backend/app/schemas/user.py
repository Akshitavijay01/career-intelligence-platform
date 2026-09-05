from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    profile_photo: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EducationBase(BaseModel):
    degree: str
    college: Optional[str] = None
    university: Optional[str] = None
    semester: Optional[int] = None
    cgpa: Optional[str] = None
    graduation_year: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class EducationUpdate(EducationBase):
    pass

class EducationResponse(EducationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserSkillBase(BaseModel):
    proficiency_level: str = "beginner"

class UserSkillCreate(UserSkillBase):
    skill_name: str
    category: Optional[str] = None

class UserSkillResponse(UserSkillBase):
    id: int
    user_id: int
    skill_id: int
    skill: SkillResponse
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CertificationBase(BaseModel):
    certificate_name: str
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    credential_url: Optional[str] = None

class CertificationCreate(CertificationBase):
    pass

class CertificationResponse(CertificationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ExperienceBase(BaseModel):
    company: str
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(ExperienceBase):
    pass

class ExperienceResponse(ExperienceBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True