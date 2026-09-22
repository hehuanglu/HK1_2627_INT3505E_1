# Tổng Hợp Kiến Thức Tuần 02: Kiến Trúc REST & HTTP Fundamentals

## 1. Bản Chất Kiến Trúc REST & 6 Ràng Buộc (Architectural Constraints)

REST (Representational State Transfer) được Roy Fielding công bố năm 2000 (§5), là một **phong cách kiến trúc (Architectural Style)**, không phải là một giao thức hay chuẩn dữ liệu cụ thể (REST $\neq$ JSON qua HTTP). REST được thiết kế để chuẩn hóa việc xây dựng ứng dụng phân tán trên nền tảng Web thông qua **6 ràng buộc**:

```
+-----------------------------------------------------------------------------------+
|                            6 RÀNG BUỘC KIẾN TRÚC REST                             |
+-----------------------------------------------------------------------------------+
| 1. Client-Server     | Bắt buộc | Tách rời UI và Data Storage; độc lập tiến hóa.  |
| 2. Stateless         | Bắt buộc | Server không lưu session; mỗi request tự đầy đủ.|
| 3. Cacheable         | Bắt buộc | Phản hồi tự khai báo khả năng lưu trữ đệm.      |
| 4. Uniform Interface | Bắt buộc | Hợp đồng giao tiếp chuẩn hóa (4 ràng buộc con). |
| 5. Layered System    | Bắt buộc | Kiến trúc trung gian đa tầng (Gateway, CDN).    |
| 6. Code on Demand    | Tùy chọn | Server gửi mã chạy được (JS); duy nhất có thể bỏ.|
+-----------------------------------------------------------------------------------+
```

- **Client-Server**: Tách biệt mối bận tâm (concerns). Khác với các hệ thống Web thập niên 1990 trộn lẫn UI và dữ liệu trong HTML render kèm session ẩn, Client-Server yêu cầu hai bên chỉ trao đổi qua định dạng chuẩn (URI + Representation). Server có thể đổi DB mà Client không cần biết.
- **Stateless**: Mỗi request phải tự mang đầy đủ ngữ cảnh để server xử lý độc lập. 
  - *Cơ chế Token vs Session*: Thay vì gửi Cookie chứa Session ID buộc server phải tra cứu bảng session tập trung (gây nghẽn khi scale), Client gửi kèm Token (JWT) trong header `Authorization: Bearer <token>`.
  - *Lợi ích*: Server scale ngang (horizontal scaling) tùy ý qua Round-Robin Load Balancer mà không cần Sticky Session; log độc lập, tăng khả năng quan sát (observability).
  - *Lưu ý*: Ràng buộc nói về *Request*. Server vẫn lưu trạng thái dữ liệu (Database, Cache, Audit Log), chỉ là không lưu trạng thái hội thoại của client.
- **Layered System**: Client chỉ nhìn thấy lớp trung gian kế tiếp (API Gateway, CDN, Reverse Proxy) mà không thể biết có phải máy chủ gốc (Origin) hay không. Ví dụ thực tế: Shopee Việt Nam (2020) tách API Gateway để xử lý xác thực và rate-limit cho 2 tỷ request/ngày, bảo vệ Origin Server chỉ tập trung vào business logic.
- **So sánh REST vs RPC**: RPC tập trung vào **Hành động** (`POST /createOrder`, `/getBook?id=1`), trong khi REST tập trung vào **Tài nguyên** (`POST /orders`, `GET /books/1`).

---

## 2. Uniform Interface & Quy Tắc Thiết Kế Tài Nguyên (URI & Representation)

Uniform Interface là ràng buộc sâu nhất phân biệt REST với các mô hình mạng khác, gồm **4 ràng buộc con**:

