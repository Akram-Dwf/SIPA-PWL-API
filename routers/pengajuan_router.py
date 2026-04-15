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

@router.patch("/{pengajuan_id}/status", response_model=sipa_schemas.PengajuanResponse)
def update_status_pengajuan(pengajuan_id: int, status_update: sipa_schemas.PengajuanUpdateStatus, db: Session = Depends(get_db)):
    db_pengajuan = db.query(sipa_models.PengajuanJadwal).filter(sipa_models.PengajuanJadwal.id == pengajuan_id).first()
    
    if not db_pengajuan:
        raise HTTPException(status_code=404, detail="Pengajuan tidak ditemukan")
    
    status_rapi = status_update.status.capitalize()
    
    if status_rapi not in ["Disetujui", "Ditolak", "Pending"]:
        raise HTTPException(status_code=400, detail="Status tidak valid. Gunakan: Disetujui, Ditolak, atau Pending")
        
    db_pengajuan.status = status_rapi
    db.commit()
    db.refresh(db_pengajuan)
    return db_pengajuan

@router.delete("/{pengajuan_id}")
def delete_pengajuan(pengajuan_id: int, db: Session = Depends(get_db)):
    db_pengajuan = db.query(sipa_models.PengajuanJadwal).filter(sipa_models.PengajuanJadwal.id == pengajuan_id).first()
    
    if not db_pengajuan:
        raise HTTPException(status_code=404, detail="Pengajuan tidak ditemukan")
    
    db.delete(db_pengajuan)
    db.commit()
    return {"message": f"Pengajuan dengan ID {pengajuan_id} berhasil dibatalkan"}