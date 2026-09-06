# Ghi Chép Công Cụ Môn Học: Tooling Notes

Tài liệu này tổng hợp hướng dẫn nhanh, cách sử dụng cơ bản và vai trò kiến trúc của 4 bộ công cụ tiêu chuẩn trong học phần **Kiến trúc hướng dịch vụ (SOA)**: Swagger/OpenAPI, Postman/Newman, Node.js + Mongoose, và Git/GitHub.

---

## 1. Swagger / OpenAPI Specification (OAS)

### Tổng quan & Bản chất
- **OpenAPI Specification (OAS)** là chuẩn định dạng mô tả giao diện máy-đọc-được (machine-readable) cho RESTful APIs, độc lập với ngôn ngữ lập trình (thường viết bằng YAML hoặc JSON).
- **Swagger** là bộ công cụ mã nguồn mở xây dựng quanh chuẩn OpenAPI (bao gồm Swagger UI để render giao diện tài liệu tương tác, Swagger Editor để soạn thảo, Swagger Codegen để sinh code).

### Vai trò trong một API Service điển hình
- Đóng vai trò là **Bản hợp đồng giao tiếp (API Contract)** giữa Consumer và Provider theo phương pháp tiếp cận *Contract-First / API-First*.
- Nguồn chân lý duy nhất (Single Source of Truth) để:
  - Sinh tài liệu tương tác cho lập trình viên (Developer Documentation).
  - Tự động kiểm tra tính hợp lệ của Request/Response (Contract Testing & Request Validation).
  - Khởi tạo Mock Server cho frontend phát triển độc lập trước khi backend hoàn thành.

### Cách dùng cơ bản & Mẫu đặc tả (YAML)
```yaml
openapi: 3.0.3
info:
  title: Product Catalog Service API
  version: 1.0.0
  description: API quản lý danh mục sản phẩm minh họa theo chuẩn SOA
paths:
  /products:
    get:
      summary: Liệt kê danh sách sản phẩm (List Pattern)
      parameters:
        - name: pageSize
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: Danh sách sản phẩm trả về thành công
          content:
            application/json:
              schema:
                type: object
                properties:
                  products:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  nextPageToken:
                    type: string
components:
  schemas:
    Product:
      type: object
      required:
        - id
        - name
        - price
      properties:
        id:
          type: string
        name:
          type: string
        price:
          type: number
```

---

## 2. Postman & Newman

### Tổng quan & Bản chất
- **Postman** là nền tảng kiểm thử và quản lý API tương tác trực quan (GUI client), hỗ trợ gửi request, tổ chức bộ sưu tập (Collection), thiết lập biến môi trường (Environment Variables) và viết script kiểm thử (Test Scripts).
- **Newman** là trình thực thi dòng lệnh (CLI companion) của Postman, cho phép chạy trực tiếp các Postman Collection mà không cần giao diện đồ họa.

### Vai trò trong một API Service điển hình
- **Postman**: Dùng để khám phá (exploratory testing), thiết kế test cases, debug endpoint trong quá trình phát triển tính năng mới.
- **Newman**: Đóng vai trò là công cụ kiểm thử tự động trong đường ống tích hợp liên tục (CI/CD Pipeline), tự động chạy kiểm thử hồi quy (Regression Testing) và Contract Testing mỗi khi có bản build mới.

### Cách dùng cơ bản & Lệnh thực thi
1. **Viết kịch bản test trong Postman (Tab Tests):**
   ```javascript
   // Kiểm tra HTTP Status
   pm.test("Status code is 200 OK", function () {
       pm.response.to.have.status(200);
   });

   // Kiểm tra cấu trúc dữ liệu trả về
   pm.test("Response contains products array and nextPageToken", function () {
       const jsonData = pm.response.json();
       pm.expect(jsonData).to.have.property('products').that.is.an('array');
       pm.expect(jsonData).to.have.property('nextPageToken');
   });
   ```
2. **Chạy tự động bằng Newman trên terminal / CI:**
   ```bash
   # Cài đặt Newman
   npm install -g newman

   # Chạy collection kèm file biến môi trường và xuất báo cáo
   newman run postman_collection.json -e dev_environment.json --reporters cli,html
   ```

---

## 3. Node.js + Mongoose

### Tổng quan & Bản chất
- **Node.js**: Môi trường thực thi JavaScript bất đồng bộ hướng sự kiện (Event-driven, non-blocking I/O), rất phù hợp để xây dựng các API Service xử lý I/O cao với độ trễ thấp.
- **Mongoose**: Thư viện ODM (Object Data Modeling) cho MongoDB trong Node.js, cung cấp cơ chế định nghĩa Schema chặt chẽ, ép kiểu dữ liệu, xác thực (validation) và các hook tiền/hậu xử lý (pre/post middleware).

### Vai trò trong một API Service điển hình
- Đóng vai trò là **Tầng cài đặt dịch vụ (Service Implementation Layer)** và **Tầng truy cập dữ liệu (Data Access Layer)**.
- Đảm bảo dữ liệu lưu trữ tuân thủ đúng cấu trúc được mô tả trong hợp đồng OpenAPI.
- Hỗ trợ triển khai nhanh chóng các pattern như Soft Deletion (qua schema middleware), Pagination, Field Masking.

