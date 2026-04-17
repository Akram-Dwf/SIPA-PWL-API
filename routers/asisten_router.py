from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import sipa_models
from schemas import sipa_schemas
from auth.security import get_password_hash, get_current_user

router = APIRouter(
    prefix="/asisten",
    tags=["Manajemen Asisten"]
)

@router.post("/", response_model=sipa_schemas.AsistenResponse)
def create_asisten(asisten: sipa_schemas.AsistenCreate, db: Session = Depends(get_db)):
    db_asisten = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.username == asisten.username).first()
    if db_asisten:
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    
    hashed_pwd = get_password_hash(asisten.password)
    
    new_asisten = sipa_models.Asisten(
        nama=asisten.nama,
        kelompok=asisten.kelompok,
        username=asisten.username,
        password=hashed_pwd
    )
    
    db.add(new_asisten)
    db.commit()
    db.refresh(new_asisten)
    return new_asisten

@router.get("/", response_model=list[sipa_schemas.AsistenResponse])
def get_all_asisten(db: Session = Depends(get_db)):
    return db.query(sipa_models.Asisten).all()

@router.get("/{asisten_id}", response_model=sipa_schemas.AsistenResponse)
def get_asisten(asisten_id: int, db: Session = Depends(get_db)):
    db_asisten = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.id == asisten_id).first()
    if not db_asisten:
        raise HTTPException(status_code=404, detail="Asisten tidak ditemukan")
    return db_asisten

@router.put("/{asisten_id}", response_model=sipa_schemas.AsistenResponse)
def update_asisten(asisten_id: int, asisten: sipa_schemas.AsistenCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_asisten = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.id == asisten_id).first()
    if not db_asisten:
        raise HTTPException(status_code=404, detail="Asisten tidak ditemukan")
    
    db_asisten.nama = asisten.nama
    db_asisten.kelompok = asisten.kelompok
    db_asisten.username = asisten.username
    db_asisten.password = get_password_hash(asisten.password)
    
    db.commit()
    db.refresh(db_asisten)
    return db_asisten

@router.delete("/{asisten_id}")
def delete_asisten(asisten_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_asisten = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.id == asisten_id).first()
    if not db_asisten:
        raise HTTPException(status_code=404, detail="Asisten tidak ditemukan")
    
    db.delete(db_asisten)
    db.commit()
    return {"message": f"Asisten dengan ID {asisten_id} berhasil dihapus"}