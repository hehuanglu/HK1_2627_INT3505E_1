---
marp: true
theme: default
paginate: true
size: 16:9
header: "VNU-UET | Service-Oriented Architecture (SOA)"
footer: "Khoa CNTT | Department of Software Engineering"
style: |
  section {
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    font-size: 24px;
    padding: 40px 50px;
    color: #1a1a1a;
  }
  h1 { color: #003366; font-size: 36px; margin-bottom: 16px; }
  h2 { color: #006699; font-size: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; margin-bottom: 16px; }
  h3 { color: #003366; font-size: 24px; margin-bottom: 8px; }
  ul, ol { font-size: 22px; line-height: 1.6; }
  li { margin-bottom: 6px; }
  code { font-family: 'Consolas', 'JetBrains Mono', monospace; font-size: 18px; background: #f3f3f3; padding: 2px 6px; border-radius: 3px; color: #c7254e; }
  pre { background: #1e1e1e; color: #d4d4d4; border-radius: 6px; padding: 16px 20px; font-size: 18px; line-height: 1.5; }
  pre code { background: transparent; color: #d4d4d4; padding: 0; }
  table { font-size: 20px; width: 100%; border-collapse: collapse; }
  th { background-color: #003366; color: white; padding: 8px 12px; text-align: left; }
  td { padding: 6px 12px; border-bottom: 1px solid #e0e0e0; }
  tr:nth-child(even) td { background-color: #f8f9fa; }
  blockquote { border-left: 4px solid #006699; background: #f0f7ff; padding: 10px 16px; margin: 12px 0; font-style: italic; color: #003366; }
  footer, header { font-size: 13px; color: #999999; }
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# Tuần 00: Nhập Môn Kiến Trúc Hướng Dịch Vụ (SOA)
### Tổng Quan Môn Học, Khái Niệm Nền Tảng & Resource Naming
**Giảng viên / Nhóm báo cáo:** Bộ môn Công nghệ Phần mềm  
**Khoa Công nghệ Thông tin - Trường ĐH Công nghệ (VNU-UET)**

<!-- Note: Chào mừng các bạn sinh viên đến với học phần Kiến trúc hướng dịch vụ (SOA). Hôm nay là buổi mở đầu (Week 00) nhằm định hình bức tranh toàn cảnh của môn học, hiểu rõ bản chất của SOA trong kỷ nguyên Cloud-Native và tiếp cận quy tắc thiết kế tài nguyên chuẩn công nghiệp. -->

---

## Mục Tiêu & Kế Hoạch Bài Học (Agenda)

1. **Bản chất Kiến trúc SOA**: Tại sao monolithic chuyển dịch sang hướng dịch vụ?
2. **Nguyên lý cốt lõi**: Khớp nối lỏng (Loose Coupling) và Hợp đồng dịch vụ (Service Contract).
3. **Tư duy API-as-a-Product**: Tháp nhu cầu API và Developer Experience (DX).
4. **Mẫu thiết kế Resource Naming (JJ Geewax)**: Chuẩn hóa URI danh từ, số nhiều và phân cấp.
5. **Mã nguồn minh họa**: Dịch vụ `Course Service` chuẩn RESTful API.
6. **So sánh & Đánh giá**: RPC/Chữ ký hàm truyền thống vs. Resource-Oriented Design.
7. **Định hướng thực hành**: Bộ công cụ học tập (OpenAPI, Postman, Newman, Express).

<!-- Note: Nhấn mạnh vào tính chuyển giao từ tư duy lập trình hàm sang tư duy thiết kế hệ thống phân tán hướng dịch vụ. -->

---

## 1. Khái Niệm: Kiến Trúc Hướng Dịch Vụ (SOA)

- **Định nghĩa (SOA - Service-Oriented Architecture)**:
  > Phong cách kiến trúc phần mềm trong đó các chức năng ứng dụng được chia thành các đơn vị dịch vụ độc lập (**Services**), cung cấp năng lực cho nhau thông qua các giao thức mạng chuẩn hóa.
- **3 vai trò trọng yếu trong tam giác SOA**:
  - **Service Provider (Bên cung cấp)**: Triển khai và công bố dịch vụ.
  - **Service Consumer / Client (Bên tiêu thụ)**: Tìm kiếm và kích hoạt dịch vụ.
  - **Service Registry / Contract (Hợp đồng)**: Cầu nối xác lập luật chơi chung.

<!-- Note: Nhắc lại mô hình Provider-Consumer. Trong Web API hiện đại, OpenAPI chính là bản hợp đồng này. -->

---

## 1. Khái Niệm: Khớp Nối Lỏng & Hợp Đồng Dịch Vụ

### Nguyên lý vàng: Loose Coupling (Khớp nối lỏng)
- Các thành phần phụ thuộc tối thiểu vào nhau.
- Service Provider có thể thay đổi cơ sở dữ liệu từ SQL sang NoSQL, đổi ngôn ngữ từ Java sang Node.js mà **không làm gãy Client**.

### Điều kiện tiên quyết: Service Contract (Hợp đồng dịch vụ)
- Hợp đồng quy định: Định dạng trao đổi (`application/json`), các tham số đầu vào, mã trạng thái HTTP trả về (`200`, `201`, `400`, `404`).
- Trong môn học này: **OpenAPI Specification (OAS 3.0.3)** là hợp đồng chuẩn.

<!-- Note: Nhấn mạnh rằng thay đổi logic nội bộ không sao, nhưng phá vỡ hợp đồng (breaking change) sẽ làm sụp đổ toàn bộ hệ sinh thái phụ thuộc. -->

---

## 2. Vấn Đề: Lối Mòn Thiết Kế "Ngây Thơ" (Naive Design)

### Những sai lầm thường gặp khi bắt đầu làm Web API:
- **Lẫn lộn hành động vào URI**:
  - `POST /api/getCourseById`
  - `GET /api/deleteCourse?id=123`
  - `POST /api/create_new_course_record`
- **Hậu quả hệ thống**:
  - Client không thể đoán định (lack of predictability).
  - Vi phạm tính an toàn và lũy kế của HTTP (dùng `GET` để xóa dữ liệu).
  - Tài liệu API nhanh chóng trở thành "bãi rác" không thể bảo trì tự động.

<!-- Note: Cho sinh viên thấy sự hỗn loạn khi 10 lập trình viên trong một nhóm tự đặt tên endpoint theo thói quen cá nhân. -->

---

## 2. Vấn Đề: Khủng Hoảng Trải Nghiệm Lập Trình Viên (DX)

### Theo Bruno Pedro (*Building an API Product*):
- API không chỉ là cổng truyền bit; API là một **Sản phẩm (Product)** có khách hàng mục tiêu là **Lập trình viên (Developers)**.
- **Triệu chứng của một API thất bại**:
  - Không có thông báo lỗi rõ ràng (luôn trả `200 OK` kèm `{"error": "something went wrong"}`).
  - Thời gian tạo cuộc gọi đầu tiên (TTFHW - Time To First Hello World) kéo dài hàng tuần.
  - Client phải đọc mã nguồn backend mới biết payload cần truyền những gì!

<!-- Note: Đặt câu hỏi cho sinh viên: Nếu Stripe hoặc GitHub API không có tài liệu chuẩn, liệu có ai sử dụng dịch vụ của họ không? -->

---

## 3. Giải Pháp: Mẫu Thiết Kế Resource Naming (JJ Geewax)

### Quy tắc chuẩn hóa danh mục tài nguyên:
1. **Dùng Danh từ số nhiều** đại diện cho tập hợp (Collection):
   - `/courses`, `/students`, `/registrations`
2. **Định danh cụ thể** bằng ID trực thuộc danh từ số nhiều:
   - `/courses/{courseId}` (Ví dụ: `/courses/soa-uet`)
3. **Ánh xạ hành vi qua HTTP Verbs chuẩn**:
   - `GET /courses` $\rightarrow$ Liệt kê danh sách học phần (List).
   - `POST /courses` $\rightarrow$ Đăng ký/Tạo mới học phần (Create).
   - `GET /courses/{id}` $\rightarrow$ Xem chi tiết (Get).
   - `DELETE /courses/{id}` $\rightarrow$ Hủy học phần (Delete).

<!-- Note: Giải thích lý do tại sao không dùng động từ trong URI RESTful chuẩn. HTTP Verbs đã mang ngữ nghĩa của hành động. -->

---

## 3. Cấu Trúc URI & Payload Mẫu (Course Service)

### Endpoint: `POST /api/v1/courses` (Tạo mới học phần)
- **HTTP Header**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "code": "INT3111",
  "title": "Service-Oriented Architecture",
  "credits": 3,
  "department": "Software Engineering"
}
```
- **Response Status**: `201 Created`
- **Location Header**: `/api/v1/courses/65e5f1...`

<!-- Note: Chú ý mã 201 Created thay vì 200 thông thường. Đây là chỉ dấu trực quan cho client biết tài nguyên mới đã được ghi nhận. -->

---

## 4. Minh Họa Mã Nguồn: Express.js Controller

```javascript
// POST /api/v1/courses - Resource Creation Pattern
app.post('/api/v1/courses', async (req, res) => {
  const { code, title, credits, department } = req.body;
  if (!code || !title || !credits) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  const course = await Course.create({ code, title, credits, department });
  return res.status(201).json(course);
});

// GET /api/v1/courses/:id - Single Resource Access
app.get('/api/v1/courses/:id', async (req, res) => {
  const course = await Course.findById(req.params.id);
  if (!course) return res.status(404).json({ error: 'Course not found' });
  return res.status(200).json(course);
});
```

<!-- Note: Chỉ ra tính mạch lạc: đường dẫn ngắn gọn, tập trung vào tài nguyên Course, mã lỗi tường minh (400, 404, 201). -->

---

## 5. So Sánh & Đánh Giá Đánh Đổi (Trade-offs)

| Tiêu chí so sánh | Phong cách RPC Cổ Điển | Hướng Tài Nguyên (Resource-Oriented) |
| :--- | :--- | :--- |
| **Mô hình URI** | Hỗn hợp động từ (`/doAction`) | Thuần danh từ số nhiều (`/resources`) |
| **Khả năng Cache** | Kém (hầu hết dùng POST) | Tối ưu tuyệt đối với HTTP Caching (GET) |
| **Tính nhất quán (DX)** | Thấp, phụ thuộc cá nhân | Cao, tuân theo quy chuẩn toàn cầu |
| **Hành vi phi thực thể** | Tự nhiên (như gọi hàm) | Cần Custom Method (`/resource:action`) |
| **Áp dụng tối ưu** | Streaming, tính toán thuần | CRUD nghiệp vụ, Quản lý dữ liệu hệ thống |

<!-- Note: Phân tích khách quan: Resource-Oriented không phải là vạn năng, nhưng nó là xương sống của 90% Web APIs thương mại hiện nay. -->

---

## 6. Góc Nhìn API-as-a-Product (Bruno Pedro)

### Tháp Nhu Cầu API (API Hierarchy of Needs):
1. **Functionality**: API tạo và truy xuất được học phần.
2. **Reliability**: Phản hồi ổn định < 50ms, không crash server khi lỗi input.
3. **Usability**: Tên trường nhất quán (`camelCase`), mã lỗi có cấu trúc.
4. **Delight (DX)**: Cung cấp đầy đủ file OpenAPI (`openapi.yaml`) và Postman Collection sẵn kịch bản chạy thử (TTFHW < 2 phút).

> *"Đừng bắt người tiêu dùng dịch vụ phải đoán xem hệ thống của bạn hoạt động thế nào."*

<!-- Note: Nhấn mạnh đây là lý do môn học bắt buộc phải có đầy đủ OpenAPI Contract và Postman Test Suite đi kèm mỗi bài lab. -->

---

## 7. Khung Công Cụ Cho Sinh Viên

- **Thiết kế hợp đồng**: Viết bản đặc tả `openapi.yaml` theo chuẩn OpenAPI 3.0.3.
- **Phát triển dịch vụ**: Node.js + Express + Mongoose (nguyên lý KISS).
- **Kiểm thử tự động**:
  - Dùng Postman để khám phá trực quan.
  - Dùng Newman CLI chạy kiểm thử hồi quy trên terminal:
    ```bash
    newman run postman_collection.json
    ```
- **Tài liệu hóa**: Render slide bằng Marp CLI.

<!-- Note: Hướng dẫn sinh viên tự tin làm chủ bộ công cụ chuyên nghiệp phục vụ cho các đồ án sau này. -->

---

<!-- _class: lead -->

## Tổng Kết Tuần 00 & Thảo Luận

### Ghi nhớ cốt lõi:
1. **SOA** là kiến trúc phân rã chức năng dựa trên **Khớp nối lỏng** và **Hợp đồng**.
2. **Resource Naming** biến URI thành danh mục tài nguyên có trật tự, dễ đoán.
3. Luôn coi **API là một sản phẩm** phục vụ lập trình viên.

**Hỏi & Đáp (Q&A) - Chuẩn bị môi trường cho Tuần 01**
