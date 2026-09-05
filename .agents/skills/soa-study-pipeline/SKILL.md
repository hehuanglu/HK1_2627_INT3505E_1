---
name: soa-study-pipeline
description: Master skill điều phối toàn diện quy trình 5 chặng học tập SOA (Sàng lọc kiến thức -> Implement hạt nhân -> Audit mã nguồn -> Nghiệm thu snapshot -> Thiết kế slide minh chứng) với các điểm dừng (Logic Gates) phê duyệt của sinh viên.
---

# Master Skill: SOA Study Pipeline (Quy Trình Học Tập 5 Chặng Tương Tác)

## 1. Tuyên Ngôn Triết Lý & Vai Trò
- **Mục tiêu**: Giúp sinh viên học thật, hiểu sâu bản chất kiến trúc và làm được thật, tuyệt đối không tạo ra sự "trôi tuột" kiến thức hay sự phụ thuộc thụ động vào AI.
- **Hạt nhân định hướng**: Bài giảng của thầy cô trên lớp và hệ thống tài liệu chuẩn mực (`.agents/context/`: JJ Geewax, Bruno Pedro, Glossary SOA).
- **Phân vai rõ ràng**:
  - **Sinh viên**: Đóng vai trò hạt nhân với **Tư duy thiết kế kiến trúc sâu (Deep Thinking)**, tự tay hiện thực hóa (implement) các khối logic hạt nhân, phản biện và ra quyết định phê duyệt tại từng chặng.
  - **LLM**: Đóng vai trò người cộng sự/trợ giảng cao cấp với **Tư duy phản biện (Critical Thinking)**, đặt câu hỏi gợi mở, loại bỏ các gánh nặng phi nghiệp vụ (scaffold, DB setup boilerplate), audit mã nguồn, tự động nghiệm thu lấy minh chứng, và hỗ trợ soạn thảo slide bài giảng chuẩn mực.

---

## 2. Sơ Đồ Tổng Quan 5 Chặng & Logic Gates

```
[Bài giảng & Sách tham khảo]
            │
            ▼
┌────────────────────────────────────────────────────────┐
│  Chặng 1: SÀNG LỌC KIẾN THỨC (course-digest)           │
│  - LLM: Trích xuất Core Concept + Đề xuất Scenarios    │
│  - SV: Đối chiếu bài giảng thầy cô, chọn bài toán      │
│  ==> LOGIC GATE 1: Sinh viên bấm duyệt tri thức gốc   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  Chặng 2: IMPLEMENT HẠT NHÂN (api-code-scaffold)       │
│  - LLM: Giải thích bối cảnh, phản biện, dựng Scaffold  │
│  - SV: Tranh luận thông suốt kiến trúc -> Tự code TODO │
│  ==> LOGIC GATE 2: SV xác nhận code hạt nhân hoàn tất  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  Chặng 3: AUDIT & TỐI ƯU MÃ NGUỒN (Architectural Review)│
│  - LLM: Phản biện mã nguồn SV, chỉ ra rủi ro hệ thống  │
│  - SV: Thảo luận, tiếp thu và chốt phiên bản code tối ưu│
│  ==> LOGIC GATE 3: Chốt mã nguồn hoàn thiện cuối cùng  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  Chặng 4: NGHIỆM THU & SNAPSHOT (openapi + postman)     │
│  - LLM: Sinh Spec OAS 3.0.3, chạy test tự động         │
│  - LLM: Snapshot logs, request/response, test pass     │
│  ==> LOGIC GATE 4: Đủ bằng chứng thực nghiệm tin cậy   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  Chặng 5: THIẾT KẾ SLIDE MINH CHỨNG (weekly-slide)     │
│  - LLM: Tổng hợp lý thuyết + code + snapshot thực tế   │
│  - LLM: Soạn draft slide.md (Core takeaways, no fluff) │
│  - SV: Duyệt kết luận & khuyến nghị -> Xuất slide.pdf  │
│  ==> FINISH: Hoàn thành tuần học với đầy đủ học liệu   │
└────────────────────────────────────────────────────────┘
```

---

## 3. Quy Trình Điều Phối Chi Tiết Từng Chặng

