---
name: project-incrementor
description: >
  Chặng C (Phần 1) — Đề xuất Use Case nhỏ nhất minh họa concept tuần học
  trên codebase xuyên suốt (project/), scaffold boilerplate + khối TODO
  để sinh viên tự implement logic cốt lõi. Phối hợp với architecture-audit
  và evidence-snapshot trong cùng Chặng C.
---

# Skill: project-incrementor (Chặng C — Phần 1)

## Mục Tiêu

Xác định **đúng một UC nhỏ nhất** có thể implement trong ~1 buổi, đủ để minh họa concept tuần học mà không làm phức tạp codebase. Scaffold sạch sẽ để sinh viên chỉ cần điền vào phần logic cốt lõi.

---

## Bước Thực Hiện

### 1. Tham Chiếu Context

```
[Semi-static] project-scope.md  → hiểu domain, resource hiện tại, constraints
[Semi-static] uc-backlog.md     → tránh đề xuất UC đã làm hoặc đã reject
[Dynamic]     input-log.md      → concept của tuần, kỹ năng cần đạt
```

### 2. Đề Xuất UC

Trình bày đề xuất theo mẫu:

```markdown
## 💡 Đề xuất UC — Tuần XX

**Tên UC**: [tên ngắn, ≤ 6 từ]
**Concept minh họa**: [concept cốt lõi của tuần]
**Resource tác động**: [User / resource mới / ...]
**Endpoint(s)**: [METHOD /path]

**Tại sao UC này?**
> [2–3 câu giải thích: UC nhỏ nhất có thể, liên quan trực tiếp concept, không break UC cũ]

**Câu hỏi phản biện cho sinh viên trước khi code**:
1. [Câu hỏi kiến trúc: tại sao chọn method này? tại sao path này?]
2. [Câu hỏi edge case: điều gì xảy ra nếu ...?]
3. [Câu hỏi trade-off: có cách nào khác không? đánh đổi gì?]
```

Chờ sinh viên thảo luận và xác nhận UC trước khi scaffold.

### 3. Scaffold Code

Sau khi UC được chấp nhận, tạo/sửa file trong `project/` với:

**Nguyên tắc scaffold:**
- Viết đầy đủ boilerplate (imports, route wiring, error handling shell, response structure)
- Đánh dấu phần sinh viên cần implement bằng block:

```javascript
// ============================================================
// TODO [HỌC VIÊN IMPLEMENT — Tuần XX]:
// [Mô tả rõ ràng bằng tiếng Việt: cần làm gì]
// Gợi ý: [1 gợi ý kỹ thuật tối giản, không đưa code đầy đủ]
// ============================================================
```

- Chỉ có **1 block TODO chính** per UC (tránh chia nhỏ quá mức)
- Các phần còn lại (DB connection, route mounting, error handler) đã hoàn chỉnh

### 4. Tạo `weeks/week-XX/demo-delta.diff`

Sau khi sinh viên implement xong (báo AI), ghi diff vào file này bằng:

```bash
git diff project/ > weeks/week-XX/demo-delta.diff
```

### 5. 🛑 Bàn Giao cho Sinh Viên

> **🔨 Đến lượt bạn**: File `project/[...]` đã có scaffold. Hãy mở và implement phần TODO. Khi xong, báo tôi để chuyển sang **architecture-audit**.

---

## Ràng Buộc

- Không tự implement TODO — dù sinh viên yêu cầu "làm giúp tạm".
- Nếu sinh viên hỏi "làm như thế nào" → dùng câu hỏi Socratic dẫn dắt, không code hộ.
- Delta không được break endpoint nào đã có từ tuần trước.
