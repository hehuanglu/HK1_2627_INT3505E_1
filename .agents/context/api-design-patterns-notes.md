# Ghi Chép Cốt Lõi: "API Design Patterns" - JJ Geewax

Tài liệu này tổng hợp và chắt lọc các mẫu thiết kế (design patterns) API chuẩn công nghiệp từ cuốn sách *API Design Patterns* (JJ Geewax - Manning Publications). Toàn bộ nội dung được diễn giải lại theo góc nhìn sư phạm và kỹ thuật hệ thống phục vụ học phần Kiến trúc hướng dịch vụ (SOA).

---

## 1. Resource Naming (Quy tắc đặt tên tài nguyên)
- **Vấn đề nó giải quyết:** Sự bất nhất trong việc đặt tên URI, khó đoán định (predictability) cho client, xung đột giữa danh từ và động từ trong REST.
- **Ý tưởng chính:** 
  - Tài nguyên là danh từ số nhiều đại diện cho collection (`/users`, `/orders`).
  - Phân cấp rõ ràng giữa collection và individual resource (`/users/{userId}`).
  - Sử dụng định dạng `kebab-case` hoặc `snake_case` thống nhất cho segment URI; `camelCase` cho body JSON; tránh dùng động từ trong đường dẫn tiêu chuẩn.
- **Khi nào dùng trong thiết kế API thực tế:** Ngay từ giai đoạn định hình Resource Model cho toàn bộ hệ thống API/SOA nhằm đảm bảo tính trực quan và khả năng mở rộng.

---

## 2. Resource Hierarchy & Scoping (Phân cấp và phạm vi tài nguyên)
- **Vấn đề nó giải quyết:** Biểu diễn các mối quan hệ sở hữu phụ thuộc (parent-child, 1-N) mà không làm phức tạp hóa mô hình dữ liệu của client.
- **Ý tưởng chính:** 
  - Tài nguyên con (sub-resource) nằm dưới tài nguyên cha nếu vòng đời của con gắn chặt với cha (`/customers/{id}/addresses/{addressId}`).
  - Nếu tài nguyên con có thể tồn tại độc lập hoặc truy cập từ nhiều ngữ cảnh, ưu tiên đưa lên top-level collection kèm thuộc tính tham chiếu (`foreign key`).
- **Khi nào dùng trong thiết kế API thực tế:** Khi thiết kế các thực thể liên kết mật thiết như mục đơn hàng trong đơn hàng (`/orders/{id}/items`), bình luận của bài viết (`/posts/{id}/comments`).

---

## 3. Standard Methods (Các phương thức chuẩn: List, Get, Create, Update, Delete)
- **Vấn đề nó giải quyết:** Mỗi lập trình viên tự chế các phương thức CRUD với động từ và mã HTTP tùy tiện, gây khó khăn cho tích hợp tự động.
- **Ý tưởng chính:** Chuẩn hóa tập 5 hành vi cốt lõi (LGCUD) map trực tiếp với HTTP verbs:
  - `GET /resources`: List (trả về mảng kèm phân trang).
  - `GET /resources/{id}`: Get (lấy chi tiết 1 tài nguyên).
  - `POST /resources`: Create (tạo mới, trả về 201 Created kèm URI).
  - `PUT /resources/{id}` hoặc `PATCH /resources/{id}`: Update (cập nhật toàn phần hoặc một phần).
  - `DELETE /resources/{id}`: Delete (xóa, trả về 204 No Content hoặc 200).
- **Khi nào dùng trong thiết kế API thực tế:** Là nền tảng bắt buộc cho hơn 80% các endpoint quản lý tài nguyên trong bất kỳ hệ thống SOA/RESTful API nào.

---

## 4. Partial Updates & Field Masks (Cập nhật một phần với Field Mask)
- **Vấn đề nó giải quyết:** Hiện tượng ghi đè mất dữ liệu (overwriting) khi nhiều client cùng update, lãng phí băng thông khi chỉ cần đổi 1-2 trường trong document lớn, và sự mơ hồ giữa "xóa giá trị về null" với "không muốn cập nhật trường đó".
- **Ý tưởng chính:** 
  - Dùng HTTP `PATCH` kết hợp khái niệm `FieldMask` (danh sách các trường cần cập nhật, ví dụ `updateMask=status,description`).
  - Server chỉ đọc và cập nhật các trường có tên trong mask, giữ nguyên các trường khác.
- **Khi nào dùng trong thiết kế API thực tế:** Khi tài nguyên có nhiều trường (profile người dùng, cấu hình sản phẩm), hoặc hệ thống có nhiều role cùng cập nhật các phân vùng dữ liệu khác nhau trên cùng một record.

---

