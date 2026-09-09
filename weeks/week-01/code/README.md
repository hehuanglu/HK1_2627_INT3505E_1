# Tuần 01: Giới thiệu API, Web Services & VNU-UET Student Registry Gateway

## 1. Bối Cảnh Nghiệp Vụ
Hệ thống quản lý đào tạo Trường Đại học Công nghệ (VNU-UET) đóng vai trò là **Service Provider**, cung cấp dịch vụ xác thực trạng thái sinh viên và nhịp tim kết nối cho các phân hệ vệ tinh (**Service Consumers**) như:
- Cổng quản lý Thư viện (`LIBRARY_SYSTEM`)
- Cổng quản lý Ký túc xá (`DORMITORY_SYSTEM`)
- Cổng thanh toán học phí (`PAYMENT_GATEWAY`)

## 2. Cấu Trúc Thư Mục
```
weeks/week-01/code/
├── package.json        # Cấu hình dự án & dependencies (express, mongoose)
├── server.js           # Điểm khởi chạy Express Server & khai báo endpoints
├── models/
│   └── Student.js      # Lược đồ Mongoose biểu diễn thông tin sinh viên
└── README.md           # Hướng dẫn thực hành & cài đặt hạt nhân
```

## 3. Các Khối Hạt Nhân Cần Cài Đặt (TODOs)
Trong file [`server.js`](server.js), bạn cần hoàn thiện 2 khối logic nghiệp vụ chính:
1. **`TODO 1` (`POST /api/v1/registry/echo`)**: Xử lý tín hiệu bắt tay (Handshake/Echo) giữa các dịch vụ, đo đạc độ trễ (`latencyMs`) và trả về `200 OK` hoặc `400 Bad Request`.
2. **`TODO 2` (`POST /api/v1/students/verify`)**: Tiếp nhận yêu cầu từ Consumer, tra cứu thông tin sinh viên (DB hoặc In-Memory), trả về `200 OK` (kèm cờ `eligibleForServices`) hoặc `404 Not Found` / `400 Bad Request`.

## 4. Hướng Dẫn Cài Đặt & Chạy Thử
```bash
# Di chuyển vào thư mục code tuần 01
cd weeks/week-01/code

# Cài đặt thư viện phụ thuộc (nếu chưa có node_modules)
npm install

# Khởi động dịch vụ
npm start
```
Dịch vụ sẽ lắng nghe tại cổng `http://localhost:3000`. Endpoint kiểm tra sức khỏe: `http://localhost:3000/healthz`.
