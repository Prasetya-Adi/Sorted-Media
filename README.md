# 📷 Sorted Media

Script Python untuk **otomatis sorting & rename** file foto dan video berdasarkan tanggal pengambilan dan nama perangkat (kamera/HP) dari metadata EXIF.

---

## ✨ Fitur

- 📅 **Sort by date** — folder dibuat per bulan (`2024 03 [NAMA DEVICE]`)
- 🏷️ **Auto rename** — file direname ke format `20240315_143022.jpg`
- 🔁 **Auto deduplikasi** — jika nama bentrok, otomatis jadi `20240315_143022_1.jpg`
- ⚡ **Multi-threading** — proses paralel, cepat untuk ribuan file
- 📊 **Progress bar** — via `tqdm`
- 🎯 **Filter ekstensi** — hanya foto & video yang diproses, file lain diabaikan
- 🔒 **Fallback aman** — jika EXIF tidak tersedia, pakai `mtime` file

---

## 📁 Struktur Project

```
sorted-media/
├── main.py               ← entry point utama
├── requirements.txt
├── .gitignore
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── config.py         ← konfigurasi path, thread, ekstensi
│   └── processor.py      ← pipeline multi-thread
│
├── utils/
│   ├── __init__.py
│   └── helpers.py        ← fungsi EXIF, clean name, deduplikasi
│
└── exiftool-13.49_64/    ← ⚠️ DOWNLOAD SENDIRI (tidak ada di repo)
    └── exiftool.exe
```

---

## ⚙️ Requirements

### 1. Python

Python 3.10+ (karena pakai type hints modern)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. ExifTool _(wajib, download manual)_

> ExifTool **tidak disertakan** di repo ini karena merupakan software pihak ketiga.

1. Download di: **https://exiftool.org** → pilih _Windows Executable_
2. Ekstrak, lalu rename foldernya menjadi `exiftool-13.49_64`
3. Pastikan `exiftool.exe` ada di dalam folder tersebut
4. Letakkan folder itu **sejajar dengan `main.py`**

Struktur yang benar:

```
sorted-media/
├── main.py
└── exiftool-13.49_64/
    └── exiftool.exe      ✅
```

---

## 🚀 Cara Pakai

### Opsi A — Jalankan di folder saat ini

```bash
cd D:\Photos
python path\to\main.py
```

### Opsi B — Tentukan folder target

```bash
python main.py "D:\Photos\Liburan 2024"
```

### Output

Semua file akan dipindahkan ke subfolder `sorted/` di dalam folder target:

```
D:\Photos\
└── sorted\
    ├── 2024 03 Samsung Galaxy S23\
    │   ├── 20240315_143022.jpg
    │   └── 20240316_091500.mp4
    └── 2024 04 UnknownDevice\
        └── 20240402_120000.jpg
```

---

## 📋 Ekstensi yang Didukung

| Kategori  | Format                                                                                                                                    |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Foto**  | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.tiff` `.heic` `.heif` `.webp` `.raw` `.cr2` `.cr3` `.nef` `.arw` `.dng` `.orf` `.rw2` `.pef` `.srw` |
| **Video** | `.mp4` `.mov` `.avi` `.mkv` `.wmv` `.flv` `.webm` `.m4v` `.3gp` `.mts` `.m2ts` `.ts` `.mpg` `.mpeg`                                       |

---

## ⚠️ Catatan Penting

- Script ini **memindahkan (MOVE)** file, bukan copy. Pastikan backup dulu jika perlu.
- File yang sudah ada di folder `sorted/` tidak akan diproses ulang.
- Jika EXIF tidak ditemukan, tanggal fallback ke **modification time** file.

---

## 📜 Lisensi

MIT License — bebas dipakai dan dimodifikasi.
