# A4 Knowledge Digest — Template

> **Hướng dẫn sử dụng**: Đây là template cố định cho skill `a4-knowledge-digest` (Chặng E). Mỗi tuần tạo một file `weeks/week-XX/digest-A4.md` theo đúng cấu trúc 5 mục bên dưới. Không thêm mục, không bỏ mục, không đổi thứ tự.

---

```markdown
# Knowledge Digest — Tuần XX: [Tên chủ đề]
> Ngày: YYYY-MM-DD | Dự án: [tên project/]

---

## 1. Core Concept

**Vấn đề hệ thống** (system failure mode mà pattern này giải quyết):
> [1–2 câu mô tả bài toán thực tế, không phải định nghĩa sách vở]

**Cơ chế pattern** (cách pattern hoạt động — ngắn gọn, súc tích):
> [3–5 bullet, mỗi bullet 1 câu]
- ...
- ...
- ...

**Thuật ngữ chuẩn** (từ `glossary-soa.md`):
| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| ... | ... | ... |

---

## 2. Evidence (Minh Chứng Thực Nghiệm)

> Chèn trực tiếp từ output của `evidence-snapshot` (Chặng C). Không dùng ví dụ lý thuyết.

**Use Case thực hành**: [tên UC delta đã implement]

**Request/Response thực tế**:
\`\`\`http
[Request và response thực tế từ Newman snapshot]
\`\`\`

**Newman test result**:
\`\`\`
[PASS/FAIL log từ Newman]
\`\`\`

**Bài học kiến trúc từ audit** (1–2 câu):
> [Điều quan trọng nhất rút ra từ `architecture-audit`]

---

## 3. Homework Lesson

> Tổng hợp từ Chặng B (`homework-critique`). Không chép lại bài tập — chỉ ghi bài học rút ra.

**Bài tập**: [mô tả ngắn bài tập của tuần]

**Lỗi/Điểm yếu phát hiện**:
- [tiêu chí 1 — pattern]: ...
- [tiêu chí 2 — status codes]: ...
- [tiêu chí 3 — race condition]: ...
- [tiêu chí 4 — DX]: ...

**Câu trả lời cho câu hỏi Socratic quan trọng nhất**:
> [Sinh viên tự điền sau khi đã thảo luận tại Gate B]

---

## 4. Industry Application

> **Nguồn bắt buộc**: Lấy nguyên từ `industry-mapping.md` cho tuần tương ứng. Không tự bịa.

[Dán nội dung từ `industry-mapping.md` — tuần XX]

---

## 5. Creative LLM Idea

> Ý tưởng cụ thể, mới của tuần này — khác với mục 4 (vốn là bảng tĩnh chung). Đã kiểm tra không trùng `creative-log.md`.

**Ý tưởng**: [tên ngắn gọn]

**Mô tả chi tiết**:
> [2–4 câu: ý tưởng là gì, thử như thế nào, kết quả mong đợi]

**Kết quả thực nghiệm** (nếu đã thử):
> [Hoặc ghi "Chưa thử — sẽ thực hiện ở tuần sau" nếu cần thêm thời gian]

**Liên kết `creative-log.md`**: Ý tưởng này đã được thêm vào `creative-log.md` (dòng: Tuần XX — [tên ý tưởng]).
```

---

## Quy tắc xuất PDF

Sau khi sinh viên duyệt Gate E, chạy lệnh:

```bash
# Dùng Pandoc (khuyến nghị cho A4 digest)
pandoc weeks/week-XX/digest-A4.md \
  -o weeks/week-XX/digest-A4.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1.5cm \
  -V fontsize=11pt

# Hoặc dùng Marp (nếu đã cài sẵn và muốn format slide-like)
# npx @marp-team/marp-cli --no-stdin weeks/week-XX/digest-A4.md --pdf --allow-local-files -o weeks/week-XX/digest-A4.pdf
```
