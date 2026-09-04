---
name: api-code-scaffold
description: Sinh mã nguồn minh họa dịch vụ API (Node.js + Express + Mongoose) làm nổi bật pattern của tuần học và lưu vào weeks/week-XX/code/.
---

# Kỹ Năng: API Code Scaffold (Khởi Tạo Mã Nguồn Dịch Vụ Minh Họa)

## 1. Tên Kỹ Năng
**api-code-scaffold** (Khởi tạo mã nguồn demo dịch vụ API)

## 2. Khi Nào Kích Hoạt
Kích hoạt kỹ năng này khi:
- Đã hoàn thành dàn ý slide hoặc đã có chủ đề tuần học cụ thể.
- Sinh viên cần một dự án backend mini chạy được ngay để demo trực tiếp trên lớp.
- Cần mã nguồn mẫu chứng minh tính đúng đắn của pattern thiết kế (ví dụ: chạy thử endpoint để thấy rõ Idempotency key hoạt động thế nào, hoặc Field Mask lọc dữ liệu ra sao).

## 3. Input Mong Đợi
- **Chủ đề tuần học & Pattern cần mô phỏng**: (ví dụ: Custom Methods, Cursor-based Pagination, Soft Deletion, v.v.).
- **Dàn ý slide**: File `weeks/week-XX/slide.md` để đảm bảo tên endpoint, model dữ liệu trong code khớp 100% với ví dụ trên slide.
- **Thư mục tuần**: `weeks/week-XX/`.

## 4. Output Mong Đợi
Một dự án Node.js tối giản, chạy được độc lập đặt trong `weeks/week-XX/code/`, bao gồm:
- `package.json`: Danh sách dependencies tối giản (`express`, `mongoose`, `dotenv`, v.v.).
- `server.js` (hoặc `app.js`): Khởi tạo Express server, kết nối MongoDB, cấu hình middleware JSON.
- `models/`: Định nghĩa Schema Mongoose thể hiện đúng cấu trúc tài nguyên.
- `routes/` hoặc `controllers/`: Cài đặt logic nghiệp vụ của pattern với chú thích (comments) giải thích rõ từng bước xử lý.
- `README.md`: Hướng dẫn sinh viên cách cài đặt dependencies (`npm install`), cấu hình cơ sở dữ liệu và lệnh chạy demo (`npm start` hoặc `node server.js`).

## 5. Các Bước Xử Lý
1. **Đọc tài liệu quy chuẩn**: Đọc [`.agents/context/tooling-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/tooling-notes.md) để nắm rõ convention của môn học đối với Node.js và Mongoose.
2. **Đối chiếu với Pattern tương ứng**: Đọc [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md) để đảm bảo logic code phản ánh chính xác quy tắc của pattern:
   - Nếu là *Custom Method*: dùng cú pháp route `POST /resources/:id/action` hoặc `POST /resources/:id:action`.
   - Nếu là *Pagination Token*: sử dụng con trỏ base64 hoặc timestamp/id index thay vì `skip/limit` thuần túy.
   - Nếu là *Soft Delete*: dùng middleware Mongoose `pre('find')` để tự động lọc `isDeleted: false` và viết endpoint `:undelete`.
   - Nếu là *Idempotency*: dùng middleware bắt `Idempotency-Key` header và lưu kết quả vào cache/collection tạm.
3. **Giữ cho code tối giản & tập trung (KISS Principle)**:
   - **KHÔNG** thêm các thành phần phức tạp không cần thiết cho buổi thuyết trình (bỏ qua JWT auth phức tạp, microservices orchestration, winston logging đa tầng, Docker cluster...).
   - Viết code mạch lạc, tường minh, có chú thích bằng tiếng Việt ngay tại các dòng code thực thi pattern cốt lõi để sinh viên dễ chỉ trỏ khi trình bày trên máy chiếu.
4. **Tạo file vào thư mục đích**: Sử dụng công cụ ghi file vào `weeks/week-XX/code/`.

## 6. Nguồn Dữ Liệu Cần Đọc
- [`.agents/context/tooling-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/tooling-notes.md)
- [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md)
- `weeks/week-XX/slide.md` (nếu đã có)