### Chặng 1: Sàng Lọc Kiến Thức (Knowledge Filtering & Alignment)
- **Kỹ năng kích hoạt**: `course-digest`
- **Hành động của LLM**:
  1. Đọc `.agents/context/syllabus.md`, `api-design-patterns-notes.md`, `building-api-product-notes.md`, `glossary-soa.md`.
  2. Tổng hợp ngắn gọn:
     - Vấn đề hệ thống (Failure Modes nếu thiết kế non nớt).
     - Bản chất Pattern giải quyết vấn đề đó thế nào.
     - Lợi ích sản phẩm & Developer Experience (DX).
     - Thuật ngữ chuẩn xác (Việt - Anh).
  3. Đề xuất 2-3 kịch bản nghiệp vụ thực tế (ví dụ: E-commerce Order, IoT Tracking, Banking Ledger).
- **Hành động của Sinh viên**:
  - Đối chiếu với bài giảng của giảng viên trên lớp tuần đó.
  - Chọn 1 kịch bản nghiệp vụ mong muốn hoặc đưa ra kịch bản của riêng mình.
- **Logic Gate 1 (Bắt buộc dừng)**:
  - LLM dừng lại và hỏi: *"Bạn hãy xác nhận kịch bản nghiệp vụ và định hướng lý thuyết trên đã khớp với nội dung bài học trên lớp chưa?"*.
  - Chỉ khi sinh viên phản hồi xác nhận hoặc điều chỉnh xong, LLM mới chuyển sang Chặng 2.

---

### Chặng 2: Thiết Kế Kiến Trúc & Implement Hạt Nhân (Scaffold + Deep Thinking)
- **Kỹ năng kích hoạt**: `api-code-scaffold`
- **Hành động của LLM**:
  1. Mô tả luồng kiến trúc (Architecture Context): Request vào đâu, qua middleware nào, dữ liệu lưu trữ ra sao.
  2. Đặt câu hỏi phản biện kiến trúc (Critical Thinking): Ví dụ *"Tại sao trong trường hợp này ta không dùng Offset Pagination thông thường?", "Nếu mạng chập chờn client gửi lại 2 lần thì hệ thống ứng xử thế nào?"*.
  3. Khởi tạo Scaffold vào `weeks/week-XX/code/`:
     - Cấu hình `package.json`, Express server, kết nối Database mock/local.
     - Định nghĩa models, route signatures.
     - Để lại các khối `// TODO [HỌC VIÊN CÀI ĐẶT HẠT NHÂN]` kèm chú thích gợi ý thuật toán, input/output, và HTTP status code mong đợi.
- **Hành động của Sinh viên**:
  - Thảo luận, phản biện lại các câu hỏi của LLM cho đến khi thực sự hiểu thấu đáo lý do tại sao phải dùng pattern đó.
  - Mở các file mã nguồn tại `weeks/week-XX/code/`, tự tay viết code cài đặt cho các khối `TODO`.
- **Logic Gate 2 (Bắt buộc dừng)**:
  - Sinh viên thông báo đã hoàn thành phần code tự tay cài đặt (hoặc gửi đoạn code đã viết).
  - LLM kiểm tra sinh viên đã điền đầy đủ các khối TODO trước khi sang Chặng 3.

---

### Chặng 3: Audit & Tinh Chỉnh Mã Nguồn (Code Review & Progressive Feedback)
- **Hành động của LLM**:
  1. Đọc trực tiếp phần code do sinh viên tự viết tại `weeks/week-XX/code/`.
  2. Thực hiện Audit kiến trúc theo 4 tiêu chí:
     - **Tính đúng đắn của Pattern**: Đã giải quyết triệt để vấn đề gốc chưa?
     - **Xử lý ngoại lệ & Biên (Edge cases)**: Mã lỗi trả về (400, 404, 409, 500) đã chuẩn REST/SOA chưa?
     - **An toàn & Bền vững (Robustness)**: Có nguy cơ race condition, rò rỉ dữ liệu, hay sập server không?
     - **Hiệu năng & DX**: Có payload dư thừa không, header có tường minh không?
  3. Trình bày nhận xét mang tính sư phạm, giải thích *Tại sao đoạn này tốt, đoạn kia có rủi ro*, và đề xuất bản vá/tối ưu cụ thể.
- **Hành động của Sinh viên**:
  - Đọc nhận xét audit, phản hồi nếu có chỗ chưa hiểu.
  - Phê duyệt phương án tối ưu để LLM áp dụng refactor vào mã nguồn.
- **Logic Gate 3 (Bắt buộc dừng)**:
  - Sinh viên và LLM cùng đồng thuận mã nguồn đã đạt chuẩn kiến trúc sạch sẽ, tối ưu.

---

