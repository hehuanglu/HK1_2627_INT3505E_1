# Lý Thuyết Mở Rộng & Bộ Câu Hỏi Đào Sâu Kiến Thức — Tuần 02

> **Tài liệu tham chiếu chuẩn**:
> - Bài giảng: *SOA - B2: Kiến trúc REST và HTTP Fundamentals* (Slides 1–27)
> - Ghi chú lớp học: [note.txt](file:///Users/hahoangloc/Working/UET/SOA/weeks/week-02/note.txt)
> - Bài tập thực hành & Git Log: [practice/app.py](file:///Users/hahoangloc/Working/UET/SOA/weeks/week-02/practice/app.py)
> - Nguồn ngữ cảnh: [syllabus.md](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/syllabus.md), [industry-mapping.md](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/industry-mapping.md), [glossary-soa.md](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/glossary-soa.md), [api-design-patterns-notes.md](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md), [building-api-product-notes.md](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/building-api-product-notes.md).

---

## PHẦN 1: TỔNG HỢP & LÝ THUYẾT MỞ RỘNG CHUYÊN SÂU

### 1. Bản Chất 6 Ràng Buộc Kiến Trúc REST (Roy Fielding 2000)

Kiến trúc Web năm 2000 đã có ~17 triệu website phục vụ ~300 triệu người dùng. Giao thức HTTP/1.1 (RFC 2616, 1999) có khả năng chịu tải rất cao nhưng thiếu phương pháp chuẩn hóa thiết kế API. Luận án tiến sĩ của Roy Fielding (2000, §5) đã định hình phong cách kiến trúc **REST** gồm 6 ràng buộc (5 bắt buộc + 1 tùy chọn):

```
+-----------------------------------------------------------------------+
|                       6 RÀNG BUỘC KIẾN TRÚC REST                     |
+-----------------------------------------------------------------------+
|  1. Client-Server        (Bắt buộc) -> Tách UI khỏi Data Storage      |
|  2. Stateless            (Bắt buộc) -> Không lưu session trên server  |
|  3. Cacheable            (Bắt buộc) -> Khai báo đệm rõ ràng           |
|  4. Uniform Interface    (Bắt buộc) -> Hợp đồng chuẩn (Sâu nhất)      |
|  5. Layered System       (Bắt buộc) -> Kiến trúc trung gian đa tầng   |
|  6. Code on Demand       (Tùy chọn) -> Server gửi mã chạy được        |
+-----------------------------------------------------------------------+
```

1. **Client-Server (Bắt buộc)**:
   - *Phát biểu gốc*: Tách biệt mối bận tâm (concerns) giữa giao diện người dùng và lưu trữ dữ liệu $\to$ Tăng tính di động (*portability*) của UI trên đa nền tảng (Web, iOS, Android, CLI) và khả năng mở rộng (*scalability*) của server.
   - *Bối cảnh lịch sử*: Trước REST (thập niên 1990), nhiều hệ thống trộn lẫn mã HTML render sẵn với session ID nằm trong hidden input field; đổi giao diện đồng nghĩa với việc đập đi viết lại toàn bộ hệ thống.
   - *Nguyên tắc*: Client và server chỉ giao tiếp qua định dạng chuẩn (URI + Representation). Server có thể thay đổi cơ sở dữ liệu (từ SQLite sang PostgreSQL/MongoDB) mà không ảnh hưởng tới client.

2. **Stateless (Bắt buộc)**:
   - *Phát biểu gốc*: Mỗi request từ client phải chứa toàn bộ thông tin cần thiết để server hiểu và xử lý; server không lưu session state giữa các request.
   - *Sai lầm*: `POST /orders` kèm `Cookie: sid=ABC123` buộc server phải tra bảng session trong memory/database để tìm `user_id` và `cart_id`.
   - *Chuẩn mực*: `POST /orders` kèm header `Authorization: Bearer <token>` và payload chứa đầy đủ thông tin giao dịch (`cart_id`, `items`).
   - *Lợi ích kiến trúc*:
     + **Scale ngang (Horizontal Scalability)**: Mọi server instance đều xử lý được request bất kỳ mà không cần sticky session; Load Balancer có thể round-robin tự do.
     + **Khả năng quan sát (Observability)**: Mỗi request là một sự kiện độc lập; log, audit, và debug đều mang tính cục bộ và chứa đủ ngữ cảnh.
     + **Tái sử dụng Cache**: Gateway/Proxy có thể serve lại response cũ một cách chính xác.
   - *Lưu ý quan trọng*: Stateless nói về **request**. Server vẫn lưu trạng thái dữ liệu (Resource State) trong Database, Cache, Audit Log; chúng chỉ không được ảnh hưởng đến việc phân tích cú pháp của request hiện tại.

3. **Cacheable (Bắt buộc)**:
   - Response phải tự khai báo khả năng lưu đệm (`cacheable` hoặc `not cacheable`).
   - Giúp giảm tải cho server gốc và giảm độ trễ (latency) cho mạng Internet.

4. **Uniform Interface (Bắt buộc — Trọng tâm cốt lõi)**:
   - Là ràng buộc sâu nhất phân biệt REST với RPC. Bao gồm **4 ràng buộc con**:
     + **A. Identification of Resources**: Tài nguyên được định danh ổn định bằng URI danh từ số nhiều (Ví dụ: `/books/42`, `/orders`), không dùng động từ thao tác.
     + **B. Manipulation through Representations**: Client thao tác dữ liệu thông qua biểu diễn (JSON, XML), không can thiệp trực tiếp vào cấu trúc lưu trữ nội bộ của server.
     + **C. Self-descriptive Messages**: Thông điệp tự mang đầy đủ chỉ dẫn về kiểu dữ liệu (`Content-Type`), mã kết quả (`Status Code`), bộ đệm (`Cache-Control`) để bất kỳ client nào cũng tự giải mã được.
     + **D. HATEOAS (Hypermedia as the Engine of Application State)**: Phản hồi chứa các siêu liên kết (`_links`) dẫn tới các trạng thái/hành động tiếp theo, biến server thành nguồn duy nhất dẫn dắt trạng thái ứng dụng.

5. **Layered System (Bắt buộc)**:
   - Client không thể biết nó đang kết nối trực tiếp với máy chủ gốc (Origin Server) hay một thành phần trung gian (API Gateway, Load Balancer, Reverse Proxy, CDN).
   - Mỗi lớp chỉ biết đến lớp kề nó, cho phép bổ sung bảo mật, caching và rate-limiting độc lập.

6. **Code on Demand (Tùy chọn duy nhất)**:
   - Server có thể gửi mã nguồn thực thi (JavaScript, Java Applet) về cho client chạy trực tiếp.
   - *Đánh đổi*: Làm giảm tính minh bạch (visibility) và khả năng lưu đệm của mạng trung gian. Trong backend REST API hiện đại (chỉ trả JSON), ràng buộc này hầu như luôn được bỏ qua.

---

### 2. Giải Đáp Trực Tiếp Vấn Đề Cache Với Dữ Liệu Nhạy Cảm (`note.txt`)

> *Ghi chú lớp học đặt câu hỏi*: **"Hiểu rõ cơ chế cache với các trường thông tin nhạy cảm?"**

Khi xử lý các tài nguyên mang tính định danh cá nhân hoặc nhạy cảm (như `/users/me`, `/users/me/orders`, `/accounts/balance`), việc cấu hình sai Cache-Control sẽ dẫn đến thảm họa rò rỉ dữ liệu giữa các người dùng qua Shared Cache (CDN/Proxy):

```
                   +------------------------+
                   |     SHARED CACHE       |
                   |   (CDN / ISP Proxy)    |
                   +-----------+------------+
                               |
               NGUY CƠ LỘ DỮ LIỆU NẾU LÀ "PUBLIC"
                               |
            +------------------+------------------+
            |                                     |
+-----------v------------+            +-----------v------------+
|  User A (Đăng nhập)   |            |  User B (Người lạ)     |
| Nhận thông tin của A   |            | Vô tình nhận dữ liệu A |
+------------------------+            +------------------------+
```

#### Các nguyên tắc kiểm soát Cache cho dữ liệu nhạy cảm:

1. **Chỉ thị `private` vs `public`**:
   - `public`: Cho phép **mọi cấp bộ đệm** (trình duyệt, CDN Cloudflare, Gateway Proxy) lưu trữ bản sao response. Tuyệt đối **không dùng** cho dữ liệu cá nhân.
   - `private`: **Chỉ duy nhất trình duyệt của người dùng cuối** (User-Agent Cache) được phép lưu trữ bản sao; cấm tất cả các Shared Cache/CDN trung gian lưu trữ.
2. **Chỉ thị `no-store` vs `no-cache`**:
   - `no-store`: Lệnh nghiêm ngặt nhất. Cấm mọi hệ thống lưu trữ bất kỳ phần nào của request/response xuống ổ cứng hoặc bộ nhớ đệm (bắt buộc dùng cho thông tin thẻ tín dụng, mật khẩu, token ngân hàng).
   - `no-cache`: Vẫn cho phép lưu trữ bản copy, nhưng **bắt buộc phải gửi request hỏi lại server** (Revalidate qua `ETag`/`If-None-Match`) trước khi tái sử dụng cho client.
3. **Chỉ thị `must-revalidate`**:
   - Ngăn không cho cache server sử dụng lại dữ liệu đã hết hạn (stale data) khi bị mất kết nối tới server gốc.
4. **Header `Vary: Authorization, Cookie`**:
   - Nếu bắt buộc phải cache ở tầng trung gian cho từng người dùng, header `Vary` yêu cầu Cache Server phải băm (hash) cả header `Authorization` vào Cache Key. Nhờ đó, người dùng B sẽ không bao giờ nhận được bản cache của người dùng A dù cùng truy cập URI `/users/me`.

**Cấu hình khuyến nghị trong thực tế**:
- Endpoint công cộng (Danh mục sách): `Cache-Control: public, max-age=300`
- Endpoint thông tin cá nhân: `Cache-Control: private, no-cache, must-revalidate`
- Endpoint giao dịch tài chính / thanh toán: `Cache-Control: private, no-store`

---

### 3. Mô Hình Trưởng Thành Richardson (RMM) & Phê Bình Của Roy Fielding

Leonard Richardson chia quá trình phát triển của một Web API hướng tới REST thành 4 cấp bậc:

```
[Level 3] Hypermedia Controls (HATEOAS: _links định hướng hành động)
    ^
[Level 2] HTTP Verbs & Status Codes (URI danh từ + GET/POST/PUT/DELETE + 2xx/4xx/5xx)
    ^
[Level 1] Resources (Mỗi tài nguyên có 1 URI riêng, nhưng chưa dùng đúng HTTP verbs)
    ^
[Level 0] The Swamp of POX (1 URI duy nhất, 1 method POST duy nhất - SOAP, XML-RPC)
```

- **Level 0 (The Swamp of POX)**: Dùng HTTP như một đường ống truyền tin mù quáng (ví dụ: `POST /api` với RPC payload dạng XML/JSON).
- **Level 1 (Resources)**: Bắt đầu chia tách URI cho từng thực thể (`/books`, `/authors`), nhưng vẫn dùng chung một method (ví dụ `POST /books/1/delete`).
- **Level 2 (HTTP Verbs & Status Codes)**: Sử dụng chuẩn xác các động từ HTTP và mã trạng thái (`GET /books/1`, `DELETE /books/1` $\to$ `204`). **Đây là mục tiêu thực tế của 90% REST API trong công nghiệp.**
- **Level 3 (Hypermedia Controls - HATEOAS)**: Phản hồi cung cấp đầy đủ liên kết điều hướng ứng dụng tự động.

#### Phê bình của Roy Fielding (2010):
> Roy Fielding khẳng định: **"REST không phải là một mô hình cấp bậc (hierarchy)."**  
> REST là một tập hợp các ràng buộc rời rạc được thiết kế đồng bộ. Một API thỏa mãn tất cả các ràng buộc khác (Stateless, Cacheable, Client-Server) nhưng chưa hỗ trợ HATEOAS thì nên gọi là **"Resource-Oriented API"** hoặc **"RESTful-ish"**, thay vì coi nó là "bậc 2 chưa hoàn thiện". Một API chỉ thêm hypermedia mà vi phạm tính Stateless thì vẫn là một thiết kế tồi.

---

### 4. Bốn Ràng Buộc Con Của Uniform Interface & Chuẩn Hóa URI

#### A. Phân biệt Tài nguyên (Resource) và Biểu diễn (Representation)
- **Tài nguyên (Resource)**: Là khái niệm trừu tượng (Abstract Concept), là bất kỳ thực thể thông tin nào có thể đặt tên (Cuốn sách "Clean Code", Người dùng Nguyễn Văn A).
- **Biểu diễn (Representation)**: Là dữ liệu cụ thể (Concrete Serialization) thể hiện trạng thái của tài nguyên đó tại một thời điểm (JSON payload, XML payload, HTML page, CSV export).
- Cùng một URI `/books/42` có thể trả về các representation khác nhau tùy thuộc vào header đàm phán nội dung `Accept` từ phía client.

#### B. Quy tắc đặt tên URI (JJ Geewax Ch. 3, 5, 6 & Bruno Pedro Ch. 2, 8)
1. **Danh từ số nhiều, tuyệt đối không chứa động từ**:
   - Đúng: `GET /books`, `POST /orders`, `DELETE /sessions/sess_123`
   - Sai (RPC-hóa): `GET /getBook?id=42`, `POST /createOrder`, `POST /deleteUser`
2. **Phân cấp tự nhiên biểu diễn quan hệ Cha - Con (Sub-resources)**:
   - `GET /books/42/reviews`: Lấy danh sách đánh giá của cuốn sách số 42.
   - `POST /books/42/reviews`: Tạo mới đánh giá cho cuốn sách 42.
3. **Quy chuẩn ký tự**:
   - Sử dụng chữ thường (`lowercase`) và dấu gạch nối (`kebab-case`) cho URI path segments: `/flight-bookings`.
   - Tránh gạch dưới (`snake_case`) hoặc chữ hoa lạc đà (`camelCase`) trên URI.
4. **Không đưa phần mở rộng tệp tin vào URI**:
   - Sai: `GET /books/42.json`, `GET /reports/2026.pdf`
   - Đúng: `GET /books/42` kết hợp `Accept: application/json`
5. **Định danh duy nhất toàn cục (Resource Identification - Geewax Ch. 6)**:
   - Tránh phơi bày số nguyên tự tăng (Auto-increment integer ID: `1, 2, 3...`) ra public API vì dễ bị tấn công duyệt tuần tự (IDOR - Insecure Direct Object Reference).
   - Khuyến nghị dùng UUIDv4 hoặc chuỗi định danh có tiền tố: `ord_91f3a2b4c5d6`.

---

### 5. So Sánh Bản Chất HTTP Methods: Idempotency & Safety

Bảng đối chiếu chuẩn theo **RFC 9110 §9.2**:

| Method | Vai trò chính | Safe (An toàn) | Idempotent (Bất biến) | Body Request | Body Response | Status Code thành công |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **GET** | Đọc dữ liệu tài nguyên | **Có** | **Có** | Không | Bắt buộc | `200 OK` |
| **HEAD** | Lấy headers giống GET | **Có** | **Có** | Không | Không | `200 OK` |
| **OPTIONS** | Thăm dò khả năng endpoint | **Có** | **Có** | Tùy chọn | Tùy chọn | `200 OK` (kèm `Allow`) |
| **POST** | Tạo mới tài nguyên / Xử lý generic | Không | Không | Bắt buộc | Khuyến nghị | `201 Created` / `200 OK` |
| **PUT** | Thay thế toàn bộ tài nguyên | Không | **Có** | Bắt buộc | Tùy chọn | `200 OK` / `204 No Content` |
| **PATCH** | Cập nhật một phần tài nguyên | Không | **Không\*** | Bắt buộc | Khuyến nghị | `200 OK` |
| **DELETE** | Xóa tài nguyên | Không | **Có** | Không khuyến nghị | Tùy chọn | `204 No Content` / `200 OK` |

#### Phân tích sâu:
1. **Safe (RFC 9110 §9.2.1)**: Thao tác chỉ đọc, việc gọi request không làm thay đổi trạng thái tài nguyên trên server (không ghi DB, không trigger state chuyển tiếp). Trình duyệt có thể tự do pre-fetch, web crawler có thể quét tự do.
2. **Idempotent (RFC 9110 §9.2.2)**: Gọi 1 lần hay $N$ lần liên tiếp với cùng tham số đều để lại trạng thái hệ thống y hệt nhau.
   - `DELETE /books/42`: Lần 1 trả `204` (đã xóa), lần 2 trả `404` (không còn tồn tại). Kết quả mã trạng thái HTTP có thể khác nhau, nhưng **trạng thái server không đổi: tài nguyên sách 42 không còn tồn tại**. Do đó DELETE là idempotent!
3. **Vì sao PATCH không mặc định Idempotent?**
   - Nếu PATCH dùng thao tác tăng giá trị: `{"op": "increment", "field": "view_count", "value": 1}` $\to$ Mỗi lần gọi view count lại tăng 1 $\to$ Không idempotent!
   - Hai chuẩn cập nhật từng phần:
     + **JSON Merge Patch (RFC 7396)**: Gửi bản ghi JSON chứa các trường cần sửa. Nếu chỉ gán đè giá trị cố định thì mang tính idempotent.
     + **JSON Patch (RFC 6902)**: Gửi danh sách các lệnh (`add`, `remove`, `replace`, `move`, `copy`, `test`).
4. **Kỹ thuật Idempotency Key cho POST (Stripe Pattern)**:
   - Để biến thao tác POST thanh toán rủi ro thành an toàn khi rớt mạng, client gửi kèm header `Idempotency-Key: <UUID>`.
   - Server lưu kết quả của key này trong 24 giờ. Nếu client retry cùng key, server trả lại response cũ thay vì charge tiền hai lần.

---

### 6. Ngữ Nghĩa Mã Trạng Thái HTTP (Status Codes Semantics)

#### Lớp 2xx — Thành công
- `200 OK`: Thành công với payload trả về trong body (GET, PUT, PATCH).
- `201 Created`: Tạo mới tài nguyên thành công (POST, PUT tạo mới). **Bắt buộc/Khuyến nghị kèm header `Location: /resources/{id}`**.
- `202 Accepted`: Đã tiếp nhận yêu cầu nhưng chưa hoàn thành (tác vụ bất đồng bộ / message queue).
- `204 No Content`: Xử lý thành công nhưng không có body trả về (DELETE, đôi khi là PUT).

#### Lớp 3xx — Chuyển tiếp
- `301 Moved Permanently`: Tài nguyên đã chuyển vĩnh viễn sang URI mới. Trình duyệt tự động cache URL mới. **Không nên dùng cho POST vì nhiều client cũ sẽ tự ý đổi method sang GET**.
- `308 Permanent Redirect`: Giống 301 nhưng **nghiêm ngặt bảo toàn method** (POST vẫn giữ nguyên POST).
- `302 Found`: Chuyển tiếp tạm thời cổ điển. RFC 9110 khuyến cáo tránh dùng vì hành vi không nhất quán giữa các client.
- `307 Temporary Redirect`: Chuyển tiếp tạm thời chuẩn hóa, **đảm bảo giữ nguyên HTTP method gốc**.
- `304 Not Modified`: Phục vụ Conditional Requests (`ETag` hoặc `If-Modified-Since`). Báo cho client dùng bản cache cục bộ, không gửi lại body.

#### Lớp 4xx — Lỗi từ phía Client
- `400 Bad Request`: Request malformed — sai cú pháp JSON, sai kiểu dữ liệu query string trên URL.
- `401 Unauthorized`: Bản chất là **Unauthenticated** (chưa cung cấp token xác thực hoặc token không hợp lệ). Kèm header `WWW-Authenticate`.
- `403 Forbidden`: Đã xác thực danh tính thành công nhưng **không có quyền (Forbidden / Unauthorized role)** truy cập tài nguyên.
- `404 Not Found`: Tài nguyên không tồn tại, hoặc server cố tình trả về để ẩn giấu sự tồn tại của tài nguyên vì lý do an ninh.
- `409 Conflict`: Xung đột trạng thái tài nguyên (hai giao dịch cùng cập nhật một phiên bản dữ liệu).
- `415 Unsupported Media Type`: Client gửi dữ liệu với định dạng không được hỗ trợ (ví dụ server chỉ nhận `application/json` nhưng client gửi `text/plain`).
- `422 Unprocessable Entity`: Cú pháp JSON hoàn toàn hợp lệ nhưng vi phạm quy tắc nghiệp vụ (ví dụ: `age < 0`, thiếu trường bắt buộc `title`, email sai cấu trúc domain).
- `429 Too Many Requests`: Vượt quá hạn mức tần suất (Rate Limiting). Kèm header `Retry-After: <seconds>`.

#### Lớp 5xx — Lỗi từ phía Server
- `500 Internal Server Error`: Lỗi máy chủ không mong đợi. Nguyên tắc bảo mật: **Tuyệt đối không để lộ Stack Trace cho client**, chỉ log ở server và trả về mã lỗi tổng quát.
- `501 Not Implemented`: Server không hỗ trợ chức năng/method này.
- `502 Bad Gateway`: Máy chủ đóng vai trò Gateway/Proxy nhận được phản hồi không hợp lệ từ máy chủ cấp trên (Upstream Server - ví dụ Nginx không kết nối được tới Gunicorn/Flask).
- `503 Service Unavailable`: Hệ thống tạm thời quá tải hoặc đang bảo trì. Luôn kèm header `Retry-After`.
- `504 Gateway Timeout`: Máy chủ Gateway chờ quá lâu mà không nhận được phản hồi từ upstream server (503 = chủ động từ chối; 504 = chờ quá thời gian timeout).

---

### 7. Phản Biện Mã Nguồn Thực Hành (`weeks/week-02/practice/app.py`)

Dựa trên lịch sử commit (`06533dc`, `16ac830`, `1459a9c`), các điểm yếu kiến trúc trong mã nguồn thực hành cần được lưu ý:

1. **Lỗ hổng bảo mật ghi đè ID trong `PATCH`**:
   ```python
   # Trong practice/app.py (Commit 16ac830, dòng 86):
   BOOKS[i].update(p)
   ```
   *Rủi ro*: Nếu client gửi payload `{"id": 999, "price": 50}`, cuốn sách sẽ bị thay đổi ID trong mảng. Trong RESTful API, định danh tài nguyên là bất biến.  
   *Sửa chuẩn*: Whitelist danh sách các trường được phép sửa như trong Slide 24:
   ```python
   for k in ["title", "author", "isbn", "price"]:
       if k in p:
           BOOKS[i][k] = p[k]
   ```
2. **Sai lệch mã trạng thái tại tầng kiểm soát tham số Query**:
   ```python
   # Trong practice/app.py (Commit 1459a9c, dòng 107):
   except ValueError:
       return jsonify(error = "page and size must be integers"), 422
   ```
   *Rủi ro*: Tham số trên Query String (`?page=abc`) bị sai kiểu dữ liệu là lỗi cú pháp yêu cầu (Malformed Request Syntax), thuộc về `400 Bad Request`, không phải lỗi ngữ nghĩa nghiệp vụ payload (`422`).
3. **Nguy cơ Race Condition từ biến đếm In-Memory**:
   - Việc dùng `_next` tự tăng và danh sách Python `BOOKS = []` không an toàn khi chạy nhiều worker process (ví dụ Gunicorn workers). Khi hai request tạo sách đến đồng thời, cả hai có thể nhận cùng một ID. Cần áp dụng cơ sở dữ liệu (SQLite) với Transaction và ID duy nhất (UUIDv4).

---

## PHẦN 2: HỆ THỐNG CÂU HỎI ĐÀO SÂU & TỰ ĐÁNH GIÁ (SOCRATIC QUESTIONS)

Bộ câu hỏi được thiết kế theo cấp độ tư duy từ nắm bắt khái niệm đến phân tích, phản biện và thiết kế hệ thống thực tế.

### Nhóm 1: Bản Chất Kiến Trúc REST & 6 Ràng Buộc
1. **Câu hỏi 1 (Khái niệm)**: Tại sao Roy Fielding lại khẳng định *“REST không phải là JSON qua HTTP”*? Một API trả về dữ liệu định dạng XML qua HTTP có thể được coi là RESTful không?
   - *Gợi ý suy ngẫm*: Hãy nhớ lại ràng buộc Uniform Interface (phân biệt giữa Resource và Representation). JSON chỉ là một phương tiện tuần tự hóa dữ liệu (Serialization Format).
2. **Câu hỏi 2 (Stateless)**: Trong kiến trúc REST, việc lưu trữ Access Token trong Cookie có vi phạm ràng buộc Stateless không? Tại sao việc lưu trữ Session ID trên máy chủ lại vi phạm Stateless, nhưng việc gửi JWT Bearer Token trong mỗi request lại được chấp nhận?
   - *Gợi ý suy ngẫm*: Xem lại Slide 7 — server có phải tra cứu "bảng trạng thái phiên làm việc" (Session Store) để hiểu ý nghĩa của request hay bản thân token đã mang đủ thông tin xác thực?
3. **Câu hỏi 3 (Layered System)**: Case study Shopee Việt Nam tách riêng API Gateway ra khỏi backend chính (năm 2020) để chịu tải 2 tỷ request/ngày minh họa cho ràng buộc kiến trúc nào của REST? Lợi ích cụ thể của việc phân lớp này đối với tính sẵn sàng và khả năng scale của hệ thống là gì?
   - *Gợi ý suy ngẫm*: Xem lại Slide 13 và nguyên lý các lớp trung gian xử lý Rate Limiting, Auth, Caching độc lập với Origin Server.

### Nhóm 2: Ngữ Nghĩa HTTP & Xử Lý Tình Huống Biên
4. **Câu hỏi 4 (Safety vs Idempotency)**: Tại sao phương thức `DELETE` không an toàn (`Safe = False`) nhưng lại có tính lũy kế (`Idempotent = True`)? Nếu lần gọi DELETE thứ nhất trả về `204 No Content` và lần gọi thứ hai trả về `404 Not Found`, thì thao tác này có còn được coi là idempotent không? Tại sao?
   - *Gợi ý suy ngẫm*: Đối chiếu định nghĩa RFC 9110 §9.2.2 về trạng thái tài nguyên trên máy chủ (Resource State on Server) thay vì mã trạng thái HTTP trả về trên đường truyền.
5. **Câu hỏi 5 (PUT vs PATCH)**: Giả sử một tài nguyên người dùng có 10 trường dữ liệu. Client chỉ muốn đổi mật khẩu. Nếu gửi bằng `PUT /users/1` với body `{"password": "new_secret"}`, điều gì sẽ xảy ra với 9 trường còn lại theo đúng chuẩn REST? Phương thức nào phù hợp hơn trong tình huống này và tại sao?
   - *Gợi ý suy ngẫm*: Slide 16 và Slide 24 nhấn mạnh sự khác biệt sống còn giữa *Full Replacement* của PUT và *Partial Update* của PATCH.
6. **Câu hỏi 6 (Redirect Semantics)**: Tại sao khi muốn chuyển hướng một request `POST /orders` sang phiên bản API mới, chúng ta bắt buộc phải sử dụng mã `307 Temporary Redirect` hoặc `308 Permanent Redirect` thay vì dùng `301` hoặc `302`?
   - *Gợi ý suy ngẫm*: Xem Slide 18 và RFC 9110 về hiện tượng các HTTP client tự động chuyển đổi phương thức từ POST sang GET khi gặp mã 301/302.

### Nhóm 3: Caching, Bảo Mật & Concurrency Control
7. **Câu hỏi 7 (Bảo vệ dữ liệu nhạy cảm)**: Để ngăn chặn tuyệt đối nguy cơ rò rỉ dữ liệu cá nhân trên các máy chủ Proxy/CDN trung gian đối với endpoint `GET /users/me/profile`, lập trình viên backend cần thiết lập các giá trị nào trong header `Cache-Control`?
   - *Gợi ý suy ngẫm*: Phân tích sự kết hợp giữa `private`, `no-store` và header `Vary: Authorization` (Slide 8, 14 và Phần 1.2 của tài liệu này).
8. **Câu hỏi 8 (Optimistic Concurrency Control)**: Trong bài tập về nhà số 3 (Slide 26), cơ chế Conditional Request với `ETag` hoạt động như thế nào? Làm thế nào để phối hợp `ETag` với header `If-Match` để giải quyết triệt để bài toán hai người dùng cùng cập nhật đè dữ liệu (Lost Update Problem)?
   - *Gợi ý suy ngẫm*: Tham chiếu thuật ngữ `Resource Revisions & Concurrency Control` trong [glossary-soa.md](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/glossary-soa.md).

### Nhóm 4: HATEOAS, RMM & Ứng Dụng Trong Hệ Thống Hiện Đại
9. **Câu hỏi 9 (HATEOAS trong thực tế)**: Tại sao mặc dù là ràng buộc cấp cao nhất trong Richardson Maturity Model (Level 3), HATEOAS lại bị hơn 90% các hệ thống REST API công nghiệp (kể cả GitHub, Stripe) bỏ qua hoặc chỉ triển khai một phần?
   - *Gợi ý suy ngẫm*: Đánh giá chi phí băng thông, độ phức tạp khi lập trình client-side, và sự phổ biến của các tài liệu đặc tả hợp đồng máy-đọc-được như OpenAPI/Swagger.
10. **Câu hỏi 10 (LLM Agent Tool Calling)**: Tại sao các hệ thống Agentic AI hiện đại (OpenAI Assistants, Gemini Tool Use) lại phụ thuộc sống còn vào tính chuẩn hóa của HTTP Status Codes (như `429`, `422`, `204`) để vận hành Reasoning Loop tự chủ? Điều gì sẽ xảy ra nếu một API luôn trả về `200 OK` nhưng nhúng mã lỗi `{"status": "error", "code": 401}` bên trong body?
    - *Gợi ý suy ngẫm*: Đối chiếu mục 4 trong [industry-mapping.md](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/industry-mapping.md) — khi API trả 200 kèm error body, LLM Agent sẽ bị đánh lừa rằng công cụ đã thực thi thành công, dẫn đến ảo giác (Hallucination) và sai lệch trong chuỗi suy luận logic tiếp theo.
