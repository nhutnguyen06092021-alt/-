"""Build ONEFILE.exe tự chứa frontend và toàn bộ converter."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
PYTHON = ROOT / "backend" / ".onefile-venv" / "Scripts" / "python.exe"
STATIC = ROOT / "prototype_ui" / "dist"


def main() -> int:
    if not PYTHON.is_file():
        print("Hãy chạy START_ONEFILE.cmd một lần trước khi build EXE.", file=sys.stderr)
        return 1
    if not (STATIC / "onefile" / "index.html").is_file():
        print("Thiếu frontend build. Hãy chạy START_ONEFILE.cmd.", file=sys.stderr)
        return 1
    command = [
        str(PYTHON), "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
        "--name", "ONEFILE", "--paths", str(ROOT),
        "--icon", str(ROOT / "src-tauri" / "icons" / "icon.ico"),
        "--add-data", f"{STATIC}{os.pathsep}onefile_static",
        "--collect-submodules", "backend.onefile",
        "--collect-all", "imageio_ffmpeg",
        "--collect-all", "pillow_heif",
        "--distpath", str(ROOT / "release"),
        "--workpath", str(ROOT / "build" / "onefile-exe-work"),
        "--specpath", str(ROOT / "build" / "onefile-exe-spec"),
        str(ROOT / "onefile_windows.py"),
    ]
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Build ONEFILE.exe thất bại: {exc}", file=sys.stderr)
        return 1
    print(f"Đã tạo: {ROOT / 'release' / 'ONEFILE.exe'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
