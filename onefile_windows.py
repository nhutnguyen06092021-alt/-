"""Entrypoint cho ONEFILE.exe độc lập trên Windows."""

from __future__ import annotations

import os
from pathlib import Path
import secrets
import sys
import threading


if len(sys.argv) >= 2 and sys.argv[1] == "--onefile-runner":
    sys.argv = [sys.argv[0], *sys.argv[2:]]
    from backend.onefile.runner import main as run_conversion

    raise SystemExit(run_conversion())


bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
os.environ["ONEFILE_STATIC_DIR"] = str(bundle_root / "onefile_static")

from run_onefile import PORT, choose_port, lan_ip, open_when_ready


def main() -> int:
    try:
        port = choose_port(PORT)
    except RuntimeError as exc:
        print(f"[ONEFILE] {exc}")
        input("Nhấn Enter để đóng...")
        return 1
    token = secrets.token_urlsafe(18)
    os.environ["ONEFILE_ACCESS_TOKEN"] = token
    local_url = f"http://127.0.0.1:{port}/onefile/?token={token}"
    address = lan_ip()
    print(f"\n[ONEFILE] Máy tính: {local_url}")
    if address:
        print(f"[ONEFILE] Điện thoại cùng Wi-Fi: http://{address}:{port}/onefile/?token={token}")
    print("[ONEFILE] Đóng cửa sổ này để dừng ứng dụng.\n")
    threading.Thread(target=open_when_ready, args=(local_url, token, port), daemon=True).start()

    from backend.onefile.web import app
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
