---
name: course-digest
description: Chặng 1 của quy trình học tập - Sàng lọc tri thức cốt lõi (JJ Geewax, Bruno Pedro, SOA Glossary) và đề xuất kịch bản nghiệp vụ thực tế, có điểm dừng (Logic Gate 1) chờ sinh viên đối chiếu bài giảng và phê duyệt.
---

# Kỹ Năng: Course Digest (Chặng 1 - Sàng Lọc Kiến Thức & Kịch Bản Nghiệp Vụ)

## 1. Tên Kỹ Năng
**course-digest** (Sàng lọc tri thức tuần & Thống nhất kịch bản nghiệp vụ)

## 2. Khi Nào Kích Hoạt
- Bắt đầu tuần học mới (`week-XX`) trong Master Skill `soa-study-pipeline`.
- Cần đối chiếu bài toán của tuần với hệ thống tài liệu chuẩn (`.agents/context/`) và bài giảng trên lớp của thầy cô.
- Chuẩn bị cơ sở lý thuyết vững chắc trước khi bắt tay vào thiết kế kiến trúc và viết mã nguồn.

## 3. Input Mong Đợi
- **Số thứ tự tuần**: `week-XX` (ví dụ `week-02`, `week-08`).
- **Chủ đề tuần học**: Tên chủ đề theo syllabus (ví dụ: "Cursor Pagination", "Idempotency Pattern", "Partial Updates & Field Masks").
- **Ghi chú bài giảng của sinh viên**: Những điểm thầy cô đặc biệt nhấn mạnh trên lớp, các lưu ý riêng hoặc yêu cầu đặc thù của giảng viên.

## 4. Output Mong Đợi
Một bản tóm tắt tri thức sàng lọc có cấu trúc rõ ràng:
1. **Core Problem (Vấn đề hệ thống)**: Các lỗi sai phổ biến (failure modes), thắt nút cổ chai (bottlenecks), hoặc race conditions khi thiết kế ngây thơ (naive implementation).
2. **Architectural Pattern**: Bản chất giải pháp kiến trúc trong sách *API Design Patterns* (JJ Geewax).
3. **Product & DX Mindset**: Góc nhìn trải nghiệm lập trình viên và quản trị sản phẩm từ sách *Building an API Product* (Bruno Pedro).
4. **Chuẩn hóa thuật ngữ**: Bảng thuật ngữ song ngữ Việt - Anh trích từ `glossary-soa.md`.
5. **2-3 Đề xuất Kịch bản Nghiệp vụ thực tế (Business Scenarios)**: Ví dụ các bài toán gần gũi (E-commerce, FinTech, IoT, Logistics...) để sinh viên lựa chọn làm bài thực hành xuyên suốt tuần.

## 5. Quy Trình Thực Hiện
1. **Đọc tài liệu chuẩn**:
   - Mở [`.agents/context/syllabus.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/syllabus.md) để xác định mục tiêu tuần.
   - Mở [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md) để trích xuất pattern tương ứng.
   - Mở [`.agents/context/building-api-product-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/building-api-product-notes.md) để lấy góc nhìn sản phẩm và DX.
   - Mở [`.agents/context/glossary-soa.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/glossary-soa.md) để lấy thuật ngữ chuẩn.
2. **Tổng hợp & Chắt lọc**:
   - Loại bỏ chi tiết rườm rà, tập trung vào bản chất kiến trúc và các cạm bẫy hệ thống.
   - Thiết kế 2-3 kịch bản nghiệp vụ có tính ứng dụng cao.
3. **Logic Gate 1 (Dừng lại để Sinh viên phê duyệt)**:
   - LLM xuất bản Digest kèm câu hỏi:
     > *"Bạn hãy đối chiếu với nội dung thầy/cô giảng trên lớp: Tri thức cốt lõi này đã đúng trọng tâm chưa? Bạn chọn kịch bản nghiệp vụ nào trong 3 kịch bản trên (hoặc muốn đề xuất kịch bản riêng)?"*
   - **Bắt buộc dừng lại** để sinh viên phản hồi và chốt trước khi chuyển sang Chặng 2.
