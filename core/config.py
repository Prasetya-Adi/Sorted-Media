import os
import sys
from pathlib import Path

# =========================================================
# PATH DETECTION
# works untuk .py maupun .exe (PyInstaller frozen)
# =========================================================

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

EXIFTOOL = BASE_DIR / "exiftool-13.49_64" / "exiftool.exe"

# =========================================================
# THREAD CONFIG
# =========================================================

CPU = os.cpu_count() or 8
WORKERS = max(4, int(CPU * 0.75))

# =========================================================
# MEDIA EXTENSIONS WHITELIST
# =========================================================

MEDIA_EXT = {
    # foto
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".heic", ".heif", ".webp", ".raw", ".cr2", ".cr3", ".nef",
    ".arw", ".dng", ".orf", ".rw2", ".pef", ".srw",
    # video
    ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm",
    ".m4v", ".3gp", ".mts", ".m2ts", ".ts", ".mpg", ".mpeg",
}