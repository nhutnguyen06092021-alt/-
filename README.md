# MNHUT Platform

## ONEFILE TOOL — web/PWA

ONEFILE dùng chung React/TypeScript/Vite của dự án, mở tại `/onefile/`.
Ứng dụng MNHUT và Tauri hiện có tiếp tục dùng `/`.

### Dùng trên máy Windows khác — không cần cài gì

Chép duy nhất `release\ONEFILE.exe` sang máy Windows 10/11 x64 rồi nhấp đúp,
hoặc chạy một lệnh:

```powershell
.\ONEFILE.exe
```

File EXE đã chứa web, Python, FastAPI, PDF/HEIC, tài liệu và FFmpeg. Ứng dụng tự
chọn cổng trống và mở trình duyệt; không cần Python, Node.js, `.env` hoặc Internet.
Giữ cửa sổ ONEFILE mở trong lúc sử dụng. Máy khác cùng Wi-Fi dùng được liên kết
có token in trong cửa sổ nếu Windows Firewall cho phép trên mạng riêng.

### Chạy từ mã nguồn

Trên Windows, nhấp đúp `START_ONEFILE.cmd`. File này tự tìm Python trong `.onefile-venv`,
Codex runtime hoặc Python hệ thống; không cần gọi lệnh `python` đang trỏ Microsoft Store.

Chạy ONEFILE đầy đủ bằng một lệnh từ thư mục này:

```powershell
.\START_ONEFILE.cmd
```

Script tự tạo hoặc sửa môi trường Python khi source được chuyển sang máy khác, cài
dependency, build web và mở URL có token. Công cụ local vẫn có thể chạy riêng:

```powershell
cd prototype_ui
npm ci
npm run dev
```

Mở `http://localhost:5173/onefile/`. ONEFILE xử lý ảnh/PDF ngay trong browser,
không cần khởi động backend. Xem [ONEFILE_README.md](ONEFILE_README.md) để chạy
bản PWA, kiểm thử và xem giới hạn chức năng.

Một ứng dụng desktop Windows thống nhất cho Đại học 4 năm, đồ án, thực tập và công việc IT. React/TypeScript là lớp giao diện nhúng trong cửa sổ Tauri; FastAPI được đóng gói thành sidecar và tự chạy cùng app, không yêu cầu mở trình duyệt.

## Chạy app ngay bằng một lệnh

Từ thư mục `mnhut_build`:

```powershell
& '.\src-tauri\target\x86_64-pc-windows-gnu\release\mnhut_platform.exe'
```

Bộ cài Windows đã tạo tại:

```text
src-tauri\target\x86_64-pc-windows-gnu\release\bundle\nsis\MNHUT Platform_0.6.0_x64-setup.exe
```

## Chạy nhanh môi trường phát triển

Yêu cầu: Python 3.11 đến 3.14 và Node.js 20.19+ hoặc 22.12+.

```powershell
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
cd ..\prototype_ui
npm ci
cd ..
python run_dev.py --desktop
```

Lệnh trên mở cửa sổ Tauri; Vite chỉ phục vụ nội bộ cho chế độ phát triển. Backend chỉ bind `127.0.0.1:8000`.

Kiểm tra entrypoint mà không khởi động dịch vụ:

```text
python run_dev.py --kiem-tra
```

## Build app Windows bằng một lệnh

Sau khi dependency đã cài:

```powershell
backend\.venv\Scripts\python.exe build_desktop.py
```

Script đóng gói sidecar, build frontend, biên dịch Tauri và tạo NSIS. Máy hiện tại dùng Rust target `x86_64-pc-windows-gnu` với MinGW tại `D:\Compiler\mingw64\bin`.

Đóng gói ONEFILE standalone và source ZIP sạch:

```powershell
backend\.onefile-venv\Scripts\python.exe build_onefile_exe.py
backend\.onefile-venv\Scripts\python.exe package_onefile_release.py
```

## Kiểm thử riêng

```text
backend\.venv\Scripts\python.exe -m pytest tests -q
cd prototype_ui
npm run typecheck
npm run build
```

Desktop release, NSIS installer và lifecycle sidecar đã được build/smoke test thực tế ngày 12/09/2026.

## Cấu trúc

- `prototype_ui/`: React, TypeScript, Vite và UI sản phẩm hiện tại.
- `backend/`: FastAPI local core.
- `migrations/`: migration SQLite tuần tự.
- `src-tauri/`: Tauri 2 và native boundary.
- `tests/`: smoke và integration tests.
- `AUDIT_P0_2026-09-12.md`: đối chiếu chức năng, lỗi và kế hoạch P0 đến P3.

Không đưa `.env`, database người dùng, `node_modules`, `.venv`, cache hoặc secret vào source ZIP.
