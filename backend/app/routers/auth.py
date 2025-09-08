from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import Base, engine
from ..deps import get_db
from ..security import get_password_hash, verify_password, create_access_token

Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/signup", response_model=schemas.UserOut)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter((models.User.username == payload.username) | (models.User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    user = models.User(
        username=payload.username,
        email=payload.email,
        contact=payload.contact,
        hashed_password=get_password_hash(payload.password),
        role=models.Role(payload.role)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.TokenOut)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.id, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer", "role": user.role.value}
