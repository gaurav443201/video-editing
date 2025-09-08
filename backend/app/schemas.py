from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from enum import Enum

class Role(str, Enum):
    customer = "customer"
    editor = "editor"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    contact: str
    password: str
    role: Role

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    contact: str
    role: Role
    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role

class ProjectCreate(BaseModel):
    instructions: str = ""
    max_budget: float = 0.0

class ProjectOut(BaseModel):
    id: int
    customer_id: int
    assigned_editor_id: Optional[int] = None
    instructions: str
    max_budget: float
    status: str
    media_paths: str
    sample_path: str
    class Config:
        from_attributes = True

class PaymentInit(BaseModel):
    project_id: int
    amount_total: float
    upfront_amount: float
    transaction_id: str

class PaymentOut(BaseModel):
    id: int
    project_id: int
    amount_total: float
    amount_paid: float
    status: str
    transaction_id: str
    commission_pct: float
    class Config:
        from_attributes = True

class AssignProject(BaseModel):
    project_id: int
    editor_id: int

class ReviewCreate(BaseModel):
    project_id: int
    rating: int = Field(ge=1, le=5)
    feedback: str = ""
