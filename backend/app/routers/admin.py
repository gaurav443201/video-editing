from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..deps import get_db, require_role
from ..models import Role, ProjectStatus, PaymentStatus

router = APIRouter()

@router.post("/assign", response_model=schemas.ProjectOut)
def assign_editor(payload: schemas.AssignProject, db: Session = Depends(get_db), admin=Depends(require_role(Role.admin))):
    prj = db.query(models.Project).filter(models.Project.id == payload.project_id).first()
    ed = db.query(models.User).filter(models.User.id == payload.editor_id, models.User.role == Role.editor).first()
    if not prj or not ed:
        raise HTTPException(status_code=404, detail="Project or editor not found")
    if prj.status != ProjectStatus.pending:
        raise HTTPException(status_code=400, detail="Project not pending")
    prj.assigned_editor_id = ed.id
    prj.status = ProjectStatus.assigned
    db.commit()
    db.refresh(prj)
    return prj

@router.post("/review/{project_id}", response_model=schemas.ProjectOut)
def review_sample(project_id: int, approve: bool, db: Session = Depends(get_db), admin=Depends(require_role(Role.admin))):
    prj = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    if prj.status != ProjectStatus.review:
        raise HTTPException(status_code=400, detail="No sample to review")
    prj.status = ProjectStatus.completed if approve else ProjectStatus.rejected
    db.commit()
    db.refresh(prj)
    return prj

@router.post("/payment-release/{project_id}", response_model=schemas.PaymentOut)
def release_payment(project_id: int, db: Session = Depends(get_db), admin=Depends(require_role(Role.admin))):
    pay = db.query(models.Payment).filter(models.Payment.project_id == project_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    if pay.status != PaymentStatus.completed:
        raise HTTPException(status_code=400, detail="Customer payment not completed")
    # compute editor payout after commission
    editor_payout = pay.amount_total * (1 - pay.commission_pct / 100.0)
    # in real life, trigger transfer to editor's account here
    return pay
