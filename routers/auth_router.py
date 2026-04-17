from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import sipa_models
from auth.security import verify_password, create_access_token

router = APIRouter(
    tags=["Autentikasi"]
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_asisten = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.username == form_data.username).first()
    

    if not db_asisten or not verify_password(form_data.password, db_asisten.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    access_token = create_access_token(data={"sub": db_asisten.username})
    

    return {"access_token": access_token, "token_type": "bearer"}