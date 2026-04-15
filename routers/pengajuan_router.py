from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import sipa_models
from schemas import sipa_schemas

router = APIRouter(
    prefix="/pengajuan",
    tags=["Pengajuan Jadwal"]
)

@router.post("/", response_model=sipa_schemas.PengajuanResponse)
def create_pengajuan(pengajuan: sipa_schemas.PengajuanCreate, db: Session = Depends(get_db)):
    db_asisten = db.query(sipa_models.Asisten).filter(sipa_models.Asisten.id == pengajuan.asisten_id).first()
    
    if not db_asisten:
        raise HTTPException(status_code=404, detail="Asisten tidak ditemukan")
    
    new_pengajuan = sipa_models.PengajuanJadwal(
        nama_mahasiswa=pengajuan.nama_mahasiswa,
        nim_mahasiswa=pengajuan.nim_mahasiswa,
        waktu_pengajuan=pengajuan.waktu_pengajuan,
        asisten_id=pengajuan.asisten_id
    )
    
    db.add(new_pengajuan)
    db.commit()
    db.refresh(new_pengajuan)
    return new_pengajuan