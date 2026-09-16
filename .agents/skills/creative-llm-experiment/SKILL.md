---
name: creative-llm-experiment
description: >
  Chặng D — Đề xuất một ý tưởng/thử nghiệm cụ thể về cách vận dụng LLM
  liên quan đến concept tuần học. Ý tưởng phải mới (không trùng creative-log.md),
  cụ thể (không chung chung), và khả thi trong bối cảnh khóa học. Chờ Gate D.
---

# Skill: creative-llm-experiment (Chặng D)

## Mục Tiêu

Kích thích tư duy ứng dụng sáng tạo — kết nối concept SOA/REST đang học với cách vận dụng LLM theo cách **cụ thể, mới, và có thể thử nghiệm**, khác với mục Industry application (bảng tĩnh chung trong `industry-mapping.md`).

---

## Phân Biệt: Industry Application vs Creative LLM Idea

| | Industry Application (Chặng E, Mục 4) | Creative LLM Idea (Chặng D) |
|---|---|---|
| **Nguồn** | `industry-mapping.md` — bảng tĩnh, cố định | Mới mỗi tuần, không trùng `creative-log.md` |
| **Tính chất** | Mô tả cách industry đang làm | Đề xuất thử nghiệm mới, chưa có trong bảng |
| **Độ cụ thể** | Chung cho mọi sinh viên | Riêng cho tuần này, project này |
| **Ví dụ** | "LLM agent dùng status code để quyết định retry" | "Thử dùng GPT-4 tự gọi `GET /users` và so sánh response với schema mong đợi" |

---

## Bước Thực Hiện

### 1. Đọc `creative-log.md`

Xem toàn bộ danh sách ý tưởng đã đề xuất trước. **Không được đề xuất ý tưởng trùng** (dù diễn đạt khác đi).

### 2. Brainstorm Ý Tưởng

Dựa trên:
- Concept tuần học (từ `input-log.md`)
- Evidence từ Chặng C (từ `evidence-snapshot.md`)
- Codebase hiện tại (`project/`)

Ý tưởng tốt có các tính chất:
- **Cụ thể**: có thể mô tả thành prompt/code/test cụ thể
- **Nhỏ**: có thể thử trong 30–60 phút
- **Liên quan trực tiếp**: connect với concept tuần, không chỉ là "dùng LLM để..."
- **Có thể sai**: chấp nhận kết quả không như mong đợi — đó cũng là học

### 3. Đề Xuất Ý Tưởng

```markdown
## 💡 Creative LLM Idea — Tuần XX

**Tên**: [tên ngắn, ≤ 8 từ]

**Liên quan đến concept**: [concept tuần học]

**Ý tưởng cụ thể**:
> [3–5 câu mô tả: làm gì, dùng LLM như thế nào, với project/ ra sao]

**Cách thử** (gợi ý):
\`\`\`
[prompt mẫu / pseudocode / lệnh cụ thể để bắt đầu thử]
\`\`\`

**Kết quả mong đợi**: [mô tả điều gì có thể xảy ra — cả thành công và thất bại]

**Điểm khác với Industry Application**: [1 câu giải thích sự khác biệt]
```

### 4. Kiểm Tra Không Trùng

Trước khi đề xuất, xác nhận:

> "Ý tưởng '[tên]' chưa xuất hiện trong `creative-log.md`. Đây là ý tưởng mới."

Nếu có ý tưởng tương tự → điều chỉnh cho khác biệt đủ hoặc brainstorm ý tưởng mới.

### 5. Ghi Output

- `weeks/week-XX/creative-idea.md` — ý tưởng đầy đủ
- Cập nhật `creative-log.md` sau Gate D:

```markdown
| Tuần XX | [Tên ý tưởng] | [Mô tả 1 câu] | ⏳ Đề xuất |
```

### 6. 🛑 Gate D

> **🛑 Gate D**: Ý tưởng trên đã được xác nhận là mới và không trùng với các tuần trước. Bạn có muốn thử nghiệm ngay trong buổi này không, hay ghi vào `creative-log.md` để thử ở tuần sau? Sau khi xác nhận, chúng ta sang **Chặng E — A4 Knowledge Digest**.

---

## Nguyên Tắc

- **1 ý tưởng per tuần** — không đề xuất danh sách để sinh viên chọn (làm loãng sự đầu tư).
- Nếu sinh viên đề xuất ý tưởng của riêng họ → kiểm tra không trùng và chấp nhận nếu phù hợp.
- Kết quả "thất bại" của thử nghiệm cũng có giá trị — ghi rõ vào `creative-idea.md`.
