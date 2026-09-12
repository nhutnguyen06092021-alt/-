from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import socket
import secrets
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "prototype_ui"
VENV = ROOT / "backend" / ".onefile-venv"
PYTHON = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
REQUIREMENTS = ROOT / "backend" / "requirements.txt"
PORT = int(os.environ.get("ONEFILE_PORT", "8787"))


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def python_environment_works() -> bool:
    if not PYTHON.is_file():
        return False
    try:
        checked = subprocess.run(
            [str(PYTHON), "-c", "import sys; raise SystemExit(0 if sys.prefix != sys.base_prefix else 1)"],
            capture_output=True,
            timeout=10,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return checked.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def python_dependencies_work() -> bool:
    if not PYTHON.is_file():
        return False
    check = (
        "import click, fastapi, uvicorn, fitz, PIL, pillow_heif, docx, openpyxl, "
        "reportlab, imageio_ffmpeg, multipart; assert hasattr(click, 'Choice')"
    )
    try:
        checked = subprocess.run(
            [str(PYTHON), "-c", check],
            capture_output=True,
            timeout=30,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return checked.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def rebuild_python_environment() -> None:
    base_python = Path(getattr(sys, "_base_executable", sys.executable))
    if not base_python.is_file():
        base_python = Path(sys.executable)
    print("[ONEFILE] Môi trường Python bị thiếu file; đang tạo lại bản sạch...")
    run([str(base_python), "-m", "venv", "--clear", str(VENV)])


def prepare_python() -> None:
    rebuilt = False
    if not python_environment_works():
        if sys.version_info < (3, 11) or sys.version_info >= (3, 15):
            raise RuntimeError("Cần Python 3.11 đến 3.14.")
        rebuild_python_environment()
        rebuilt = True
    digest = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
    marker = VENV / ".onefile-requirements"
    requirements_changed = not marker.is_file() or marker.read_text(encoding="ascii", errors="ignore") != digest
    dependencies_healthy = python_dependencies_work()
    if not dependencies_healthy and not rebuilt:
        rebuild_python_environment()
        marker = VENV / ".onefile-requirements"
        requirements_changed = True
    if requirements_changed or not dependencies_healthy:
        print("[ONEFILE] Đang cài hoặc sửa engine PDF, HEIC, tài liệu và media...")
        command = [str(PYTHON), "-m", "pip", "install", "--disable-pip-version-check"]
        run(command + ["-r", str(REQUIREMENTS)])
        if not python_dependencies_work():
            raise RuntimeError("Dependency Python vẫn lỗi sau khi tự sửa. Hãy kiểm tra kết nối mạng hoặc phần mềm antivirus.")
        marker.write_text(digest, encoding="ascii")


def prepare_frontend() -> None:
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    if not npm:
        raise RuntimeError("Không tìm thấy Node.js/npm. Cần Node.js 20 trở lên.")
    installed = (FRONTEND / "node_modules").is_dir()
    if not installed:
        print("[ONEFILE] Đang cài frontend lần đầu...")
        run([npm, "ci"], FRONTEND)
    print("[ONEFILE] Đang build frontend...")
    try:
        run([npm, "run", "build"], FRONTEND)
    except subprocess.CalledProcessError:
        if not installed:
            raise
        print("[ONEFILE] Frontend dependency có lỗi; đang tự cài sạch và build lại...")
        run([npm, "ci"], FRONTEND)
        run([npm, "run", "build"], FRONTEND)


def lan_ip() -> str | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
            connection.connect(("8.8.8.8", 80))
            return connection.getsockname()[0]
    except OSError:
        return None


def port_available(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False


def choose_port(preferred: int) -> int:
    if port_available(preferred):
        return preferred
    if "ONEFILE_PORT" in os.environ:
        raise RuntimeError(f"Cổng ONEFILE_PORT={preferred} đang được sử dụng.")
    for candidate in range(preferred + 1, preferred + 21):
        if port_available(candidate):
            print(f"[ONEFILE] Cổng {preferred} đang bận; chuyển sang {candidate}.")
            return candidate
    raise RuntimeError(f"Không tìm thấy cổng trống trong khoảng {preferred}–{preferred + 20}.")


def open_when_ready(url: str, token: str, port: int) -> None:
    for _ in range(60):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/v1/onefile/capabilities?token={token}", timeout=1) as response:
                if response.status == 200:
                    if os.environ.get("ONEFILE_NO_BROWSER") != "1":
                        webbrowser.open(url)
                    return
        except OSError:
            time.sleep(.25)


def main() -> int:
    try:
        port = choose_port(PORT)
        prepare_python()
        prepare_frontend()
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"[ONEFILE] Không thể khởi động: {exc}", file=sys.stderr)
        return 1
    token = secrets.token_urlsafe(18)
    local_url = f"http://127.0.0.1:{port}/onefile/?token={token}"
    address = lan_ip()
    print(f"\n[ONEFILE] Máy tính: {local_url}", flush=True)
    if address:
        print(f"[ONEFILE] Điện thoại cùng Wi-Fi: http://{address}:{port}/onefile/?token={token}", flush=True)
        print("[ONEFILE] Nếu điện thoại không mở được, cho phép Python qua Windows Firewall cho mạng riêng.", flush=True)
    print("[ONEFILE] Nhấn Ctrl+C để dừng.\n", flush=True)
    environment = os.environ.copy()
    environment["ONEFILE_STATIC_DIR"] = str(FRONTEND / "dist")
    environment["ONEFILE_ACCESS_TOKEN"] = token
    threading.Thread(target=open_when_ready, args=(local_url, token, port), daemon=True).start()
    try:
        return subprocess.call([str(PYTHON), "-m", "uvicorn", "backend.onefile.web:app", "--host", "0.0.0.0", "--port", str(port)], cwd=ROOT, env=environment)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
