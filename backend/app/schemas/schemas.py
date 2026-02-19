from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    student_name: str = Field(..., min_length=1, max_length=255)
    student_email: Optional[str] = None

class ProjectCreate(ProjectBase):
    submission_type: str = Field(..., pattern="^(zip|github|pdf)$")
    github_url: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    student_name: Optional[str] = None
    student_email: Optional[str] = None

class Project(ProjectBase):
    id: int
    submission_type: Optional[str] = None
    file_path: Optional[str] = None
    github_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class EvaluationBase(BaseModel):
    overall_score: float = Field(..., ge=0, le=100)
    code_quality_score: Optional[float] = Field(None, ge=0, le=100)
    functionality_score: Optional[float] = Field(None, ge=0, le=100)
    documentation_score: Optional[float] = Field(None, ge=0, le=100)
    innovation_score: Optional[float] = Field(None, ge=0, le=100)

class EvaluationCreate(EvaluationBase):
    project_id: int
    code_analysis: Optional[Dict[str, Any]] = None
    report_analysis: Optional[Dict[str, Any]] = None
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None

class Evaluation(EvaluationBase):
    id: int
    project_id: int
    max_score: int
    code_analysis: Optional[Dict[str, Any]] = None
    report_analysis: Optional[Dict[str, Any]] = None
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    ai_model_used: Optional[str] = None
    evaluation_time: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class EvaluationCriteriaBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    code_quality_weight: float = Field(0.3, ge=0, le=1)
    functionality_weight: float = Field(0.4, ge=0, le=1)
    documentation_weight: float = Field(0.2, ge=0, le=1)
    innovation_weight: float = Field(0.1, ge=0, le=1)
    max_score: int = Field(100, gt=0)

class EvaluationCriteriaCreate(EvaluationCriteriaBase):
    rubric_details: Optional[Dict[str, Any]] = None

class EvaluationCriteria(EvaluationCriteriaBase):
    id: int
    rubric_details: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SubmissionResponse(BaseModel):
    message: str
    project_id: Optional[int] = None
    evaluation_id: Optional[int] = None
    status: str
    comprehensive_analysis: Optional[Dict[str, Any]] = None
    overall_score: Optional[float] = None

class EvaluationRequest(BaseModel):
    project_id: int
    criteria_id: Optional[int] = None
