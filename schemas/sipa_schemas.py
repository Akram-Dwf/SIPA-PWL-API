from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PengajuanBase(BaseModel):
    nama_mahasiswa: str
    nim_mahasiswa: str
    waktu_pengajuan: datetime

class PengajuanCreate(PengajuanBase):
    asisten_id: int

class PengajuanResponse(PengajuanBase):
    id: int
    status: str
    asisten_id: int

    class Config:
        from_attributes = True

class AsistenBase(BaseModel):
    nama: str
    kelompok: str
    username: str

class AsistenCreate(AsistenBase):
    password: str

class AsistenResponse(AsistenBase):
    id: int
    pengajuan: List[PengajuanResponse] = []

    class Config:
        from_attributes = True