import re
import subprocess
from pathlib import Path
from datetime import datetime

from core.config import EXIFTOOL


def clean_name(name: str) -> str:
    """Hapus karakter yang tidak valid untuk nama folder/file Windows."""
    return re.sub(r'[\\/:*?"<>|]', '', name).strip()


def get_meta(file_path: Path) -> tuple[datetime, str]:
    """
    Ambil tanggal & device dari EXIF metadata.

    Priority:
        1. DateTimeOriginal
        2. CreateDate
        3. MediaCreateDate
        4. mtime (fallback)
    """
    cmd = [
        str(EXIFTOOL),
        "-s", "-s", "-s",
        "-DateTimeOriginal",
        "-CreateDate",
        "-MediaCreateDate",
        "-Model",
        "-d", "%Y-%m-%d %H:%M:%S",
        str(file_path)
    ]

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().splitlines()

        date = None
        model = "UnknownDevice"

        for line in out:
            if not date and re.match(r"\d{4}-\d{2}-\d{2}", line):
                date = datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
            elif line and not re.match(r"\d{4}-", line):
                model = clean_name(line)

        if date:
            return date, model

    except Exception:
        pass

    # fallback ke mtime
    try:
        return datetime.fromtimestamp(file_path.stat().st_mtime), "UnknownDevice"
    except Exception:
        return datetime.now(), "UnknownDevice"


def unique_dest(dest: Path) -> Path:
    """Tambahkan suffix _1, _2, dst. jika nama file sudah ada."""
    if not dest.exists():
        return dest

    i = 1
    while True:
        candidate = dest.with_stem(dest.stem + f"_{i}")
        if not candidate.exists():
            return candidate
        i += 1