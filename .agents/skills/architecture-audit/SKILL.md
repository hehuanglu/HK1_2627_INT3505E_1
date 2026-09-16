---
name: architecture-audit
description: >
  Chặng C (Phần 2) — Review kiến trúc delta code sinh viên vừa implement
  theo 4 tiêu chí (pattern fidelity, REST status codes, race condition resilience, DX).
  Đề xuất bản vá tối ưu có giải thích "tại sao". Chờ Gate C.
---

# Skill: architecture-audit (Chặng C — Phần 2)

## Mục Tiêu

Đọc code delta sinh viên vừa implement, nhận xét theo 4 tiêu chí kiến trúc, đề xuất bản cải thiện có kèm giải thích nguyên lý — không chỉ đưa code tốt hơn mà còn phải giải thích *tại sao*.

---

## 4 Tiêu Chí Audit

| # | Tiêu chí | Câu hỏi kiểm tra |
|---|---|---|
| 1 | **Pattern Fidelity** | Delta có implement đúng pattern/concept của tuần không? Có đúng semantics REST, idempotency, hay pattern nâng cao đang học? |
| 2 | **REST Status Codes** | Mọi response path (success + error) dùng đúng HTTP status code? Có `Location` header khi `201`? Có body khi `204`? |
| 3 | **Race Condition Resilience** | Concurrent requests có gây inconsistent state? Có dùng DB unique index? Có xử lý duplicate key error? |
| 4 | **DX (Developer Experience)** | Error message có đủ `type`, `title`, `detail` (RFC 7807)? Response structure nhất quán với các endpoint cũ? |

---

## Bước Thực Hiện

### 1. Đọc Code Delta

Yêu cầu sinh viên paste code đã implement (hoặc đọc trực tiếp từ `project/` nếu có quyền truy cập).

### 2. Audit Từng Tiêu Chí

```markdown
## 🔍 Architecture Audit — Tuần XX — [Tên UC]

### Tiêu chí 1 — Pattern Fidelity
**Đánh giá**: [✅ Đạt / ⚠️ Cần cải thiện / ❌ Chưa đạt]
**Nhận xét**: [giải thích cụ thể]
**Bản vá đề xuất** (nếu cần):
\`\`\`javascript
// [code cải thiện + comment giải thích tại sao]
\`\`\`

### Tiêu chí 2 — REST Status Codes
...

### Tiêu chí 3 — Race Condition Resilience
...

### Tiêu chí 4 — DX
...

### Tổng Kết
**Điểm mạnh**: [1–2 điểm tốt cần ghi nhận]
**Điểm cần cải thiện ưu tiên**: [1–2 điểm quan trọng nhất]
**Bài học kiến trúc rút ra**: [1–2 câu súc tích — dùng cho Chặng E]
```

### 3. Thảo Luận & Chốt Bản Cuối

Sau khi đề xuất, hỏi:
> "Bạn đồng ý với bản cải thiện không? Có điểm nào bạn muốn giữ nguyên theo design của bạn và tại sao?"

Chờ sinh viên phản hồi. Chỉ chốt khi hai bên đồng thuận.

### 4. 🛑 Gate C

Sau khi thống nhất code cuối:

> **🛑 Gate C**: Để qua chặng này, hãy phát biểu bài học kiến trúc tuần này bằng 1–2 câu của bạn. Sau đó tôi sẽ chạy `evidence-snapshot` để lấy bằng chứng thực nghiệm.

---

## Nguyên Tắc

- Luôn giải thích **tại sao** khi đề xuất bản vá — không chỉ đưa code tốt hơn.
- Nhận xét theo thứ tự quan trọng: Pattern > Status Codes > Race Condition > DX.
- Ghi nhận điểm mạnh trước điểm yếu — tránh chỉ tập trung vào lỗi.
