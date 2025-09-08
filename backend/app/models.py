from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .db import Base

class Role(str, enum.Enum):
    customer = "customer"
    editor = "editor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    contact = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.customer)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProjectStatus(str, enum.Enum):
    pending = "pending"
    assigned = "assigned"
    under_editing = "under_editing"
    review = "review"
    completed = "completed"
    rejected = "rejected"

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    assigned_editor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    instructions = Column(Text, default="")
    max_budget = Column(Float, default=0.0)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.pending)
    media_paths = Column(Text, default="")  # comma-separated file paths
    sample_path = Column(Text, default="")  # uploaded by editor
    created_at = Column(DateTime, default=datetime.utcnow)

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    partial = "partial"
    completed = "completed"

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    amount_total = Column(Float, default=0.0)
    amount_paid = Column(Float, default=0.0)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    transaction_id = Column(String, default="")  # e.g., UPI txn ref
    commission_pct = Column(Float, default=10.0)  # admin commission %
    created_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    rating = Column(Integer, default=5)
    feedback = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
