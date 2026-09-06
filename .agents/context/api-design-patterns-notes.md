# Ghi Chép Cốt Lõi: "API Design Patterns" - JJ Geewax

Tài liệu này tổng hợp và chắt lọc toàn diện các mẫu thiết kế (Design Patterns) API chuẩn công nghiệp từ cuốn sách kinh điển ***API Design Patterns*** của tác giả **JJ Geewax** (Manning Publications, 2021). 
Cấu trúc tài liệu bám sát **6 Phần và 30 Chương** của giáo trình gốc, được diễn giải lại dưới góc độ sư phạm và kỹ thuật hệ thống phục vụ trực tiếp cho học phần Kiến trúc hướng dịch vụ (SOA) tại VNU-UET.

---

## PHẦN 1: TỔNG QUAN VỀ THIẾT KẾ API (INTRODUCTION)

### 1. Bản Chất API & Mẫu Thiết Kế (Ch. 1 & Ch. 2)
- **Vấn đề nó giải quyết:** Các hệ thống phần mềm phân tán thường được xây dựng phân mảnh, mỗi đội ngũ kỹ thuật tự quy ước chuẩn truyền nhận dữ liệu riêng, dẫn đến mã nguồn khó bảo trì, tích hợp tốn kém và trải nghiệm lập trình viên (DX) yếu kém.
- **Ý tưởng chính:**
  - *API (Application Programming Interface)*: Giao diện trừu tượng hóa cho phép các thành phần phần mềm tương tác với nhau mà không cần biết chi tiết cài đặt nội bộ.
  - *Sự phân hóa kiến trúc*: Từ RPC (gọi thủ tục từ xa - định hướng hành động) sang REST (chuyển giao trạng thái đại diện - định hướng tài nguyên) và Web Services.
  - *Design Patterns*: Tập hợp các giải pháp chuẩn hóa cho các bài toán thiết kế lặp đi lặp lại trong API, tạo ra tính nhất quán (Consistency) và khả năng đoán định (Predictability) trên toàn bộ hệ sinh thái dịch vụ.
- **Khi nào dùng trong thiết kế API thực tế:** Thiết lập quy chuẩn kiến trúc nền tảng trước khi bắt tay vào dự án (Week 01).

---

## PHẦN 2: CÁC NGUYÊN TẮC THIẾT KẾ NỀN TẢNG (DESIGN PRINCIPLES)

### 2. Quy Tắc Đặt Tên Tài Nguyên — Resource Naming (Ch. 3)
- **Vấn đề nó giải quyết:** Sự bất nhất trong URI, xung đột giữa danh từ và động từ, gây nhầm lẫn cho client khi gọi tài nguyên.
- **Ý tưởng chính:**
  - Tài nguyên luôn là **danh từ số nhiều** đại diện cho tập hợp (collection): `/users`, `/orders`, `/products`.
  - Phân cấp rõ ràng giữa collection và individual resource bằng định danh: `/users/{userId}`.
  - Chuẩn hóa định dạng: Dùng `kebab-case` hoặc `snake_case` cho URI segments; dùng `camelCase` cho các trường trong JSON body; tuyệt đối tránh lồng ghép động từ vào URI chuẩn REST.
- **Khi nào dùng trong thiết kế API thực tế:** Ngay từ khi định nghĩa sơ đồ đường dẫn URI cho hệ thống (Week 02).

### 3. Phân Cấp & Phạm Vi Tài Nguyên — Resource Scope & Hierarchy (Ch. 4)
- **Vấn đề nó giải quyết:** Biểu diễn các mối quan hệ phụ thuộc sở hữu (1-N, cha-con) mà không làm phình to hoặc phức tạp hóa mô hình dữ liệu của client.
- **Ý tưởng chính:**
  - *Tài nguyên con (Sub-resource)*: Đặt dưới tài nguyên cha nếu vòng đời của con gắn liền không thể tách rời với cha: `/customers/{customerId}/addresses/{addressId}` hoặc `/posts/{postId}/comments/{commentId}`.
  - *Tài nguyên độc lập (Top-level Resource)*: Nếu thực thể con có thể tồn tại độc lập hoặc cần được truy vấn từ nhiều ngữ cảnh khác nhau, đưa lên root collection và dùng khóa ngoại (foreign key/cross-reference) để liên kết.
