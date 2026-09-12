# Bàn giao MNHUT Platform

## Đã làm

- Audit toàn bộ source và ghi kết quả trong `AUDIT_P0_2026-09-12.md`.
- Giữ nguyên app shell và phong cách UI hiện tại.
- Tạo lockfile, bổ sung typings React và pin dependency frontend thực tế.
- Sửa frontend typecheck/build, lỗi mạng tiếng Anh, trạng thái API và nút tạo sai ngữ cảnh.
- Sửa hợp đồng PATCH Kanban.
- Sửa FastAPI import lỗi do HTTP 204 và chuyển startup sang lifespan.
- Thêm migration runner, đóng kết nối SQLite đúng và thêm integration test.
- Cấu hình Tauri dev/build URL và lệnh frontend.
- Thêm `run_dev.py` làm entrypoint dev thống nhất.
- Thêm `build_desktop.py` làm quy trình một lệnh: đóng gói FastAPI bằng PyInstaller, build Tauri và tạo NSIS.
- Tauri tự khởi động sidecar, lưu SQLite trong thư mục dữ liệu ứng dụng và dừng sidecar khi cửa sổ chính thoát.
- Bổ sung icon Windows và cấu hình cache công cụ bundle cục bộ.
- Build release, tạo installer và smoke test cửa sổ/API/lifecycle thành công.
- Chuẩn bị schema/API Đại học ở trạng thái logic chưa nối UI; không đánh dấu hoàn thành.

## Đang dở

- P1 config logging error model, session token và native boundary.
- Module Đại học backend chưa nối vào frontend.

## Chưa làm

- Các workflow P3 chưa có bằng chứng trong bảng audit.

## File quan trọng

- `AUDIT_P0_2026-09-12.md`
- `run_dev.py`
- `build_desktop.py`
- `prototype_ui/src/App.tsx`
- `prototype_ui/src/styles.css`
- `prototype_ui/package.json`
- `prototype_ui/package-lock.json`
- `backend/main.py`
- `backend/sidecar.py`
- `backend/university.py`
- `migrations/001_tao_du_an.sql`
- `migrations/002_dai_hoc.sql`
- `src-tauri/tauri.conf.json`
- `src-tauri/src/lib.rs`

## Dependency mới

- Dev frontend: `@types/react` 19.3.0, `@types/react-dom` 19.3.0, `@tauri-apps/cli` 2.11.4.
- Dev backend: `httpx` 0.28.1, `pytest` 8.4.1, `pyinstaller` 6.16.0.
- Native: `tauri-plugin-shell` 2.x.

## Lỗi biết trước

- Python 3.14 cần tự build `pydantic-core` đã pin; dùng Python 3.11 đến 3.13 cho dev tái lập.
- GNU linker hiện cảnh báo `.rsrc merge failure: multiple non-default manifests`; release và smoke test vẫn đạt, cần xử lý khi chuyển về MSVC Build Tools.
- Terminal blocklist chưa đủ cho production; API file chưa giới hạn workspace; API loopback chưa có session token.

## Kiểm thử và đóng gói đã chạy

- Frontend typecheck: PASS.
- Frontend production build: PASS.
- Backend pytest: PASS, 4 bài test.
- Dev entrypoint check: PASS.
- Web UI và backend loopback tại 1366 x 768: PASS.
- Desktop build một bước: PASS.
- Tauri Windows release: PASS.
- NSIS installer: PASS.
- Desktop smoke và sidecar lifecycle: PASS.

## Bước tiếp theo

1. Bắt đầu P1 bằng session token, config logging error model và tách domain an toàn.
2. Thu hẹp capability và đồng bộ context multi-window.
3. Sau đó nối chức năng Đại học từ API vào UI, kèm workflow test.
