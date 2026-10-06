# Tổng Hợp Kiến Thức Tuần 03: API Design Principles & Best Practices

## 1. Bản Chất Thiết Kế API & Trải Nghiệm Lập Trình Viên (Developer Experience)

Thiết kế API là thiết kế **hợp đồng giao tiếp (Service Contract)** giữa bên cung cấp và bên sử dụng dịch vụ. API chạy đúng nghiệp vụ mới đáp ứng yêu cầu về chức năng; một API tốt còn phải **nhất quán, dễ đoán định và dễ sử dụng**. Khi đã công bố, thay đổi URI, kiểu dữ liệu hoặc cấu trúc phản hồi có thể buộc tất cả client phải sửa mã nguồn.

- **Consistency (Tính nhất quán)**: Cùng một quy tắc được áp dụng xuyên suốt các endpoint: tên tài nguyên, kiểu dữ liệu, cấu trúc response, mã trạng thái và định dạng lỗi.
  - *Ví dụ*: Nếu `/posts` dùng `limit`, `cursor` và `pagination.next_cursor`, `/comments` nên sử dụng cùng quy ước thay vì chuyển sang `pageSize` và `nextPageToken` mà không có lý do.
- **Predictability (Khả năng đoán định)**: Biết cách dùng một tài nguyên thì có thể suy ra cách dùng tài nguyên khác. Từ `GET /posts/{id}`, client có thể dự đoán `GET /comments/{id}` và `DELETE /comments/{id}`.
- **Simplicity (Tính tối giản)**: Mỗi endpoint có ý nghĩa rõ ràng; không tạo nhiều cách gọi khác nhau cho cùng một thao tác. Dùng `GET /posts?status=published` thay vì thêm `/getPublishedPosts`.
- **Usability (Khả năng sử dụng)**: Tên dễ hiểu, mặc định hợp lý, ví dụ request/response rõ ràng; thông báo lỗi giúp người dùng biết phải sửa gì.
- **Compatibility (Tính tương thích)**: Thiết kế cần tính đến client đang hoạt động. Đổi `/userList` thành `/users` sau khi công bố vẫn là **Breaking Change**, dù URI mới dễ đọc hơn.

*Liên hệ hai giáo trình*: **JJ Geewax (Ch. 7)** chuẩn hóa các thao tác tài nguyên để giảm những quyết định tùy hứng; **Bruno Pedro (Ch. 2, 7)** đặt nhà phát triển vào vai trò người dùng và yêu cầu kiểm chứng thiết kế trước khi hiện thực hóa.

```
                THÁP NHU CẦU API (BRUNO PEDRO, CH. 2)

                  Delight     : SDK, ví dụ, onboarding thuận tiện
                Usability     : Dễ học, nhất quán, lỗi dễ xử lý
              Reliability     : Hoạt động ổn định, hành vi đáng tin cậy
            Functionality     : Giải quyết đúng nhu cầu nghiệp vụ
```

- *Ý nghĩa*: Tài liệu đẹp không bù được một API thường xuyên lỗi; API đầy đủ chức năng nhưng khó tích hợp cũng tạo ra chi phí cho người sử dụng.
- *Kiểm chứng thiết kế (Design Validation)*: Viết hợp đồng và ví dụ trước, cho frontend/mobile thử các luồng gọi qua mock, ghi nhận điểm khó hiểu rồi điều chỉnh. Đây là nền tảng cho OpenAPI ở tuần 4, không cần chờ viết xong backend mới review.

---

## 2. Thiết Kế Hướng Tài Nguyên & Quy Ước Đặt Tên (Resource-Oriented Design)

**URL định danh tài nguyên, HTTP method diễn đạt thao tác**. Tài nguyên xuất phát từ miền nghiệp vụ (User, Post, Comment, Order), không phải tên hàm trong controller hoặc tên bảng trong database.

### Ba Dạng Endpoint Cơ Bản:

1. **Collection (Tập hợp)**: `/posts` — `GET` lấy danh sách, `POST` tạo một bài viết mới.
2. **Item (Một phần tử)**: `/posts/{post_id}` — `GET` đọc chi tiết, `PUT/PATCH` cập nhật, `DELETE` xóa.
3. **Sub-resource (Tài nguyên con)**: `/posts/{post_id}/comments` — biểu diễn các bình luận thuộc một bài viết.

