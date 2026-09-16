---
name: input-conflict-audit
description: >
  Chặng A — Tiếp nhận input tuần học (slide, ghi chú, bài tập, vấn đề giáo viên nhắc),
  đối chiếu với nguồn tri thức chuẩn (.agents/context/*), và nêu rõ mọi mâu thuẫn
  hoặc điểm mờ dưới dạng câu hỏi thảo luận. Chờ Gate A trước khi sang Chặng B.
---

# Skill: input-conflict-audit (Chặng A)

## Mục Tiêu

Đảm bảo input của tuần học hiện tại được **tiếp nhận đầy đủ** và **đối chiếu chính xác** với nguồn tri thức chuẩn trước khi bắt đầu các chặng tiếp theo. Không được im lặng bỏ qua mâu thuẫn.

---

## Bước Thực Hiện

### 1. Tiếp nhận & Phân loại Input

Thu thập từ sinh viên các thành phần của tuần học:

| Thành phần | Ví dụ | Bắt buộc? |
|---|---|---|
| Slide/note bài giảng | PDF, ảnh chụp, text | Bắt buộc |
| Bài tập về nhà (Practice) | Mã nguồn đặt tại `weeks/week-XX/practice/` | Bắt buộc (nếu tuần có bài tập) |
| Ghi chú giáo viên | Vấn đề mở rộng, cảnh báo đặc biệt | Nếu có |
| Tuần học (số) | "Tuần 03" | Bắt buộc |

Nếu thiếu slide/note → **hỏi sinh viên trước khi tiếp tục**, không tự suy diễn nội dung.

### 2. Xây Dựng Context (Theo Thứ Tự Bắt Buộc)

```
[1] Static: syllabus.md → xác định tuần, topic, tài liệu đọc trước
[2] Static: api-design-patterns-notes.md (JJ Geewax) — phần liên quan
[3] Static: building-api-product-notes.md (Bruno Pedro) — phần liên quan
[4] Static: glossary-soa.md — thuật ngữ của tuần
[5] Static: industry-mapping.md — dòng của tuần này
[6] Semi-static: project-scope.md, uc-backlog.md
[7] Dynamic: input sinh viên vừa cung cấp
```

**Không** nạp toàn bộ 2 cuốn sách gốc. Chỉ đọc chương được nhắc trong `syllabus.md` cho tuần đó nếu bản tóm tắt chưa đủ.

### 3. Đối Chiếu & Phát Hiện Mâu Thuẫn

So sánh nội dung input với context trên. Tìm kiếm:

- **Định nghĩa khác nhau**: ví dụ input dùng "Uniform Interface" theo nghĩa hẹp, nhưng JJ Geewax chia thành 4 sub-constraint.
- **Thuật ngữ không chuẩn**: ví dụ gọi `PATCH` là "partial PUT" thay vì phân biệt rõ semantics.
- **Thiếu concept quan trọng**: ví dụ slide nói về REST nhưng không đề cập Stateless constraint.
- **Khẳng định sai**: ví dụ "DELETE phải trả về 200 với body xác nhận" (sai — chuẩn là 204 No Content).

### 4. Output — Báo Cáo Đối Chiếu

Trình bày theo cấu trúc:

```markdown
## 📥 Input Tuần XX — [Tên chủ đề]

### ✅ Điểm nhất quán
- [Nội dung input khớp hoàn toàn với context chuẩn]

### ⚠️ Điểm cần thảo luận
**[Tên mâu thuẫn/điểm mờ]**
- Input nói: "[trích dẫn từ slide/note sinh viên]"
- Nguồn chuẩn nói: "[trích dẫn từ glossary/notes — ghi rõ nguồn]"
- Câu hỏi thảo luận: "[câu hỏi mở để sinh viên suy nghĩ, không đưa kết luận]"

### 📋 Tóm tắt nội dung tuần (để làm context cho Chặng B, C)
- Concept chính: ...
- Kỹ năng cần đạt: ...
- Bài tập: ...
```

### 5. Ghi `weeks/week-XX/input-log.md`

Lưu toàn bộ báo cáo đối chiếu vào file này để các chặng sau tham chiếu.

### 6. 🛑 Gate A

Kết thúc bằng:

> **🛑 Gate A**: Tôi đã trình bày [N] điểm cần thảo luận. Sau khi bạn xem xét và chúng ta đã thống nhất về những mâu thuẫn trên, hãy xác nhận để sang **Chặng B — Nhận xét bài tập**.

**Không tự động tiếp tục sang Chặng B**.

---

## Nguyên Tắc

- Luôn trích dẫn **cả hai nguồn** khi có mâu thuẫn — không tự chọn nguồn nào "đúng hơn".
- Không im lặng bỏ qua dù mâu thuẫn nhỏ.
- Nếu không có mâu thuẫn nào → vẫn viết "Không phát hiện mâu thuẫn — nội dung nhất quán với context chuẩn" và hỏi Gate A.
