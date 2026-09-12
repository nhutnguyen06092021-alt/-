from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "prototype_ui"
VENV_PYTHON = BACKEND / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def kiem_tra() -> tuple[Path, str]:
    if not VENV_PYTHON.exists():
        raise RuntimeError("Chưa có môi trường backend. Hãy tạo backend/.venv và cài backend/requirements-dev.txt.")
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    if not npm:
        raise RuntimeError("Không tìm thấy npm trong PATH.")
    subprocess.run([str(VENV_PYTHON), "-c", "import fastapi,uvicorn,pydantic"], check=True)
    subprocess.run([npm, "--version"], cwd=FRONTEND, check=True, stdout=subprocess.DEVNULL)
    if not (FRONTEND / "node_modules").exists():
        raise RuntimeError("Chưa có dependency frontend. Hãy chạy npm install trong prototype_ui/.")
    return VENV_PYTHON, npm


def dung_tien_trinh(processes: list[subprocess.Popen[bytes]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()
    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Khởi động môi trường phát triển MNHUT Platform")
    parser.add_argument("--kiem-tra", action="store_true", help="Chỉ kiểm tra dependency và entrypoint")
    parser.add_argument("--desktop", action="store_true", help="Mở Tauri; yêu cầu Rust và Cargo")
    args = parser.parse_args()

    try:
        python, npm = kiem_tra()
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Không thể khởi động: {exc}", file=sys.stderr)
        return 1

    if args.kiem_tra:
        print("Kiểm tra entrypoint: ĐẠT")
        print(f"Backend Python: {python}")
        print(f"Frontend npm: {npm}")
        return 0

    backend = subprocess.Popen(
        [str(python), "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=ROOT,
    )
    frontend_command = [npm, "run", "dev"]
    frontend_env = os.environ.copy()
    if args.desktop:
        cargo_home = Path.home() / ".cargo" / "bin"
        mingw = Path("D:/Compiler/mingw64/bin")
        frontend_env["PATH"] = os.pathsep.join([str(cargo_home), str(mingw), frontend_env.get("PATH", "")])
        frontend_env["MNHUT_EXTERNAL_BACKEND"] = "1"
        frontend_env["RUSTUP_TOOLCHAIN"] = "stable-x86_64-pc-windows-gnu"
        frontend_command = [npm, "run", "desktop:dev", "--", "--target", "x86_64-pc-windows-gnu"]
    frontend = subprocess.Popen(frontend_command, cwd=FRONTEND, env=frontend_env)
    processes = [backend, frontend]
    print("MNHUT Platform đang chạy. Nhấn Ctrl+C để dừng.")
    try:
        while all(process.poll() is None for process in processes):
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("Đang dừng các dịch vụ...")
    finally:
        dung_tien_trinh(processes)
    failed = next((process.returncode for process in processes if process.returncode not in (0, None)), 0)
    return int(failed or 0)


if __name__ == "__main__":
    raise SystemExit(main())
