from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
import os, uuid
from .. import schemas, models
from ..deps import get_db, get_current_user
from ..models import Role, ProjectStatus

UPLOAD_DIR = "backend/app/storage/uploads"

router = APIRouter()

@router.post("", response_model=schemas.ProjectOut)
async def create_project(
    instructions: str = Form(""),
    max_budget: float = Form(0.0),
    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != Role.customer:
        raise HTTPException(status_code=403, detail="Only customers can create projects")
    paths = []
    if files:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        for f in files:
            ext = os.path.splitext(f.filename)[1]
            fname = f"{uuid.uuid4().hex}{ext}"
            dest = os.path.join(UPLOAD_DIR, fname)
            with open(dest, "wb") as out:
                out.write(await f.read())
            paths.append(dest)
    project = models.Project(
        customer_id=user.id,
        instructions=instructions,
        max_budget=max_budget,
        media_paths=",".join(paths) if paths else ""
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/available", response_model=List[schemas.ProjectOut])
def available_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != Role.editor:
        raise HTTPException(status_code=403, detail="Editors only")
    items = db.query(models.Project).filter(models.Project.status == ProjectStatus.pending).all()
    return items

@router.post("/{project_id}/accept", response_model=schemas.ProjectOut)
def accept_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != Role.editor:
        raise HTTPException(status_code=403, detail="Editors only")
    prj = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    if prj.status != ProjectStatus.pending:
        raise HTTPException(status_code=400, detail="Already taken by someone else")
    prj.assigned_editor_id = user.id
    prj.status = ProjectStatus.assigned
    db.commit()
    db.refresh(prj)
    return prj

SAMPLES_DIR = "backend/app/storage/samples"

@router.post("/{project_id}/sample", response_model=schemas.ProjectOut)
async def upload_sample(project_id: int, sample: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != Role.editor:
        raise HTTPException(status_code=403, detail="Editors only")
    prj = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    if prj.assigned_editor_id != user.id:
        raise HTTPException(status_code=403, detail="Not your project")
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    path = os.path.join(SAMPLES_DIR, f"{project_id}_{uuid.uuid4().hex}_{sample.filename}")
    with open(path, "wb") as out:
        out.write(await sample.read())
    prj.sample_path = path
    prj.status = ProjectStatus.review
    db.commit()
    db.refresh(prj)
    return prj

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    prj = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == Role.customer and prj.customer_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if user.role == Role.editor and prj.assigned_editor_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return prj
