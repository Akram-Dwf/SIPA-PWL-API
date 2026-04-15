from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import sipa_models
from schemas import sipa_schemas

router = APIRouter(
    prefix="/asisten",
    tags=["Asisten"]
)

@router.post("/", response_model=sipa_schemas.AsistenResponse)
def create_asisten(asisten: sipa_schemas.AsistenCreate, db: Session = Depends(get_db)):
    db_asisten = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.username == asisten.username).first()
    if db_asisten:
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    
    new_asisten = sipa_models.Asisten(
        nama=asisten.nama,
        kelompok=asisten.kelompok,
        username=asisten.username,
        password=asisten.password 
    )
    
    db.add(new_asisten)
    db.commit()
    db.refresh(new_asisten)
    return new_asisten

@router.get("/", response_model=list[sipa_schemas.AsistenResponse])
def get_all_asisten(db: Session = Depends(get_db)):
    return db.query(sipa_models.Asisten).all()