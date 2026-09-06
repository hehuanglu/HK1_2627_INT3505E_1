# SOA Course Syllabus & 13-Week Curriculum Registry

Tài liệu này là bản đăng ký khung chương trình chuẩn chính thức cho học phần **Kiến trúc hướng dịch vụ (Service-Oriented Architecture - SOA)** tại **Trường Đại học Công nghệ, ĐHQGHN (VNU-UET)**.
Khung chương trình được thiết kế theo lộ trình chuẩn hóa **13 tuần**, tích hợp chặt chẽ giữa các mẫu thiết kế thực tiễn từ cuốn *API Design Patterns* (**JJ Geewax** - Manning Publications, 30 chương) và phương pháp luận quản trị sản phẩm API từ cuốn *Building an API Product* (**Bruno Pedro** - Packt Publishing, 18 chương).

---

## 1. Khung Chương Trình Chuẩn 13 Tuần (13-Week Standard Curriculum)

| Tuần | Nội Dung Chính | Mục Tiêu Sinh Viên Đạt Được | Tham Chiếu JJ Geewax (Manning, 30 Ch.) | Tham Chiếu Bruno Pedro (Packt, 18 Ch.) | Thư Mục Sản Phẩm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Week 01** | **Giới thiệu API, Web Services** | Hiểu vai trò API trong hệ thống phần mềm | Phân biệt RPC vs REST vs Web Services, vai trò Design Patterns (Ch. 1, 2) | Khái niệm API, Phân định giao thức, Tư duy API Sản phẩm & Tháp nhu cầu DX (Ch. 1, 2, 3) | `weeks/week-01/` |
| **Week 02** | **REST & HTTP Fundamentals** | Thiết kế request/response đúng chuẩn | Resource Naming, Data Types & Defaults, Resource Identification (Ch. 3, 5, 6) | Tính trực quan của URI, Ngữ nghĩa mã HTTP & Giao tiếp có ý nghĩa (Ch. 2, 8) | `weeks/week-02/` |
| **Week 03** | **Nguyên tắc thiết kế API** | Xây dựng API nhất quán, dễ dùng | Bộ 5 phương thức CRUD chuẩn (Standard Methods: List, Get, Create, Update, Delete) (Ch. 7) | API Usability, Tính đoán định & Cấu trúc thông báo lỗi thân thiện RFC 7807 (Ch. 2, 7) | `weeks/week-03/` |
| **Week 04** | **OpenAPI & Swagger** | Tạo tài liệu API tự động | Nguyên lý Hợp đồng giao tiếp chuẩn hóa (Contract-First Interface) | Triết lý Design-First làm Single Source of Truth, Kiểm định Spec với Spectral (Ch. 4, 7, 8) | `weeks/week-04/` |
| **Week 05** | **Data Modeling & Resource Design** | Thiết kế cấu trúc dữ liệu cho API | Resource Hierarchy, Singleton, Cross References, Association & Polymorphism (Ch. 4, 12, 13, 14, 16) | Phân rã ranh giới nghiệp vụ (DDD) & Mô hình hóa lược đồ dữ liệu phức tạp (Ch. 5, 8) | `weeks/week-05/` |
| **Week 06** | **Authentication & Authorization** | Bảo mật API | Ngữ cảnh xác thực yêu cầu & Định danh người dùng (Request Authentication) (Ch. 30) | Quản trị bảo mật API toàn diện: AuthN vs AuthZ, OAuth2, JWT, API Keys, RBAC & Fuzzing (Ch. 10) | `weeks/week-06/` |
| **Week 07** | **Backend Implementation** | Xây dựng backend từ spec | Ánh xạ Contract-to-Code & Kiểm tra dữ liệu đầu vào (Request Validation) (Ch. 7, 27) | Kỹ thuật phát triển phần mềm: Kiến trúc phân tầng, sinh boilerplate từ OpenAPI (Ch. 9) | `weeks/week-07/` |
| **Week 08** | **API Testing** | Kiểm thử tự động, hiệu năng | Xác minh hợp đồng, kiểm thử ngoại lệ và hành vi thử lại (Ch. 7, 27, 29) | Kiểm thử hợp đồng, Tự động hóa Postman/Newman, Kiểm thử hiệu năng & Quality Gates (Ch. 11, 12) | `weeks/week-08/` |
| **Week 09** | **API Versioning** | Quản lý thay đổi API | Phiên bản hóa ngữ nghĩa (SemVer), Quy tắc tương thích ngược & Bản sửa đổi tài nguyên (Ch. 24, 28) | Chiến lược tiến hóa an toàn, Header Deprecation & Sunset, Kế hoạch đóng dịch vụ (Ch. 17, 18) | `weeks/week-09/` |
| **Week 10** | **Service Operation** | Deploy, monitoring, bảo mật production | Xử lý yêu cầu thử lại an toàn & Thực thi chính sách qua Gateway (Ch. 29, 30) | Đóng gói Docker, Cổng API Gateway, Rate Limiting & 3 Trụ cột Observability (Logs, Metrics, Traces) (Ch. 13, 14) | `weeks/week-10/` |
| **Week 11** | **API Design Patterns** | Áp dụng mẫu thiết kế cho các tình huống thực tế | Toàn bộ Advanced Patterns: Idempotency Key, LRO, FieldMask, Cursor Pagination, Batch, Soft Delete, ETag Concurrency (Ch. 8, 9, 10, 11, 14, 15, 17, 18, 21, 22, 25, 26, 27, 28) | Độ tin cậy cao, Dự đoán lỗi & Khả năng chịu lỗi trong môi trường phân tán (Ch. 2, 7, 14) | `weeks/week-11/` |
| **Week 12** | **API as a Product** | Xem API là sản phẩm kinh doanh | Hệ sinh thái API và thiết kế lấy nhà phát triển làm trung tâm (Ch. 1, 2) | Toàn diện Chiến lược Sản phẩm: Mô hình kiếm tiền, Developer Portal, Onboarding tự phục vụ, SLA/SLO & KPIs (Ch. 3, 5, 6, 15, 16) | `weeks/week-12/` |
| **Week 13** | **Dự án nhóm (Capstone Project)** | Triển khai API hoàn chỉnh + quản lý vòng đời | Tổng hợp toàn diện Design Patterns (Ch. 1 - 30) | Quản trị vòng đời API toàn diện từ ý tưởng đến vận hành (Full API Lifecycle Governance) (Ch. 4 & Ch. 5 - 18) | `weeks/week-13/` |

