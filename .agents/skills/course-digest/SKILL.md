---
name: course-digest
description: Trích xuất và tổng hợp tri thức cốt lõi từ tài liệu học tập (JJ Geewax, Bruno Pedro, SOA Glossary) theo chủ đề tuần để làm đầu vào cho slide và code.
---

# Kỹ Năng: Course Digest (Tổng Hợp Ngữ Cảnh Học Tập)

## 1. Tên Kỹ Năng
**course-digest** (Trích xuất & Tổng hợp tri thức tuần học)

## 2. Khi Nào Kích Hoạt
Kích hoạt kỹ năng này khi:
- Sinh viên cung cấp tên chủ đề tuần học mới (ví dụ: "Tuần 2: Resource-Oriented Design & Standard Methods", "Tuần 4: Custom Methods & Long-Running Operations", "Tuần 7: Pagination & Filtering", v.v.).
- Bắt đầu quy trình chuẩn bị bài giảng hoặc bài tập tuần mới trước khi viết slide hay viết code.
- Cần tra cứu nhanh lý thuyết và cơ sở khoa học để đối chiếu một bài toán thiết kế API cụ thể với 2 giáo trình môn học.

## 3. Input Mong Đợi
- **Chủ đề tuần học**: Tên chủ đề hoặc từ khóa nghiệp vụ (ví dụ: "Pagination", "Idempotency", "Partial Update với Field Mask").
- **Số thứ tự tuần**: `week-XX` (ví dụ: `week-01`, `week-02`).
- **Yêu cầu bổ sung của giảng viên (nếu có)**: Tập trung vào khía cạnh thiết kế hay khía cạnh kinh doanh/sản phẩm.

## 4. Output Mong Đợi
Một bản tóm tắt tri thức kỹ thuật cô đọng (dưới dạng văn bản hoặc block markdown), đóng vai trò làm ngữ cảnh đầu vào (prompt context) chuẩn xác cho 2 kỹ năng kế tiếp (`weekly-slide-outline` và `api-code-scaffold`). Bản digest gồm 4 phần:
1. **Khái niệm & Pattern tương ứng** trong sách *API Design Patterns* (JJ Geewax).
2. **Góc nhìn Quản trị Sản phẩm & Trải nghiệm Lập trình viên (DX)** từ sách *Building an API Product* (Bruno Pedro).
3. **Thuật ngữ chuẩn xác** trích từ `glossary-soa.md`.
4. **Ràng buộc kỹ thuật & lưu ý triển khai** cho tuần học đó.

## 5. Các Bước Xử Lý
1. **Phân tích chủ đề**: Tách các từ khóa chính trong chủ đề sinh viên yêu cầu (ví dụ: "Pagination" -> Cursor-based, Token, PageSize, SQL OFFSET vs Index).
2. **Truy vấn chéo tài liệu trong `.agents/context/`**:
   - Mở và đọc file [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md): Tìm các mục pattern liên quan trực tiếp đến từ khóa.
   - Mở và đọc file [`.agents/context/building-api-product-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/building-api-product-notes.md): Tìm các khía cạnh về vòng đời, trải nghiệm DX, thiết kế hợp đồng Spec-First, hoặc bảo mật liên quan.
   - Mở và đọc file [`.agents/context/glossary-soa.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/glossary-soa.md): Trích xuất định nghĩa tiếng Việt & thuật ngữ tiếng Anh chuẩn hóa để dùng nhất quán trong slide và code.
3. **Tổng hợp & Chắt lọc**:
   - Loại bỏ các chi tiết thừa thãi không thuộc phạm vi tuần học.
   - Định dạng thông tin rõ ràng theo cấu trúc: Vấn đề hệ thống gặp phải -> Bản chất giải pháp (Pattern) -> Lợi ích kiến trúc và DX -> Rủi ro nếu làm sai.
4. **Bàn giao dữ liệu**: Xuất nội dung digest sẵn sàng chuyển tiếp cho kỹ năng `weekly-slide-outline` và `api-code-scaffold`.

## 6. Nguồn Dữ Liệu Cần Đọc
- [`.agents/context/api-design-patterns-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/api-design-patterns-notes.md)
- [`.agents/context/building-api-product-notes.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/building-api-product-notes.md)
- [`.agents/context/glossary-soa.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/glossary-soa.md)
