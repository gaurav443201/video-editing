from fastapi import APIRouter, Depends
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

# Create a new project
@router.post("/create")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {"message": "Project created successfully", "project": new_project}

# Get all projects
@router.get("/all")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects

# Get a single project by ID
@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return {"error": "Project not found"}
    return project