- **Khi nào dùng trong thiết kế API thực tế:** Khi thiết kế mô hình dữ liệu quan hệ (Data Modeling) ở Week 05.

### 4. Kiểu Dữ Liệu & Giá Trị Mặc Định — Data Types and Defaults (Ch. 5)
- **Vấn đề nó giải quyết:** Xung đột kiểu dữ liệu giữa client và server (ví dụ: chuỗi biểu diễn số, ngày tháng sai định dạng ISO, giá trị `null` gây crash ứng dụng).
- **Ý tưởng chính:**
  - Sử dụng các kiểu dữ liệu chuẩn: Chuỗi thời gian theo định dạng ISO 8601 UTC (`2026-09-06T16:47:49Z`).
  - Tiền tệ: Tách biệt rõ ràng giá trị số nguyên (nano/cents) và mã tiền tệ ISO 4217 (`{ "amount": 100000, "currency": "VND" }`) để tránh sai số dấu phẩy động.
  - Định nghĩa rõ ràng giá trị mặc định (defaults) và phân biệt giữa `null` (xóa dữ liệu) với không truyền trường đó (giữ nguyên dữ liệu).
- **Khi nào dùng trong thiết kế API thực tế:** Khi thiết kế schema hợp đồng OpenAPI và Mongoose Model (Week 02, Week 05).

---

## PHẦN 3: CÁC MẪU CƠ BẢN (FUNDAMENTALS)

### 5. Định Danh Tài Nguyên — Resource Identification (Ch. 6)
- **Vấn đề nó giải quyết:** Định danh tài nguyên bị trùng lặp, dễ bị tấn công đoán ID tuần tự (Insecure Direct Object Reference - IDOR).
- **Ý tưởng chính:**
  - Sử dụng định danh duy nhất toàn cục: UUIDv4 hoặc chuỗi định danh tự sinh an toàn (ví dụ: `usr_9a8b7c6d`).
  - Tách bạch giữa ID nội bộ database (auto-increment integer / MongoDB ObjectId) và Public ID phơi bày ra API.
- **Khi nào dùng trong thiết kế API thực tế:** Thiết kế lược đồ định danh tài nguyên trong RESTful API (Week 02).

### 6. Bộ Phương Thức Tiêu Chuẩn — Standard Methods (Ch. 7)
- **Vấn đề nó giải quyết:** Lập trình viên tùy tiện tạo endpoint với các động từ lạ (`/getUser`, `/createNewOrder`, `/modifyItem`), phá vỡ tính tương thích của HTTP client.
- **Ý tưởng chính:** Chuẩn hóa bộ 5 phương thức CRUD cơ bản (List, Get, Create, Update, Delete - LGCUD):
  - `GET /resources`: List — Lấy danh sách tài nguyên (hỗ trợ phân trang, lọc, sắp xếp). Trả về `200 OK`.
  - `GET /resources/{id}`: Get — Lấy chi tiết một tài nguyên cụ thể. Trả về `200 OK` hoặc `404 Not Found`.
  - `POST /resources`: Create — Tạo mới tài nguyên. Trả về `201 Created` kèm header `Location: /resources/{id}`.
  - `PUT /resources/{id}` hoặc `PATCH /resources/{id}`: Update — Cập nhật toàn phần (`PUT`) hoặc cập nhật từng phần (`PATCH`). Trả về `200 OK`.
  - `DELETE /resources/{id}`: Delete — Xóa tài nguyên. Trả về `204 No Content` hoặc `200 OK`.
- **Khi nào dùng trong thiết kế API thực tế:** Là xương sống của 80% nghiệp vụ quản lý tài nguyên trong REST/SOA (Week 03, Week 07).

