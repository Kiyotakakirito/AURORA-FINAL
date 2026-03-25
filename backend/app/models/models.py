from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from datetime import datetime
from ..core.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    student_name = Column(String(255), nullable=False)
    student_email = Column(String(255), nullable=True)
    submission_type = Column(String(20), nullable=False)  # 'zip', 'github', 'pdf'
    file_path = Column(String(500), nullable=True)        # Path to uploaded project file
    pdf_path = Column(String(500), nullable=True)         # Path to PDF report
    github_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)
    overall_score = Column(Float, nullable=False)
    max_score = Column(Integer, default=100)
    
    # Detailed scores
    code_quality_score = Column(Float)
    functionality_score = Column(Float)
    documentation_score = Column(Float)
    innovation_score = Column(Float)
    
    # Analysis results — JSON works on both SQLite (text) and PostgreSQL (jsonb)
    code_analysis = Column(JSON)
    report_analysis = Column(JSON)
    comprehensive_analysis = Column(JSON)
    feedback = Column(Text)
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    recommendations = Column(JSON)
    
    # Metadata
    ai_model_used = Column(String(100))
    evaluation_time = Column(Float)                         # seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EvaluationCriteria(Base):
    __tablename__ = "evaluation_criteria"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Weights (should sum to 1.0)
    code_quality_weight = Column(Float, default=0.3)
    functionality_weight = Column(Float, default=0.4)
    documentation_weight = Column(Float, default=0.2)
    innovation_weight = Column(Float, default=0.1)
    
    # Scoring rubric
    max_score = Column(Integer, default=100)
    rubric_details = Column(JSON)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
