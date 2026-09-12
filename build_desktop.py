"""Đóng gói MNHUT Platform thành ứng dụng Windows có backend đi kèm."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "prototype_ui"
TAURI = ROOT / "src-tauri"
TARGET = "x86_64-pc-windows-gnu"
VENV_PYTHON = BACKEND / ".venv" / "Scripts" / "python.exe"


def phai_co(path: Path, mo_ta: str) -> Path:
    if not path.exists():
        raise RuntimeError(f"Không tìm thấy {mo_ta}: {path}")
    return path


def main() -> int:
    try:
        python = phai_co(VENV_PYTHON, "Python của backend")
        cargo = phai_co(Path.home() / ".cargo" / "bin" / "cargo.exe", "Cargo")
        mingw = phai_co(Path("D:/Compiler/mingw64/bin"), "MinGW")
        npm = shutil.which("npm.cmd")
        if not npm:
            raise RuntimeError("Không tìm thấy npm trong PATH")

        binaries = TAURI / "binaries"
        binaries.mkdir(parents=True, exist_ok=True)
        dich = binaries / f"mnhut-backend-{TARGET}.exe"
        dist = ROOT / "build" / "sidecar-dist"
        work = ROOT / "build" / "sidecar-work"
        spec = ROOT / "build" / "sidecar-spec"
        add_data = f"{ROOT / 'migrations'}{os.pathsep}migrations"

        print("[1/2] Đang đóng gói dịch vụ FastAPI đi kèm...")
        subprocess.run(
            [
                str(python), "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
                "--name", "mnhut-backend", "--paths", str(ROOT), "--add-data", add_data,
                "--distpath", str(dist), "--workpath", str(work), "--specpath", str(spec),
                str(BACKEND / "sidecar.py"),
            ],
            cwd=ROOT,
            check=True,
        )
        shutil.copy2(dist / "mnhut-backend.exe", dich)

        print("[2/2] Đang biên dịch ứng dụng Windows Tauri...")
        env = os.environ.copy()
        env["PATH"] = os.pathsep.join([str(cargo.parent), str(mingw), env.get("PATH", "")])
        env["RUSTUP_TOOLCHAIN"] = "stable-x86_64-pc-windows-gnu"
        thu_muc_tam = ROOT / "build" / "tauri-temp"
        thu_muc_tam.mkdir(parents=True, exist_ok=True)
        env["TEMP"] = str(thu_muc_tam)
        env["TMP"] = str(thu_muc_tam)
        subprocess.run(
            [npm, "run", "desktop:build", "--", "--target", TARGET],
            cwd=FRONTEND,
            env=env,
            check=True,
        )
        print("Đóng gói ứng dụng Windows: ĐẠT")
        return 0
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Đóng gói ứng dụng Windows thất bại: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
