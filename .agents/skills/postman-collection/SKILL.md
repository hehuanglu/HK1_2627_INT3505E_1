---
name: postman-collection
description: Chặng 4 của quy trình học tập (Khâu 2) - Khởi tạo bộ test Postman v2.1.0, chạy kiểm thử tự động với Newman CLI, và chụp Snapshot minh chứng thực nghiệm (logs, response, assertions) làm học liệu và ví dụ cho slide.
---

# Kỹ Năng: Postman Collection & Verification Snapshots (Chặng 4 - Nghiệm Thu & Lấy Minh Chứng)

## 1. Tên Kỹ Năng
**postman-collection** (Kiểm thử tự động Postman / Newman & Thu thập Snapshot minh chứng)

## 2. Khi Nào Kích Hoạt
- Kích hoạt trong **Chặng 4 (Nghiệm thu & Lấy minh chứng)** sau khi đã có file `openapi.yaml`.
- Cần chạy kiểm thử tự động toàn bộ luồng nghiệp vụ để chứng minh mã nguồn hoạt động chính xác.
- Cần thu thập các minh chứng thực nghiệm (snapshots của Request, Response, Terminal Log) để đưa trực tiếp vào slide bài giảng ở Chặng 5.

## 3. Input Mong Đợi
- **File đặc tả OpenAPI**: `weeks/week-XX/code/openapi.yaml`.
- **Mã nguồn dịch vụ**: `weeks/week-XX/code/` (đang sẵn sàng khởi chạy).
- **Kịch bản kiểm thử**: Bao gồm cả Happy Path (thành công) và Edge Cases (thử thách tính chịu lỗi của pattern).

## 4. Output Mong Đợi
1. `weeks/week-XX/code/postman_collection.json`: File collection chuẩn Postman v2.1.0 kèm các script assertions `pm.test`.
2. **Minh chứng thực nghiệm (Snapshots)**:
   - Các trích đoạn log xử lý của server khi có request đến.
   - Các cặp Request Header / Response Body JSON đại diện minh họa cho hoạt động của pattern.
   - Báo cáo kết quả chạy Newman CLI (xanh lá - PASS).

## 5. Quy Trình Thực Hiện
1. **Xây dựng Collection từ `openapi.yaml`**:
   - Khởi tạo `info` với schema Postman v2.1.0.
   - Sắp xếp các requests theo thứ tự tuần tự:
     - `01. Setup/Create Resource`
     - `02. Test Pattern Primary Logic (Happy Path)`
     - `03. Test Edge Cases & Fault Tolerance (Repeated Key / Invalid Cursor / FieldMask Error)`
     - `04. Verify Final State`
   - Viết các test script tự động (`pm.test` kiểm tra status code, cấu trúc response JSON, headers).
2. **Khởi chạy nghiệm thu (Run Verification)**:
   - Chạy dịch vụ Node.js trong nền hoặc qua kịch bản kiểm thử.
   - Chạy Newman CLI:
     ```bash
     npx newman run weeks/week-XX/code/postman_collection.json
     ```
3. **Chụp Snapshot minh chứng**:
   - Trích xuất các dữ liệu quan trọng nhất:
     - Dạng Request/Response chứng minh pattern hoạt động (ví dụ: lần gọi 1 trả 201 Created kèm dữ liệu, lần gọi 2 cùng `Idempotency-Key` trả 200/409 kèm header nhận diện cache).
     - Bảng tổng kết kết quả kiểm thử Newman.
   - Chuẩn bị sẵn dữ liệu này để chuyển tiếp cho Chặng 5 (`weekly-slide-outline`).
4. **Logic Gate 4 (Dừng lại để Sinh viên nghiệm thu)**:
   - Trình bày kết quả chạy test và các snapshots tiêu biểu cho sinh viên.
   - Sinh viên kiểm tra và xác nhận: *"Hệ thống chạy ổn định, minh chứng thực nghiệm đầy đủ tin cậy"* trước khi sang Chặng 5.