---

## 2. Chi Tiết Từng Tuần Học (Detailed Weekly Specifications)

### Tuần 01: Giới thiệu API, Web Services
- **Mục tiêu học tập**:
  - Nắm vững lịch sử tiến hóa từ nguyên khối (Monolith) sang hướng dịch vụ (SOA) và Microservices.
  - Phân biệt rõ Web Service, SOAP (XML-based), REST (HTTP/JSON), RPC (gRPC) và Event-Driven (Webhooks).
  - Hiểu vì sao API trở thành cầu nối thông tin cốt lõi trong kỷ nguyên điện toán đám mây và kinh tế số.
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 1, 2)**: Khái niệm API, sự khác biệt giữa RPC và REST, vai trò của Design Patterns trong việc chuẩn hóa hệ thống phân tán.
  - **Bruno Pedro (Ch. 1, 2, 3)**: Lịch sử và phân loại API; Tư duy xem API là sản phẩm (API-as-a-Product); Tháp nhu cầu trải nghiệm lập trình viên (DX Hierarchy of Needs: Functionality $\to$ Reliability $\to$ Usability $\to$ Delight).
  - Các khái niệm nền tảng: Service Provider, Service Consumer, Service Contract.
- **Bài tập thực hành**: Phân tích ca sử dụng thực tế (Case Study), xây dựng dịch vụ Ping/Pong đơn giản minh họa luồng giao tiếp Client-Server.

### Tuần 02: REST & HTTP Fundamentals
- **Mục tiêu học tập**:
  - Nắm vững 6 ràng buộc kiến trúc của REST (Architectural Constraints of REST).
  - Thành thạo chu trình HTTP Request/Response: Verbs (GET, POST, PUT, PATCH, DELETE), Status Codes (2xx, 3xx, 4xx, 5xx), Headers (Accept, Content-Type, Authorization).
  - Thiết kế cấu trúc URI chuẩn mực, dễ hiểu, dễ đoán định và an toàn.
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 3, 5, 6)**: Quy tắc đặt tên tài nguyên (Resource Naming - danh từ số nhiều, phân cấp, kebab-case); Kiểu dữ liệu và giá trị mặc định (Data Types & Defaults); Định danh tài nguyên duy nhất (Resource Identification - UUID vs internal ID).
  - **Bruno Pedro (Ch. 2, 8)**: Tính trực quan của URI, ngữ nghĩa chuẩn mã trạng thái HTTP, truyền thông tường minh giữa client và server.