### 7. Cập Nhật Từng Phần & Mặt Nạ Trường — Partial Updates & Field Masks (Ch. 8)
- **Vấn đề nó giải quyết:** Hiện tượng ghi đè mất dữ liệu (Overwriting) khi nhiều client cùng update; lãng phí băng thông mạng khi chỉ muốn cập nhật 1 trường trong tài nguyên có hàng trăm trường.
- **Ý tưởng chính:**
  - Dùng HTTP `PATCH` kết hợp khái niệm `FieldMask` (danh sách các trường cần cập nhật, ví dụ query: `updateMask=status,description`).
  - Server chỉ đọc và cập nhật các trường có tên trong mask, giữ nguyên vẹn giá trị các trường còn lại trong database.
- **Khi nào dùng trong thiết kế API thực tế:** Các form chỉnh sửa hồ sơ người dùng, thông tin cấu hình sản phẩm phức tạp (Week 11).

### 8. Phương Thức Tùy Biến — Custom Methods (Ch. 9 & Ch. 15)
- **Vấn đề nó giải quyết:** Các hành động nghiệp vụ thực tế không thể ép vừa vào khuôn khổ CRUD (ví dụ: hủy đơn hàng, xuất bản bài viết, dịch văn bản, checkout thanh toán). Nếu cố ép vào CRUD sẽ làm méo mó mô hình tài nguyên.
- **Ý tưởng chính:**
  - Cú pháp chuẩn hóa sử dụng dấu hai chấm `:` ở cuối URI kết hợp với HTTP `POST`:
    - Với tài nguyên cụ thể: `POST /orders/{id}:cancel`, `POST /documents/{id}:publish`.
    - Với toàn bộ tập hợp hoặc tác vụ độc lập: `POST /translations:translate`, `POST /batch:process`.
  - Ch. 15 hướng dẫn mẫu *Add & Remove Custom Methods* cho quan hệ nhiều-nhiều: `POST /teams/{id}:addMember`, `POST /teams/{id}:removeMember`.
- **Khi nào dùng trong thiết kế API thực tế:** Kích hoạt các luồng quy trình nghiệp vụ (Workflows), chuyển đổi trạng thái máy (State Transitions) (Week 11).

### 9. Tác Vụ Chạy Ngầm Thời Gian Dài — Long-Running Operations (LRO) (Ch. 10)
- **Vấn đề nó giải quyết:** Client gọi API cho các tác vụ tốn nhiều thời gian (huấn luyện mô hình AI, render video, đối soát tài chính lớn). Giữ kết nối HTTP liên tục sẽ gây nghẽn kết nối, timeout và sập hạ tầng.
- **Ý tưởng chính:**
  - Server tiếp nhận yêu cầu, tạo ra một tài nguyên đại diện cho tác vụ (`Operation`) và phản hồi ngay lập tức mã `202 Accepted` kèm header `Location: /operations/{operationId}`.
  - Client thăm dò (Polling) trạng thái: `GET /operations/{opId}` $\to$ nhận về `{ "done": false, "progress": 45 }`.
  - Khi hoàn tất, server trả về: `{ "done": true, "response": { ... } }` hoặc `{ "done": true, "error": { ... } }`.
- **Khi nào dùng trong thiết kế API thực tế:** Mọi tác vụ có thời gian thực thi lớn hơn 2-5 giây hoặc cần giao tiếp bất đồng bộ qua hàng đợi (Week 11).

### 10. Tác Vụ Có Thể Chạy Lại & Khóa Lũy Kế — Rerunnable Jobs & Deduplication (Ch. 11 & Ch. 26)
- **Vấn đề nó giải quyết:** Mạng internet chập chờn khiến client gửi lại yêu cầu (retry), dẫn đến giao dịch bị nhân đôi ngoài ý muốn (trừ tiền 2 lần, tạo 2 đơn hàng trùng).
- **Ý tưởng chính:**
  - Client sinh một chuỗi UUID duy nhất gọi là `Idempotency-Key` (truyền qua HTTP Header `Idempotency-Key: <uuid>`).
  - Server lưu key này vào bộ đệm (Redis/DB) kèm trạng thái xử lý:
    - Nếu request mới: Lưu key ở trạng thái `PROCESSING`, thực thi nghiệp vụ, lưu lại kết quả và phản hồi.
    - Nếu request trùng key: Kiểm tra trạng thái; nếu đã thành công thì trả về ngay kết quả đã lưu trong bộ đệm mà không chạy lại logic nghiệp vụ.
