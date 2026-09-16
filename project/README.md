# SOA Continuous Project

Dự án Node.js/Express xuyên suốt học phần SOA — VNU-UET. Codebase cộng dồn 1 Use Case nhỏ mỗi tuần, bắt đầu từ `User` resource cơ bản.

## Cài đặt & Chạy

```bash
cd project
npm install
npm start
# Dịch vụ chạy tại http://localhost:3000
```

## Yêu cầu

- Node.js ≥ 18.x LTS
- MongoDB tại `mongodb://localhost:27017` (hoặc Docker: `docker run -d -p 27017:27017 --name mongo-soa mongo:latest`)

## Biến môi trường (tùy chọn)

Tạo file `.env` tại thư mục `project/`:
```
PORT=3000
MONGO_URI=mongodb://localhost:27017/soa-project
```

## Endpoints hiện tại

> Cập nhật sau mỗi tuần khi UC mới được implement qua Gate C.

| Method | Path | Mô tả | Tuần thêm | Trạng thái |
|---|---|---|---|---|
| `GET` | `/health` | Health check | Khởi tạo | ✅ Active |
| `GET` | `/users` | Danh sách user | Tuần 01 | ⏳ TODO |
| `GET` | `/users/:id` | Chi tiết 1 user | Tuần 01 | ⏳ TODO |
| `POST` | `/users` | Tạo user mới | Tuần 01 | ⏳ TODO |
| `PATCH` | `/users/:id` | Cập nhật một phần | Tuần 01 | ⏳ TODO |
| `DELETE` | `/users/:id` | Xoá user | Tuần 01 | ⏳ TODO |

## Lịch sử cộng dồn

| Tuần | Delta thêm vào | UC |
|---|---|---|
| Khởi tạo | Scaffold: server.js, User model, route stubs | — |
