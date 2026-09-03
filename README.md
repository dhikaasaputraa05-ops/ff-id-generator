# Free Fire ID Generator

Generator ID Free Fire yang lengkap dengan multi-threading, pattern analysis, dan sistem penyimpanan hasil otomatis.

## 🎯 Fitur Utama

### Generator
- ✅ Generate ID numerik 11 digit (customizable)
- ✅ Multi-threading untuk performa maksimal
- ✅ Real-time monitoring ID yang diproses
- ✅ Perhitungan kecepatan generator (ID/detik)
- ✅ Start, Stop, dan Pause yang aman

### Pattern Detection (Pola Rare)
- 🔹 **Kembar** - Angka kembar berturut-turut (111, 222, 333)
- 🔹 **Berulang** - Pola ABA (121, 131, 242)
- 🔹 **Urutan** - Urutan angka naik/turun (123, 456, 789)
- 🔹 **Palindrome** - ID yang sama jika dibaca terbalik (12321, 54345)
- 🔹 **Kombinasi Pendek** - Kombinasi unik (111222, 123321)
- 🔹 **Custom Pattern** - Pola custom sesuai keinginan

### Penyimpanan & Logging
- 💾 Otomatis simpan hasil ke file TXT
- 💾 Otomatis simpan hasil ke file JSON
- 📋 Sistem error logging lengkap
- 📊 Statistik generator yang detail

### User Interface
- 🎨 Tampilan terminal dengan warna (colorama)
- 📱 Menu interaktif yang user-friendly
- 📈 Real-time status bar display
- ⚙️ Pengaturan thread dan panjang ID

### Account Creator (Template)
- 🔐 Template integrasi API resmi untuk pembuatan akun
- ✅ Validation kredensial dan input
- ✅ Rate limiter untuk menghormati API limits
- ❌ TIDAK melakukan bypass CAPTCHA, OTP, atau verifikasi
- ✅ Hanya menggunakan API sandbox/development

## 📋 Struktur Project

```
ff-id-generator/
├── main.py                 # File utama aplikasi
├── generator.py            # Multi-threading ID generator
├── pattern_checker.py      # Pattern detection & analysis
├── storage.py              # Penyimpanan file & logging
├── display.py              # Terminal display dengan warna
├── account_creator.py      # Template integrasi API
├── config.json             # Konfigurasi default
├── requirements.txt        # Dependencies
└── README.md               # Dokumentasi
```

## 🚀 Instalasi di Termux

### 1. Clone Repository
```bash
git clone https://github.com/dhikaasaputraa05-ops/ff-id-generator.git
cd ff-id-generator
```

### 2. Install Python & Dependencies
```bash
# Update package manager
pkg update && pkg upgrade

# Install Python 3
pkg install python

# Install pip
pkg install python-pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Verifikasi Instalasi
```bash
python main.py
# atau
python3 main.py
```

## 💻 Cara Menggunakan

### Jalankan Aplikasi
```bash
# Dari direktori project
python main.py

# Atau dengan Python 3 explicit
python3 main.py
```

### Menu Utama
```
1. Mulai Generator (Mode Normal)
   - Generate ID dengan pola rare detection
   - Input durasi running time

2. Mulai Generator (Mode Custom Pattern)
   - Define custom pattern dengan wildcard (?)
   - Contoh: 1?2?3???1?3
   - Pattern akan di-cek saat generate

3. Pengaturan Thread & ID Length
   - Ubah jumlah thread (2-16)
   - Ubah panjang ID (5-20 digit)

4. Lihat Info Pola Rare
   - Penjelasan lengkap setiap pola
   - Contoh ID untuk tiap pola
   - Tingkat kelangkaan

5. Baca File Hasil
   - Baca file TXT
   - Baca file JSON
   - View statistik

6. Exit
   - Keluar dengan aman
```

## 📊 Output & Hasil

### File TXT (rare_ids.txt)
```
================================================================================
                    FREE FIRE RARE ID GENERATOR - HASIL SCAN
