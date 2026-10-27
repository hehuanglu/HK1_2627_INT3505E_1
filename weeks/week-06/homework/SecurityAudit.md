# Security Audit

### 1. Email và mật khẩu đăng nhập trong log

- **Điểm có thể lộ:** Giá trị `email` và `password` trong body `POST /api/v1/auth/login`.
- **Đường lộ và tác động:** Nếu ứng dụng, proxy hoặc công cụ giám sát ghi toàn bộ body, người có quyền xem log có thể đọc mật khẩu và đăng nhập bằng tài khoản đó. Đây là rủi ro thực tế khi bật log request body hoặc debug thiếu chọn lọc; spec chưa mô tả cách ghi log.

### 2. Access token và refresh token trong log

- **Điểm có thể lộ:** `access_token` và `refresh_token` trong response của login/refresh; token trong header `Authorization` khi gọi refresh hoặc đọc bài.
- **Đường lộ và tác động:** Nếu log ghi response body hoặc header Authorization, người đọc log có thể dùng access token để đọc bài theo quyền của chủ token, hoặc dùng refresh token còn hiệu lực để xin cặp token mới. Việc log header hoặc body là tình huống thực tế nhưng phụ thuộc cấu hình; `Cache-Control: no-store` trong spec không tự ngăn ghi log.

### 3. Nội dung bài của người khác qua ID

- **Điểm có thể lộ:** `title`, `content`, `status` và `author_id` của bài viết trả từ `GET /api/v1/posts/{id}`.
- **Đường lộ và tác động:** Nếu server chỉ kiểm tra access token và scope `posts:read` mà bỏ qua quyền trên bài, user A có thể thay ID để đọc bài của user B, kể cả bài `draft`. Đây là lỗi phân quyền đối tượng có thể xảy ra khi triển khai; spec yêu cầu kiểm tra tác giả hoặc admin nhưng chưa chứng minh backend thực hiện đúng.

### 4. Email có đăng ký tài khoản qua lỗi login

- **Điểm có thể lộ:** Việc một email cụ thể có tài khoản trong hệ thống hay không.
- **Đường lộ và tác động:** Nếu login trả status, nội dung hoặc thời gian phản hồi khác biệt có thể phân biệt được giữa email không tồn tại và mật khẩu sai, người gọi có thể thử nhiều email để suy ra danh sách tài khoản. Spec yêu cầu cùng lỗi `401` và thông báo chung, nhưng không xác nhận cách xử lý thời gian hoặc rate limit thực tế.
- **Đánh giá:** Rò rỉ qua thông báo khác nhau dễ nhận biết; suy luận qua thời gian phụ thuộc mức chênh lệch, nhiễu mạng và giới hạn thử, nên không thể giả định chắc chắn khai thác được.

### 5. Sự tồn tại của bài viết qua `403` và `404`

- **Điểm có thể lộ:** Một ID bài viết cụ thể có tồn tại hay không, kể cả khi nội dung bài không được trả về.
- **Đường lộ và tác động:** Theo spec, caller có token hợp lệ và scope `posts:read` nhận `403` nếu bài tồn tại nhưng không có quyền, còn bài không tồn tại trả `404`. Bằng cách thử ID, caller có thể phân biệt hai trường hợp.
- **Đánh giá:** Đây là hệ quả trực tiếp của hợp đồng, nhưng chỉ ảnh hưởng caller đã có token và scope phù hợp; mức độ nhạy cảm phụ thuộc việc danh sách ID hay sự tồn tại của bài có cần giữ kín. Không suy ra nội dung bài đã bị lộ.

## Giới hạn

Spec không xác định cấu hình log, danh sách claim JWT đầy đủ, nơi lưu token hay hành vi backend thực tế. Các điểm trên là phân tích theo điều kiện nêu trong từng mục; chưa thể kết luận thông tin đã bị lộ hoặc đã xảy ra tấn công.
