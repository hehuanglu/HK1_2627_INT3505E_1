# Thuật Ngữ Cốt Lõi Kiến Trúc Hướng Dịch Vụ & Thiết Kế API (SOA & API Glossary)

Bảng chú giải thuật ngữ chuẩn mực phục vụ học phần **Kiến trúc hướng dịch vụ (SOA) - VNU-UET**, tổng hợp từ các nguyên lý SOA kinh điển, cuốn sách *API Design Patterns* (JJ Geewax) và *Building an API Product* (Bruno Pedro).

---

## 1. Khái Niệm Cốt Lõi SOA & Kiến Trúc Hệ Thống

| Thuật ngữ | Thuật ngữ tiếng Anh | Định nghĩa & Ý nghĩa kiến trúc |
| :--- | :--- | :--- |
| **Kiến trúc hướng dịch vụ** | Service-Oriented Architecture (SOA) | Phong cách kiến trúc phần mềm trong đó các thành phần ứng dụng cung cấp dịch vụ cho các thành phần khác thông qua giao thức truyền thông qua mạng. |
| **Bên cung cấp dịch vụ** | Service Provider | Thành phần hoặc hệ thống xây dựng, lưu trữ và phơi bày dịch vụ ra ngoài cho các client gọi tới. |
| **Bên tiêu thụ dịch vụ** | Service Consumer / Client | Ứng dụng hoặc dịch vụ khác thực hiện gọi và sử dụng năng lực do Service Provider cung cấp. |
| **Hợp đồng dịch vụ** | Service Contract | Bản đặc tả chính thức xác định cách thức giao tiếp giữa Provider và Consumer (bao gồm định dạng dữ liệu, phương thức, giao thức, ràng buộc lỗi). Trong REST API, OpenAPI chính là bản hợp đồng này. |
| **Khớp nối lỏng** | Loose Coupling | Nguyên lý vàng trong SOA: Các dịch vụ duy trì mối quan hệ phụ thuộc tối thiểu với nhau; sự thay đổi logic nội bộ của một bên không làm gãy bên còn lại miễn là Hợp đồng dịch vụ được giữ vững. |
| **Tính tự quản của dịch vụ** | Service Autonomy | Mỗi dịch vụ có toàn quyền kiểm soát logic nghiệp vụ và dữ liệu (database) của riêng mình, không bị phụ thuộc vào môi trường bên ngoài. |
| **Cổng kết nối API** | API Gateway | Điểm tiếp nhận yêu cầu tập trung (Single Entry Point) cho toàn bộ hệ thống client bên ngoài, thực thi các tính năng xuyên suốt (cross-cutting concerns) như định tuyến (routing), xác thực (auth), giới hạn tần suất (rate limiting), và giám sát (observability). |
| **Trục tích hợp dịch vụ** | Enterprise Service Bus (ESB) | Mô hình trung tâm truyền thống trong SOA để chuyển đổi giao thức, định tuyến thông điệp phức tạp và tích hợp các hệ thống kế thừa (legacy systems). Trong kiến trúc Microservices hiện đại, ESB thường được thay thế bằng mô hình *Smart Endpoints, Dumb Pipes* kết hợp API Gateway. |

---

## 2. Mẫu Thiết Kế API & Hướng Tài Nguyên (Resource-Oriented Design Patterns)