## 5. Custom Methods (Phương thức tùy biến)
- **Vấn đề nó giải quyết:** Các hành động nghiệp vụ thực tế không thể ánh xạ tự nhiên vào CRUD (ví dụ: kích hoạt tài khoản, gửi email, dịch văn bản, checkout giỏ hàng). Cố ép vào CRUD sẽ làm méo mó mô hình tài nguyên.
- **Ý tưởng chính:** 
  - Dùng cú pháp dấu hai chấm `:` ở cuối URI kết hợp HTTP `POST`: `POST /orders/{id}:cancel`, `POST /documents/{id}:publish`, hoặc top-level: `POST /translations:translate`.
  - Giữ nguyên bản chất hướng tài nguyên nhưng tường minh về mặt hành động nghiệp vụ.
- **Khi nào dùng trong thiết kế API thực tế:** Khi cần kích hoạt quy trình nghiệp vụ (workflow), chuyển đổi trạng thái máy (state transition), hoặc thực thi tác vụ tính toán không tạo tài nguyên bền vững.

---

## 6. Long-Running Operations - LRO (Tác vụ chạy ngầm thời gian dài)
- **Vấn đề nó giải quyết:** Client gọi API nhưng tác vụ mất vài phút/giờ (ví dụ: huấn luyện AI, render video, xuất báo cáo tài chính). Giữ kết nối HTTP sẽ bị timeout hoặc rớt mạng.
- **Ý tưởng chính:** 
  - Pattern bất đồng bộ: Client gửi yêu cầu, server tạo một tài nguyên đại diện cho tác vụ `Operation` và trả về ngay mã `202 Accepted` kèm `operationId` hoặc URL kiểm tra trạng thái (`/operations/{opId}`).
  - Client định kỳ polling hoặc server gửi webhook / SSE thông báo khi trạng thái chuyển sang `done: true` kèm kết quả hoặc lỗi.
- **Khi nào dùng trong thiết kế API thực tế:** Bất kỳ thao tác nào có thời gian xử lý lớn hơn ngưỡng chịu tải thông thường của HTTP (thường là > 2 - 5 giây) hoặc phụ thuộc hệ thống bên thứ ba.

---

## 7. Rerunnable Jobs & Idempotency (Tác vụ chạy lại an toàn & Tính lũy kế/Idempotent)
- **Vấn đề nó giải quyết:** Mạng chập chờn khiến client gửi lại request, dẫn đến giao dịch bị nhân đôi (ví dụ: quẹt thẻ 2 lần, tạo 2 đơn hàng trùng).
- **Ý tưởng chính:** 
  - Client sinh ra một `Idempotency-Key` (UUID) truyền qua Header.
  - Server ghi nhận key này kèm trạng thái xử lý; nếu nhận lại key cũ đã thành công, server trả về kết quả đã cache mà không thực thi lại logic nghiệp vụ.
- **Khi nào dùng trong thiết kế API thực tế:** Cực kỳ quan trọng trong API tài chính, thanh toán (payment gateway), đặt chỗ (booking), trừ kho hàng.

---

## 8. Singleton Sub-Resources (Tài nguyên đơn bản)
- **Vấn đề nó giải quyết:** Những tài nguyên chỉ có duy nhất một thực thể phụ thuộc trong ngữ cảnh cha, việc định danh bằng ID số nhiều là thừa thãi (`/users/{id}/settings/1` là vô nghĩa).
- **Ý tưởng chính:** 
  - Thiết kế endpoint dạng số ít không cần identifier: `/users/{id}/settings`, `/profile`, `/system/config`.
  - Hỗ trợ các phương thức `GET`, `PATCH` (không cần `POST` hay `DELETE` nếu nó tự sinh theo cha).
- **Khi nào dùng trong thiết kế API thực tế:** Cài đặt cá nhân, thông tin cấu hình hệ thống, giỏ hàng hiện tại của phiên người dùng (`/cart`).

---

## 9. Association Resources (Tài nguyên quan hệ Many-to-Many)
- **Vấn đề nó giải quyết:** Mô hình hóa mối quan hệ nhiều - nhiều phức tạp (ví dụ: Sinh viên tham gia Lớp học, User thuộc Nhóm) khi mối quan hệ đó cần lưu metadata riêng (ngày gia nhập, vai trò, quyền hạn).
- **Ý tưởng chính:** 
  - Biến bảng liên kết (join table) thành một tài nguyên bậc nhất (first-class resource): `/memberships`, `/enrollments`.
  - Có thể truy vấn hai chiều: `/groups/{id}/memberships` và `/users/{id}/memberships`.
- **Khi nào dùng trong thiết kế API thực tế:** Quản lý quyền truy cập RBAC, hệ thống phân công công việc, mạng xã hội (follow/friendship), đăng ký môn học.

---

