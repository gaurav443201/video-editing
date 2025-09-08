from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..deps import get_db, get_current_user
from ..models import Role, PaymentStatus, ProjectStatus

router = APIRouter()

@router.post("/initiate", response_model=schemas.PaymentOut)
def initiate_payment(payload: schemas.PaymentInit, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != Role.customer:
        raise HTTPException(status_code=403, detail="Customers only")
    prj = db.query(models.Project).filter(models.Project.id == payload.project_id, models.Project.customer_id == user.id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    pay = models.Payment(
        project_id=prj.id,
        amount_total=payload.amount_total,
        amount_paid=payload.upfront_amount,
        transaction_id=payload.transaction_id,
        status=PaymentStatus.partial if payload.upfront_amount > 0 else PaymentStatus.pending
    )
    db.add(pay)
    db.commit()
    db.refresh(pay)
    return pay

@router.post("/complete/{project_id}", response_model=schemas.PaymentOut)
def complete_payment(project_id: int, amount: float, txn: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != Role.customer:
        raise HTTPException(status_code=403, detail="Customers only")
    pay = db.query(models.Payment).filter(models.Payment.project_id == project_id).first()
    if not pay:
        raise HTTPException(status_code=404, detail="Payment not found")
    pay.amount_paid += amount
    if pay.amount_paid >= pay.amount_total:
        pay.status = PaymentStatus.completed
    pay.transaction_id = txn
    db.commit()
    db.refresh(pay)
    return pay