- **Bài tập thực hành**: Xây dựng service quản lý thông tin tài nguyên cơ bản tuân thủ nghiêm ngặt chuẩn HTTP semantics và quy ước đặt tên REST.

### Tuần 03: Nguyên tắc thiết kế API (API Design Principles)
- **Mục tiêu học tập**:
  - Nắm vững các nguyên tắc vàng: Tính nhất quán (Consistency), Khả năng đoán định (Predictability), Tính tối giản (Simplicity).
  - Chuẩn hóa bộ phương thức CRUD cơ bản và cấu trúc dữ liệu phản hồi (Response Payloads).
  - Chuẩn hóa cấu trúc báo lỗi chi tiết theo tiêu chuẩn RFC 7807 (Problem Details for HTTP APIs).
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 7)**: Bộ 5 phương thức chuẩn (Standard Methods: List, Get, Create, Update, Delete) — đầu vào, đầu ra, quy tắc ánh xạ HTTP verbs và mã kết quả.
  - **Bruno Pedro (Ch. 2, 7)**: Khả năng sử dụng (Usability), thiết kế thông báo lỗi thân thiện và có thể hành động được (Actionable Error Messages) hỗ trợ tối đa cho lập trình viên.
- **Bài tập thực hành**: Triển khai trọn bộ 5 phương thức CRUD chuẩn mực kèm middleware xử lý lỗi tập trung chuẩn RFC 7807.

### Tuần 04: OpenAPI & Swagger
- **Mục tiêu học tập**:
  - Hiểu sâu sắc sự khác biệt giữa *Code-First* và *Design-First (Contract-First)*.
  - Làm chủ cú pháp OpenAPI Specification v3.0.3 (YAML/JSON).
  - Tự động hóa kiểm tra hợp đồng bằng công cụ Linting (Spectral) và sinh tài liệu tương tác với Swagger UI, Redoc.
- **Trọng tâm kiến thức**:
  - **Bruno Pedro (Ch. 4, 7, 8)**: Giai đoạn Create/Design trong vòng đời API; Triết lý Design-First làm Single Source of Truth; Tạo Mock Server sớm để frontend và backend phát triển song song; Linting bản đặc tả bằng Spectral.
  - Cấu trúc OpenAPI: `openapi`, `info`, `paths`, `components/schemas`, `components/responses`, `components/securitySchemes`.
- **Bài tập thực hành**: Viết file `openapi.yaml` chuẩn chỉnh cho một nghiệp vụ dịch vụ và nhúng Swagger UI vào Express server.

### Tuần 05: Data Modeling & Resource Design
- **Mục tiêu học tập**:
  - Thiết kế mô hình dữ liệu tài nguyên hướng dịch vụ (Resource-Oriented Data Modeling).
  - Ánh xạ giữa quan hệ cơ sở dữ liệu (1-1, 1-N, N-N) sang mô hình tài nguyên RESTful API.
  - Sử dụng ODM (Mongoose) để xây dựng lược đồ dữ liệu chặt chẽ, tối ưu và nhất quán.
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 4, 12, 13, 14, 16)**: Phân cấp tài nguyên cha - con (Hierarchy); Tài nguyên đơn bản (Singleton Sub-resource `/users/{id}/settings`); Tham chiếu chéo qua URI (Cross References); Tài nguyên quan hệ nhiều - nhiều (Association Resources `/memberships`); Tài nguyên đa hình (Polymorphic Resources).
  - **Bruno Pedro (Ch. 5, 8)**: Phân rã ranh giới miền nghiệp vụ theo Domain-Driven Design (DDD), định nghĩa mô hình thực thể và cấu trúc lược đồ dữ liệu (Schema Modeling).
- **Bài tập thực hành**: Thiết kế hệ thống dữ liệu có quan hệ phức tạp (Khách hàng - Đơn hàng - Chi tiết đơn hàng, hoặc Người dùng - Nhóm - Quyền) có áp dụng Singleton và Association Resources.

### Tuần 06: Authentication & Authorization
- **Mục tiêu học tập**:
  - Phân biệt rõ ràng giữa Xác thực (Authentication - "Bạn là ai?") và Phân quyền (Authorization - "Bạn được phép làm gì?").
  - Nắm vững các phương thức bảo mật API: API Keys, HTTP Bearer Auth, JWT (JSON Web Tokens), OAuth 2.0 / OIDC.
  - Áp dụng mô hình kiểm soát truy cập dựa trên vai trò (RBAC - Role-Based Access Control).
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 30)**: Cơ chế xác thực yêu cầu (Request Authentication), truyền thông tin danh tính an toàn và thiết lập Security Context trong request pipeline.
  - **Bruno Pedro (Ch. 10)**: Quản trị bảo mật API toàn diện (API Security): Luồng cấp phát OAuth 2.0, ký và xác minh JWT Access Token / Refresh Token, quản lý API Keys, và kiểm thử bảo mật bằng kỹ thuật Fuzz Testing.
