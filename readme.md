# SIPA (Sistem Informasi Pengelolaan Asistensi)

SIPA adalah RESTful API berbasis microservices yang dirancang untuk mendigitalisasi alur pengajuan jadwal asistensi antara mahasiswa (praktikan) dan asisten laboratorium. Proyek ini menggunakan **MySQL** sebagai sistem manajemen database utama.

## 🚀 Stack Teknologi
* **Framework**: FastAPI
* **Bahasa**: Python 3.9+
* **ORM**: SQLAlchemy
* **Database**: MySQL (via PyMySQL Driver)
* **Autentikasi**: JWT (JSON Web Token)
* **Validasi**: Pydantic v2

## 🛠️ Fitur Unggulan
1. **Sistem Autentikasi & Otorisasi**:
   - Pendaftaran dan Login Asisten untuk mengamankan endpoint sensitif.
   - **Otorisasi Level Objek (403 Forbidden)**: Menjamin asisten hanya dapat mengubah atau menghapus data akun miliknya sendiri.
2. **Manajemen Pengajuan Jadwal**:
   - Relasi One-to-Many antara Asisten dan Pengajuan.
   - Validasi ketat pada NIM (wajib 10 karakter) menggunakan Pydantic.
   - Fitur update status pengajuan (ACC/Tolak) oleh asisten.
3. **Pencegahan Kebocoran Data**:
   - Skema respons telah dioptimasi untuk menyembunyikan data sensitif pada endpoint publik.

## 📂 Struktur Proyek
.
├── main.py              # Entry point aplikasi
├── database.py          # Konfigurasi koneksi MySQL
├── models/              # Struktur tabel SQLAlchemy
├── schemas/             # Validasi data Pydantic
├── routers/             # Logika endpoint (Asisten & Pengajuan)
├── auth/                # Keamanan & JWT Token
├── requirements.txt     # Daftar dependensi lengkap
└── README.md            # Dokumentasi proyek