- **Khi nào dùng trong thiết kế API thực tế:** Bắt buộc trong cổng thanh toán (Payment Gateway), trừ tồn kho, đặt phòng/vé máy bay (Week 11).

---

## PHẦN 4: QUAN HỆ TÀI NGUYÊN PHỨC TẠP (RESOURCE RELATIONSHIPS)

### 11. Tài Nguyên Đơn Bản — Singleton Sub-Resources (Ch. 12)
- **Vấn đề nó giải quyết:** Các tài nguyên chỉ có duy nhất một bản thể phụ thuộc vào tài nguyên cha. Việc đánh số ID trong URI là dư thừa và kỳ quặc (`/users/{id}/settings/1` là vô nghĩa).
- **Ý tưởng chính:**
  - Dùng danh từ số ít, không kèm ID: `/users/{id}/settings`, `/profile`, `/system/config`.
  - Hỗ trợ `GET` và `PATCH` (không cần `POST` hay `DELETE` vì tài nguyên này tự sinh ra và mất đi cùng cha).
- **Khi nào dùng trong thiết kế API thực tế:** Thiết kế cấu hình người dùng, giỏ hàng hiện tại (`/cart`), bảng cài đặt hệ thống (Week 05).

### 12. Tham Chiếu Chéo — Cross References (Ch. 13)
- **Vấn đề nó giải quyết:** Một tài nguyên cần liên kết đến tài nguyên ở domain khác mà không muốn lồng ghép toàn bộ dữ liệu (tránh over-fetching và dữ liệu cũ/stale).
- **Ý tưởng chính:**
  - Sử dụng định danh tài nguyên đầy đủ (Full Resource Name hoặc Resource URI): `{ "author": "users/usr_123", "publisher": "publishers/pub_456" }`.
  - Client có thể trực tiếp dùng giá trị này để truy vấn tài nguyên liên kết mà không cần tự lắp ghép URI.
- **Khi nào dùng trong thiết kế API thực tế:** Mô hình hóa quan hệ liên dịch vụ trong kiến trúc microservices (Week 05).

### 13. Tài Nguyên Liên Kết Nhiều-Nhiều — Association Resources (Ch. 14)
- **Vấn đề nó giải quyết:** Quan hệ Nhiều - Nhiều (N-N) có chứa dữ liệu riêng của mối quan hệ (ví dụ: ngày gia nhập, vai trò trong nhóm, trạng thái lời mời).
- **Ý tưởng chính:**
  - Biến bảng liên kết thành một tài nguyên độc lập hạng nhất (First-Class Resource): `/memberships`, `/enrollments`.
  - Hỗ trợ truy vấn linh hoạt theo 2 chiều: `/groups/{groupId}/memberships` và `/users/{userId}/memberships`.
- **Khi nào dùng trong thiết kế API thực tế:** Quản trị phân quyền nhóm người dùng (RBAC), đăng ký lớp học, hệ thống bạn bè/theo dõi (Week 05).

### 14. Tài Nguyên Đa Hình — Polymorphic Resources (Ch. 16)
- **Vấn đề nó giải quyết:** Một endpoint trả về danh sách các thực thể có cấu trúc khác nhau nhưng chung một danh mục cha (ví dụ: Phương thức thanh toán gồm Thẻ tín dụng, Ví điện tử, Chuyển khoản ngân hàng).
- **Ý tưởng chính:**
  - Sử dụng trường phân biệt loại (`type` hoặc `kind`) làm mỏ neo định danh schema (`"type": "CREDIT_CARD"` vs `"type": "E_WALLET"`).
  - Kết hợp với `oneOf` hoặc `anyOf` trong OpenAPI specification để đảm bảo tính an toàn kiểu (Type Safety).
- **Khi nào dùng trong thiết kế API thực tế:** Quản lý giao dịch thanh toán, các loại tài sản đa dạng trong hệ thống (Week 05).

---

## PHẦN 5: THAO TÁC TẬP HỢP & DỮ LIỆU LỚN (COLLECTIVE OPERATIONS)

