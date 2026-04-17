from fastapi import FastAPI
from database import engine
from models import sipa_models
from routers import asisten_router, pengajuan_router, auth_router

sipa_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIPA API",
    description="Sistem Manajemen Persetujuan Asistensi Praktikum",
    version="1.0.0"
)

app.include_router(auth_router.router)
app.include_router(asisten_router.router)
app.include_router(pengajuan_router.router)

@app.get("/")
def read_root():
    return {"message": "Server SIPA API berhasil berjalan!"}