- *Phân biệt Item vs Singleton*: `/users/{id}` là một phần tử trong collection. Singleton là tài nguyên duy nhất trong một ngữ cảnh, chẳng hạn `/users/{id}/settings` hoặc `/me`; không phải cứ endpoint trả về một object thì đó là mẫu Singleton.
- *Phân cấp hợp lý*: Nesting thể hiện quan hệ miền nghiệp vụ, không sao chép toàn bộ chuỗi khóa ngoại của database. Theo khuyến nghị trong slide, nên giữ khoảng 2-3 cấp tài nguyên; nếu quá sâu, cân nhắc `GET /tasks?project_id=...` thay cho `/orgs/{o}/teams/{t}/projects/{p}/tasks`.

### Quy Tắc Naming Của Buổi 3:

- **Lowercase** cho các segment tên tài nguyên: `/users`, không phải `/Users`. ID vẫn được giữ nguyên theo hợp đồng định danh.
- **Danh từ số nhiều** cho collection: `/posts`, `/orders`, `/products`.
- **kebab-case** cho tên nhiều từ trong path: `/shopping-cart-items`.
- **snake_case** cho query parameters trong quy ước bài học: `created_after`, `customer_id`, `per_page`. Tên trường JSON cũng cần chọn một quy ước và áp dụng nhất quán; ví dụ Blog API hiện dùng `author_id`.
- **Không lặp động từ CRUD** trong URI: `POST /orders` thay cho `POST /createOrder`; `DELETE /users/42` thay cho `POST /users/42/deleteUser`.
- **Không gắn `.json` vào path** trong thiết kế đang áp dụng; biểu diễn dữ liệu được xác định qua `Accept` và `Content-Type`.
- **Path cho định danh, query cho truy vấn collection**: `/products/42` lấy một sản phẩm; `/products?category=phones` lọc danh sách sản phẩm.

*Lưu ý*: Các lựa chọn về case, số nhiều và tên query là **quy ước thiết kế**, không phải tất cả đều là ràng buộc bắt buộc của REST. Quan trọng là hợp đồng rõ ràng và nhất quán.

### Ví Dụ Blog API (Lab 1):

```text
/api/v1
├── /users                         GET, POST
│   └── /{user_id}                  GET, PATCH, DELETE
│       ├── /posts                 GET
│       └── /following             GET, POST
├── /posts                         GET, POST
│   └── /{post_id}                  GET, PUT/PATCH, DELETE
│       └── /comments              GET, POST
├── /comments/{comment_id}         GET, PATCH, DELETE
└── /tags                          GET, POST
    └── /{tag_id}                   GET, PATCH, DELETE
```

- *Case Study GitHub trong slide*: `/repos/{owner}/{repo}/issues/{number}` sử dụng định danh tự nhiên nhiều phần; `/user` là người dùng đang xác thực nên số ít có ý nghĩa. Không nên áp dụng máy móc quy tắc số nhiều cho mọi tài nguyên.
- *Ngoại lệ nghiệp vụ (JJ Geewax Ch. 9, mở rộng)*: Các hành động như xuất bản hoặc hủy đơn hàng có thể cần custom method, ví dụ `POST /posts/{id}:publish`, hoặc được mô hình hóa thành tài nguyên phù hợp. Tránh biến mọi thao tác thành RPC, nhưng cũng không ép mọi workflow vào CRUD.
- *Định danh và bảo mật*: Public ID dạng UUID giúp hạn chế đoán ID tuần tự; **không tự ngăn IDOR/BOLA**. Server vẫn phải kiểm tra người gọi có quyền truy cập đúng tài nguyên đó hay không.

---

## 3. Bộ 5 Phương Thức Chuẩn & Hợp Đồng Request/Response (Standard Methods)

**JJ Geewax (Ch. 7)** phân biệt **5 phương thức chuẩn: List, Get, Create, Update, Delete**. CRUD có 4 nhóm hành động nhưng thao tác Read được tách thành List và Get; PUT/PATCH là hai cách biểu diễn Update trên HTTP.