- **Bài tập thực hành**: Xây dựng hệ thống bảo mật Auth hoàn chỉnh với JWT middleware và RBAC bảo vệ các endpoint nhạy cảm (User vs Admin).

### Tuần 07: Backend Implementation
- **Mục tiêu học tập**:
  - Hiện thực hóa dịch vụ Backend hoàn chỉnh từ bản hợp đồng OpenAPI đặc tả từ trước (Spec-to-Code).
  - Tổ chức cấu trúc mã nguồn theo mô hình kiến trúc nhiều tầng (Layered Architecture: Route $\to$ Controller $\to$ Service $\to$ Model).
  - Thực thi Contract Validation: Tự động kiểm tra tính hợp lệ của request payload theo schema định nghĩa trong OpenAPI spec.
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 7, 27)**: Ánh xạ chuẩn bộ 5 phương thức CRUD từ hợp đồng vào mã nguồn; Xác thực dữ liệu đầu vào (Request Validation) tại tầng biên middleware.
  - **Bruno Pedro (Ch. 9)**: Kỹ thuật phát triển phần mềm (Development Techniques): Sinh boilerplate từ OpenAPI spec, phân tách độc lập giữa tầng giao vận HTTP và tầng nghiệp vụ thuần túy (Service Layer).
- **Bài tập thực hành**: Xây dựng trọn vẹn một microservice backend bằng Node.js + Express + Mongoose chuẩn hóa từ file spec `openapi.yaml`, đảm bảo 100% Contract Compliance.

### Tuần 08: API Testing
- **Mục tiêu học tập**:
  - Hiểu vai trò của kiểm thử trong việc đảm bảo SLA/SLO và độ tin cậy của dịch vụ.
  - Thiết kế kịch bản kiểm thử: Kiểm thử chức năng (Functional Testing), Kiểm thử hợp đồng (Contract Testing), Kiểm thử biên và ngoại lệ (Fault Tolerance Testing).
  - Tự động hóa kiểm thử bằng Postman & Newman CLI, bước đầu đo lường hiệu năng API (Response Time, Latency).
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 7, 27, 29)**: Xác minh hành vi phương thức chuẩn, kiểm thử các phản hồi lỗi chi tiết và kiểm thử cơ chế thử lại (Retrial).
  - **Bruno Pedro (Ch. 11, 12)**: Kiểm thử API và Đảm bảo chất lượng (API Testing & QA): Kiểm thử hợp đồng (Contract Testing với Pact/Postman), kiểm thử hiệu năng và độ trễ, thiết lập Quality Gates trong CI/CD.
  - Postman Collection Schema v2.1.0, viết assertion scripts bằng JavaScript (`pm.test`, `pm.expect`).
- **Bài tập thực hành**: Viết bộ test suite toàn diện trên Postman bao gồm Happy Path và Negative Path, chạy tự động và xuất báo cáo qua Newman CLI làm minh chứng thực nghiệm.

### Tuần 09: API Versioning
- **Mục tiêu học tập**:
  - Hiểu rõ thách thức khi nâng cấp dịch vụ: Thay đổi gây đứt gãy (Breaking Changes) vs Thay đổi tương thích ngược (Non-breaking Changes).
  - Nắm vững các chiến lược phiên bản: URI Path Versioning (`/v1/`), Query Parameter, Custom Header, Content Negotiation (Accept Header).
  - Xây dựng lộ trình ngừng hỗ trợ (API Deprecation) và ngắt kết nối an toàn (Sunsetting).
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 24, 28)**: Phiên bản hóa ngữ nghĩa (Semantic Versioning), các quy tắc duy trì tính tương thích ngược, và quản lý bản sửa đổi tài nguyên (Resource Revisions).
  - **Bruno Pedro (Ch. 17, 18)**: Chiến lược quản lý phiên bản API (API Versioning) và Kế hoạch ngừng hỗ trợ (Planning API Retirement): Sử dụng HTTP Headers chuẩn (`Deprecation`, `Sunset`), quy trình tập dượt ngắt kết nối (Brownouts) và họp rút kinh nghiệm (Retrospective).
