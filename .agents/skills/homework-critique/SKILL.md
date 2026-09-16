---
name: homework-critique
description: >
  Chặng B — Nhận xét bài tập về nhà theo 4 tiêu chí cố định (pattern fidelity,
  status codes, race condition, DX) bằng chế độ Socratic: kiểm tra trực tiếp mã nguồn
  trong thư mục weeks/week-XX/practice/, đặt câu hỏi phản biện, không đưa đáp án trực tiếp. Chờ Gate B.
---

# Skill: homework-critique (Chặng B)

## Mục Tiêu

Giúp sinh viên **tự nhận ra** điểm yếu trong bài làm qua câu hỏi phản biện, thay vì chỉ nhận kết luận từ AI. 

> **Vị trí bài tập cần kiểm tra**: Thư mục `weeks/week-XX/practice/` của tuần tương ứng. AI chủ động đọc các file mã nguồn, cấu hình và ghi chú trong thư mục này trước khi thực hiện nhận xét.
>
> Gate B chỉ mở khi sinh viên phát biểu lại được lý do đúng/sai — không chỉ nói "tôi hiểu rồi".

---

## 4 Tiêu Chí Đánh Giá Cố Định

| # | Tiêu chí | Câu hỏi kiểm tra |
|---|---|---|
| 1 | **Pattern fidelity** | Code trong `practice/` có implement đúng pattern/concept của tuần không? Có đúng semantics REST, HTTP, hay pattern đang học? |
| 2 | **Status codes** | Các HTTP status code được dùng trong `practice/` có đúng ngữ nghĩa? `201` khi tạo mới? `204` khi xóa? `404` khi không tìm thấy? `409` khi conflict? |
| 3 | **Race condition** | Trong code bài tập, có kịch bản nào (concurrent requests, retry) dẫn đến inconsistent state? Có cơ chế phòng ngừa không? |
| 4 | **DX (Developer Experience)** | Nếu là developer dùng API trong bài tập này: error message có rõ ràng? Response structure có nhất quán? Docs/README có đủ để chạy thử không? |

---

## Bước Thực Hiện

### 1. Đọc và Kiểm Tra Mã Nguồn Bài Tập Trong `weeks/week-XX/practice/`

AI sử dụng các công cụ file viewer để đọc:
- `weeks/week-XX/practice/` (ví dụ: `app.py`, `server.js`, `README.md`, models, routes, v.v.).
- Nếu thư mục `practice/` còn trống hoặc chưa có code xử lý: AI thông báo và nhắc sinh viên đặt code bài tập vào thư mục này trước khi tiếp tục.

### 2. Yêu Cầu Sinh Viên Tự Đánh Giá Trước

Trước khi AI đưa ra nhận xét chi tiết, hỏi:

> "Tôi đã đọc code bài tập của bạn trong `weeks/week-XX/practice/`. Trước khi tôi đưa ra review chi tiết, bạn thấy phần nào bạn tự tin nhất và phần nào bạn còn băn khoăn nhất về mặt kiến trúc/chuẩn REST?"

Chờ sinh viên phản hồi.

### 3. Review Từng Tiêu Chí (Socratic Mode)

Đối chiếu code thực tế trong `weeks/week-XX/practice/` với 4 tiêu chí. Với mỗi tiêu chí, **trích dẫn dòng code cụ thể** và **đặt câu hỏi phản biện** trước:

**Ví dụ cho tiêu chí Status Codes / Endpoint Semantics:**
- Trích dẫn: `weeks/week-XX/practice/app.py`
- Đặt câu hỏi: "Ở route `/books` phương thức POST, bạn đang dùng `request.args` để lấy tham số phân trang thay vì nhận dữ liệu từ request body. Theo chuẩn REST, POST dùng cho mục đích gì và có nên dùng để truy vấn danh sách không?"

**Ví dụ cho tiêu chí Race Condition / Data Integrity:**
- Đặt câu hỏi: "Trong đoạn xử lý thêm item vào giỏ hàng, nếu 2 request đến cùng lúc, việc tính toán số lượng tồn kho có nguy cơ bị dirty read hay race condition không?"

### 4. Output — Báo Cáo Nhận Xét

Lưu vào file `weeks/week-XX/homework-review.md`:

```markdown
## 📝 Homework Review — Tuần XX

**Mã nguồn kiểm tra**: `weeks/week-XX/practice/`

### Tiêu chí 1 — Pattern Fidelity
- **Trích dẫn code**: `practice/...`
- **Nhận xét**: [đánh giá ngắn]
- **Câu hỏi Socratic**: [câu hỏi để sinh viên tự suy ngẫm và phát biểu]

### Tiêu chí 2 — Status Codes & HTTP Semantics
- **Trích dẫn code**: ...
- **Nhận xét**: ...
- **Câu hỏi Socratic**: ...

### Tiêu chí 3 — Race Condition Resilience
- **Trích dẫn code**: ...
- **Nhận xét**: ...
- **Câu hỏi Socratic**: ...

### Tiêu chí 4 — Developer Experience (DX)
- **Trích dẫn code**: ...
- **Nhận xét**: ...
- **Câu hỏi Socratic**: ...

---

### Câu hỏi tổng hợp quan trọng nhất:
> [1 câu hỏi mở cốt lõi nhất yêu cầu sinh viên tự giải thích lý do tại sao cần sửa/tối ưu mã nguồn]
```

### 5. 🛑 Gate B

> **🛑 Gate B**: Để qua chặng này, hãy trả lời câu hỏi tổng hợp ở trên bằng lời của bạn dựa trên code tại `weeks/week-XX/practice/`. Sau khi chúng ta thống nhất được lý do bản chất, chúng ta sẽ chuyển sang **Chặng C — Project Incrementor**.

**Không tự ý nhảy sang Chặng C khi sinh viên chưa phát biểu rõ lý do**.

---

## Nguyên Tắc

- Luôn kiểm tra code trực tiếp trong thư mục `weeks/week-XX/practice/`.
- Không tự động sửa code hoặc đưa code giải hoàn chỉnh vào thư mục `practice/`.
- Hướng dẫn sinh viên tự sửa và nhận diện vấn đề thông qua phản biện.