1. **List — `GET /posts`**:
   - Input: Tham số phân trang, lọc, sắp xếp, lựa chọn trường.
   - Output: `200 OK`, danh sách và metadata phân trang theo hợp đồng.
   - Không có kết quả vẫn trả `200` với `data: []`, không phải `404`.
2. **Get — `GET /posts/{post_id}`**:
   - Input: Định danh tài nguyên.
   - Output: `200 OK` với một object; `404 Not Found` khi không tìm thấy hoặc không công khai sự tồn tại.
3. **Create — `POST /posts`**:
   - Input: Các trường client được phép cung cấp, chẳng hạn `title`, `content`; trường server quản lý như ID không được tùy tiện ghi đè.
   - Output: `201 Created`, nên kèm `Location: /api/v1/posts/{id}` và biểu diễn tài nguyên vừa tạo.
4. **Update — `PUT/PATCH /posts/{post_id}`**:
   - `PUT`: Thay thế biểu diễn theo schema cập nhật toàn phần; phải quy định rõ trường nào client quản lý và ý nghĩa của trường bị bỏ qua.
   - `PATCH`: Áp dụng cập nhật từng phần theo định dạng patch đã công bố. Ví dụ thay `title` nhưng giữ các trường khác.
   - Output: `200 OK` khi trả biểu diễn sau cập nhật, hoặc `204 No Content` nếu hợp đồng không trả body. PUT cũng có thể trả `201` nếu API cho phép tạo tài nguyên tại URI chưa tồn tại.
5. **Delete — `DELETE /posts/{post_id}`**:
   - Output: `204 No Content` khi xóa thành công và không trả body; có thể chọn `200` nếu cần trả kết quả theo hợp đồng.
   - Xóa lại có thể trả `404` hoặc tiếp tục `204`, nhưng phải thống nhất và ghi rõ hành vi.

### Safety, Idempotency & Retry:

- **Safe**: Client chỉ yêu cầu đọc dữ liệu; GET/HEAD/OPTIONS không được thiết kế để gây thay đổi nghiệp vụ. Việc server ghi access log không làm GET mất tính safe. Không dùng `GET /checkout` để tạo đơn hàng.
- **Idempotent**: Hiệu ứng dự kiến của nhiều request giống nhau tương đương một request; **không yêu cầu response giống hệt nhau**. DELETE lần đầu trả `204`, lần sau `404` vẫn idempotent vì tài nguyên đều đã bị xóa.
- **PUT idempotent**, còn **POST/PATCH không được mặc định coi là idempotent**. PATCH đặt `title` về cùng một giá trị có thể idempotent; PATCH tăng bộ đếm thì không.
- **Idempotency-Key (mở rộng từ Ch. 26)**: Với POST tạo giao dịch cần retry an toàn, client dùng lại cùng key cho cùng một thao tác; server kiểm tra và lưu kết quả để không thực thi nghiệp vụ hai lần. Thời gian lưu, phạm vi key và xử lý cùng key nhưng khác payload phải được định nghĩa trong hợp đồng.
- *Retry sau timeout*: Timeout không chứng minh server chưa xử lý request. Chỉ retry khi ngữ nghĩa thao tác hoặc cơ chế chống trùng cho phép; dùng backoff và giới hạn số lần thử. Không phải mọi lỗi 5xx đều có thể retry mù quáng.

### Cấu Trúc Phản Hồi Nhất Quán:

```json
{
  "data": [
    {"id": 42, "title": "API Design", "status": "published"}
  ],
  "pagination": {
    "limit": 5,
    "has_more": true,
    "next_cursor": "<opaque-token>"
  }
}
```

- Đây là một **quy ước response của Blog API**, không phải envelope bắt buộc của REST. Có API dùng mảng trực tiếp và header `Link`; có API dùng trường `nextPageToken`.
- Khi hết dữ liệu: `has_more: false`, `next_cursor: null`. Không ép client giải mã token để tự tính trang kế tiếp.
- Phải phân biệt trường không được gửi, giá trị `null` và giá trị mặc định; tránh tự suy diễn rằng `null` luôn có nghĩa là xóa ở mọi API hoặc mọi định dạng PATCH.

---

