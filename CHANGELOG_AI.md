# CHANGELOG AI

## 12/09/2026 — ONEFILE 0.2 hardening

- Thêm `ONEFILE.exe` tự chứa frontend, Python, FastAPI, thư viện chuyển đổi và FFmpeg;
  máy Windows x64 khác chỉ cần chép một file rồi nhấp đúp, không cần Python/Node/.env.
- Thêm entrypoint frozen tự gọi chính EXE làm runner chuyển đổi; kiểm thử thực tế
  26 capabilities, trang web, TXT → PDF và WAV → MP3 đều PASS.
- Thêm `build_onefile_exe.py`, icon Windows và khóa PyInstaller để tái tạo bản phát hành.
- Thêm `START_ONEFILE.cmd` để chạy trên máy Windows có app execution alias Microsoft
  Store nhưng không có lệnh `python`; ưu tiên `.venv` và Codex runtime sẵn có.
- Kiểm tra import thật của toàn bộ engine; tự sửa `.venv`/`click` hoặc cài sạch
  `node_modules` khi dependency tồn tại trên đĩa nhưng bị thiếu file.
- Tách runtime web sang `backend/.onefile-venv` để không xung đột với backend desktop
  hoặc tiến trình Python cũ đang khóa `.venv`.
- Sửa launcher tự phát hiện và tạo lại `.venv` bị khóa theo đường dẫn máy cũ.
- Chuyển runner server sang subprocess bất đồng bộ; hủy request dừng cả cây process,
  timeout vẫn cleanup, log/response có job ID và không log nội dung file.
- Bổ sung tách PDF theo nhiều nhóm range như `1-5;6-10;11,13-15`.
- Launcher tự chọn một cổng kế tiếp khi cổng mặc định đang bận; cổng cấu hình cố định
  vẫn được tôn trọng và báo lỗi rõ ràng.
- Xác minh browser + backend thật: 18/18 Playwright, 12/12 pytest và production build PASS.
- Đồng bộ README/PROJECT_STATE với các converter PDF, HEIC, tài liệu, bảng và media đã có.

## 12/09/2026 — ONEFILE CORE 0.1

- Thêm entry `/onefile/` trong Vite hiện có; giữ nguyên entry MNHUT/Tauri.
- Bổ sung detection, capability registry, worker queue, cancel/retry, validation,
  download/ZIP, metadata history và giao diện mobile-first/desktop.
- Triển khai chuyển đổi ảnh JPG/PNG/WebP, ảnh → PDF, PDF → ảnh, gộp/tách và
  chọn/đổi thứ tự/lặp/xóa/xoay trang PDF. Không giả lập converter server.
- Thêm PWA scope riêng, icon, offline shell, lazy PDF/ZIP và cơ chế cập nhật.
- Khắc phục lỗi worker nằm ngoài scope cache, nhãn form, nút ZIP lặp, tên dài
  mất đuôi định dạng; kiểm tra giới hạn kết quả PDF ngay trong vòng xử lý.
- Nâng Vite trong major 7 và dependency mới lên bản vá; npm audit 0 vulnerabilities.
- Thêm Playwright kiểm tra file tải về thật, malformed/empty/oversized input,
  Unicode/collision, hủy/retry, mobile và offline. Backend hiện có PASS 4/4.
- Các chức năng còn thiếu được ghi rõ trong PROJECT_STATE.md và ONEFILE_README.md.

## 12/09/2026 — P0 desktop Windows
- Cài và cấu hình Rust GNU để dùng MinGW hiện có; không đổi stack.
- Đóng gói FastAPI thành sidecar PyInstaller và tích hợp `tauri-plugin-shell` vào vòng đời ứng dụng.
- Lưu database production trong thư mục dữ liệu của app, thêm origin Tauri và chờ backend sẵn sàng lúc khởi động.
- Dừng sạch cả hai tiến trình PyInstaller khi đóng app bằng theo dõi PID cha.
- Bổ sung icon MNHUT và `useLocalToolsDir` để bundle NSIS ổn định trên source ở ổ D.
- Thêm `build_desktop.py`; lệnh một bước build sidecar, frontend, Tauri release và NSIS đã PASS.
- Smoke test desktop PASS: cửa sổ phản hồi, API `ok`, đóng app không còn sidecar/cổng lắng nghe.
- Tạo installer `MNHUT Platform_0.6.0_x64-setup.exe`; không đánh dấu các module UI-only là hoàn thành.

## 12/09/2026 — Phiên 0.6.0 P0
- Audit toàn bộ source theo tài liệu Word và yêu cầu tiếp quản, không viết lại UI/project.
- Tạo frontend lockfile, bổ sung typings React và Tauri CLI; sửa typecheck/build.
- Cấu hình Tauri `devUrl`, before dev/build command và lệnh CLI đúng.
- Sửa FastAPI HTTP 204, lifespan startup, migration runner và rò rỉ kết nối SQLite.
- Sửa hợp đồng cập nhật Kanban, lỗi mạng tiếng Anh và trạng thái kết nối sai trên dashboard.
- Thêm dev launcher, `.gitignore`, `.env.example`, requirements kiểm thử và API integration tests.
- Chuẩn bị migration/API Đại học ở trạng thái logic chưa tích hợp UI; không đánh dấu hoàn thành.
- Frontend build PASS, backend 4 tests PASS, UI web 1366 x 768 PASS; Tauri build NOT TESTED do thiếu Rust/Cargo.

## 12/09/2026 — Phiên 0.5.0
- Cập nhật theo Bộ Siêu Prompt hợp nhất.
- Loại rõ Git/GitHub UI, API Tester, Data Lab, Notes độc lập khỏi roadmap lõi.
- Mở rộng app shell và các module sản phẩm.
- Thêm FastAPI + SQLite cho dữ liệu nền thật.
- Thêm CRUD cơ bản cho Dự án, Nhiệm vụ, Lỗi, Quy trình, ADR, Ứng tuyển.
- Thêm lập chỉ mục metadata Tệp & Thư mục.
- Thêm endpoint trạng thái hệ thống.
- Không tạo `.bat` hoặc `.ps1`.
- Chưa tuyên bố build frontend/Tauri thành công vì môi trường hiện tại thiếu dependency/toolchain.
