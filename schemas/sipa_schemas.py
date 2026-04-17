from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# --- SCHEMAS UNTUK PENGAJUAN ---

class PengajuanBase(BaseModel):
    nama_mahasiswa: str = Field(..., min_length=3, max_length=100, description="Nama lengkap mahasiswa")
    nim_mahasiswa: str = Field(..., min_length=10, max_length=10, description="NIM Mahasiswa (10 karakter)")
    waktu_pengajuan: datetime

class PengajuanCreate(PengajuanBase):
    asisten_id: int = Field(..., gt=0, description="ID asisten yang dituju")

class PengajuanResponse(PengajuanBase):
    id: int
    status: str
    asisten_id: int

    class Config:
        from_attributes = True
        
class PengajuanUpdateStatus(BaseModel):
    status: str = Field(..., min_length=5, description="Status baru (Disetujui/Ditolak/Pending)")

# --- SCHEMAS UNTUK ASISTEN ---

class AsistenBase(BaseModel):
    nama: str = Field(..., min_length=3, max_length=100)
    kelompok: str = Field(..., min_length=1, description="Kelompok praktikum")
    username: str = Field(..., min_length=5, pattern="^[a-zA-Z0-9_]+$")

class AsistenCreate(AsistenBase):
    password: str = Field(..., min_length=6)

class AsistenResponse(AsistenBase):
    id: int
    pengajuan: List[PengajuanResponse] = []

    class Config:
        from_attributes = True