---
name: weekly-slide-outline
description: Tạo dàn ý và nội dung slide bài giảng tuần theo cấu trúc chuẩn sư phạm (Khái niệm -> Vấn đề -> Ví dụ -> So sánh) và lưu vào weeks/week-XX/slide.md.
---

# Kỹ Năng: Weekly Slide Outline (Sinh Dàn Ý & Nội Dung Slide Thuyết Trình)

## 1. Tên Kỹ Năng
**weekly-slide-outline** (Sinh slide thuyết trình hàng tuần)

## 2. Khi Nào Kích Hoạt
Kích hoạt kỹ năng này khi:
- Đã có bản tổng hợp tri thức từ kỹ năng `course-digest`.
- Sinh viên yêu cầu soạn slide thuyết trình cho một tuần cụ thể (`week-XX`).
- Cần cấu trúc lại bài nói trên lớp cho sinh viên để thuyết phục giảng viên và các bạn học về lý do chọn giải pháp/pattern thiết kế.

## 3. Input Mong Đợi
- **Bản tổng hợp tri thức tuần**: Output từ kỹ năng `course-digest`.
- **Số thứ tự tuần**: `week-XX` (ví dụ `weeks/week-01`, `weeks/week-02`).
- **Thời lượng dự kiến hoặc số slide mục tiêu**: Thông thường từ 10 đến 15 slide cho một buổi seminar 15-20 phút.

## 4. Output Mong Đợi
File markdown hoàn chỉnh tại đường dẫn: `weeks/week-XX/slide.md` (hỗ trợ định dạng phân tách slide Marp bằng dấu `---`).
Nội dung slide phải đảm bảo đủ 4 trục trụ cột:
1. **Khái niệm (Concept)**: Định nghĩa tường minh, ngôn ngữ chuẩn mực, trích dẫn chuẩn pattern từ JJ Geewax hoặc Bruno Pedro.
2. **Vấn đề nó giải quyết (Problem Statement)**: Sự đau khổ (pain point) của hệ thống nếu không dùng pattern này (lỗi xung đột, timeout, rò rỉ dữ liệu, trải nghiệm lập trình viên tồi tệ).
3. **Ví dụ minh họa (Concrete Example)**: Kịch bản đời thực (E-commerce, Banking, Ride-hailing), kèm flow request/response hoặc diagram đơn giản.
4. **So sánh với pattern liên quan (Trade-offs & Alternatives)**: Bảng đối chiếu ưu/nhược điểm so với giải pháp ngây thơ (naive approach) hoặc pattern tương đương.

## 5. Các Bước Xử Lý
1. **Xác định đường dẫn đích**: Kiểm tra và tạo thư mục `weeks/week-XX/` nếu chưa có. Đích đến là `weeks/week-XX/slide.md`.
2. **Khung cấu trúc Slide (Slide Deck Structure)**:
   - **Slide 1**: Trang bìa (Tên chủ đề tuần, Mã môn học SOA - UET, Người trình bày).
   - **Slide 2**: Mục tiêu bài học & Agenda (Tổng quan nội dung sẽ đi qua).
   - **Slide 3 - 4 (Khái niệm)**: Bản chất kỹ thuật của Pattern / Chủ đề. Nêu rõ thuật ngữ tiếng Anh và tiếng Việt.
   - **Slide 5 - 6 (Vấn đề cần giải quyết)**: Các lỗi sai thường gặp khi thiết kế "ngây thơ", rủi ro về hiệu năng, bảo mật hoặc tính mở rộng.
   - **Slide 7 - 9 (Giải pháp & Thiết kế chi tiết)**: Kiến trúc giải pháp theo chuẩn JJ Geewax (Cấu trúc URI, HTTP Verbs, Header, Request/Response payload, Mã trạng thái HTTP).
   - **Slide 10 - 11 (Ví dụ thực tế)**: Kịch bản áp dụng với dữ liệu cụ thể (kết nối trực tiếp tới phần demo code sắp tới).
   - **Slide 12 (So sánh & Trade-offs)**: Bảng so sánh (Ưu điểm, Nhược điểm, Khi nào nên dùng và Khi nào KHÔNG nên dùng).
   - **Slide 13 (Góc nhìn API-as-a-Product)**: Tác động của pattern này tới Developer Experience (DX) theo Bruno Pedro.
   - **Slide 14**: Tổng kết & Câu hỏi thảo luận (Q&A cho cả lớp).
3. **Chèn Speaker Notes**: Trong mỗi slide markdown, thêm phần ghi chú người thuyết trình (`<!-- Note: ... -->`) giải thích những ý sinh viên cần nói bằng lời trên lớp mà không đưa hết chữ lên slide.
4. **Ghi file**: Dùng công cụ ghi file vào `weeks/week-XX/slide.md`.

## 6. Nguồn Dữ Liệu Cần Đọc
- [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md)
- [`.agents/context/building-api-product-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/building-api-product-notes.md)
- [`.agents/context/glossary-soa.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/glossary-soa.md)