| Thuật ngữ | Thuật ngữ tiếng Anh | Định nghĩa & Ý nghĩa kiến trúc |
| :--- | :--- | :--- |
| **Kiến trúc hướng tài nguyên** | Resource-Oriented Architecture (ROA) | Phong cách tổ chức API xoay quanh các thực thể dữ liệu ("Tài nguyên" - Resources) có thể định danh qua URI và thao tác qua tập hữu hạn các phương thức tiêu chuẩn. |
| **Tính lũy kế / Bất biến** | Idempotency | Thuộc tính của một thao tác mà việc thực thi nó một lần hay nhiều lần liên tiếp với cùng tham số đều cho ra cùng một trạng thái hệ thống (ví dụ: HTTP GET, PUT, DELETE theo chuẩn REST là idempotent; POST mặc định không idempotent). |
| **Khóa lũy kế** | Idempotency Key | Chuỗi định danh duy nhất (UUID) do client sinh ra gửi kèm request (thường qua header) để server nhận biết và loại trừ các yêu cầu trùng lặp do rớt mạng hoặc retry. |
| **Phương thức chuẩn** | Standard Methods | Tập hợp 5 phương thức CRUD cơ bản được quy chuẩn hóa: List (`GET /res`), Get (`GET /res/{id}`), Create (`POST /res`), Update (`PUT/PATCH /res/{id}`), Delete (`DELETE /res/{id}`). |
| **Phương thức tùy biến** | Custom Methods | Phương thức dành cho các hành động nghiệp vụ phức tạp không thể quy về CRUD chuẩn, sử dụng cú pháp dấu hai chấm (ví dụ: `POST /orders/{id}:cancel`). |
| **Mặt nạ trường** | Field Mask | Cơ chế cho phép client chỉ định tường minh danh sách các trường cần lấy (partial response) hoặc cần cập nhật (partial update), giúp tiết kiệm băng thông và tránh ghi đè dữ liệu ngoài ý muốn. |
| **Tài nguyên đơn bản** | Singleton Sub-Resource | Tài nguyên phụ thuộc cha nhưng chỉ tồn tại tối đa một bản thể duy nhất (ví dụ: `/users/{id}/settings`), không cần định danh bằng ID trong URI. |
| **Tài nguyên liên kết** | Association Resource | Việc mô hình hóa một quan hệ Nhiều - Nhiều (N-N) thành một tài nguyên độc lập hạng nhất có URI riêng để quản lý các thuộc tính liên kết (ví dụ: `/memberships` nối giữa User và Team). |
| **Phân trang bằng con trỏ** | Cursor/Token-based Pagination | Kỹ thuật phân trang sử dụng một token mã hóa vị trí bản ghi cuối cùng của trang trước thay vì dùng `offset/limit`, giúp tăng tốc độ truy vấn trên tập dữ liệu lớn và tránh trùng lặp khi dữ liệu biến động liên tục. |
| **Tác vụ chạy ngầm** | Long-Running Operation (LRO) | Pattern thiết kế cho các tác vụ tốn thời gian xử lý: Server trả về HTTP `202 Accepted` kèm ID tác vụ (`Operation`) để client theo dõi tiến độ một cách bất đồng bộ thay vì chặn kết nối HTTP. |
| **Xóa mềm** | Soft Deletion | Kỹ thuật đánh dấu cờ xóa (`isDeleted = true`) trên bản ghi cơ sở dữ liệu thay vì xóa vật lý, cho phép khôi phục dữ liệu (`undelete`) và lưu vết kiểm toán. |
| **Tương thích ngược** | Backward Compatibility | Khả năng phiên bản API mới vẫn hoạt động hoàn hảo với các client được lập trình cho phiên bản API cũ mà không yêu cầu client phải sửa đổi code. |
| **Thay đổi gây đứt gãy** | Breaking Change | Bất kỳ thay đổi nào trong hợp đồng API (xóa endpoint, đổi kiểu dữ liệu, bắt buộc thêm trường mới trong request) khiến client cũ gặp lỗi khi gọi đến. |

---

## 3. Quản Trị Sản Phẩm API & Trải Nghiệm Lập Trình Viên (API Product & DX)

| Thuật ngữ | Thuật ngữ tiếng Anh | Định nghĩa & Ý nghĩa kiến trúc |
| :--- | :--- | :--- |
| **Tư duy API như sản phẩm** | API-as-a-Product | Coi API là một sản phẩm thương mại độc lập với đối tượng khách hàng mục tiêu là lập trình viên, có lộ trình phát triển, mục tiêu kinh doanh và chỉ số thành công rõ ràng. |
| **Trải nghiệm lập trình viên** | Developer Experience (DX) | Tổng hòa cảm xúc, tốc độ tiếp cận, tính tiện dụng và sự hài lòng của lập trình viên khi tương tác với API, tài liệu, SDK và cộng đồng của sản phẩm. |
| **Thời gian tạo cuộc gọi đầu tiên** | Time To First Hello World (TTFHW) | Khoảng thời gian từ lúc một lập trình viên truy cập Developer Portal lần đầu tiên cho đến khi thực hiện thành công cuộc gọi API có kết quả đầu tiên (mục tiêu tiêu chuẩn là < 5 phút). |
| **Tiếp cận ưu tiên đặc tả** | Design-First / Contract-First | Phương pháp luận viết và thống nhất tài liệu đặc tả API (OpenAPI spec) trước khi tiến hành viết code backend, cho phép frontend/client phát triển song song thông qua mock server. |
| **Giới hạn lưu lượng** | Rate Limiting | Kỹ thuật khống chế số lượng yêu cầu mà một client (hoặc một API key) có thể gửi tới API trong một đơn vị thời gian (ví dụ: 100 requests/phút) nhằm chống tấn công DoS và bảo vệ tài nguyên hạ tầng. |
| **Khả năng quan sát** | Observability | Khả năng thấu hiểu trạng thái bên trong của hệ thống API dựa trên dữ liệu đầu ra từ 3 trụ cột: Nhật ký (Logs), Chỉ số hiệu năng (Metrics) và Dấu vết phân tán (Distributed Traces). |
| **Ngừng hỗ trợ & Đóng dịch vụ** | Deprecation & Sunsetting | Quy trình thông báo trước rằng một phiên bản API sắp hết hạn hỗ trợ (Deprecation) và thời điểm chính thức ngắt kết nối ngừng hoạt động vĩnh viễn (Sunsetting). |