## 10. Pagination: Token/Cursor-based (Phân trang bằng Token/Con trỏ)
- **Vấn đề nó giải quyết:** Phân trang truyền thống `offset/limit` chạy rất chậm với dữ liệu lớn (`OFFSET 1000000` quét toàn bộ bảng) và bị lỗi nhảy trang/lặp bản ghi khi có dữ liệu mới chèn vào giữa lúc người dùng đang duyệt.
- **Ý tưởng chính:** 
  - Client gửi `pageSize` và `pageToken` (hoặc `cursor`). Server trả về danh sách kèm `nextPageToken` (mã hóa vị trí bản ghi cuối cùng của trang trước).
  - Truy vấn database dựa vào chỉ mục: `WHERE id > last_seen_id LIMIT pageSize`.
- **Khi nào dùng trong thiết kế API thực tế:** Danh sách dữ liệu liên tục thay đổi (tin nhắn, feed bài viết, lịch sử giao dịch) hoặc bảng có từ hàng chục nghìn bản ghi trở lên.

---

## 11. Filtering & Searching (Lọc và Tìm kiếm có cấu trúc)
- **Vấn đề nó giải quyết:** Mỗi API tự chế query parameters riêng lẻ (`?name=abc&price_min=10&price_max=20`), khó biểu diễn các điều kiện logic phức tạp (AND, OR, NOT, so sánh mảng).
- **Ý tưởng chính:** 
  - Dùng tham số chuẩn hóa `filter` với cú pháp biểu thức đơn giản (ví dụ: `filter="status = 'ACTIVE' AND price < 100"`).
  - Tách bạch giữa lọc chính xác (filtering theo field) và tìm kiếm văn bản toàn văn (full-text search: `query="từ khóa"`).
- **Khi nào dùng trong thiết kế API thực tế:** Các màn hình tìm kiếm nâng cao, danh mục hàng hóa thương mại điện tử, báo cáo log/audit trail.

---

## 12. Soft Deletion & Undelete (Xóa mềm và Phục hồi)
- **Vấn đề nó giải quyết:** Tránh mất mát dữ liệu vĩnh viễn do thao tác nhầm của người dùng, đáp ứng yêu cầu kiểm toán và truy vết lịch sử nghiệp vụ.
- **Ý tưởng chính:** 
  - Phương thức `DELETE /resources/{id}` không xóa bản ghi vật lý mà đánh dấu cờ `deleted: true` hoặc `deletedAt: timestamp`.
  - Ẩn tài nguyên này khỏi API List thông thường (trừ khi có query `showDeleted=true`).
  - Hỗ trợ custom method để phục hồi: `POST /resources/{id}:undelete`.
- **Khi nào dùng trong thiết kế API thực tế:** Tài liệu làm việc, tài khoản khách hàng, đơn hàng, dữ liệu nghiệp vụ quan trọng cần tính năng "Thùng rác" (Trash/Recycle Bin).

---

## 13. Request Validation & Dry-Run (Xác thực dữ liệu và Chạy thử nghiệm)
- **Vấn đề nó giải quyết:** Client muốn kiểm tra xem toàn bộ form nhập liệu phức tạp có hợp lệ không trước khi thực hiện giao dịch lớn, tránh việc submit lỗi giữa chừng gây thất thoát hoặc rollback nặng nề.
- **Ý tưởng chính:** 
  - Hỗ trợ cờ `validateOnly=true` hoặc `dryRun=true` trong query parameters của yêu cầu `POST/PUT/PATCH`.
  - Server thực thi toàn bộ logic validate cú pháp và logic nghiệp vụ, trả về lỗi nếu có, nhưng tuyệt đối không ghi dữ liệu vào database.
- **Khi nào dùng trong thiết kế API thực tế:** Các form thanh toán nhiều bước, import danh sách hàng loạt, cấu hình hạ tầng phức tạp.

---

## 14. Versioning & Backward Compatibility (Phiên bản hóa và Tính tương thích ngược)
- **Vấn đề nó giải quyết:** Nâng cấp API làm đứt gãy ứng dụng của các client cũ đang chạy trên môi trường thực tế (breaking changes).
- **Ý tưởng chính:** 
  - Đặt version trong URL path cho major version: `/v1/orders`, `/v2/orders`.
  - Quy tắc tương thích ngược: Cho phép thêm trường mới trong response, thêm query parameter tùy chọn; nghiêm cấm đổi kiểu dữ liệu trường cũ, xóa trường, hoặc thêm trường bắt buộc trong request cũ.
- **Khi nào dùng trong thiết kế API thực tế:** Bất kỳ API nào phục vụ bên thứ ba hoặc có nhiều client (Web, Mobile iOS, Mobile Android) với chu kỳ cập nhật khác nhau.