- **Bài tập thực hành**: Thiết kế và triển khai song song hai phiên bản v1 và v2 của một dịch vụ, kiểm thử tính tương thích và gửi cảnh báo sunset qua HTTP headers.

### Tuần 10: Service Operation
- **Mục tiêu học tập**:
  - Nắm vững các yêu cầu vận hành dịch vụ trên môi trường Production: Triển khai (Deployment), Đóng gói Container (Docker), Giám sát (Monitoring), Khả năng quan sát (Observability).
  - Xây dựng các endpoint kiểm tra sức khỏe hệ thống (`/healthz`, `/livez`, `/readyz`).
  - Thiết lập cơ chế bảo vệ lưu lượng: Giới hạn tần suất (Rate Limiting) và Bóp nghẽn (Traffic Shaping).
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 29, 30)**: Xử lý yêu cầu thử lại khi rớt mạng, áp thi chính sách bảo mật biên qua Gateway.
  - **Bruno Pedro (Ch. 13, 14)**: Triển khai dịch vụ (Deploying the API) với Docker và CI/CD; Vai trò của API Gateway trong định tuyến và giới hạn lưu lượng; Ba trụ cột Observability (Logs, Metrics, Traces); Quản trị chỉ số độ tin cậy (SLI $\to$ SLO $\to$ SLA).
  - Graceful Shutdown, nhật ký truy cập có cấu trúc (Structured Logging với Correlation ID / Trace ID).
- **Bài tập thực hành**: Đóng gói dịch vụ bằng Dockerfile, tích hợp endpoint `/healthz`, cài đặt Express Rate Limit middleware và thiết lập logging truy vết giao dịch.

### Tuần 11: API Design Patterns
- **Mục tiêu học tập**:
  - Làm chủ và vận dụng linh hoạt các mẫu thiết kế nâng cao từ JJ Geewax để giải quyết các bài toán kỹ thuật phức tạp trong môi trường phân tán.
  - Xử lý các vấn đề: Rớt mạng gây trùng giao dịch, tác vụ tốn nhiều thời gian gây treo kết nối, lãng phí băng thông mạng, xung đột ghi đè đồng thời.
- **Trọng tâm kiến thức (JJ Geewax - Toàn bộ Advanced Patterns)**:
  - **Idempotency Key Pattern (Ch. 11 & Ch. 26)**: Chống trùng lặp giao dịch (rất quan trọng trong thanh toán/đặt hàng).
  - **Long-Running Operations - LRO (Ch. 10)**: Xử lý tác vụ bất đồng bộ với `202 Accepted` và Polling `Operation`.
  - **Partial Updates with FieldMask (Ch. 8)**: Cập nhật một phần dữ liệu tránh ghi đè mất mát.
  - **Cursor/Token-based Pagination (Ch. 21)**: Phân trang hiệu năng cao bằng con trỏ cho tập dữ liệu lớn.
  - **Filtering & Searching (Ch. 22)**: Cú pháp truy vấn có cấu trúc chuẩn hóa.
  - **Soft Deletion & Undelete (Ch. 25)**: Xóa mềm và phục hồi dữ liệu (`POST /resources/{id}:undelete`).
  - **Request Validation & Dry-Run (Ch. 27)**: Kiểm thử hợp lệ trước khi cam kết thay đổi (`validateOnly=true`).
  - **Custom Methods (Ch. 9 & Ch. 15)**: Biểu diễn hành động nghiệp vụ đặc thù (`/orders/{id}:cancel`, `/teams/{id}:addMember`).
  - **Resource Revisions & Concurrency Control (Ch. 28)**: Kiểm soát đồng thời lạc quan với HTTP Header `ETag` và `If-Match` chống mất dữ liệu (Lost Update).
  - **Batch Operations (Ch. 18)**: Gom cụm nhiều thao tác xử lý trong một request để giảm thiểu số lượng kết nối mạng (N+1 problem).
- **Trọng tâm kiến thức (Bruno Pedro Ch. 2, 7, 14)**: Đảm bảo tính khả dụng cao, phản hồi lỗi dễ dự đoán và khả năng chịu lỗi cho hệ thống.
- **Bài tập thực hành**: Chọn 2-3 advanced patterns (ví dụ: Idempotency Key kết hợp Soft Deletion hoặc ETag Concurrency Control) để cài đặt hoàn chỉnh và kiểm thử tính ổn định.

