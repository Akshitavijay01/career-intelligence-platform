from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OpportunitySkillBase(BaseModel):
    skill_id: int
    is_required: bool = True

class OpportunitySkillCreate(OpportunitySkillBase):
    pass

class OpportunitySkillResponse(OpportunitySkillBase):
    id: int
    opportunity_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class OpportunityBase(BaseModel):
    title: str
    company: str
    description: Optional[str] = None
    location: Optional[str] = None
    work_type: Optional[str] = "on-site"
    stipend: Optional[float] = None
    salary: Optional[float] = None
    employment_type: Optional[str] = "internship"
    education_requirements: Optional[str] = None
    experience_requirements: Optional[str] = None
    application_deadline: Optional[str] = None
    application_url: Optional[str] = None
    source: Optional[str] = None
    posting_date: Optional[str] = None
    status: Optional[str] = "active"
    is_verified: Optional[bool] = False

class OpportunityCreate(OpportunityBase):
    skills: Optional[List[dict]] = []

class OpportunityUpdate(OpportunityBase):
    pass

class OpportunityResponse(OpportunityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RecommendationBase(BaseModel):
    opportunity_id: int
    overall_score: Optional[float] = 0
    skill_match: Optional[float] = 0
    semantic_similarity: Optional[float] = 0
    education_match: Optional[float] = 0
    experience_match: Optional[float] = 0
    location_match: Optional[float] = 0
    project_relevance: Optional[float] = 0
    matched_skills: Optional[List[str]] = []
    missing_skills: Optional[List[str]] = []
    explanation: Optional[str] = None

class RecommendationResponse(RecommendationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True