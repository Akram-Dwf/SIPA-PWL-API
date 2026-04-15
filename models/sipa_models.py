from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Asisten(Base):
    __tablename__ = "asisten"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    kelompok = Column(String(50))
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))

    pengajuan = relationship("PengajuanJadwal", back_populates="asisten_pembimbing")

class PengajuanJadwal(Base):
    __tablename__ = "pengajuan_jadwal"

    id = Column(Integer, primary_key=True, index=True)
    nama_mahasiswa = Column(String(100))
    nim_mahasiswa = Column(String(20))
    waktu_pengajuan = Column(DateTime)
    status = Column(String(20), default="Pending")
    asisten_id = Column(Integer, ForeignKey("asisten.id"))

    asisten_pembimbing = relationship("Asisten", back_populates="pengajuan")