================================================================================
Waktu Export: 2026-09-03 15:35:42
Total ID Rare: 42
================================================================================

ID #1
  ID: 12345678901
  Pola: urutan, kombinasi_pendek
  Waktu: 2026-09-03T15:30:12.345678
--------...
```

### File JSON (rare_ids.json)
```json
{
  "export_time": "2026-09-03T15:35:42.123456",
  "total_rare_ids": 42,
  "rare_ids": [
    {
      "id": "12345678901",
      "patterns": {
        "urutan": true,
        "kombinasi_pendek": true
      },
      "timestamp": "2026-09-03T15:30:12.345678"
    }
  ]
}
```

### Error Log (logs/errors.log)
```
================================================================================
                    FREE FIRE ID GENERATOR - ERROR LOG
================================================================================
Total Errors: 3
================================================================================

Error #1
  Waktu: 2026-09-03 15:28:15
  Tipe: thread_error
  Pesan: Thread 2 error: ...
```

## ⚙️ Konfigurasi (config.json)

```json
{
  "default_threads": 4,
  "default_id_length": 11,
  "output_dir": "./output",
  "logs_dir": "./logs",
  "rare_patterns": {
    "kembar": {"enabled": true},
    "berulang": {"enabled": true},
    "urutan": {"enabled": true},
    "palindrome": {"enabled": true},
    "kombinasi_pendek": {"enabled": true}
  },
  "save_formats": ["txt", "json"],
  "display_refresh_rate": 1
}
```

## 📚 Module Documentation

### generator.py
```python
from generator import IDGenerator
from storage import Storage

# Inisialisasi
storage = Storage()
gen = IDGenerator(id_length=11, num_threads=4, storage=storage)

# Start generator
gen.start(custom_patterns=['1?2?3'])

# Dapatkan statistik
stats = gen.get_statistics()

# Stop generator
gen.stop()
```

### pattern_checker.py
```python
from pattern_checker import PatternChecker

checker = PatternChecker()

# Check patterns
print(checker.is_kembar("11123456789"))    # True
print(checker.is_urutan("12345678901"))   # True

# Analyze full ID
patterns = checker.analyze("11123456789")
```

### storage.py
```python
from storage import Storage

storage = Storage()

# Add rare ID
storage.add_rare_id("12345678901", {'kembar': True})

# Save to files
storage.save_all()
```

## 🔒 Keamanan & Etika

### account_creator.py
⚠️ **PENTING**: Modul ini adalah TEMPLATE saja!
- ✅ Menggunakan API sandbox/development resmi
- ✅ Memiliki kredensial yang sah dan terdaftar
- ✅ Menghormati rate limit dari provider
- ❌ TIDAK melakukan bypass CAPTCHA
- ❌ TIDAK melakukan otomasi OTP/verifikasi

## 📝 Contoh Penggunaan

### Mode Normal
```bash
$ python main.py
[Menu] Pilih: 1
[Duration] Masukkan durasi: 60
[Running...]
Total ID: 5420 | Rare: 32 | Speed: 90 ID/s
```

### Custom Pattern
```bash
$ python main.py
[Menu] Pilih: 2
[Pattern] Masukkan: 1?2?3?4?5?6
[Running...]
Ditemukan: 8 ID dengan pattern
```

## 🐛 Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Generator lambat
- Naikkan thread count (Settings)
- Kurangi panjang ID

### File tidak tersimpan
- Check folder `output/` dibuat
- Check permission direktori

## 📈 Performance Tips

1. **Optimal Thread**
   - 2-core: 2-4 threads
   - 4-core: 4-8 threads
   - 8-core: 8-16 threads

2. **Speed Improvement**
   - Naikkan thread count
   - Kurangi panjang ID

## 📄 Lisensi

MIT License - Bebas digunakan

## 👤 Author

**dhikaasaputraa05-ops**

---

**Happy ID Generating! 🚀**
