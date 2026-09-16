# UC Backlog — Dự Án Xuyên Suốt SOA: App Quản Lý Bán Đồ Ăn Nhanh

> **Quy tắc**: AI chỉ được đọc file này để lấy context. Mọi thay đổi trạng thái UC (thêm/chuyển trạng thái) phải qua Gate C — sinh viên duyệt. AI không tự ý ghi trực tiếp.

---

## Bảng Trạng Thái Use Cases (Tổng hợp 18 Use Cases)

| ID | Nhóm | Tên Use Case | Actor | Nghiệp vụ chính | Tuần gán | Trạng thái |
|:---|:---|:---|:---|:---|:---|:---|
| **UC01** | A. Tài khoản | Đăng ký tài khoản | Khách hàng | Kiểm tra thông tin → tạo tài khoản | — | ⏳ Pending |
| **UC02** | A. Tài khoản | Đăng nhập | Khách hàng / Nhân viên | Kiểm tra tài khoản → xác thực → cấp token | — | ⏳ Pending |
| **UC03** | B. Món ăn | Xem danh sách món ăn | Khách hàng | Lấy danh sách món đang bán | — | ⏳ Pending |
| **UC04** | B. Món ăn | Xem chi tiết món ăn | Khách hàng | Lấy thông tin chi tiết món | — | ⏳ Pending |
| **UC05** | B. Món ăn | Tìm kiếm món ăn | Khách hàng | Xử lý điều kiện tìm kiếm → truy vấn món | — | ⏳ Pending |
| **UC06** | B. Món ăn | Thêm món ăn | Admin | Kiểm tra dữ liệu → tạo món mới | — | ⏳ Pending |
| **UC07** | B. Món ăn | Cập nhật món ăn | Admin | Kiểm tra → cập nhật thông tin món | — | ⏳ Pending |
| **UC08** | B. Món ăn | Xóa món ăn | Admin | Kiểm tra trạng thái → xóa/ngừng bán (soft delete) | — | ⏳ Pending |
| **UC09** | C. Giỏ hàng | Xem giỏ hàng | Khách hàng | Lấy giỏ hàng hiện tại của user | — | ⏳ Pending |
| **UC10** | C. Giỏ hàng | Thêm món vào giỏ hàng | Khách hàng | Kiểm tra món → thêm/cập nhật item trong cart | — | ⏳ Pending |
| **UC11** | C. Giỏ hàng | Cập nhật số lượng món | Khách hàng | Kiểm tra số lượng → cập nhật item | — | ⏳ Pending |
| **UC12** | C. Giỏ hàng | Xóa món khỏi giỏ hàng | Khách hàng | Xóa item khỏi giỏ hàng | — | ⏳ Pending |
| **UC13** | D. Đơn hàng | Tạo đơn hàng | Khách hàng | Kiểm tra giỏ → tính tiền → tạo đơn | — | ⏳ Pending |
| **UC14** | D. Đơn hàng | Xem đơn hàng | Khách hàng | Lấy danh sách hoặc chi tiết đơn của mình | — | ⏳ Pending |
| **UC15** | D. Đơn hàng | Hủy đơn hàng | Khách hàng | Kiểm tra trạng thái đơn → hủy đơn | — | ⏳ Pending |
| **UC16** | D. Đơn hàng | Xác nhận đơn hàng | Nhân viên | Kiểm tra đơn → duyệt/xác nhận đơn | — | ⏳ Pending |
| **UC17** | D. Đơn hàng | Cập nhật trạng thái đơn | Nhân viên | Thay đổi trạng thái chế biến/vận chuyển/hoàn thành | — | ⏳ Pending |
| **UC18** | D. Đơn hàng | Xem danh sách đơn cần xử lý | Nhân viên | Lấy danh sách các đơn đang chờ xử lý | — | ⏳ Pending |

---

## Phân Bổ Dự Kiến Theo 13 Tuần Học

> *Lưu ý: Phân bổ dưới đây là gợi ý để ánh xạ kiến trúc tuần học vào Use Case phù hợp, sẽ được chốt chính thức tại Gate C của từng tuần.*

- **Tuần 01 - Giới thiệu API**: Giới thiệu tổng quan hệ thống, phân tích Service Contract & kiến trúc REST vs RPC cho các UC01–UC04.
- **Tuần 02 - REST & HTTP Fundamentals**: UC03 (Xem danh sách món) & UC04 (Xem chi tiết món) — chuẩn hóa HTTP GET, Status codes (200, 404).
- **Tuần 03 - Nguyên tắc thiết kế API**: UC06 (Thêm món) & UC07 (Cập nhật món) — 5 standard methods, RFC 7807 error format, validation.
- **Tuần 04 - OpenAPI & Swagger**: Viết OpenAPI 3.0 contract đặc tả cho toàn bộ nhóm Quản lý món ăn (UC03–UC08).
- **Tuần 05 - Data Modeling & Resource Design**: Nhóm Quản lý giỏ hàng (UC09–UC12) — sub-resource cha-con `/users/{id}/cart` hoặc association resource `/cart/items`.
- **Tuần 06 - Authentication & Authorization**: UC01 (Đăng ký), UC02 (Đăng nhập) — JWT Token, RBAC phân quyền giữa Khách hàng, Nhân viên, Admin.
- **Tuần 07 - Backend Implementation**: Ánh xạ contract sang code backend hoàn chỉnh, kết nối database (JPA/Mongoose).
- **Tuần 08 - API Testing**: Bộ test Newman/Postman tự động kiểm thử luồng đặt hàng (UC10 → UC13).
- **Tuần 09 - API Versioning**: Versioning v1 -> v2 cho nghiệp vụ thanh toán & tạo đơn hàng (UC13).
- **Tuần 10 - Service Operation**: Containerize Docker, rate limiting cho endpoint đăng nhập (UC02) và tìm kiếm (UC05).
- **Tuần 11 - API Design Patterns**: Idempotency Key cho tạo đơn hàng (UC13) để chống duplicate payment; Soft-delete cho UC08.
- **Tuần 12 - API as a Product**: Developer Portal, SDK/Docs, SLA cho đối tác tích hợp menu món ăn.
- **Tuần 13 - Capstone**: Hoàn thiện tích hợp end-to-end từ UC01 đến UC18.
