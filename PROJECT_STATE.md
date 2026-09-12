# MNHUT Platform trạng thái dự án

## ONEFILE 0.2 — 12/09/2026

ONEFILE là entry web/PWA `/onefile/` trong frontend hiện có. MNHUT `/`, FastAPI,
SQLite và Tauri được giữ lại. Audit/cách chạy: [ONEFILE_README.md](ONEFILE_README.md).

### Completed

- File picker, drag/drop, input camera, magic bytes/MIME/extension, kiểm tra size,
  số trang PDF và giới hạn pixel ảnh trước decode. Unicode và tên dài được xử lý.
- Registry chỉ mở action hỗ trợ; batch hỗn hợp từng file; queue tuần tự trong
  worker, cancel/retry/remove/clear completed, timeout và lỗi độc lập.
- 10 action local thật: ảnh → JPG/PNG/WebP; ảnh → PDF; PDF → JPG/PNG/WebP;
  gộp, tách, sắp xếp/xóa/lặp/xoay trang PDF bằng danh sách số trang.
- Converter server thật: nén/trích ảnh PDF, HEIC → JPG/PNG/WebP, TXT/DOCX/HTML,
  CSV/XLSX, audio 6 định dạng và video MP4/MOV/WebM/MKV/AVI/GIF/MP3.
- Upload server kiểm tra magic bytes, giới hạn dung lượng, tên/path an toàn; mỗi lần xử
  lý dùng thư mục ngẫu nhiên và tự xóa khi thành công, lỗi, timeout hoặc client hủy.
- Capability endpoint chỉ bật action có dependency; tiến trình converter tách biệt,
  có timeout, mã job trong log/response và dừng cây tiến trình khi browser hủy.
- Resize/quality/rotate/flip và bỏ metadata ảnh; PDF A4/fit, lề, hướng giấy.
- Kiểm tra đầu ra; download, ZIP chống trùng tên, số liệu lấy từ Blob thật.
- Mobile-first, sidebar/workspace/job panel desktop, search, theme và metadata history.
- PWA manifest/icons/standalone configuration; scoped service worker, offline shell,
  image worker precache, PDF/ZIP lazy chunks và update action.
- Không sửa file gốc. Tác vụ local chỉ ở RAM; tác vụ server lưu tạm trong lúc xử lý.
- `ONEFILE.exe` tự chứa frontend, Python và toàn bộ converter; chạy trên Windows x64
  bằng một file, không cần Python, Node.js hay `.env`; runner đóng gói đã chuyển đổi
  TXT → PDF và WAV → MP3 thật thành công.

### In Progress

- Đang kiểm tra khả năng chạy trên thiết bị vật lý và thiết kế page manager có thumbnail.

### Not Implemented

- PDF thumbnail page manager kéo thả.
- BMP/TIFF/GIF/APNG động; PPTX; DOCX → PDF giữ nguyên bố cục bằng LibreOffice.
- API job lưu trạng thái độc lập (`GET/cancel/download`); hiện conversion server dùng
  một HTTP request có timeout/cancel/cleanup thật.
- Ngôn ngữ ngoài tiếng Việt; preset nén, auto ZIP setting; khôi phục file/job sau reload.

### Known Issues / Limits

- 32 MB/file; tối đa 40 job; input/output 128 MB; 200 trang PDF; 16 MP/ảnh;
  timeout 120 giây. JPEG có header quá 1 MB chưa hỗ trợ.
- PDF thao tác trang không cam kết giữ form/bookmark/chữ ký số. PDF mã hóa bị từ chối.
- Tải kết quả trước khi đóng/reload/update. Lịch sử không chứa file để khôi phục.
- Offline chỉ có shell/ảnh ngay sau cài SW; công cụ PDF/ZIP cần được dùng online lần đầu.
- Server mặc định 64 MB/file, output 192 MB và timeout 180 giây; media phụ thuộc FFmpeg.
- Chưa QA cài homescreen/camera/share trên Android/iOS thật, Firefox hoặc điện thoại RAM 4 GB.
- Chưa publish HTTPS và chưa rebuild installer Tauri trong milestone ONEFILE.

### Validation

