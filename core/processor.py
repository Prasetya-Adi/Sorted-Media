import shutil
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

from core.config import WORKERS
from utils.helpers import get_meta, unique_dest


def process(file: Path, sorted_dir: Path) -> None:
    """
    Proses satu file:
    - Ambil metadata (tanggal + device)
    - Buat folder tujuan
    - Move + rename otomatis
    """
    try:
        date, device = get_meta(file)

        folder = sorted_dir / f"{date.strftime('%Y %m')} {device}"
        folder.mkdir(parents=True, exist_ok=True)

        new_name = date.strftime("%Y%m%d_%H%M%S") + file.suffix.lower()
        dest = unique_dest(folder / new_name)

        shutil.move(str(file), dest)

    except Exception as e:
        tqdm.write(f"⚠️  Skip {file.name}: {e}")


def run_pipeline(files: list[Path], sorted_dir: Path) -> None:
    """Jalankan pipeline dengan ThreadPoolExecutor + progress bar."""
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        list(tqdm(
            executor.map(lambda f: process(f, sorted_dir), files),
            total=len(files),
            desc="Sorting",
            unit="file"
        ))