### 15. Sao Chép & Di Chuyển — Copy & Move (Ch. 17)
- **Vấn đề nó giải quyết:** Client cần nhân bản một tài nguyên phức tạp hoặc di chuyển tài nguyên sang thư mục/cha khác mà không muốn tải về rồi gửi tạo lại (tốn băng thông và mất liên kết).
- **Ý tưởng chính:** Dùng custom method: `POST /files/{id}:copy` kèm body chỉ định đích đến, hoặc `POST /files/{id}:move`.
- **Khi nào dùng:** Hệ thống quản lý tài liệu, kho lưu trữ drive, phân loại danh mục (Week 11).

### 16. Thao Tác Theo Lô — Batch Operations (Ch. 18)
- **Vấn đề nó giải quyết:** Vấn đề gọi API quá nhiều lần (Chatty API / N+1 network calls) khi client cần tạo, cập nhật hoặc xóa hàng loạt bản ghi, gây nghẽn đường truyền và tải nặng server.
- **Ý tưởng chính:**
  - Cung cấp endpoint gom cụm: `POST /orders:batchCreate`, `POST /products:batchUpdate`.
  - Hỗ trợ xử lý nguyên khối (Atomic Transaction - tất cả thành công hoặc rollback) hoặc xử lý độc lập từng phần (Partial Success) trả về mảng kết quả kèm mã lỗi riêng cho từng phần tử.
- **Khi nào dùng trong thiết kế API thực tế:** Đồng bộ hóa dữ liệu POS, import file excel dữ liệu lớn, xử lý kho vận (Week 11).

### 17. Phân Trang Bằng Con Trỏ — Cursor/Token-based Pagination (Ch. 21)
- **Vấn đề nó giải quyết:** Phân trang truyền thống `offset/limit` chạy chậm dần theo cấp số cộng khi bảng dữ liệu lớn (`OFFSET 1000000` quét hàng triệu bản ghi), đồng thời gây lỗi bỏ sót hoặc trùng lặp bản ghi khi có dữ liệu mới chèn vào giữa lúc người dùng duyệt trang.
- **Ý tưởng chính:**
  - Client gửi `pageSize` và `pageToken` (hoặc `cursor`).
  - Server truy vấn dữ liệu dựa trên chỉ mục đã được đánh index: `WHERE id > last_seen_id ORDER BY id ASC LIMIT pageSize`.
  - Server trả về mảng dữ liệu kèm `nextPageToken` (mã hóa base64 thông tin con trỏ của bản ghi cuối).
- **Khi nào dùng trong thiết kế API thực tế:** Mọi API trả về danh sách lớn, bảng tin tức, mạng xã hội, lịch sử giao dịch (Week 11).

### 18. Lọc & Tìm Kiếm Chuẩn Hóa — Filtering & Searching (Ch. 22)
- **Vấn đề nó giải quyết:** Mỗi lập trình viên tự đặt query params tùy hứng (`?min_price=10&status=active`), không thể biểu diễn các điều kiện logic phức hợp (AND, OR, NOT, lồng ngoặc).
- **Ý tưởng chính:**
  - Chuẩn hóa tham số query `filter` sử dụng cú pháp biểu thức tường minh: `filter="status = 'PAID' AND totalAmount > 500"`.
  - Phân định rõ giữa lọc chính xác theo trường dữ liệu (Filtering) và tìm kiếm toàn văn mờ (Searching: `query="từ khóa"`).
- **Khi nào dùng trong thiết kế API thực tế:** Tìm kiếm nâng cao trong thương mại điện tử, báo cáo thống kê, truy vấn log hệ thống (Week 11).

---

## PHẦN 6: AN TOÀN & ĐỘ TIN CẬY (SAFETY & SECURITY)

### 19. Phiên Bản Hóa & Tính Tương Thích — Versioning & Compatibility (Ch. 24)
- **Vấn đề nó giải quyết:** Nâng cấp tính năng làm gãy vỡ (Breaking Changes) ứng dụng di động hoặc đối tác đang dùng phiên bản cũ.
- **Ý tưởng chính:**
  - Quy tắc tương thích ngược: Cho phép thêm trường tùy chọn trong request, thêm trường mới trong response; nghiêm cấm đổi kiểu dữ liệu trường cũ, xóa trường, hoặc thêm trường bắt buộc vào request cũ.
  - Sử dụng Semantic Versioning (SemVer) và đặt phiên bản chính trong URI: `/v1/resources`, `/v2/resources`.
