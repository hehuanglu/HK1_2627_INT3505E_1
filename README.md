# Học Phần Kiến Trúc Hướng Dịch Vụ (SOA) - VNU-UET

Chào mừng bạn đến với kho lưu trữ tài liệu học tập, bài giảng và mã nguồn minh họa thực hành cho học phần **Kiến trúc hướng dịch vụ (Service-Oriented Architecture - SOA)** - Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội (VNU-UET).

Kho lưu trữ này được xây dựng theo phương pháp tiếp cận **API-First & Contract-First**, kết hợp lý thuyết thiết kế mẫu (*API Design Patterns* - JJ Geewax) và tư duy sản phẩm API (*Building an API Product* - Bruno Pedro).

---

## 1. Cấu Trúc Kho Lưu Trữ

```text
SOA/
├── README.md                 # Tài liệu hướng dẫn chung (Tiếng Việt)
├── ARCHITECTURE.md           # Sơ đồ kiến trúc & luồng sinh dữ liệu tự động
├── AGENTS.md                 # Quy tắc và hướng dẫn điều phối hệ thống Agent AI
├── slides-template/          # Mẫu slide thuyết trình chuẩn Marp (UET Theme)
├── weeks/                    # Nội dung chi tiết từng tuần học (Week 01 - Week 15)
│   └── week-XX/
│       ├── slide.md          # Slide thuyết trình dạng Markdown (hỗ trợ Marp)
│       └── code/             # Dự án mã nguồn minh họa chạy được độc lập
│           ├── openapi.yaml  # Bản hợp đồng đặc tả API chuẩn OpenAPI 3.0.3
│           ├── server.js     # Backend Express.js + Mongoose demo pattern
│           └── postman_collection.json # Bộ kịch bản kiểm thử Postman & Newman
└── .agents/                  # Hệ thống tri thức và kỹ năng tự động hóa
    ├── context/              # Cơ sở tri thức chuẩn (Syllabus, Patterns, Glossary)
    └── skills/               # Các kỹ năng sinh bài giảng tự động
```

---

## 2. Yêu Cầu Môi Trường Cài Đặt

Để chạy thử các dự án mẫu và xuất slide bài giảng, máy tính của bạn cần cài đặt sẵn:

1. **Node.js**: Phiên bản LTS `>= 18.x` ([Tải tại đây](https://nodejs.org/)).
2. **MongoDB**: Cài đặt MongoDB Community cục bộ hoặc chạy qua Docker:
   ```bash
   docker run -d -p 27017:27017 --name mongo-soa mongo:latest
   ```
3. **Newman CLI** (Công cụ chạy kiểm thử Postman tự động qua dòng lệnh):
   ```bash
   npm install -g newman
   ```
4. **Marp CLI** (Công cụ chuyển đổi slide Markdown sang PDF/HTML/PPTX):
   ```bash
   npm install -g @marp-team/marp-cli
   ```

---

## 3. Hướng Dẫn Sử Dụng Theo Tuần Học

### Chạy mã nguồn demo một tuần (Ví dụ: `week-01`):
```bash
# 1. Di chuyển vào thư mục code của tuần
cd weeks/week-01/code

# 2. Cài đặt các gói phụ thuộc
npm install

# 3. Khởi chạy máy chủ API
npm start
# Server sẽ lắng nghe tại http://localhost:3000
```

### Chạy kiểm thử tự động với Newman:
Trong khi máy chủ `server.js` đang chạy, mở terminal mới và thực thi:
```bash
newman run weeks/week-01/code/postman_collection.json
```
Kết quả kiểm thử từng kịch bản sẽ hiển thị trực tiếp trên terminal với trạng thái `PASS/FAIL`.

### Xuất Slide bài giảng sang định dạng HTML / PDF:
```bash
# Xuất sang file trình chiếu HTML tương tác
marp weeks/week-01/slide.md -o weeks/week-01/slide.html

# Xuất sang file PDF để in ấn hoặc nộp bài
marp --pdf weeks/week-01/slide.md -o weeks/week-01/slide.pdf
```

---

## 4. Danh Sách Chủ Đề Bài Giảng (15 Tuần)

Chi tiết khung chương trình và tài liệu tham khảo được cập nhật liên tục tại [`.agents/context/syllabus.md`](file:///Users/hahoangloc/Working/UET/SOA/.agents/context/syllabus.md).

* **Tuần 01**: Giới thiệu Kiến trúc SOA, Microservices & Tư duy API-as-a-Product.
* **Tuần 02**: Resource-Oriented Design & Standard Methods (List, Get, Create, Update, Delete).
* **Tuần 03**: Resource Hierarchy, Scoping & Singleton Sub-resources.
* **Tuần 04**: Partial Updates & Field Masks trong RESTful APIs.
* **Tuần 05**: Custom Methods & State Transitions.
* **Tuần 06**: Long-Running Operations (LRO) & Asynchronous Jobs.
* **Tuần 07**: Rerunnable Jobs & Idempotency Key Pattern.
* **Tuần 08**: Phân trang nâng cao: Cursor/Token-based vs. Offset/Limit.
* **Tuần 09**: Lọc dữ liệu có cấu trúc (Filtering & Structured Search).
* **Tuần 10**: Soft Deletion, Thùng rác & Phục hồi tài nguyên (Undelete).
* **Tuần 11**: Association Resources & Mô hình hóa quan hệ Many-to-Many.
* **Tuần 12**: Request Validation, Dry-Run & Safe Mutations.
* **Tuần 13**: API Versioning, Tương thích ngược & Chiến lược Deprecation.
* **Tuần 14**: API Gateway, Rate Limiting & Bảo mật phân tầng (OAuth2 / JWT).
* **Tuần 15**: Giám sát hiệu năng (Observability), Tracing phân tán & Tổng kết học phần.

---

## 5. Quy Chuẩn Đóng Góp (Contribution Guidelines)

- Mọi endpoint mẫu bắt buộc phải có tài liệu đặc tả tương ứng trong `openapi.yaml` (chuẩn 3.0.3).
- Mã nguồn minh họa tuân thủ nguyên tắc tối giản (**KISS** - Keep It Simple, Stupid), tập trung làm nổi bật pattern thiết kế và có chú thích bằng tiếng Việt.
- Tuân thủ quy trình nhánh tính năng: `git checkout -b feature/week-XX-topic`.