## 4. Ngữ Nghĩa Status Codes & Thiết Kế Lỗi (Problem Details)

**HTTP status code giúp client và hạ tầng hiểu kết quả; body giải thích chi tiết**. Trả `200 OK` cùng `{"success": false}` cho một request thất bại làm sai lệch monitoring và cách xử lý lỗi của client.

### Các Mã Cần Dùng Đúng Trong Tuần 3:

- **`200 OK` / `201 Created` / `204 No Content`**: Đọc hoặc xử lý thành công / tạo mới / thành công không body. `204` không được kèm JSON, kể cả `{}`.
- **`202 Accepted`**: Đã tiếp nhận nhưng chưa hoàn tất; chỉ dùng khi có xử lý bất đồng bộ và cách theo dõi kết quả.
- **`400 Bad Request`**: JSON hỏng, query/cursor sai định dạng, tham số truy vấn không hợp lệ.
- **`401 Unauthorized`**: Thiếu hoặc không có thông tin xác thực hợp lệ; phản hồi phải có `WWW-Authenticate` phù hợp.
- **`403 Forbidden`**: Server hiểu request nhưng từ chối thực hiện, thường vì không đủ quyền. Có thể dùng `404` nếu cần che giấu sự tồn tại của tài nguyên.
- **`404 Not Found` / `405 Method Not Allowed`**: Không có tài nguyên / không hỗ trợ method tại endpoint đó. `405` cần header `Allow`.
- **`409 Conflict`**: Xung đột với trạng thái tài nguyên, ví dụ email đã tồn tại hoặc chuyển trạng thái đơn hàng không hợp lệ.
- **`412 Precondition Failed`**: Điều kiện HTTP như `If-Match` không thỏa mãn. Khi ETag không khớp, đây là mã cần phân biệt với lỗi xung đột nghiệp vụ `409`. [RFC 9110 §13.1.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.1).
- **`415 Unsupported Media Type` / `422 Unprocessable Content`**: Định dạng request không được hỗ trợ / nội dung có cú pháp hợp lệ nhưng không xử lý được theo quy tắc dữ liệu hoặc nghiệp vụ. API cần thống nhất việc dùng `400` và `422` cho validation.
- **`429 Too Many Requests`**: Vượt giới hạn lưu lượng; nên cung cấp `Retry-After` để hướng dẫn client.
- **`500 Internal Server Error` / `503 Service Unavailable`**: Lỗi nội bộ bất ngờ / dịch vụ tạm không sẵn sàng. Trả thông báo trung tính, log chi tiết ở server.

### Problem Details — RFC 7807 / RFC 9457:

Slide và giáo trình dùng tên **RFC 7807**; **RFC 9457** thay thế tiêu chuẩn này từ năm 2023. Response JSON dùng `Content-Type: application/problem+json` với các trường chuẩn:

- **`type`**: URI định danh *loại lỗi*, là khóa để client phân nhánh xử lý; có thể dẫn tới tài liệu giải thích.
- **`title`**: Tóm tắt ngắn, tương đối ổn định cho loại lỗi.
- **`status`**: Mã HTTP dạng số; nếu có, phải khớp mã server trả.
- **`detail`**: Diễn giải cụ thể cho lần lỗi này, giúp biết cách sửa.
- **`instance`**: URI tham chiếu *lần phát sinh lỗi*, không nhất thiết chỉ là path endpoint.