- **Khi nào dùng trong thiết kế API thực tế:** Quản lý vòng đời và thay đổi hệ thống API (Week 09).

### 20. Xóa Mềm & Phục Hồi — Soft Deletion & Undelete (Ch. 25)
- **Vấn đề nó giải quyết:** Tránh mất mát dữ liệu vĩnh viễn do người dùng thao tác nhầm, phục vụ truy vết kiểm toán (Audit Trail) và tuân thủ pháp lý.
- **Ý tưởng chính:**
  - `DELETE /resources/{id}` không xóa bản ghi vật lý mà chỉ gán cờ `deleted: true` hoặc `deletedAt: timestamp`.
  - Mặc định ẩn tài nguyên bị xóa mềm khỏi API `List` (trừ khi có tham số `showDeleted=true`).
  - Hỗ trợ khôi phục qua custom method: `POST /resources/{id}:undelete`.
- **Khi nào dùng trong thiết kế API thực tế:** Áp dụng cho các thực thể dữ liệu quan trọng như tài khoản, hợp đồng, hóa đơn, bài viết (Week 11).

### 21. Xác Thực Dữ Liệu & Chạy Thử — Request Validation & Dry-Run (Ch. 27)
- **Vấn đề nó giải quyết:** Client cần kiểm tra xem biểu mẫu giao dịch lớn gồm hàng chục bước có hợp lệ không trước khi thực thi thực tế, tránh trường hợp submit giữa chừng gặp lỗi gây treo giao dịch.
- **Ý tưởng chính:**
  - Hỗ trợ cờ `validateOnly=true` hoặc `dryRun=true` trong query parameters của `POST/PUT/PATCH`.
  - Server chạy toàn bộ middleware validation cú pháp và kiểm tra ràng buộc logic nghiệp vụ, trả về lỗi chi tiết nếu có, nhưng tuyệt đối không ghi dữ liệu vào cơ sở dữ liệu.
- **Khi nào dùng trong thiết kế API thực tế:** Quy trình thanh toán giỏ hàng nhiều bước, import danh sách hàng loạt, cấu hình hạ tầng (Week 11).

### 22. Quản Lý Bản Sửa Đổi & Kiểm Soát Đồng Thời — Resource Revisions & Concurrency Control (Ch. 28)
- **Vấn đề nó giải quyết:** Xung đột ghi đè đồng thời (Lost Update Problem) trong hệ thống phân tán khi hai người dùng cùng tải một tài nguyên về, sửa đổi và cùng bấm lưu, dẫn đến người lưu sau ghi đè mất dữ liệu của người trước.
- **Ý tưởng chính:**
  - Sử dụng cơ chế khóa lạc quan (Optimistic Concurrency Control) với HTTP Header `ETag` hoặc trường `revisionId`/`etag` trong dữ liệu.
  - Khi client gửi request cập nhật (`PUT`/`PATCH`), bắt buộc phải truyền header `If-Match: "<etag_cũ>"`.
  - Server so khớp: Nếu ETag trùng khớp, thực hiện update và sinh ETag mới; nếu không khớp (đã có ai khác sửa trước đó), server từ chối với mã lỗi `412 Precondition Failed` hoặc `409 Conflict`.
- **Khi nào dùng trong thiết kế API thực tế:** Cực kỳ quan trọng trong môi trường microservices, soạn thảo văn bản cộng tác, điều chỉnh hạn mức tài chính (Week 11).

### 23. Xác Thực Yêu Cầu & Bối Cảnh Bảo Mật — Request Authentication (Ch. 30)
- **Vấn đề nó giải quyết:** Đảm bảo mọi cuộc gọi API đều được định danh an toàn, ngăn chặn giả mạo và thiết lập ngữ cảnh người dùng tin cậy cho tầng nghiệp vụ.
- **Ý tưởng chính:**
  - Sử dụng cơ chế xác thực dựa trên token chuẩn hóa (JWT Bearer Token qua header `Authorization: Bearer <token>`).
  - Tách bạch giữa thông tin danh tính xác thực (Authentication Context) và việc kiểm tra quyền hạn (Authorization).
