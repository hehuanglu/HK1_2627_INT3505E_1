# Industry Mapping — SOA Concepts → LLM Industry Applications

> **Quy tắc sử dụng**: File này là nguồn **duy nhất và bắt buộc** cho mục "Industry application" trong A4 Knowledge Digest mỗi tuần. AI không được tự bịa nội dung ngoài file này. Nếu cần bổ sung, AI phải đề xuất và chờ sinh viên duyệt trước khi ghi vào đây.

---

## Tuần 01 — Giới thiệu API, Web Services

**Concept**: API-as-a-Product; SOAP vs REST vs RPC; Developer Experience (DX)

**Industry application**:
Các công ty xây dựng **LLM-powered API products** (OpenAI API, Google Gemini API, Anthropic API) áp dụng tư duy API-as-a-Product triệt để: họ coi developer là khách hàng chính, đo lường Time-to-First-Hello-World (TTFHW), và thiết kế onboarding để developer gọi được API đầu tiên trong < 5 phút. REST thống trị vì đơn giản và stateless — phù hợp cho LLM inference API vốn không cần duy trì session giữa các request.

---

## Tuần 02 — REST & HTTP Fundamentals

**Concept**: 6 ràng buộc REST; HTTP methods & status codes; Headers

**Industry application**:
Một **LLM agent** gọi tool HTTP cần hiểu đúng status code semantics để tự quyết định hành vi:
- `429 Too Many Requests` → backoff/retry theo `Retry-After` header
- `4xx` (lỗi client) → sửa lại input, không retry mù quáng
- `5xx` (lỗi server) → có thể retry vì lỗi tạm thời
- `200` nhưng body rỗng vs `204 No Content` → agent cần phân biệt để xử lý đúng response

OpenAI Function Calling và Google Gemini Tool Use đều dựa trên cơ chế này: agent tự đánh giá HTTP response để quyết định bước tiếp theo trong reasoning loop.

---

## Tuần 03 — Nguyên tắc thiết kế API

**Concept**: 5 phương thức chuẩn (List, Get, Create, Update, Delete); RFC 7807 error format; DX Usability

**Industry application**:
**LLM-generated API clients**: khi một LLM (ví dụ GitHub Copilot) sinh code gọi API tự động, nó phụ thuộc vào tính nhất quán của API — endpoint đặt tên đúng chuẩn, error response có `type`/`title`/`detail` theo RFC 7807 — để sinh code không cần thêm context. API không nhất quán buộc developer (và LLM) phải nhớ ngoại lệ, tăng cognitive load và tỷ lệ lỗi sinh code.

---

## Tuần 04 — OpenAPI & Swagger

**Concept**: Spec-First / Design-First; OpenAPI Specification 3.0.3; Swagger UI

**Industry application**:
**LLM tool specification**: OpenAPI (hoặc JSON Schema tương đương) là ngôn ngữ mà các LLM framework (LangChain, LlamaIndex, OpenAI Assistants) dùng để mô tả tool cho agent. Khi bạn viết một `openapi.yaml` chuẩn, bạn đang viết đúng định dạng mà agent cần để tự chọn tool, tự build request body, và parse response — không cần prompt engineering thêm.

---

## Tuần 05 — Data Modeling & Resource Design

**Concept**: Phân cấp tài nguyên cha-con; Singleton sub-resources; Association resources (N-N)

**Industry application**:
**RAG (Retrieval-Augmented Generation) data architecture**: cấu trúc phân cấp resource trong API ánh xạ trực tiếp sang cách tổ chức knowledge base cho RAG. Ví dụ: `Document` → `Chunk` → `Embedding` là phân cấp cha-con, và mối quan hệ `Chunk ↔ Tag` là association (N-N). Thiết kế sai phân cấp dẫn đến retrieval kém chính xác vì chunk không mang đủ metadata context của document cha.

---

## Tuần 06 — Authentication & Authorization

**Concept**: AuthN vs AuthZ; JWT; OAuth 2.0; RBAC

**Industry application**:
**LLM agent OAuth flow**: khi một AI agent cần gọi API thay mặt người dùng (ví dụ agent đặt lịch Google Calendar), nó phải thực hiện OAuth 2.0 Authorization Code flow để lấy access token giới hạn scope. JWT claims (`sub`, `scope`, `exp`) cho phép API backend phân quyền RBAC mà không cần stateful session — phù hợp cho môi trường serverless nơi agent có thể chạy trên nhiều instance song song.

