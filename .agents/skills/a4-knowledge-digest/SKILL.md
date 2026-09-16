---
name: a4-knowledge-digest
description: >
  Chặng E — Tổng hợp tri thức của tuần học thành 1 trang A4 Knowledge Digest
  với 5 mục cố định (Core Concept, Evidence, Homework Lesson, Industry Application,
  Creative LLM Idea). Chờ Gate E → xuất PDF.
---

# Skill: a4-knowledge-digest (Chặng E)

## Mục Tiêu

Đúc kết toàn bộ tuần học thành **1 trang A4 có thể in ra** — không phải summary dài, mà là bản tinh chất nhất để ôn tập về sau. Mọi nội dung phải đến từ các chặng trước (A, B, C, D) — không thêm nội dung mới.

---

## Nguồn Dữ Liệu (Bắt Buộc Dùng)

| Mục trong Digest | Lấy từ |
|---|---|
| Core Concept | `input-log.md` (Chặng A) + `glossary-soa.md` |
| Evidence | `evidence-snapshot.md` (Chặng C) |
| Homework Lesson | `homework-review.md` (Chặng B) |
| Industry Application | `industry-mapping.md` — đúng dòng tuần này |
| Creative LLM Idea | `creative-idea.md` (Chặng D) |

**Không được thêm nội dung không có trong các nguồn trên.**

---

## Bước Thực Hiện

### 1. Thu Thập & Tổng Hợp

Đọc 5 nguồn trên, rút ra phần tinh chất nhất cho mỗi mục. Ưu tiên cụ thể > trừu tượng, ví dụ thực tế > định nghĩa lý thuyết.

### 2. Soạn Nội Dung Theo Template

Dùng template từ `a4-digest-template.md`. **Không được thay đổi cấu trúc 5 mục.**

Giới hạn độ dài:
- Mục 1 (Core Concept): ≤ 150 từ
- Mục 2 (Evidence): chỉ 1 request/response + 1 test result
- Mục 3 (Homework Lesson): ≤ 100 từ
- Mục 4 (Industry Application): sao chép đúng từ `industry-mapping.md`, ≤ 100 từ
- Mục 5 (Creative LLM Idea): ≤ 80 từ

**Tổng: phải vừa 1 trang A4 (cỡ chữ 11pt, margin 1.5cm)**

### 3. Ghi `weeks/week-XX/digest-A4.md`

Lưu nội dung hoàn chỉnh theo template.

### 4. Trình Bày Cho Sinh Viên

Hiển thị nội dung Digest và nêu rõ:

> **Tóm tắt Digest Tuần XX:**
> - Core Concept: [1 câu]
> - Evidence: [X/Y tests passed]
> - Homework Lesson: [bài học chính]
> - Industry Application: [link với LLM]
> - Creative Idea: [tên ý tưởng]

### 5. 🛑 Gate E

> **🛑 Gate E**: Bạn có muốn chỉnh sửa phần nào trong Digest không? Sau khi duyệt, tôi sẽ xuất PDF với lệnh:
> ```bash
> pandoc weeks/week-XX/digest-A4.md -o weeks/week-XX/digest-A4.pdf \
>   --pdf-engine=xelatex -V geometry:margin=1.5cm -V fontsize=11pt
> ```

Chờ xác nhận của sinh viên trước khi xuất PDF.

### 6. Xuất PDF

Chạy lệnh xuất sau khi Gate E được thông qua. Xác nhận file tồn tại:

```bash
ls -lh weeks/week-XX/digest-A4.pdf
```

---

## Nguyên Tắc

- **Không thêm nội dung mới** ở Chặng E — chỉ tổng hợp từ A, B, C, D.
- Mục 4 phải sao chép đúng từ `industry-mapping.md` — không paraphrase lại.
- Nếu Chặng C không có evidence (service chưa chạy được) → ghi rõ "Evidence: [Chưa có — service lỗi: ...]" thay vì bỏ mục.
