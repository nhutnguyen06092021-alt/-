from __future__ import annotations

import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class StudyFlowHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


def find_server() -> ThreadingHTTPServer:
    for port in range(5500, 5511):
        try:
            return ThreadingHTTPServer(("127.0.0.1", port), StudyFlowHandler)
        except OSError:
            continue
    raise RuntimeError("Các cổng 5500–5510 đều đang được sử dụng.")


def check_project() -> int:
    required = ("index.html", "styles.css", "app.js")
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        print("Thiếu file:", ", ".join(missing))
        return 1
    print("StudyFlow sẵn sàng chạy.")
    return 0


def main() -> int:
    if "--check" in sys.argv:
        return check_project()

    server = find_server()
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"StudyFlow đang chạy tại {url}")
    print("Nhấn Ctrl+C để dừng.")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng StudyFlow.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