---

## Tuần 07 — Backend Implementation

**Concept**: Ánh xạ Spec-to-Code; kiến trúc nhiều tầng Express + Mongoose; Contract Validation

**Industry application**:
**API contract as LLM prompt constraint**: khi dùng LLM để sinh backend code từ OpenAPI spec (GitHub Copilot Workspace, Cursor), chất lượng spec quyết định chất lượng code sinh ra. Schema validation chặt (required fields, enum, pattern) trong spec giúp LLM sinh đúng validation logic ngay lần đầu — tương tự cách prompt rõ ràng giảm hallucination.

---

## Tuần 08 — API Testing

**Concept**: Kiểm thử tự động Postman/Newman; Happy Path & Negative Path; đo lường độ trễ

**Industry application**:
**LLM-assisted test generation**: các công cụ như GitHub Copilot hoặc Cursor có thể sinh test case từ OpenAPI spec. Tuy nhiên, chúng thường chỉ sinh Happy Path — Negative Path (invalid input, race condition, network timeout) đòi hỏi tư duy kiến trúc sâu mà LLM dễ bỏ sót. Developer cần đặt câu hỏi đúng để prompt LLM sinh đủ edge case.

---

## Tuần 09 — API Versioning

**Concept**: Semantic Versioning; Breaking vs Non-breaking changes; Header Deprecation & Sunset

**Industry application**:
**LLM model versioning**: cùng bài toán với API versioning — OpenAI duy trì song song `gpt-4`, `gpt-4-turbo`, `gpt-4o` với chính sách sunset rõ ràng. Khi model mới ra, team không xóa model cũ ngay mà deprecate dần, gửi `Deprecation` header trong response API, cho phép client migrate theo lịch. Đây chính xác là pattern Sunset/Deprecation từ JJ Geewax áp dụng vào LLM product.

---

## Tuần 10 — Service Operation

**Concept**: Docker containerization; Health Check (`/healthz`); Observability (Logs/Metrics/Traces); Rate Limiting

**Industry application**:
**LLM inference service observability**: các nhà cung cấp LLM API (OpenAI, Anthropic) áp dụng observability 3 tầng: Logs (mỗi request/response), Metrics (latency P50/P95/P99, token throughput, error rate), Traces (end-to-end từ user prompt → model inference → response). Rate Limiting (`429`) trên LLM API thường có 2 chiều: RPM (requests/minute) và TPM (tokens/minute) — phức tạp hơn REST API thông thường.

---

## Tuần 11 — API Design Patterns

**Concept**: Idempotency Key; Long-Running Operations (LRO); FieldMask; Token Pagination; Soft Delete

**Industry application**:
**LLM async job patterns**: gọi LLM inference tốn thời gian (10s–120s) ánh xạ trực tiếp sang LRO pattern — client POST job → nhận `operation_id` → poll `GET /operations/{id}` → nhận kết quả khi `done: true`. Idempotency Key đặc biệt quan trọng khi agent retry do timeout: không có key, cùng prompt có thể bị inference 2 lần, tốn cost gấp đôi. Đây là pattern Google Vertex AI và Anthropic Batch API đang dùng.

---

## Tuần 12 — API as a Product

**Concept**: Monetization tiers; Developer Portal; TTFHW (< 5 phút); SLA/SLO

**Industry application**:
**LLM API monetization**: OpenAI, Anthropic, Google đều dùng tier model (Free → Pay-as-you-go → Enterprise) với SLA cam kết khác nhau. TTFHW < 5 phút là KPI thiết kế cho LLM API playground (OpenAI Playground, Google AI Studio) — developer không cần setup môi trường, chỉ cần API key là gọi được ngay. Developer Portal với code snippet, interactive docs, và usage dashboard là yếu tố quyết định adoption của LLM API.

---

## Tuần 13 — Capstone

**Concept**: Design-First → Code → Auth → Test → CI/CD → Docker → bảo vệ đồ án

**Industry application**:
**Production LLM application stack**: một LLM-powered application production-ready cần đủ: OpenAPI spec (contract với frontend/partners), JWT auth (bảo vệ endpoint inference tốn cost), Newman test suite (regression trước mỗi deploy), Docker container (reproducible environment), và observability (trace từng LLM call). Capstone của khóa học này chính xác là skeleton của một LLM API service thực tế.