Đây là các trường chuẩn có thể sử dụng, **RFC không bắt buộc mọi response phải có đủ cả 5 trường**; nếu thiếu `type`, mặc định là `about:blank`. Có thể thêm extension như `errors`, `trace_id`; cấu trúc extension phải được API định nghĩa. [RFC 9457 §3](https://www.rfc-editor.org/rfc/rfc9457.html#section-3).

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://api.example.com/problems/invalid-post",
  "title": "Invalid post data",
  "status": 422,
  "detail": "title không được để trống.",
  "instance": "/problems/occurrences/req_abc123",
  "errors": [{"field": "title", "code": "required"}],
  "trace_id": "req_abc123"
}
```

- **Actionable Error (Bruno Pedro Ch. 2)**: `title không được để trống` hữu ích hơn `Invalid input`. Client nên xử lý bằng `type` hoặc mã extension đã công bố, không parse câu chữ trong `detail`.
- **Error Handler tập trung (Lab 2)**: Route phát sinh exception nghiệp vụ; handler chuyển thành Problem Details. Cần thêm fallback cho `HTTPException` (404/405...) và exception chưa bắt (500), để lỗi mặc định không bị trả thành HTML.
- **Metadata vẫn phải được giữ**: Chuẩn hóa body không được làm mất `Allow`, `WWW-Authenticate` hoặc các header cần thiết của lỗi gốc.
- **Không lộ thông tin nội bộ**: Stack trace, câu SQL và token chỉ được xử lý trong log phù hợp ở server. `trace_id` trong response cần liên kết với log để tra cứu được.

---

## 5. Phân Trang & Tính Ổn Định Của Danh Sách (Pagination)

Không trả toàn bộ collection khi dữ liệu có thể tăng lớn. Phân trang giới hạn chi phí truy vấn, dung lượng response và bộ nhớ client. **JJ Geewax Ch. 21** bổ sung mẫu page token cho nội dung slide 17 và Lab 3.

1. **Offset-based — `?page=2&per_page=50` hoặc `?offset=50&limit=50`**:
   - Dễ hiểu, hỗ trợ nhảy đến trang N; phù hợp giao diện quản trị và tập dữ liệu tương đối ổn định.
   - Với page bắt đầu từ 1: $offset = (page - 1) \times per\_page$.
   - Offset lớn thường phải bỏ qua nhiều dòng; insert/delete trước vị trí hiện tại có thể làm trang sau trùng hoặc thiếu bản ghi.
2. **Keyset / Seek — `?after_id=1000&limit=50`**:
   - Lấy các bản ghi sau khóa cuối trang trước: `WHERE id > 1000 ORDER BY id ASC LIMIT 50`.
   - Tận dụng index để tránh bỏ qua một đoạn dài; không hỗ trợ nhảy tùy ý tới trang N.
   - Cần thứ tự xác định. Nếu sắp xếp theo `created_at` có giá trị trùng nhau, thêm `id` làm khóa phụ và lưu cả hai giá trị tại ranh giới trang.
3. **Cursor-based — `?cursor=<token>&limit=50`**:
   - Client nhận token tiếp tục từ server và gửi lại nguyên vẹn; token có thể chứa khóa cuối trang cùng ngữ cảnh truy vấn.
   - **Cursor là giao diện tiếp tục ở mức API; keyset là cách truy vấn dữ liệu**. Cursor có thể dùng keyset bên trong, nên hai khái niệm này không loại trừ nhau.
   - *Opaque*: Client không được phụ thuộc vào cấu trúc nội bộ của token; không có nghĩa token bắt buộc không thể giải mã. Base64 chỉ mã hóa biểu diễn, không bảo mật hay chống sửa đổi.

### Quy Tắc Triển Khai Cursor:

- **Giới hạn kích thước trang**: Ví dụ mặc định `limit=5`, phạm vi `1..100` như code Blog API; kiểm tra trước khi truy vấn.
- **Sort ổn định và có khóa duy nhất**: `ORDER BY id ASC` hoặc `ORDER BY created_at ASC, id ASC`. Index phải phù hợp; không khẳng định mọi truy vấn keyset đều có cùng độ phức tạp bất kể filter và index.
- **Giữ ngữ cảnh**: Cursor cần khớp với filter và sort đang dùng; đổi `status`, `author_id` hoặc chiều sort khi tái sử dụng token cần bị từ chối hoặc có quy tắc rõ ràng.
- **Đọc thêm một bản ghi**: Query `LIMIT limit + 1`; trả tối đa `limit` bản ghi và dùng bản ghi dư để xác định `has_more`. Chỉ sinh `next_cursor` khi còn trang sau.
- **Validate cursor**: Token hỏng hoặc không khớp ngữ cảnh trả `400` dạng Problem Details. Khi cần chống sửa đổi, dùng chữ ký hoặc token do server quản lý; vẫn kiểm tra quyền truy cập mỗi request.
- *Giới hạn*: Keyset giảm vấn đề dịch chuyển offset nhưng không tự tạo snapshot. Nếu khóa sort hoặc trường filter bị cập nhật giữa hai lần đọc, kết quả vẫn có thể thay đổi.

---

## 6. Lọc, Sắp Xếp & Lựa Chọn Trường (Filtering, Sorting & Sparse Fieldsets)

Ba khả năng này giúp client lấy đúng dữ liệu cần dùng thay vì tải toàn bộ rồi xử lý ở phía sau. Cú pháp cụ thể là một phần của **API Contract**, không có một cách viết query duy nhất bắt buộc cho mọi REST API.

- **Filtering (Lọc)**: `?status=published&author_id=2` thu hẹp tập bài viết; `?created_after=...` lọc theo thời gian. Phải định nghĩa trường được lọc, kiểu dữ liệu, toán tử và cách kết hợp điều kiện.
  - *Mở rộng từ JJ Geewax Ch. 22*: Với truy vấn phức tạp, có thể định nghĩa `filter=...`; phải parse/validate biểu thức và dùng truy vấn tham số hóa, không nối trực tiếp chuỗi client vào SQL.
- **Sorting (Sắp xếp)**: Chọn quy ước rõ ràng như `sort=id` tăng dần, `sort=-id` giảm dần; hoặc `sort=updated&direction=desc` như ví dụ GitHub trong slide.
  - Hỗ trợ sort nhiều trường khi nghiệp vụ cần và backend đáp ứng; luôn có khóa phụ để xử lý giá trị trùng. Không suy ra chiều sort chỉ từ tên trường nếu hợp đồng chưa quy định.
- **Sparse Fieldsets (Chọn trường)**: `?fields=id,title,status` giảm dữ liệu dư thừa và băng thông.
  - Server dùng **allowlist các trường công khai**. Trường nhạy cảm như `password_hash` không được trả về kể cả khi client yêu cầu; không đặt trách nhiệm bảo mật vào việc client tự thêm `fields=-password_hash`.
  - Cursor phải lấy khóa sort từ model/truy vấn nội bộ, kể cả khi client không yêu cầu trường `id` trong response.
- **Validation nhất quán**: Field không tồn tại, sort không hỗ trợ, limit sai hoặc filter sai kiểu trả `400` kèm giải thích. Hợp đồng phải nêu rõ tham số mặc định và các giới hạn.

```text
GET /api/v1/posts?status=published&author_id=2&sort=-id&fields=id,title&limit=5

