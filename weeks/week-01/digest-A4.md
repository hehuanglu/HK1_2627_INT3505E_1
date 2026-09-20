# Knowledge Digest — Tuần 01: Giới Thiệu API, Web Services & REST Fundamentals
> Ngày: 2026-09-16 | Dự án: Fast Food Ordering & Management API (`project/`)

---

## 1. Core Concept

**Vấn đề hệ thống**:
> Các hệ thống phần mềm nguyên khối (Monolith) tích hợp phân mảnh, phụ thuộc chặt chẽ vào ngôn ngữ và cơ sở dữ liệu nội bộ, khiến việc mở rộng tính năng và kết nối với các ứng dụng vệ tinh (Mobile, Đối tác) dễ gây đổ vỡ diện rộng khi có thay đổi.

**Cơ chế pattern**:
- Kiến trúc hướng dịch vụ (SOA) chia nhỏ hệ thống thành các đơn vị tự trị (Services), phơi bày năng lực qua mạng thông qua bản Hợp đồng dịch vụ (Service Contract) chuẩn hóa.
- REST (Representational State Transfer) là phong cách kiến trúc định hướng tài nguyên (Resource-Oriented) với 6 ràng buộc: Client-Server, Stateless, Cacheable, Layered System, Uniform Interface, Code on Demand.
- Tách biệt rõ ngữ cảnh giao tiếp: SOAP cho giao dịch ngân hàng/enterprise nghiêm ngặt; gRPC cho giao tiếp nội bộ tốc độ cao (East-West); REST cho cổng công cộng đa nền tảng (North-South).
- Chuyển dịch từ tư duy cục bộ "API = hàm + URL" sang "API-as-a-Product" lấy trải nghiệm lập trình viên (DX) làm trung tâm.

**Thuật ngữ chuẩn**:
| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Service Contract | Hợp đồng dịch vụ | Bản đặc tả chuẩn hóa giao thức, schema và ràng buộc (OpenAPI, WSDL, Proto). |
| Loose Coupling | Khớp nối lỏng | Thay đổi nội bộ một dịch vụ không làm đứt gãy các consumer gọi tới. |
| Developer Experience (DX) | Trải nghiệm lập trình viên | Tháp nhu cầu: Functionality $\to$ Reliability $\to$ Usability $\to$ Delight (TTFHW < 5m). |

---

## 2. Evidence (Minh Chứng Thực Nghiệm)

**Use Case thực hành**: Quản lý danh mục Sách (CRUD Books API) & Validation ràng buộc nghiệp vụ (`weeks/week-01/practice/app.py`).

**Request/Response thực tế**:
```http
POST /books HTTP/1.1
Host: 127.0.0.1:5001
Content-Type: application/json

{
  "title": "The Pragmatic Programmer",
  "author": "Andy Hunt",
  "year": 1999
}

HTTP/1.1 201 CREATED
Location: /books/2
Content-Type: application/json

{
  "id": 2,
  "title": "The Pragmatic Programmer",
  "author": "Andy Hunt",
  "year": 1999
}
```

**Test Client result**:
```
[PASS] POST /books (Valid Year 1999) -> 201 CREATED with Location Header: /books/2
[PASS] POST /books (Invalid Year 1850) -> 400 BAD REQUEST {"error": "Field 'year' must be an integer >= 1900"}
[PASS] GET /books?q=pragmatic -> 200 OK (Found 1 book)
```

**Bài học kiến trúc từ audit**:
> Thao tác đọc dữ liệu bắt buộc phải dùng `GET` để đảm bảo tính an toàn (Safety), khả năng cache và tránh N+1 network calls. Mọi validation nghiệp vụ (như `year >= 1900`) phải chặn ngay tại tầng biên với mã `400 Bad Request`, không để lọt exception gây lỗi `500`.

---

## 3. Homework Lesson

**Bài tập**: Khảo sát 3 Public API (GitHub, Spotify, OpenWeather), so sánh 5 đặc điểm API giữa Slide 05 với Higginbotham & Geewax Ch.1, và lập trình Flask CRUD hoàn thiện kèm tìm kiếm, sắp xếp và kiểm soát dữ liệu `year >= 1900`.

**Lỗi/Điểm yếu phát hiện**:
- **Pattern**: Đặt nhầm `POST` cho route truy vấn danh sách (`list_books`), vi phạm tính an toàn và khả năng cache của HTTP GET; gộp chung PUT và DELETE vào một handler làm giảm tính rành mạch của kiến trúc.
- **Status codes**: Chưa kiểm soát ngoại lệ đầu vào dẫn đến nguy cơ lỗi 500 thay vì trả về `400 Bad Request` tường minh.
- **Race condition**: Sử dụng biến đếm ID nguyên tự tăng trong bộ nhớ có thể xung đột dữ liệu khi có nhiều worker xử lý đồng thời (nên dùng UUID).
- **DX**: Cần thông báo lỗi cụ thể chỉ đích danh trường bị sai (`field 'year'`) để lập trình viên client dễ dàng sửa lỗi.

**Câu trả lời cho câu hỏi Socratic quan trọng nhất**:
> Việc kiểm tra hợp lệ tại tầng biên và trả về `400 Bad Request` giúp client lập tức nhận diện lỗi sai từ request của mình để tự điều chỉnh (Actionable Error), đồng thời bảo vệ server backend khỏi tình trạng dữ liệu sai lệch hoặc sập dịch vụ không đáng có.

---

## 4. Industry Application

Các công ty xây dựng **LLM-powered API products** (OpenAI API, Google Gemini API, Anthropic API) áp dụng tư duy API-as-a-Product triệt để: họ coi developer là khách hàng chính, đo lường Time-to-First-Hello-World (TTFHW), và thiết kế onboarding để developer gọi được API đầu tiên trong < 5 phút. REST thống trị vì đơn giản và stateless — phù hợp cho LLM inference API vốn không cần duy trì session giữa các request.

---

## 5. Creative LLM Idea

**Ý tưởng**: LLM-Assisted TTFHW Auditor & Interactive Onboarding Assistant.

**Mô tả chi tiết**:
> Sử dụng LLM (Gemini 1.5 / Claude) đóng vai một lập trình viên mới tiếp cận API lần đầu. LLM tự động đọc tài liệu đặc tả OpenAPI, sinh mã gọi thử nghiệm (curl / Python), đo lường thời gian tích hợp giả lập và tự động phát hiện những điểm gây hiểu nhầm (cognitive friction) trong tài liệu để tối ưu chỉ số TTFHW xuống dưới 5 phút.

**Kết quả thực nghiệm**:
> Ý tưởng khả thi, có thể tích hợp dưới dạng script kiểm thử DX tự động trong CI/CD pipeline ở các tuần tiếp theo.

**Liên kết `creative-log.md`**: Ý tưởng này đã được ghi nhận vào `creative-log.md` (Tuần 01 — LLM-Assisted TTFHW Auditor).
