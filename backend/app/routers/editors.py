from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Role, Project
from ..schemas import ProjectOut
from typing import List

router = APIRouter()

@router.get("/my-projects", response_model=List[ProjectOut])
def my_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != Role.editor:
        return []
    items = db.query(Project).filter(Project.assigned_editor_id == user.id).all()
    return items
