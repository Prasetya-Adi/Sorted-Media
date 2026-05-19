"""
sorted_media — entry point utama.

Usage:
    python main.py                              # pakai folder saat ini
    python main.py "D:\\Photos"                 # path tanpa spasi
    python main.py "C:/Users/Nama Spasi/Foto"  # path dengan spasi, pakai quote
"""

import sys
from pathlib import Path

from core.config import EXIFTOOL, WORKERS, MEDIA_EXT
from core.processor import run_pipeline


def collect_files(root: Path) -> list[Path]:
    """Kumpulkan semua file media, kecuali yang sudah ada di folder sorted/."""
    return [
        f for f in root.rglob("*")
        if f.is_file()
        and "sorted" not in f.parts
        and f.suffix.lower() in MEDIA_EXT
    ]


def main():
    # ── resolve ROOT ──────────────────────────────────────
    # join sys.argv[1:] agar path dengan spasi tidak terpotong
    # misal: python main.py C:\Users\Prasetya Adi\Downloads
    # → argv = ['main.py', 'C:\\Users\\Prasetya', 'Adi\\Downloads']
    # → di-join → 'C:\\Users\\Prasetya Adi\\Downloads'
    if len(sys.argv) > 1:
        root = Path(" ".join(sys.argv[1:]))
    else:
        root = Path.cwd()

    sorted_dir = root / "sorted"

    # ── validasi folder target ────────────────────────────
    if not root.exists():
        print(f"\n❌ Folder tidak ditemukan: {root}")
        print("   Tips: gunakan tanda kutip jika path mengandung spasi:")
        print('   python main.py "C:/Users/Nama Dengan Spasi/Downloads"')
        sys.exit(1)

    if not root.is_dir():
        print(f"\n❌ Path bukan folder: {root}")
        sys.exit(1)

    # ── banner ────────────────────────────────────────────
    print(f"\n📂 Folder  : {root}")
    print(f"🧵 Threads : {WORKERS}")
    print("📝 Mode    : MOVE + RENAME otomatis\n")

    # ── validasi exiftool ─────────────────────────────────
    if not EXIFTOOL.exists():
        print(f"❌ ExifTool tidak ditemukan di: {EXIFTOOL}")
        print("   Download: https://exiftool.org")
        sys.exit(1)

    # ── buat folder sorted ────────────────────────────────
    sorted_dir.mkdir(parents=True, exist_ok=True)

    # ── kumpulkan file ────────────────────────────────────
    files = collect_files(root)
    if not files:
        print("ℹ️  Tidak ada file media yang ditemukan.")
        sys.exit(0)

    print(f"📦 Total file : {len(files)}")
    print("🚀 Sorting...\n")

    # ── jalankan pipeline ─────────────────────────────────
    run_pipeline(files, sorted_dir)

    print("\n✅ DONE. Semua beres, rapi, rename otomatis 😎\n")


if __name__ == "__main__":
    main()

    # pause hanya jika jalan sebagai .exe (bukan terminal biasa)
    if getattr(sys, 'frozen', False):
        input("Tekan Enter untuk menutup...")