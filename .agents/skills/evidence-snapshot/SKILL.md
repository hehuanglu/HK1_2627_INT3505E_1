---
name: evidence-snapshot
description: >
  Chặng C (Phần 3) — Chạy service tại project/, thực thi Newman test suite,
  và chụp snapshot minh chứng thực nghiệm (terminal logs, request/response payloads,
  Newman PASS/FAIL) để dùng làm evidence trong A4 Knowledge Digest.
---

# Skill: evidence-snapshot (Chặng C — Phần 3)

## Mục Tiêu

Tạo **minh chứng thực nghiệm có thể kiểm chứng** từ code đã được audit — không dùng ví dụ lý thuyết trong Digest. Snapshot phải capture đủ: request thực tế → response thực tế → assertion result.

---

## Bước Thực Hiện

### 1. Cài Đặt & Khởi Động Service

```bash
cd project
npm install
npm start
# Xác nhận: "🚀 Server running at http://localhost:3000"
# Xác nhận: "✅ MongoDB connected"
```

Nếu có lỗi → báo sinh viên fix trước khi tiếp tục.

### 2. Tạo/Cập Nhật Postman Collection

Tạo file test tại `weeks/week-XX/postman_collection.json` (Postman v2.1.0) với:

**Cấu trúc bắt buộc:**
- **Happy Path tests**: UC vừa implement hoạt động đúng với input hợp lệ
- **Negative Path tests**: ít nhất 2 scenario lỗi (invalid input, resource not found)
- **pm.test assertions** cho mỗi request: status code, response body structure, headers

**Ví dụ assertion:**
```javascript
pm.test("Status 201 Created", () => pm.response.to.have.status(201));
pm.test("Location header tồn tại", () => pm.response.to.have.header("Location"));
pm.test("Body có _id", () => {
    const body = pm.response.json();
    pm.expect(body).to.have.property("_id");
});
```

### 3. Chạy Newman & Capture Snapshot

```bash
# Cài Newman nếu chưa có
npm install -g newman

# Chạy test
newman run weeks/week-XX/postman_collection.json --reporters cli,json \
  --reporter-json-export weeks/week-XX/newman-report.json
```

### 4. Tạo Snapshot File

Ghi `weeks/week-XX/evidence-snapshot.md`:

```markdown
# Evidence Snapshot — Tuần XX — [Tên UC]

## Request/Response Thực Tế

### [Happy Path] — [Tên test]
**Request:**
\`\`\`http
[Method] [URL]
Content-Type: application/json

[request body nếu có]
\`\`\`

**Response:**
\`\`\`http
HTTP/1.1 [status code]
[headers quan trọng]

[response body]
\`\`\`

### [Negative Path] — [Tên test]
...

## Newman Test Result

\`\`\`
[paste terminal output Newman]
\`\`\`

**Tổng kết**: X/Y tests passed
```

### 5. Cập Nhật `weeks/week-XX/demo-delta.diff`

```bash
git diff HEAD -- project/ > weeks/week-XX/demo-delta.diff
```

### 6. Thông Báo Kết Quả

Sau khi có snapshot, tóm tắt cho sinh viên:

> "✅ Newman: [X/Y tests passed]. Evidence đã được lưu tại `weeks/week-XX/evidence-snapshot.md`. Sẵn sàng sang Chặng D."

Nếu có test fail → phân tích nguyên nhân với sinh viên trước khi sang Chặng D.

---

## Nguyên Tắc

- Không dùng mock hay giả lập — phải chạy service thực tế.
- Nếu MongoDB không chạy → hướng dẫn sinh viên start MongoDB trước.
- Snapshot phải đủ detail để ai đọc cũng hiểu API hoạt động như thế nào mà không cần chạy code.
