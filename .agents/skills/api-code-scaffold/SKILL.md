---
name: api-code-scaffold
description: Chặng 2 của quy trình học tập - Khởi tạo khung sườn kỹ thuật (Scaffold Boilerplate) và các khối TODO hạt nhân, thảo luận bối cảnh kiến trúc và phản biện cùng sinh viên để sinh viên tự tay cài đặt logic cốt lõi của tuần.
---

# Kỹ Năng: API Code Scaffold & Guided Implementation (Chặng 2 - Dựng Khung & Cài Đặt Hạt Nhân)

## 1. Tên Kỹ Năng
**api-code-scaffold** (Dựng khung dịch vụ & Hướng dẫn sinh viên cài đặt hạt nhân)

## 2. Khi Nào Kích Hoạt
- Đã hoàn thành Chặng 1 (`course-digest`) và sinh viên đã phê duyệt tri thức gốc cùng kịch bản nghiệp vụ.
- Chuẩn bị bước vào phần thực hành (hands-on) trong Master Skill `soa-study-pipeline`.

## 3. Input Mong Đợi
- **Kịch bản nghiệp vụ đã duyệt** từ Chặng 1 (ví dụ: E-commerce Order Processing, IoT Device Stream).
- **Pattern của tuần** (ví dụ: Idempotency Key, Cursor-based Pagination, Soft Delete, FieldMask).
- **Thư mục đích**: `weeks/week-XX/code/`.

## 4. Output Mong Đợi
1. **Bối cảnh kiến trúc & Phản biện (Context & Critical Thinking)**:
   - Mô tả đường đi của dữ liệu (Data Flow): Client -> Gateway/Route -> Middleware -> Service/DB -> Response.
   - 2-3 câu hỏi phản biện kiến trúc buộc sinh viên phải suy nghĩ sâu (Deep Thinking).
2. **Khung sườn kỹ thuật sạch sẽ (Scaffold Boilerplate) trong `weeks/week-XX/code/`**:
   - `package.json`: Danh sách dependencies tối giản (`express`, `mongoose`, `dotenv`...).
   - `server.js`: Khởi tạo Express, cấu hình middleware JSON, kết nối MongoDB (hoặc in-memory mock).
   - `models/`: Định nghĩa Schema Mongoose thể hiện cấu trúc thực thể dữ liệu.
   - `routes/` hoặc `controllers/`: Khai báo endpoints nhưng **để trống phần logic pattern cốt lõi**.
3. **Các khối TODO hạt nhân (Nucleus Implementation Blocks)**:
   - Tại file xử lý chính của Pattern, tạo các khối rõ ràng:
     ```javascript
     // ============================================================================
     // TODO [HỌC VIÊN CÀI ĐẶT HẠT NHÂN]: Cài đặt cơ chế Idempotency Key
     // - Mục tiêu: Kiểm tra xem header 'Idempotency-Key' đã tồn tại trong DB chưa.
     // - Nếu đã có và đang xử lý: trả về 409 Conflict hoặc 202 Accepted.
     // - Nếu đã có và hoàn thành: trả về kết quả lưu trong cache/DB kèm status gốc.
     // - Nếu chưa có: lưu key với trạng thái 'PROCESSING', tiếp tục thực thi request.
     // ============================================================================
     ```
   - Đi kèm gợi ý thuật toán, kiểu dữ liệu và HTTP status codes chuẩn mực.

## 5. Quy Trình Thực Hiện
1. **Làm rõ bối cảnh kiến trúc**:
   - LLM giải thích ngắn gọn vai trò của từng file trong thư mục `code/`.
   - Giúp sinh viên nắm rõ: Phần nào là "khung kỹ thuật nền tảng" (đã dựng sẵn) và phần nào là "hạt nhân kiến trúc tuần này" (sinh viên cần giải quyết).
2. **Đặt câu hỏi phản biện (Critical Thinking Gate)**:
   - LLM đưa ra các tình huống biên (edge cases) và cạm bẫy: *"Nếu hai request gửi tới cùng một miligiây thì điều gì xảy ra?", "Tại sao chúng ta không lưu con trỏ phân trang dưới dạng số trang (page number)?"*.
   - Sinh viên phản biện hoặc trả lời để đảm bảo thông suốt bản chất bài toán.
3. **Khởi tạo Scaffold**:
   - Tạo các file mã nguồn vào `weeks/week-XX/code/` với cấu trúc module rõ ràng.
   - Đảm bảo dự án có thể chạy được lệnh khởi động (`npm start` hoặc `node server.js`).
4. **Logic Gate 2 (Dừng lại để Sinh viên trực tiếp viết code)**:
   - LLM thông báo vị trí các file và các khối `TODO` cần hoàn thiện.
   - LLM **bắt buộc dừng lại**, nhường quyền chủ động cho sinh viên mở code editor và tự tay lập trình.
   - Sinh viên báo lại cho LLM sau khi hoàn thành phần code tự viết để chuyển sang Chặng 3 (Audit).