### Chặng 4: Nghiệm Thu & Lấy Minh Chứng Thực Nghiệm (Verification & Snapshots)
- **Kỹ năng kích hoạt**: `openapi-writer` & `postman-collection`
- **Hành động của LLM**:
  1. Sinh bản đặc tả chuẩn `openapi.yaml` (OpenAPI 3.0.3) khớp 100% với mã nguồn đã hoàn thiện ở Chặng 3.
  2. Tạo bộ sưu tập kiểm thử `postman_collection.json` (v2.1.0) bao gồm cả Happy Path và Edge Cases (kiểm thử lỗi).
  3. Khởi chạy thử nghiệm (qua Newman hoặc test execution nội bộ), ghi lại các **Minh chứng thực nghiệm (Snapshots)**:
     - Log console khi service xử lý logic.
     - HTTP Headers gửi đi và nhận về.
     - Response JSON payload thực tế.
     - Bảng kết quả kiểm thử Assertions Pass/Fail.
  4. Lưu trữ các snapshot này vào thư mục hoặc tài liệu trung gian làm minh chứng phục vụ bước soạn slide.
- **Hành động của Sinh viên**:
  - Quan sát các snapshot và kết quả kiểm thử.
  - Kiểm tra xem API có chạy đúng như kỳ vọng thiết kế ban đầu không.
- **Logic Gate 4 (Bắt buộc dừng)**:
  - Sinh viên xác nhận hệ thống hoạt động ổn định và các minh chứng đã đủ độ tin cậy.

---

### Chặng 5: Thiết Kế Slide Minh Chứng (Evidence-Based Slide Synthesis)
- **Kỹ năng kích hoạt**: `weekly-slide-outline`
- **Quy tắc thiết kế slide**:
  - **Không ép cứng 14 trang**: Tùy biến độ dài theo chiều sâu nội dung của tuần (thường từ 8 - 14 trang).
  - **Loại bỏ slide thừa/rác**: Tuyệt đối không đưa các slide giới thiệu đơn vị tổ chức, logo thừa, bìa phụ rườm rà.
  - **Tập trung vào giá trị cốt lõi**:
    1. Vấn đề kiến trúc thực tế (Failure scenario).
    2. Nguyên lý giải pháp (Pattern mechanism).
    3. Mã nguồn hạt nhân (trích dẫn trực tiếp từ Chặng 3).
    4. Minh chứng thực nghiệm (chèn trực tiếp snapshot từ Chặng 4: response, log, test assertion).
    5. Đánh giá đánh đổi (Trade-offs & Alternatives matrix).
    6. Kết luận cốt lõi & Khuyến nghị thực tế (Core Takeaways & Recommendations).
- **Hành động của LLM**:
  - Soạn thảo `weeks/week-XX/slide.md`.
  - Trình bày tóm tắt các **Core Takeaways & Suggestions** để sinh viên duyệt trước.
- **Hành động của Sinh viên**:
  - Đọc nội dung bản thảo, chỉnh sửa lời văn hoặc bổ sung góc nhìn cá nhân nếu cần.
  - Bấm xác nhận phê duyệt nội dung.
- **Kết thúc (Final Delivery)**:
  - LLM chạy lệnh Marp CLI xuất ra `weeks/week-XX/slide.pdf`.
  - Bàn giao trọn gói thư mục tuần học hoàn thiện cho sinh viên.

---

## 4. Bảng Tra Cứu Đầu Vào / Đầu Ra Qua Từng Chặng

| Chặng | Tên Kỹ Năng Phụ Trách | Đầu Vào | Đầu Ra | Điểm Dừng Phê Duyệt |
| :--- | :--- | :--- | :--- | :--- |
| **1. Sàng lọc** | `course-digest` | Tuần học, Giáo trình, Bài giảng SV | Bản Digest + 3 Kịch bản nghiệp vụ | Sinh viên chốt kịch bản & tri thức |
| **2. Implement** | `api-code-scaffold` | Kịch bản chặng 1 | Scaffold + File chứa TODOs | Sinh viên hoàn thành code hạt nhân |
| **3. Audit** | LLM Code Review | Mã nguồn do SV viết | Nhận xét kiến trúc + Mã nguồn tối ưu | Sinh viên duyệt phương án tối ưu |
| **4. Nghiệm thu**| `openapi-writer` & `postman-collection` | Mã nguồn chặng 3 | `openapi.yaml`, `postman_collection.json`, Snapshots log/response | Sinh viên nghiệm thu kết quả test |
| **5. Slide** | `weekly-slide-outline` | Dữ liệu chặng 1, 3, 4 | `slide.md`, Core Conclusions -> `slide.pdf` | Sinh viên duyệt nội dung -> Xuất PDF |
