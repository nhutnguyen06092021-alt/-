"""Tạo gói ONEFILE Windows dùng ngay và gói mã nguồn sạch."""

from __future__ import annotations

from datetime import date
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent
STAMP = date.today().isoformat()
EXE = ROOT / "release" / "ONEFILE.exe"

SKIP_DIR_NAMES = {
    ".git",
    ".npm-cache",
    ".onefile-venv",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "onefile_test_temp",
    "playwright-report",
    "target",
    "test-results",
}


def include_file(path: Path) -> bool:
    name = path.name.lower()
    relative = path.relative_to(ROOT)
    if relative.parts[:2] == ("src-tauri", "binaries") and path.suffix.lower() == ".exe":
        return False
    if name == ".env" or name.endswith((".pyc", ".pyo", ".sqlite3", ".sqlite3-shm", ".sqlite3-wal", ".tsbuildinfo")):
        return False
    return True


def source_files():
    for current, directories, files in os.walk(ROOT):
        directories[:] = [
            name for name in directories
            if name not in SKIP_DIR_NAMES and not name.startswith("pytest-cache-files-")
        ]
        base = Path(current)
        for name in files:
            path = base / name
            if include_file(path):
                yield path


def verify(path: Path) -> tuple[int, int]:
    with ZipFile(path) as archive:
        broken = archive.testzip()
        if broken:
            raise RuntimeError(f"CRC lỗi: {broken}")
        return len(archive.infolist()), path.stat().st_size


def main() -> int:
    if not EXE.is_file():
        raise FileNotFoundError("Chưa có release/ONEFILE.exe. Hãy chạy build_onefile_exe.py.")

    portable = OUTPUT / f"ONEFILE-Windows-x64-standalone-{STAMP}.zip"
    with ZipFile(portable, "w", ZIP_STORED) as archive:
        archive.write(EXE, "ONEFILE.exe")

    source = OUTPUT / f"MNHUT-Platform-v0.6.0-full-source-final-{STAMP}.zip"
    with ZipFile(source, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in source_files():
            archive.write(path, Path("mnhut_build") / path.relative_to(ROOT))

    for path in (portable, source):
        count, size = verify(path)
        print(f"OK {path} | {count} files | {size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