### Tuần 12: API as a Product
- **Mục tiêu học tập**:
  - Chuyển dịch góc nhìn từ kỹ sư phần mềm thuần túy sang nhà kiến trúc / người quản lý sản phẩm API.
  - Xây dựng mô hình kinh doanh API (Monetization Models: Free, Freemium, Tiered Subscriptions, Pay-per-use).
  - Thiết kế Developer Portal tự phục vụ (Self-service Onboarding) và tối ưu hóa chỉ số TTFHW (< 5 phút).
  - Định nghĩa cam kết chất lượng dịch vụ: SLA (Service Level Agreement), SLO (Service Level Objective), SLI (Service Level Indicator).
- **Trọng tâm kiến thức**:
  - **JJ Geewax (Ch. 1, 2)**: Xây dựng hệ sinh thái API trực quan, lấy nhà phát triển làm trung tâm.
  - **Bruno Pedro (Ch. 3, 5, 6, 15, 16)**: Toàn diện chiến lược sản phẩm API:
    - *API-as-a-Product*: Định vị giá trị và mô hình tạo doanh thu (Monetization).
    - *API Strategy & Personas*: Xây dựng chân dung nhà phát triển và bản đồ hành trình trải nghiệm.
    - *Distribution Channels*: Thiết kế Developer Portal tự phục vụ, môi trường thử nghiệm Sandbox, bảng giá theo gói cước (Pricing Tiers), tối ưu TTFHW < 5 phút.
    - *User Support*: Hỗ trợ cộng đồng lập trình viên, SDKs, và thu thập vòng lặp phản hồi (Feedback Loops).
    - *Business KPIs*: Quản trị chỉ số kinh doanh API (Active Developers, Call Volume, Churn Rate).
- **Bài tập thực hành**: Soạn thảo tài liệu chiến lược sản phẩm API (API Product Strategy Deck), thiết kế bảng định giá (Pricing Tiers) và tài liệu onboarding tương tác cho nhà phát triển.

### Tuần 13: Dự án nhóm (Capstone Group Project)
- **Mục tiêu học tập**:
  - Tích hợp toàn diện toàn bộ kiến thức và kỹ năng trong 12 tuần học vào một dự án thực tế quy mô nhóm.
  - Trải nghiệm toàn bộ vòng đời sản phẩm API: Ý tưởng $\to$ Bản đặc tả OpenAPI $\to$ Thiết kế Data Model $\to$ Hiện thực Backend $\to$ Bảo mật Auth/RBAC $\to$ Kiểm thử tự động Postman/Newman $\to$ Đóng gói & Vận hành Docker $\to$ Áp dụng Advanced Design Patterns.
  - Quản trị vòng đời API hoàn chỉnh (Full API Lifecycle Governance).
  - Báo cáo, thuyết trình (Demo presentation) và phản biện bảo vệ đồ án trước hội đồng/lớp học.
- **Trọng tâm kiến thức**:
  - Kết hợp toàn diện tinh hoa từ **JJ Geewax (Tổng hợp Ch. 1 - 30)** và **Bruno Pedro (Tổng hợp Ch. 4 - 18)**.
- **Sản phẩm bàn giao**:
  - Kho mã nguồn hoàn chỉnh có file đặc tả `openapi.yaml`, kiểm thử tự động `postman_collection.json`, container `Dockerfile`.
  - Bộ slide trình bày đồ án chuẩn Marp (`slide.md` $\to$ `slide.pdf`).

---

## 3. Quy Chuẩn Đóng Gói Sản Phẩm Mỗi Tuần (Weekly Deliverables Quality Checklist)

Tại mỗi thư mục tuần học `weeks/week-XX/` (với `XX` từ `01` đến `13`), quy trình 5 chặng tương tác (`soa-study-pipeline`) tạo ra các học liệu chuẩn:
1. `code/server.js` (kèm models, controllers, middleware): Microservice hoàn chỉnh với khối logic hạt nhân do sinh viên tự tay thực thi.
2. `code/openapi.yaml`: Bản đặc tả hợp đồng chuẩn OpenAPI Specification v3.0.3.
3. `code/postman_collection.json`: Bộ kịch bản kiểm thử Postman v2.1.0 kèm assertions, được xác thực thực tế qua Newman CLI.
4. `slide.md` & `slide.pdf`: Bộ slide bài giảng Marp giàu minh chứng thực nghiệm (Logs, Request/Response payloads, kết quả Newman PASS), loại bỏ nội dung hình thức sáo rỗng.

