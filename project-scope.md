# Project Scope — Dự Án Xuyên Suốt SOA

> **Trạng thái**: Đã phê duyệt đề tài & danh mục Use Case gốc
> **Cập nhật lần cuối**: Tuần 01

---

## 1. Mô Tả Dự Án

**Tên đề tài**: **App Quản Lý Bán Đồ Ăn Nhanh** (Fast Food Ordering & Management API)

**Domain**: Hệ thống thương mại điện tử / đặt món ăn nhanh, phục vụ làm nền tảng triển khai liên tục qua 13 tuần học phần SOA.

**Luồng nghiệp vụ cốt lõi**:
```
Đăng ký → Đăng nhập → Xem danh sách món → Xem chi tiết món → 
Thêm món vào giỏ hàng (Cart) → Cập nhật giỏ hàng → Đặt hàng (Checkout/Order) → 
Xem lại chi tiết đơn hàng / Thanh toán (Payment) → Ngân hàng (optional) → 
Xem trạng thái đơn hàng / Hủy đơn → Event Bus (optional)
```

---

## 2. Resource Chính (Core Resources)

| Resource | Path đề xuất | Nghiệp vụ liên quan | Trạng thái |
|---|---|---|---|
| `Auth / Account` | `/auth`, `/users` | Quản lý tài khoản (Đăng ký, Đăng nhập, Phân quyền) | ⏳ Sẵn sàng |
| `Food Item (Món ăn)` | `/foods` hoặc `/items` | Danh sách, Chi tiết, Tìm kiếm, CRUD món | ⏳ Sẵn sàng |
| `Cart (Giỏ hàng)` | `/cart`, `/cart/items` | Xem giỏ, Thêm món, Cập nhật số lượng, Xóa món | ⏳ Sẵn sàng |
| `Order (Đơn hàng)` | `/orders` | Tạo đơn, Xem đơn, Hủy đơn, Xác nhận đơn, Cập nhật trạng thái | ⏳ Sẵn sàng |

> **Quy tắc**: Mỗi tuần chọn 1 Use Case nhỏ nhất từ danh mục 18 UC để implement vào `project/` qua Gate C.

---

## 3. Công Cụ & Constraints Kỹ Thuật

**Nhóm công cụ hỗ trợ gợi ý**:
- **Backend**: Java 21 + Spring Boot 3.x (hoặc Node.js/Express tùy chọn theo module thực hành) + Maven
- **Database**: PostgreSQL / MySQL (hoặc MongoDB đối với NoSQL module)
- **Persistence & Security**: Spring Data JPA / Hibernate + Spring Security (JWT)
- **API Documentation & Testing**: Swagger / OpenAPI 3.x, Postman / Newman
- **Containerization & Messaging**: Docker, Event Bus (optional: RabbitMQ / Kafka)

**Quy chuẩn chất lượng API**:
- Error format chuẩn RFC 7807 (Problem Details)
- RESTful Status Codes chuẩn xác (`200`, `201`, `204`, `400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`)
- Hỗ trợ Idempotency, Pagination, và Data Validation chặt chẽ

---

## 4. Nguyên Tắc Cộng Dồn Delta

1. Mỗi tuần trích xuất **1 UC nhỏ nhất** trong tổng số 18 UC để minh họa concept của tuần đó.
2. Codebase tại `project/` phát triển liên tục, delta tuần mới không được phá vỡ (break) các endpoint của tuần cũ.
3. Sinh viên tự tay implement các khối `TODO [HỌC VIÊN IMPLEMENT]` sau khi AI scaffold boilerplate.
4. Sau khi hoàn thành kiểm thử thực nghiệm (evidence) và review kiến trúc qua Gate C, UC tương ứng trong `uc-backlog.md` sẽ chuyển sang trạng thái `✅ Done`.