- **Khi nào dùng trong thiết kế API thực tế:** Xây dựng middleware bảo mật cho toàn bộ dịch vụ (Week 06).

---

## 24. BẢNG ÁNH XẠ CHUẨN XÁC VÀO LỘ TRÌNH 13 TUẦN HỌC

| Tuần Học | Nội Dung Tuần | Các Chương & Mẫu Thiết Kế (JJ Geewax) Trọng Tâm | Ứng Dụng Kỹ Thuật Trong Khóa Học |
| :--- | :--- | :--- | :--- |
| **Week 01** | Giới thiệu API, Web Services | **Ch. 1 & 2**: Introduction to APIs & Design Patterns | Phân biệt RPC vs REST vs Web Services; vai trò của Design Patterns trong kiến trúc SOA |
| **Week 02** | REST & HTTP Fundamentals | **Ch. 3, 5, 6**: Naming, Data Types, Resource Identification | Chuẩn hóa danh từ số nhiều, segment path, kiểu dữ liệu, public resource IDs |
| **Week 03** | Nguyên tắc thiết kế API | **Ch. 7**: Standard Methods (List, Get, Create, Update, Delete) | Bộ 5 phương thức CRUD chuẩn mực, map đúng mã HTTP và chuẩn hóa payload lỗi |
| **Week 04** | OpenAPI & Swagger | Nguyên lý Hợp đồng giao tiếp (Contract-First Interface) | Soạn thảo bản hợp đồng machine-readable độc lập với mã nguồn |
| **Week 05** | Data Modeling & Resource Design | **Ch. 4, 12, 13, 14, 16**: Hierarchy, Singleton, Cross References, Association, Polymorphism | Thiết kế quan hệ cha-con 1-N, tài nguyên đơn bản, tham chiếu liên dịch vụ, quan hệ N-N, và tài nguyên đa hình |
| **Week 06** | Authentication & Authorization | **Ch. 30**: Request Authentication | Bảo vệ endpoint bằng Token Bearer, thiết lập Security Context trong request |
| **Week 07** | Backend Implementation | **Ch. 7, 27**: Standard Methods Implementation & Request Validation | Ánh xạ Spec-to-Code theo Layered Architecture, xác thực request tại tầng middleware |
| **Week 08** | API Testing | **Ch. 7, 27, 29**: Method Verification, Error Response Testing & Retrial | Kiểm thử hợp đồng, kiểm thử tính chịu lỗi (Fault Tolerance) qua Postman/Newman |
| **Week 09** | API Versioning | **Ch. 24, 28**: Versioning & Compatibility, Resource Revisions | Quy tắc tương thích ngược, Semantic Versioning `/v1/`, kiểm soát phiên bản tài nguyên |
| **Week 10** | Service Operation | **Ch. 29, 30**: Request Retrial, Gateway Policy Enforcement | Xử lý thử lại an toàn khi rớt mạng, áp dụng chính sách bảo vệ qua API Gateway |
| **Week 11** | API Design Patterns | **Ch. 8, 9, 10, 11, 14, 15, 17, 18, 21, 22, 25, 26, 27, 28** (Toàn bộ Advanced Patterns) | Xử lý các bài toán phân tán chuyên sâu: Idempotency Key, LRO, FieldMask, Cursor Pagination, Batch, Soft Delete, ETag Concurrency |
| **Week 12** | API as a Product | **Ch. 1, 2**: API Ecosystem & Developer-Centric Design | Xây dựng hệ sinh thái API trực quan, lấy trải nghiệm lập trình viên làm trọng tâm |
| **Week 13** | Dự án nhóm (Capstone) | **Tổng hợp toàn diện Ch. 1 - 30** | Tích hợp đầy đủ các mẫu thiết kế vào hệ thống microservices hoàn chỉnh |


