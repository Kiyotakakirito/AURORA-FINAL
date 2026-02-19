from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import models
from ..schemas import schemas

class ProjectService:
    def create_project(
        self,
        db: Session,
        project: schemas.ProjectCreate,
        file_path: Optional[str] = None,
        pdf_path: Optional[str] = None
    ) -> models.Project:
        """Create a new project"""
        db_project = models.Project(
            name=project.name,
            student_name=project.student_name,
            student_email=project.student_email,
            submission_type=project.submission_type,
            github_url=project.github_url,
            file_path=file_path,
            pdf_path=pdf_path
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def get_project(self, db: Session, project_id: int) -> Optional[models.Project]:
        """Get a project by ID"""
        return db.query(models.Project).filter(models.Project.id == project_id).first()
    
    def get_projects(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Project]:
        """Get all projects with pagination"""
        return db.query(models.Project).offset(skip).limit(limit).all()
    
    def update_project(
        self,
        db: Session,
        project_id: int,
        project: schemas.ProjectUpdate
    ) -> Optional[models.Project]:
        """Update a project"""
        db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if not db_project:
            return None
        
        update_data = project.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def delete_project(self, db: Session, project_id: int) -> bool:
        """Delete a project"""
        db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if not db_project:
            return False
        
        # Delete associated evaluations
        db.query(models.Evaluation).filter(models.Evaluation.project_id == project_id).delete()
        
        # Delete the project
        db.delete(db_project)
        db.commit()
        return True
    
    def get_project_count(self, db: Session) -> int:
        """Get total number of projects"""
        return db.query(models.Project).count()
    
    def get_projects_by_student(
        self,
        db: Session,
        student_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Project]:
        """Get projects by student name"""
        return db.query(models.Project).filter(
            models.Project.student_name == student_name
        ).offset(skip).limit(limit).all()
    
    def search_projects(
        self,
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Project]:
        """Search projects by name or student name"""
        return db.query(models.Project).filter(
            (models.Project.name.contains(query)) |
            (models.Project.student_name.contains(query))
        ).offset(skip).limit(limit).all()
