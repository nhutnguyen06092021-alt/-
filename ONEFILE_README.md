# ONEFILE 0.2

## Audit và quyết định tích hợp

Source có React 19 + TypeScript + Vite, FastAPI/SQLite và Tauri 2 cho MNHUT.
Chưa có converter, registry, hàng đợi hoặc PWA. ONEFILE được thêm thành entry
`prototype_ui/onefile/index.html`, mở tại `/onefile/`, giữ nguyên MNHUT tại `/`.
Không tạo frontend mới, không đổi framework, không dùng Tauri cho ONEFILE.

## Chạy ngay trên Windows bằng một file

`release\ONEFILE.exe` là bản Windows 10/11 x64 tự chứa. Chép file này sang máy khác
rồi nhấp đúp, hoặc mở PowerShell tại thư mục chứa file và chạy:

```powershell
.\ONEFILE.exe
```

Không cần cài Python, Node.js, thư viện hay tạo `.env`; không cần mạng để khởi động
và xử lý file. EXE tự chọn cổng trống, tạo token mới và mở trình duyệt. Giữ cửa sổ
ONEFILE mở trong lúc sử dụng; đóng cửa sổ để dừng server cục bộ. Nếu Windows Firewall
hỏi, chỉ cho phép mạng riêng khi muốn dùng liên kết trên điện thoại cùng Wi-Fi.

## Chạy từ mã nguồn

- Node.js 20.19+ hoặc 22.12+; Python 3.11–3.14; Chrome/Edge mới.
- Công cụ local không cần backend. HEIC, nén/trích ảnh PDF, tài liệu và media dùng
  FastAPI; FFmpeg được cung cấp qua `imageio-ffmpeg`.

Chạy bản đầy đủ từ `mnhut_build`:

```powershell
.\START_ONEFILE.cmd
```

Nếu Windows báo `Python was not found`, nhấp đúp `START_ONEFILE.cmd`, hoặc chạy:

```powershell
.\backend\.onefile-venv\Scripts\python.exe run_onefile.py
```

Launcher kiểm tra import thật thay vì chỉ kiểm tra file/marker. ONEFILE dùng môi trường
riêng `backend/.onefile-venv`; nếu thiếu file hay metadata, launcher tạo lại bản sạch. Nếu `node_modules` bị lỗi,
launcher chạy `npm ci` và build lại. Người dùng vẫn chỉ chạy một lệnh.

Lần đầu script tạo/sửa `.onefile-venv`, cài dependency, build frontend rồi mở trình duyệt.
Máy khác trong cùng Wi-Fi có thể dùng URL chứa token được in ra. Qua địa chỉ IP HTTP,
web vẫn hoạt động nhưng cài PWA/offline cần HTTPS.
Nếu cổng 8787 đang bận, script tự tìm một trong 20 cổng kế tiếp; khi đặt
`ONEFILE_PORT`, script giữ đúng cấu hình và báo rõ nếu cổng đó không dùng được.

Từ `mnhut_build/prototype_ui`:

```powershell
npm ci
npm run dev
```

Mở `http://localhost:5173/onefile/`. Development không đăng ký service worker.

Kiểm tra bản production/PWA:

```powershell
npm run build
npm run preview
```

Mở `http://localhost:4173/onefile/`. PWA dùng HTTPS hoặc localhost; HTTP qua IP LAN
không đáp ứng secure context. Khi đưa lên hosting HTTPS, phục vụ toàn bộ `dist/`
và giữ đường dẫn `/onefile/` cùng `/assets/`. Không rewrite `/onefile/sw.js` thành HTML.
Chưa triển khai hosting trong milestone này.

## Công cụ có xử lý thật

| Công cụ | Engine | Đầu ra |
| --- | --- | --- |
| JPG/PNG/WebP → JPG/PNG/WebP | OffscreenCanvas trong worker | Ảnh đã decode lại để kiểm tra |
| Resize, xoay, lật ngang, giảm chất lượng ảnh | OffscreenCanvas | Ảnh mới, bỏ metadata |
| Một/nhiều ảnh → PDF | pdf-lib trong worker | A4 dọc/ngang hoặc fit, lề tùy chọn |
| Gộp PDF | pdf-lib trong worker | PDF theo thứ tự file đã chọn |
| Tách PDF | pdf-lib trong worker | Từng trang hoặc nhiều nhóm range |
| Sắp xếp/xóa/lặp/xoay trang PDF | pdf-lib trong worker | PDF mới theo danh sách trang |
| PDF → JPG/PNG/WebP | PDF.js worker + canvas từng trang | Ảnh cả trang, không phải ảnh nhúng |
| ZIP nhiều kết quả | fflate async worker | ZIP thật, tên chống trùng |
| Nén/trích ảnh nhúng PDF | PyMuPDF, process riêng | PDF hoặc ảnh/ZIP đã kiểm tra |
| HEIC → JPG/PNG/WebP | Pillow + pillow-heif | Ảnh decode lại |
| TXT/DOCX/HTML, CSV/XLSX | python-docx, ReportLab, openpyxl | TXT/PDF/DOCX/XLSX/CSV thật |
| Audio/video | FFmpeg process riêng | 6 audio, 5 video, GIF hoặc MP3 |