1. **Identification of Resources (Định danh tài nguyên)**:
   - **Tài nguyên (Resource)** là thực thể trừu tượng mang giá trị dữ liệu và có thể biến đổi trạng thái theo thời gian.
   - **URI (Uniform Resource Identifier)** là nhãn định danh ổn định trỏ tới tài nguyên, không phải bản thân tài nguyên.
   - *Quy tắc chuẩn hóa URI (JJ Geewax Ch. 3, 5, 6 & Bruno Pedro Ch. 2, 8)*:
     - Dùng **danh từ số nhiều**, không dùng động từ: `/books`, `/orders` (Tránh `/getBooks`, `/updateBook`).
     - Phân cấp tự nhiên biểu diễn quan hệ sở hữu: `/books/{id}/reviews`.
     - Dùng chữ thường và `kebab-case` cho path segment (`/flight-bookings`), tránh đuôi mở rộng file (`.json`).
     - *Resource Identification*: Tránh dùng số nguyên tự tăng (Auto-increment integer ID) để phòng chống tấn công IDOR; nên dùng chuỗi định danh duy nhất toàn cục như UUIDv4 hoặc có tiền tố (`ord_91f3`).
2. **Manipulation through Representations (Thao tác qua biểu diễn)**:
   - **Resource $\neq$ Representation**: Cùng một tài nguyên (Cuốn sách "Clean Code") có thể có nhiều biểu diễn cụ thể (JSON, XML, CSV, HTML).
   - Thao tác sửa đổi thực hiện bằng cách gửi biểu diễn mới lên server (`PATCH /books/42` kèm body JSON).
3. **Self-descriptive Messages (Thông điệp tự mô tả)**:
   - Request và Response phải mang đầy đủ metadata để bên nhận hiểu được mà không cần biết trước: `Content-Type`, `Content-Length`, `Cache-Control`, `Location`, HTTP Status Code.
   - *Content Negotiation*: Client đề xuất định dạng mong muốn qua header `Accept` kèm trọng số ưu tiên `q-value` (ví dụ: `Accept: text/html, application/json;q=0.9`). Nếu server không đáp ứng được, trả về `406 Not Acceptable`.
4. **HATEOAS (Hypermedia as the Engine of Application State)**:
   - Phản hồi chứa các siêu liên kết (`_links`) trỏ tới các trạng thái kế tiếp (ví dụ: `next`, `cancel`, `self`), giúp Client tự khám phá API thay vì hard-code URI.
   - *Mô hình trưởng thành Richardson (RMM)*: Level 0 (The Swamp of POX) $\to$ Level 1 (Resources) $\to$ Level 2 (HTTP Verbs & Codes — đạt 90% production) $\to$ Level 3 (Hypermedia/HATEOAS). Roy Fielding (2010) lưu ý REST là tập ràng buộc tổng thể, không phải thang bậc chia nhỏ.

---

## 3. Ngữ Nghĩa Giao Thức HTTP: Methods, Idempotency, Safety & Status Codes

Cấu trúc HTTP Message gồm: Request/Status line + Headers + Dòng trống phân tách (CRLF CRLF) + Body. Từ HTTP/1.1, header `Host` là bắt buộc.

```
                         HTTP METHODS MATRIX (RFC 9110)
+---------+------------------------------+-------+------------+-----------------------+
| Method  | Mục đích sử dụng             | Safe  | Idempotent | Mã trạng thái chuẩn   |
+---------+------------------------------+-------+------------+-----------------------+
| GET     | Đọc dữ liệu tài nguyên       | Có    | Có         | 200 OK                |
| HEAD    | Lấy header (kiểm tra tồn tại)| Có    | Có         | 200 OK (không body)   |
| OPTIONS | Thăm dò phương thức hỗ trợ   | Có    | Có         | 200 OK (kèm Allow)    |
| POST    | Tạo mới / Xử lý generic      | Không | Không      | 201 Created / 200 OK  |
| PUT     | Thay thế TOÀN BỘ tài nguyên  | Không | Có         | 200 OK / 204 / 201    |
| PATCH   | Cập nhật MỘT PHẦN tài nguyên | Không | Không*     | 200 OK                |
| DELETE  | Xóa tài nguyên               | Không | Có         | 204 No Content        |
+---------+------------------------------+-------+------------+-----------------------+
```

