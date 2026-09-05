---
name: openapi-writer
description: Chặng 4 của quy trình học tập (Khâu 1) - Tự động trích xuất và soạn thảo bản đặc tả hợp đồng API chuẩn OpenAPI Specification v3.0.3 (openapi.yaml) từ mã nguồn đã qua audit ở Chặng 3.
---

# Kỹ Năng: OpenAPI Writer (Chặng 4 - Soạn Thảo Hợp Đồng API Specification)

## 1. Tên Kỹ Năng
**openapi-writer** (Đặc tả hợp đồng API chuẩn OpenAPI 3.0.3)

## 2. Khi Nào Kích Hoạt
- Kích hoạt trong **Chặng 4 (Nghiệm thu & Lấy minh chứng)** của Master Skill `soa-study-pipeline`.
- Kích hoạt sau khi mã nguồn đã hoàn thành phần code hạt nhân ở Chặng 2 và đã được tinh chỉnh qua bước Audit ở Chặng 3.
- Cần thiết lập bản hợp đồng chuẩn mực (Single Source of Truth) làm căn cứ sinh bộ test Postman và tài liệu hóa dịch vụ.

## 3. Input Mong Đợi
- **Mã nguồn dịch vụ đã audit**: Toàn bộ routes, controllers, middlewares và models trong `weeks/week-XX/code/`.
- **Thông tin metadata dịch vụ**: Tên service, phiên bản (v1.0.0), mô tả mục đích học tập của pattern.

## 4. Output Mong Đợi
File đặc tả hợp đồng chuẩn **OpenAPI Specification v3.0.3** tại đường dẫn:
`weeks/week-XX/code/openapi.yaml`

Đặc tả phải bao gồm:
- `info`: Tiêu đề bài học, mô tả giải thích cơ chế pattern, phiên bản.
- `servers`: URL cục bộ (`http://localhost:3000`).
- `paths`: Mọi endpoint thực tế trong mã nguồn đã qua audit (HTTP method, parameters, requestBody, responses chuẩn 200, 201, 202, 204, 400, 404, 409...).
- `components/schemas`: Các thực thể dữ liệu, kiểu dữ liệu, ràng buộc bắt buộc (`required`), và ví dụ minh họa (`example`) lấy từ kịch bản thực tế của sinh viên.

## 5. Quy Trình Thực Hiện
1. **Quét mã nguồn Chặng 3**:
   - Rà soát các route thực tế trong `weeks/week-XX/code/`.
   - Xác định chính xác các path parameters (ví dụ `{id}`), query parameters (ví dụ `pageSize`, `pageToken`, `filter`), và custom headers (ví dụ `Idempotency-Key`).
2. **Chuẩn hóa Schemas & Status Codes**:
   - Đối chiếu với Mongoose Schema và logic xử lý ngoại lệ để khai báo đầy đủ các trường hợp mã lỗi: `200`, `201`, `202`, `204`, `400`, `404`, `409`, `500`.
3. **Ghi file contract**:
   - Ghi file ra `weeks/week-XX/code/openapi.yaml`.
   - Chuẩn bị sẵn sàng làm đầu vào cho kỹ năng `postman-collection`.
