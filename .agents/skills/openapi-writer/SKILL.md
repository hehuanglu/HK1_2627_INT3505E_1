---
name: openapi-writer
description: Viết tài liệu đặc tả hợp đồng API chuẩn OpenAPI 3.0.3 (openapi.yaml) khớp hoàn toàn với mã nguồn và đặt trong weeks/week-XX/code/.
---

# Kỹ Năng: OpenAPI Writer (Soạn Thảo Hợp Đồng Dịch Vụ OpenAPI Specification)

## 1. Tên Kỹ Năng
**openapi-writer** (Soạn thảo hợp đồng API chuẩn OpenAPI)

## 2. Khi Nào Kích Hoạt
Kích hoạt kỹ năng này khi:
- Đã có mã nguồn demo trong `weeks/week-XX/code/` từ kỹ năng `api-code-scaffold` (hoặc đang tiến hành thiết kế theo quy trình API-First).
- Cần tạo file đặc tả chuẩn công nghiệp `openapi.yaml` để import vào Swagger UI, Postman, hoặc nộp bài tập lớn/bài tập tuần môn SOA.
- Cần minh họa nguyên lý *Service Contract* và *Contract-First Design* trong bài thuyết trình.

## 3. Input Mong Đợi
- **Mã nguồn dịch vụ**: Các file route, controller và model trong `weeks/week-XX/code/`.
- **Thông tin metadata dịch vụ**: Tên service, phiên bản (v1.0.0), mô tả mục đích học tập của tuần.

## 4. Output Mong Đợi
File đặc tả hợp đồng hợp lệ hoàn toàn theo chuẩn **OpenAPI Specification v3.0.3** tại đường dẫn:
`weeks/week-XX/code/openapi.yaml`

Đặc tả phải bao gồm đầy đủ:
- `info`: Tiêu đề, mô tả giải thích pattern, phiên bản.
- `servers`: URL cục bộ (`http://localhost:3000`).
- `paths`: Mọi endpoint đã cài đặt trong code (phương thức HTTP, parameters, requestBody, responses chuẩn 200, 201, 400, 404, v.v.).
- `components/schemas`: Các schema thực thể dữ liệu dùng lại được ($ref), kiểu dữ liệu (string, integer, boolean, object, array), thuộc tính bắt buộc (`required`), và ví dụ minh họa (`example`).

## 5. Các Bước Xử Lý
1. **Kiểm tra quy chuẩn**: Đọc [`.agents/context/tooling-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/tooling-notes.md) mục "Swagger / OpenAPI Specification" để đảm bảo tuân thủ cú pháp và cấu trúc mẫu.
2. **Quét toàn bộ endpoints trong code**:
   - Đọc các file trong `weeks/week-XX/code/` để liệt kê chính xác các đường dẫn (paths), phương thức HTTP (GET, POST, PUT, PATCH, DELETE).
   - Xác định rõ các tham số đường dẫn (path params, ví dụ `{id}`), tham số truy vấn (query params, ví dụ `pageSize`, `pageToken`, `filter`), và header đặc thù (ví dụ `Idempotency-Key`).
3. **Mô hình hóa Schema trong `components`**:
   - Trích xuất cấu trúc Schema từ Mongoose Model.
   - Thêm các ví dụ mẫu (examples) sinh động, gắn liền với kịch bản demo bài giảng.
4. **Chuẩn hóa mã trạng thái HTTP (Status Codes)**:
   - Sử dụng đúng mã: `200 OK` cho Get/List/Update, `201 Created` cho Create, `202 Accepted` cho LRO/Async, `204 No Content` cho Delete, `400 Bad Request` cho lỗi validate, `404 Not Found` khi không tìm thấy tài nguyên, `409 Conflict` cho lỗi trùng lặp/idempotency.
5. **Ghi file**: Ghi trực tiếp ra file `weeks/week-XX/code/openapi.yaml`.

## 6. Nguồn Dữ Liệu Cần Đọc
- [`.agents/context/tooling-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/tooling-notes.md)
- Mã nguồn trong `weeks/week-XX/code/`
- [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md)
