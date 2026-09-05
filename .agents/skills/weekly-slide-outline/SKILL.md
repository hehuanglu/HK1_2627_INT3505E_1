---
name: weekly-slide-outline
description: Chặng 5 của quy trình học tập - Soạn thảo slide bài giảng bằng Marp dựa trên tri thức Chặng 1, mã nguồn Chặng 3 và minh chứng Chặng 4; có điểm dừng (Logic Gate 5) để sinh viên duyệt kết luận & khuyến nghị trước khi xuất PDF.
---

# Kỹ Năng: Weekly Slide Outline (Chặng 5 - Thiết Kế Slide Bài Giảng Minh Chứng)

## 1. Tên Kỹ Năng
**weekly-slide-outline** (Thiết kế slide bài giảng đúc kết từ lý thuyết và thực nghiệm)

## 2. Khi Nào Kích Hoạt
- Kích hoạt trong **Chặng 5 (Chặng cuối)** của Master Skill `soa-study-pipeline`.
- Kích hoạt sau khi đã có đầy đủ:
  - Tri thức gốc và kịch bản nghiệp vụ đã duyệt từ Chặng 1 (`course-digest`).
  - Mã nguồn hạt nhân đã audit và tối ưu từ Chặng 3.
  - Hợp đồng `openapi.yaml`, bộ test `postman_collection.json` và các Snapshot minh chứng thực nghiệm từ Chặng 4.
- Cần xuất bản phẩm bài giảng hoàn chỉnh (`slide.md` và `slide.pdf`) để thuyết trình hoặc nộp bài tập lớn/tuần.

## 3. Input Mong Đợi
- **Tri thức Chặng 1**: Vấn đề hệ thống, cơ chế Pattern, góc nhìn sản phẩm (Bruno Pedro).
- **Mã nguồn Chặng 3**: Đoạn code hạt nhân đã hoàn thiện (trực quan, ngắn gọn, súc tích).
- **Minh chứng Chặng 4**: Các snapshot Request/Response JSON, console logs, bảng kết quả test Newman.
- **Số thứ tự tuần**: `week-XX`.

## 4. Output Mong Đợi
- `weeks/week-XX/slide.md` — Bản thảo Marp Markdown tập trung vào luận điểm và minh chứng.
- `weeks/week-XX/slide.pdf` — **File PDF xuất bản chính thức** qua Marp CLI sau khi sinh viên đã duyệt.

---

## 5. Quy Chuẩn Nội Dung & Bố Cục Slide

### A. Triết Lý Nội Dung: "Substance Over Fluff" (Thực Chất & Không Slide Rác)
1. **Tuyệt đối hạn chế slide thừa**:
   - **KHÔNG** làm các slide giới thiệu đơn vị tổ chức, khoa viện, chức danh rườm rà.
   - Đi thẳng vào bài toán kỹ thuật ngay từ slide đầu tiên.
2. **Linh hoạt số lượng trang (Không ép cứng 14 trang)**:
   - Độ dài tùy biến theo chiều sâu chủ đề (thường dao động từ **8 đến 14 trang**).
   - Nếu chủ đề ngắn gọn: 8 - 10 trang cô đọng, sắc bén.
   - Nếu chủ đề phức tạp (nhiều state transition / edge cases): 12 - 14 trang chi tiết.
3. **Cấu trúc khung xương bài giảng thực chiến**:
   - **Slide 1**: Tiêu đề chủ đề & Bài toán nghiệp vụ cụ thể của tuần.
   - **Slide 2-3**: Vấn đề hệ thống (Failure modes, thắt nút cổ chai, rủi ro nếu thiết kế ngây thơ).
   - **Slide 4-5**: Cơ chế giải pháp (Pattern Architecture, luồng dữ liệu, phân vai các thành phần).
   - **Slide 6-7**: Mã nguồn hạt nhân (Trích xuất các khối logic then chốt đã lập trình ở Chặng 3).
   - **Slide 8-9**: **Minh chứng thực nghiệm (Live Snapshots)**:
     - Request Header / Body và Response thực tế từ Chặng 4.
     - Log terminal minh họa quá trình xử lý ngầm.
     - Kết quả chạy kiểm thử tự động (Newman Pass).
   - **Slide 10-11**: Ma trận đánh đổi & So sánh kiến trúc (Trade-offs, ví dụ Cursor vs Offset, Soft vs Hard Delete).
   - **Slide cuối**: **Kết luận cốt lõi & Khuyến nghị thực tế (Core Takeaways & Suggestions)**.

---

### B. Quy Chuẩn Trình Bày (Typography & Visual Standards)
- **Frontmatter Marp**:
  ```markdown
  ---
  marp: true
  theme: default
  paginate: true
  size: 16:9
  style: |
    section {
      padding: 40px 50px;
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 24px;
      color: #333;
    }
    h1 { color: #003366; font-size: 36px; margin-bottom: 20px; }
    h2 { color: #006699; font-size: 28px; border-bottom: 2px solid #006699; padding-bottom: 8px; }
    code { font-family: 'Consolas', 'JetBrains Mono', monospace; font-size: 18px; }
    pre { background: #1e1e1e !important; color: #d4d4d4; padding: 15px; border-radius: 6px; }
    table { width: 100%; border-collapse: collapse; font-size: 20px; }
    th { background: #003366; color: white; padding: 10px; }
    td { padding: 10px; border: 1px solid #ddd; }
    footer { font-size: 13px; color: #888; }
  ---
  ```
- **Mật độ thông tin**:
  - Tối đa 5 bullets/slide, mỗi bullet không quá 16 âm tiết.
  - Tối đa 1 code block hoặc 1 snapshot/slide (≤15 dòng).
  - Có presenter speaker notes (`<!-- Note: ... -->`) ở mỗi slide để sinh viên nắm lời bình khi thuyết trình.

---

## 6. Quy Trình Thực Hiện & Logic Gate 5

1. **Tổng hợp dữ liệu**:
   - LLM tập hợp kiến thức lý thuyết đã duyệt ở Chặng 1.
   - LLM trích xuất đoạn code trọng tâm từ Chặng 3.
   - LLM đưa các snapshot minh chứng thực tế từ Chặng 4 vào các slide minh họa.
2. **Soạn thảo bản thảo `slide.md`**:
   - Ghi file bản thảo ra `weeks/week-XX/slide.md`.
3. **Trích xuất Core Conclusions & Recommendations**:
   - LLM tóm lược ngắn gọn danh sách các kết luận cốt lõi và khuyến nghị rút ra từ tuần học để hiển thị trực tiếp cho sinh viên đọc.
4. **Logic Gate 5 (Bắt buộc dừng để Sinh viên phê duyệt)**:
   - LLM dừng lại và hỏi:
     > *"Bạn đã xem qua bản thảo slide và các kết luận cốt lõi (Core Takeaways) chưa? Bạn có muốn điều chỉnh câu chữ, bổ sung ghi chú thuyết trình, hay thay đổi thứ tự trang nào không?"*
   - Sinh viên xem xét, phản hồi chỉnh sửa hoặc gõ xác nhận đồng ý.
5. **Xuất bản PDF (Final Build)**:
   - Sau khi sinh viên phê duyệt, LLM kích hoạt lệnh Marp CLI:
     ```bash
     npx @marp-team/marp-cli --no-stdin weeks/week-XX/slide.md --pdf --allow-local-files -o weeks/week-XX/slide.pdf
     ```
   - Xác nhận file `slide.pdf` đã được tạo thành công.