Validate → Filter → Sort ổn định → Áp dụng ranh giới cursor → Limit + 1
         → Chọn trường response → Trả metadata và next_cursor
```

---

## 7. Anti-Patterns & Checklist Review Thiết Kế API

Các lỗi nên phát hiện ngay khi review hợp đồng, trước khi client tích hợp:

- **Động từ CRUD trong URL**: `/getPosts`, `/createUser` → chuyển sang collection/item và HTTP method phù hợp.
- **Thành công giả**: `200` kèm `error` → dùng mã 4xx/5xx phù hợp và body lỗi có cấu trúc.
- **Naming lẫn lộn**: `/Users`, `/user_orders`, `/user-orders` → thống nhất quy ước; nếu đã công bố thì cần kế hoạch tương thích khi sửa.
- **Nhầm collection và item**: `/user` để trả danh sách → `/users`; tài nguyên người dùng hiện tại như `/me` là ngoại lệ có ngữ cảnh rõ ràng.
- **Credential trong query**: `?token=...`, `?password=...` → dùng cơ chế xác thực và header/body phù hợp qua HTTPS; tránh để thông tin nhạy cảm lọt vào URL và log.
- **Gắn định dạng vào URI tùy tiện**: `/posts/42.json` → trong quy ước bài học, dùng `/posts/42` và khai báo media type.
- **Lộ chi tiết database hoặc tin vào ID khó đoán**: Thiết kế public resource ID ổn định; kiểm tra quyền theo tài nguyên, không coi UUID là cơ chế phân quyền.
- **Bỏ qua content negotiation**: Định nghĩa rõ media type hỗ trợ và cách phản hồi khi không đáp ứng được; phân biệt `Accept` của response với `Content-Type` của request.

### 9 Tiêu Chí Review Theo Slide:

1. **Resource**: Tên có phản ánh miền nghiệp vụ và phân biệt collection/item/sub-resource không?
2. **Naming**: Path, query và JSON có nhất quán không?
3. **HTTP Semantics**: Method và status code có đúng ý nghĩa không?
4. **Idempotency**: Retry có gây trùng thao tác không; POST quan trọng có cần cơ chế chống trùng không?
5. **Errors**: Problem Details có giúp client nhận diện nguyên nhân và sửa request không?
6. **Pagination**: Có giới hạn, giá trị mặc định, dấu hiệu hết trang và cách xử lý token hỏng không?
7. **Filter/Sort/Fields**: Có hỗ trợ nhu cầu truy vấn chính, validate và giới hạn trường công khai không?
8. **Security**: Credential có được truyền phù hợp, quyền truy cập có được kiểm tra, giới hạn lưu lượng có rõ ràng không?
9. **Versioning & Deprecation**: Có chiến lược thay đổi và thông báo ngừng hỗ trợ không? `/api/v1` là lựa chọn của Blog API, không phải cách versioning duy nhất.

---

## 8. Liên Hệ Thực Hành Tuần 3 & Nguồn Ôn Tập

- **Lab 1 — Blog API**: [Thiết kế endpoint](practice/API.md) xác định users/posts/comments/tags và quan hệ theo dõi; chọn prefix `/api/v1`.
- **Lab 2 — Problem Details**: [ApiProblem](practice/error.py) và handler trong [app.py](practice/app.py) trả lỗi nghiệp vụ dạng `application/problem+json`. *Điểm cần phân biệt*: Handler hiện đăng ký cho `ApiProblem`; các lỗi mặc định qua `abort(404)`, 405 hoặc exception ngoài dự kiến chưa có fallback tập trung trong file này.
- **Lab 3 — Cursor Pagination**: Slide yêu cầu `/orders`; bản thực hành hiện áp dụng cùng ý tưởng cho `/posts`: filter `status`, `author_id`; sort `id/-id`; chọn `fields`; cursor gắn ngữ cảnh; lấy `limit + 1`. POST/GET/DELETE đã có route, nhưng PUT/PATCH chưa được hiện thực và POST chưa kèm `Location`; không đồng nhất thiết kế dự kiến với toàn bộ chức năng đã hoàn thành.
- **Review API công khai**: [Báo cáo review GitHub REST API](Bao_cao_review_GitHub_REST_API.pdf) là tài liệu thực hành đã có trong tuần 3.

Minh chứng chạy Lab-02 đã lưu trong dự án:

![Minh chứng Lab-02](images/Screenshot%202026-10-04%20at%2000.32.36.png)

Minh chứng chạy Lab-03 đã lưu trong dự án:

![Minh chứng Lab-03](images/Screenshot%202026-10-06%20at%2019.18.47.png)

### Nguồn Tổng Hợp:

- **Slide Buổi 3**: [API Design Principles và Best Practices](../../.agents/context/lecture-slides/SOA%20-%20B3%20-%20API_Design_Principles_va%CC%80_Best_Practices.pdf), 23 trang; trọng tâm naming (5-8), HTTP/errors (10-16), pagination/query (17-19), review (20-23).
- **JJ Geewax — API Design Patterns**: [Ghi chép cached của dự án](../../.agents/context/api-design-patterns-notes.md), trọng tâm **Ch. 7 — Standard Methods**; bổ sung Ch. 3-6 (naming và dữ liệu), Ch. 8-9 (update/custom methods), Ch. 21-22 (pagination/filtering), Ch. 24, 26 (compatibility/deduplication).
- **Bruno Pedro — Building an API Product**: [Ghi chép cached của dự án](../../.agents/context/building-api-product-notes.md), trọng tâm **Ch. 2 — API User Experience** và **Ch. 7 — Defining and Validating an API Design**. Các tham chiếu chương sách ở đây dựa trên bản ghi chép cached, không phải trích nguyên văn giáo trình.
- **Chuẩn đối chiếu**: [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) và [RFC 9457 — Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html), dùng để làm rõ các điểm về HTTP và cấu trúc lỗi.
