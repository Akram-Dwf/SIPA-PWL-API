from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
import schemas.sipa_schemas as sipa_schemas
import models.sipa_models as sipa_models
from auth.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from routers.asisten_router import create_asisten

router = APIRouter(tags=["Autentikasi"])

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@router.post("/register", response_model=sipa_schemas.AsistenResponse, status_code=status.HTTP_201_CREATED)
def register_asisten(asisten: sipa_schemas.AsistenCreate, db: Session = Depends(get_db)):
    return create_asisten(asisten=asisten, db=db)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}