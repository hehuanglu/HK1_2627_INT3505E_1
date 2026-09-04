---
name: postman-collection
description: Chuyển đổi đặc tả openapi.yaml thành Postman Collection JSON kèm test script tự động để sinh viên demo trực tiếp trên lớp hoặc chạy qua Newman CLI.
---

# Kỹ Năng: Postman Collection (Khởi Tạo Bộ Test Sưu Tập Postman / Newman)

## 1. Tên Kỹ Năng
**postman-collection** (Khởi tạo Postman Collection cho Demo & Kiểm Thử)

## 2. Khi Nào Kích Hoạt
Kích hoạt kỹ năng này khi:
- Đã có file đặc tả `weeks/week-XX/code/openapi.yaml` (hoặc mã nguồn đã hoàn thiện).
- Sinh viên chuẩn bị thuyết trình trên lớp và cần các request mẫu sẵn sàng bấm "Send" trên Postman mà không phải tự gõ thủ công từng header, body.
- Cần chạy kiểm thử tự động toàn bộ luồng bài giảng qua công cụ Newman CLI để chứng minh API hoạt động thông suốt.

## 3. Input Mong Đợi
- **File đặc tả OpenAPI**: `weeks/week-XX/code/openapi.yaml`.
- **Mã nguồn dịch vụ**: `weeks/week-XX/code/` (để đối chiếu cổng port và payload thực tế).
- **Kịch bản Demo**: Thứ tự các bước gọi API theo luồng nghiệp vụ trên slide (ví dụ: Tạo mới -> Lấy chi tiết -> Thực hiện Custom Action -> Kiểm tra kết quả).

## 4. Output Mong Đợi
File JSON định dạng **Postman Collection v2.1.0** chuẩn mực tại:
`weeks/week-XX/code/postman_collection.json`

File collection phải đạt các tiêu chuẩn:
- Có biến môi trường nội tại `baseUrl` với giá trị mặc định là `http://localhost:3000`.
- Sắp xếp các request theo thứ tự logic của kịch bản thuyết trình (được đánh số `01 - ...`, `02 - ...`).
- Có sẵn Header (`Content-Type: application/json`, `Idempotency-Key` nếu có) và Body mẫu JSON hợp lệ.
- **Có sẵn Test Scripts (`pm.test`)**: Tối thiểu kiểm tra Status code và cấu trúc JSON trả về để khi sinh viên bấm "Send" trên máy chiếu, màn hình hiện màu xanh lá cây ("PASS") tạo ấn tượng chuyên nghiệp trước giảng viên.

## 5. Các Bước Xử Lý
1. **Đọc tài liệu quy chuẩn**: Đọc [`.agents/context/tooling-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/tooling-notes.md) mục "Postman & Newman" để áp dụng đúng cú pháp `pm.test` và script kiểm thử.
2. **Phân tích file `openapi.yaml`**:
   - Đọc các path, method, query parameters, request body và responses đã định nghĩa trong `weeks/week-XX/code/openapi.yaml`.
3. **Xây dựng cấu trúc Collection JSON**:
   - Tạo `info` chứa tên bài học (ví dụ: `SOA Week XX - Pattern Demo Collection`) và schema v2.1.0.
   - Định nghĩa mảng `item`, mỗi item đại diện cho một request demo:
     - `name`: Tên dễ hiểu kèm số thứ tự (ví dụ: `01. Create Resource`, `02. Get with Field Mask`).
     - `request`: Phương thức HTTP, URL dạng `{{baseUrl}}/path`, headers, body dạng `raw` JSON.
     - `event`: Thêm script `test` tự động:
       ```javascript
       pm.test("Status code is valid", function () {
           pm.expect(pm.response.code).to.be.oneOf([200, 201, 202, 204]);
       });
       pm.test("Response body format is correct", function () {
           if (pm.response.code !== 204) {
               pm.response.to.be.json;
           }
       });
       ```
4. **Ghi file**: Lưu ra `weeks/week-XX/code/postman_collection.json`.
5. **Cung cấp lệnh chạy Newman**: Ghi chú cho sinh viên lệnh terminal để chạy toàn bộ collection:
   ```bash
   newman run weeks/week-XX/code/postman_collection.json
   ```

## 6. Nguồn Dữ Liệu Cần Đọc
- [`.agents/context/tooling-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/tooling-notes.md)
- `weeks/week-XX/code/openapi.yaml`
- [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md)
