# Hai quyết định thiết kế khó nhất

## 1. Quy tắc cập nhật một phần bằng `PATCH`

Khi cập nhật sách, client chỉ cần gửi trường muốn đổi. Ví dụ, để đổi giá, gửi:

```json
{"price": 150000}
```

Các trường không gửi sẽ được giữ nguyên. Yêu cầu phải có ít nhất một trường; vì vậy `{}` không hợp lệ và bị trả `422`. Trường lạ, `id`, và giá trị `null` cũng không được chấp nhận. Theo quy tắc này, client không thể dùng `null` để xóa ISBN.

**Vì sao khó:** nhóm phải thống nhất chính xác “không gửi trường”, “gửi `null`” và “gửi body rỗng” có nghĩa gì. Nếu client nghĩ `null` là xóa còn server lại từ chối, việc cập nhật sẽ gây bất ngờ. Quy tắc rõ ràng giúp client và server cùng xử lý một yêu cầu theo một cách.

## 2. Phân biệt lỗi `400` và `422`

- `400 Bad Request`: server không đọc được yêu cầu, ví dụ JSON sai cú pháp: `{"price":`.
- `422 Unprocessable Entity`: server đọc được JSON nhưng dữ liệu không hợp lệ, ví dụ giá âm: `{"price": -5}`.

**Vì sao khó:** ranh giới giữa “không đọc được yêu cầu” và “đọc được nhưng dữ liệu sai” cần được áp dụng nhất quán. Nếu server lúc trả `400`, lúc trả `422` cho cùng một kiểu lỗi, client sẽ khó biết nên sửa cú pháp yêu cầu hay sửa giá trị dữ liệu.
