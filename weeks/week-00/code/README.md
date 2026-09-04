# Hướng Dẫn Thực Hành - Tuần 00: Course Service Demo

Thư mục này chứa mã nguồn minh họa cho bài giảng **Tuần 00: Nhập môn Kiến trúc Hướng dịch vụ (SOA) & Mẫu Định danh Tài nguyên (Resource Naming)**.

---

## 1. Mục Tiêu Thực Hành
- Quan sát cách đặt tên URI theo tài nguyên danh từ số nhiều (`/api/v1/courses`).
- Trải nghiệm quy tắc trả về mã trạng thái HTTP chuẩn mực:
  - `200 OK` khi lấy danh sách hoặc lấy chi tiết thành công.
  - `201 Created` kèm header `Location` khi tạo mới.
  - `204 No Content` khi xóa thành công.
  - `400 Bad Request` khi dữ liệu đầu vào thiếu sót.
  - `404 Not Found` khi truy vấn tài nguyên không tồn tại.
  - `409 Conflict` khi trùng khóa định danh nghiệp vụ (`code`).

---

## 2. Cách Khởi Chạy Nhanh (Quickstart)

```bash
# 1. Cài đặt các thư viện cần thiết
npm install

# 2. Khởi chạy server
npm start
```

> **Lưu ý đặc biệt (In-Memory Fallback)**:
> Server được tích hợp sẵn chế độ dữ liệu giả lập trong bộ nhớ RAM. Do đó, ngay cả khi bạn **chưa bật MongoDB**, server vẫn tự động kích hoạt chế độ dự phòng để bạn chạy thử nghiệm ngay lập tức (Thời gian ra kết quả < 1 phút).

---

## 3. Kiểm Thử Bằng Postman & Newman

Chạy kiểm thử toàn bộ các kịch bản với Newman CLI:
```bash
newman run postman_collection.json
```

Hoặc import file `postman_collection.json` trực tiếp vào ứng dụng **Postman** trên máy tính để thực hiện từng request và theo dõi kết quả trả về.