- TypeScript strict + production build: PASS.
- Microsoft Edge: PASS 17/17 tests (real downloaded JPG/PNG/WebP/PDF/ZIP).
- Chrome: PASS 18/18 tests trên bản build cuối cùng, gồm UI gọi converter server thật.
- Mobile 360/390/412/430, tablet 768, desktop 1366: PASS kiểm tra không tràn ngang;
  ảnh chụp 390/1366 được xem trực tiếp.
- Offline shell + ảnh; PDF chỉnh sửa/tách sau lần dùng online: PASS trên Chrome/Edge.
- Backend regression: PASS 12/12; PDF/HEIC/tài liệu/bảng/audio/video, validation,
  cleanup, mã job, dừng process tree và launcher chuyển máy đều dùng output thật.
- Windows standalone EXE: PASS khởi động từ file tự chứa, 26 server operations,
  trang `/onefile/` HTTP 200, TXT → PDF và WAV → MP3 qua subprocess đóng gói.
- npm dependency audit sau nâng Vite 7.3.6 / Playwright 1.63.0 / fflate 0.8.3: 0 vulnerabilities.

### Next Step

Kiểm thử Android/iOS và Firefox trên thiết bị thật; sau đó làm PDF thumbnail manager
và API job bất đồng bộ trước khi mở thêm định dạng.

---

Phiên bản: 0.6.0
Giai đoạn hiện tại: P0 desktop đã đạt; đang chuyển sang chuẩn hóa P1

[ ] chưa làm
[>] đang làm
[U] chỉ có UI
[L] có logic nhưng chưa tích hợp đầy đủ
[T] đang kiểm thử
[x] hoàn thành thật

## P0

[x] Dependency frontend có lockfile và phiên bản thực tế
[x] TypeScript strict typecheck
[x] Frontend production build
[x] FastAPI import startup và migration trên database mới
[x] API integration test cho health project Kanban HTTP 204 và validation
[x] Entrypoint dev thống nhất có kiểm tra dependency
[x] UI web mở ở 1366 x 768 và kết nối backend thật
[x] Tauri Windows release build bằng Rust GNU và MinGW
[x] FastAPI sidecar được đóng gói và quản lý theo vòng đời ứng dụng
[x] Installer Windows NSIS

## Core

[x] React TypeScript Vite app shell
[x] Điều hướng Ctrl K dark light responsive
[x] FastAPI local API prefix `/api/v1`
[x] SQLite migration tuần tự và đóng kết nối đúng
[L] Tauri 2 native commands và multi-window; cửa sổ động đã có nhưng chưa đủ module chuyên dụng
[>] P1 config logging error model native boundary sidecar

## Module

[L] Tổng quan
[L] Đại học backend schema API đã có phần nền nhưng frontend chưa nối
[L] Dự án Code và Nhóm
[L] Tệp và Thư mục
[L] Trung tâm Lỗi
[U] Trung tâm Chất lượng
[L] Trung tâm Phát triển
[L] Hệ thống
[L] Tự động hóa lưu cấu hình chưa có engine chạy
[U] Database và SQL
[U] Phân tích
[L] Nghề nghiệp
[U] Kiến trúc và Độ tin cậy
[U] Thông báo
[U] Cài đặt

## Kiểm thử đã chạy ngày 12 09 2026

- Frontend typecheck: PASS.
- Frontend production build: PASS.
- Backend pytest: PASS, 4 bài test.
- Python compile: PASS.
- Dev entrypoint check: PASS.
- Web UI 1366 x 768 với backend: PASS.
- Tauri CLI argument check: PASS.
- Lệnh build desktop một bước `backend\.venv\Scripts\python.exe build_desktop.py`: PASS.
- Tauri Windows release và NSIS installer: PASS.
- Smoke desktop: cửa sổ phản hồi, API sidecar `ok`: PASS.
- Lifecycle: đóng app, sidecar về 0 và cổng 8000 đóng: PASS.

## Việc tiếp theo

1. P1 thêm session token cho API loopback, logging và error model dùng chung.
2. Thu hẹp capability/cửa sổ động và tách domain còn lại khỏi `backend/main.py`.
3. Nối module Đại học vào UI theo phase chức năng sau khi P1 đủ ổn định.