Ảnh: thay định dạng riêng cho từng file; tùy chọn trong một lượt dùng chung.
PNG không dùng quality lossy. Nền trong suốt chuyển sang JPG/ảnh trong PDF thành
trắng. HEIC dùng converter server; GIF động, BMP và TIFF chưa có converter.

PDF: để trống trường trang để chọn tất cả; `1,3,7-10` chọn trang; `3,1,1` đổi thứ tự
và lặp trang trong công cụ sắp xếp. Bỏ số trang để loại trang khỏi bản mới. Tách PDF
xuất từng trang hoặc nhận nhiều nhóm như `1-5;6-10;11,13-15`.
File gốc không bị sửa. PDF mới từ copy trang không cam kết giữ biểu mẫu, bookmark,
chữ ký số hoặc metadata tài liệu. PDF mã hóa bị từ chối rõ ràng.

## Core và riêng tư

- File picker, camera capture, drag/drop; nhận diện magic bytes trước extension/MIME.
- Đọc số trang PDF trong worker; kiểm tra kích thước ảnh trước khi decode.
- Hàng đợi concurrency 1; lỗi một job không dừng job khác; hủy thật bằng
  `Worker.terminate()` / PDF.js cancel/destroy; retry, remove, clear completed.
- Progress dựa trên số ảnh/trang đã xử lý; spinner khi không có tiến độ đo được.
- Kết quả kiểm tra lại; kích thước và tỷ lệ tăng/giảm lấy từ Blob thật.
- Chỉ metadata không chứa tên/nội dung file được lưu localStorage, tối đa 50 dòng.
- Reload/đóng tab làm mất file và kết quả trong RAM. Lịch sử tác vụ đang chạy được
  hiển thị là bị gián đoạn; cần chọn lại file. Không giả khôi phục job.
- Object URL chỉ tạo khi tải xuống, thu hồi sau 30 giây hoặc pagehide.
- Chia sẻ chỉ hiện khi Web Share API xác nhận hỗ trợ file.
- Service worker chỉ scope `/onefile/`, precache shell và image worker nhỏ; các
  thư viện PDF/ZIP tải khi cần và cache khi dùng. Cập nhật qua nút ở Cài đặt,
  chặn cập nhật khi còn job đang chạy. Tải kết quả trước khi cập nhật.

## Giới hạn tập trung

`prototype_ui/src/onefile/config.ts`:

- 32 MB/file; 40 file mỗi lượt và tối đa 40 job được giữ trong hàng đợi.
- Tổng đầu vào hàng đợi 128 MB; tổng kết quả giữ trong RAM 128 MB.
- 200 trang/PDF; 16 triệu điểm ảnh và 8192 px/chiều trước khi decode.
- Timeout 120 giây/job. JPEG có header quá 1 MB chưa hỗ trợ.
- PDF render từng trang, không tạo hàng trăm thumbnail hoặc decode ảnh đồng thời.

Các giới hạn hạn chế áp lực RAM, không bảo đảm mọi file hợp lệ đều xử lý được trên
mọi điện thoại. Giải mã ảnh lớn và PDF có cấu trúc phức tạp cần thử thiết bị thật.

## Kiểm thử

```powershell
npm run typecheck
npm run build
npm run test:onefile
```

Test chạy Chrome đã cài, preview production port 4178, tạo fixture tại runtime,
tải rồi đọc lại ảnh/PDF/ZIP thật. Không upload file lên API. Đổi sang Edge:

```powershell
$env:ONEFILE_BROWSER = 'msedge'
npm run test:onefile
```

Backend và converter: từ `mnhut_build`, chạy
`backend\.onefile-venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider`.

Tạo lại EXE sau khi đã chạy launcher mã nguồn một lần:

```powershell
.\backend\.onefile-venv\Scripts\python.exe build_onefile_exe.py
```

## NOT IMPLEMENTED

Quản lý trang bằng thumbnail/drag; BMP/TIFF/GIF/APNG động;
PPTX và DOCX → PDF giữ nguyên bố cục; server job API lưu trạng thái độc lập;
language ngoài tiếng Việt; auto ZIP preference; lưu file/kết quả để resume sau reload.
Không có mock API hoặc lựa chọn converter chưa hỗ trợ trong registry.

Chưa kiểm thử cài homescreen/camera/share trên Android/iOS thật, Firefox và máy
RAM 4 GB. Responsive browser emulation không thay thế các kiểm tra đó.

## Điểm mở rộng

- `src/onefile/detect.ts`, `registry.ts`, `types.ts`: nhận diện và capabilities.
- `converters/`, `worker.ts`, `engine.ts`: processing và validation output.
- `jobs.ts`, `download.ts`: lifecycle, giới hạn, metadata, ZIP/download.
- `components.tsx`, `App.tsx`, `styles.css`: UI responsive.
- `onefile-pwa.ts`, `public/onefile/`: cache, manifest, icon.
- `backend/onefile/`: capability, validator, runner process, converter và cleanup server.

Tài liệu engine: [pdf-lib](https://pdf-lib.js.org/docs/api/classes/pdfdocument),
[PDF.js](https://mozilla.github.io/pdf.js/examples/),
[Service Worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers).