- **Safety (RFC 9110 §9.2.1)**: Thao tác chỉ đọc, không làm thay đổi trạng thái tài nguyên trên server (GET, HEAD, OPTIONS). An toàn cho Web Crawler, Pre-fetching và trình duyệt nhấn F5.
- **Idempotency (RFC 9110 §9.2.2)**: Gọi $N$ lần liên tiếp cho cùng một trạng thái server như gọi 1 lần (GET, PUT, DELETE).
  - *DELETE có Idempotent không?*: Có! Gọi lần 1 trả `204`, lần 2 trả `404`, nhưng trạng thái tài nguyên trên server là không đổi (đều không còn tồn tại).
  - *PUT vs PATCH*: PUT bắt buộc gửi toàn bộ trường dữ liệu để thay thế bản ghi; PATCH chỉ gửi các trường cần cập nhật (RFC 7396 Merge Patch hoặc RFC 6902 JSON Patch). PATCH không mặc định idempotent nếu chứa thao tác tương đối (như tăng biến đếm).
  - *Idempotency-Key*: Dùng header UUID cho POST (ví dụ thanh toán) để server lưu kết quả trong 24h, hỗ trợ retry an toàn khi rớt mạng.

### Hệ Thống Mã Trạng Thái (Status Codes Semantics):
- **1xx (Informational)**: Phản hồi tạm thời (`100 Continue`, `101 Switching Protocols`).
- **2xx (Success)**: Thành công chắc chắn (`200 OK`, `201 Created` kèm header `Location`, `202 Accepted` cho tác vụ ngầm async, `204 No Content` khi xóa xong không trả body).
- **3xx (Redirection)**: Chuyển tiếp. Phân biệt rõ:
  - `301 Moved Permanently` vs `308 Permanent Redirect`: Mã 308 giữ nguyên method ban đầu (POST vẫn là POST), tránh việc client tự chuyển thành GET như 301.
  - `302 Found` (cũ, không rõ ràng) vs `307 Temporary Redirect` (giữ nguyên method cho POST).
  - `304 Not Modified`: Tương tác với Conditional Requests (`ETag` / `If-None-Match`), không trả lại body.
- **4xx (Client Error)**: Lỗi do client gửi sai, client phải sửa trước khi retry:
  - `400 Bad Request`: Sai cú pháp (Malformed JSON, query string sai định dạng).
  - `401 Unauthorized`: Chưa xác thực (Unauthenticated - thiếu hoặc sai token).
  - `403 Forbidden`: Đã xác thực nhưng không đủ quyền hạn.
  - `404 Not Found`: Không tìm thấy tài nguyên (hoặc giả vờ để ẩn giấu bảo mật).
  - `409 Conflict`: Xung đột phiên bản dữ liệu khi cập nhật đồng thời.
  - `415 Unsupported Media Type`: Client gửi sai định dạng Content-Type (ví dụ không gửi JSON).
  - `422 Unprocessable Entity`: Cú pháp đúng nhưng vi phạm nghiệp vụ (`price < 0`, thiếu `title`).
  - `429 Too Many Requests`: Vượt ngưỡng rate limit (luôn kèm header `Retry-After`).
- **5xx (Server Error)**: Lỗi từ máy chủ, client có thể retry:
  - `500 Internal Error`: Lỗi hệ thống bất ngờ (tuyệt đối không để lộ stack trace ra client).
  - `502 Bad Gateway`: Proxy/Gateway nhận response lỗi từ Upstream (Nginx $\to$ Flask).
  - `503 Service Unavailable`: Quá tải hoặc đang bảo trì (kèm `Retry-After`).
  - `504 Gateway Timeout`: Gateway chờ Upstream quá thời gian quy định.

---