### Cách dùng cơ bản (Express + Mongoose)
```javascript
const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

// 1. Định nghĩa Mongoose Schema
const productSchema = new mongoose.Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  isDeleted: { type: Boolean, default: false } // Phục vụ Soft Delete pattern
}, { timestamps: true });

const Product = mongoose.model('Product', productSchema);

// 2. Endpoint List Products có hỗ trợ Pagination & Soft Delete
app.get('/products', async (req, res) => {
  const limit = parseInt(req.query.pageSize) || 10;
  const products = await Product.find({ isDeleted: false }).limit(limit);
  res.status(200).json({ products });
});

// 3. Khởi động server
mongoose.connect('mongodb://localhost:27017/soa_demo')
  .then(() => app.listen(3000, () => console.log('Service running on port 3000')));
```

---

## 4. Git & GitHub

### Tổng quan & Bản chất
- **Git**: Hệ thống quản lý phiên bản phân tán (Distributed Version Control System) giúp ghi lại lịch sử thay đổi mã nguồn, hỗ trợ rẽ nhánh (branching) và ghép mã (merging).
- **GitHub**: Nền tảng đám mây lưu trữ kho mã nguồn Git, cung cấp các tính năng cộng tác nhóm (Pull Request, Code Review, Issue Tracking) và tự động hóa quy trình với GitHub Actions.

### Vai trò trong một API Service điển hình
- **Quản trị phiên bản hợp đồng API (Contract Version Control)**: Theo dõi sự thay đổi của file đặc tả `openapi.yaml`. Mọi breaking change đều phải được phát hiện qua Code Review trước khi merge vào nhánh chính.
- **Tự động hóa tích hợp liên tục (CI/CD Pipeline)**:
  - Tự động linting file OpenAPI bằng công cụ như Spectral (`spectral lint openapi.yaml`).
  - Tự động khởi động service và kích hoạt Newman chạy bộ test hồi quy trước khi cho phép đóng Pull Request.

### Quy trình làm việc nhóm chuẩn (Feature Branch Workflow)
```bash
# 1. Tạo nhánh phát triển tính năng/pattern mới
git checkout -b feature/pagination-token

# 2. Commit các thay đổi (OpenAPI spec, code triển khai, file Postman test)
git add weeks/week-02/
git commit -m "feat(week-02): implement cursor-based pagination pattern"

# 3. Đẩy lên GitHub và tạo Pull Request để phản biện kiến trúc
git push origin feature/pagination-token
```

---

## 5. Docker & Containerization

### Tổng quan & Bản chất
- **Docker**: Nền tảng ảo hóa mức hệ điều hành (Containerization) cho phép đóng gói toàn bộ mã nguồn, runtime Node.js, thư viện phụ thuộc và cấu hình môi trường vào một Container Image độc lập và bất biến.
- Đảm bảo tính nhất quán tuyệt đối theo nguyên lý: *"Chạy được ở local thì chắc chắn chạy được ở staging/production"*.

### Vai trò trong Vận hành Dịch vụ (Service Operation)
- Chuẩn hóa môi trường triển khai cho microservice trong Tuần 10 (Service Operation) và Tuần 13 (Capstone Project).
- Tích hợp với Docker Compose để khởi chạy đồng thời cụm dịch vụ: Express API Service + MongoDB Server + Reverse Proxy / Gateway.

### Mẫu `Dockerfile` Chuẩn Cho Node.js API Service
```dockerfile
# Sử dụng Node.js LTS Alpine tối ưu kích thước
FROM node:18-alpine

WORKDIR /usr/src/app

# Tận dụng Docker layer caching cho dependencies
COPY package*.json ./
RUN npm ci --only=production

# Sao chép toàn bộ mã nguồn
COPY . .

# Khai báo cổng phơi bày của service
EXPOSE 3000

# Thiết lập biến môi trường mặc định
ENV NODE_ENV=production

# Lệnh khởi chạy tiến trình
CMD ["node", "server.js"]
```

---

## 6. Ma Trận Phân Bổ Công Cụ Theo Lộ Trình Chuẩn 13 Tuần

| Bộ Công Cụ | Các Tuần Trọng Tâm | Vai Trò & Mục Đích Kỹ Thuật |
| :--- | :--- | :--- |
| **OpenAPI / Swagger** | Week 04, Week 07, Week 13 | Thiết kế đặc tả hợp đồng (Design-First), sinh tài liệu tương tác Swagger UI, Contract Validation |
| **Node.js, Express & Mongoose** | Week 02, Week 03, Week 05, Week 06, Week 07, Week 11, Week 13 | Hiện thực hóa backend từ spec, mô hình hóa dữ liệu (Mongoose Schemas), bảo vệ bằng JWT middleware, cài đặt Design Patterns |
| **Postman & Newman CLI** | Week 08, Week 11, Week 13 (và xác thực tại Mọi tuần) | Xây dựng test suite tự động (Happy & Negative path), đo lường độ trễ, sinh báo cáo CLI làm minh chứng snapshot |
| **Git, GitHub & CI/CD** | Week 09, Week 10, Week 13 | Quản lý phiên bản hợp đồng không gây đứt gãy, tự động hóa linting và regression testing bằng GitHub Actions |
| **Docker & Docker Compose** | Week 10, Week 13 | Đóng gói container, thiết lập health checks (`/healthz`), giả lập môi trường production nhiều thành phần |
| **Marp CLI** | Tuần 01 đến Tuần 13 | Biên dịch bài giảng Marp Markdown sang slide PDF học liệu chuẩn UET |

