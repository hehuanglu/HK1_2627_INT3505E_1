/**
 * SOA Week 01: VNU-UET Student Registry Gateway
 * Mục đích: Minh họa nguyên lý Kiến trúc hướng dịch vụ (SOA), 
 *           Giao tiếp Client-Server, Service Provider vs Service Consumer,
 *           và Chuẩn hóa phản hồi RESTful API.
 * 
 * Sách tham khảo:
 * - JJ Geewax: API Design Patterns (Ch. 1 & 2)
 * - Bruno Pedro: Building an API Product (Ch. 1, 2, 3)
 */

const express = require('express');
const mongoose = require('mongoose');
const Student = require('./models/Student');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/soa_week_01';

// ----------------------------------------------------------------------------
// MIDDLEWARE CƠ BẢN
// ----------------------------------------------------------------------------
app.use(express.json());

// Logger middleware: In thông tin request phục vụ việc giám sát và gỡ lỗi
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [REQUEST] ${req.method} ${req.url} - ClientIP: ${req.ip}`);
  next();
});

// Biến cờ theo dõi trạng thái kết nối MongoDB
let isMongoConnected = false;

// CSDL mô phỏng trong bộ nhớ (In-Memory Fallback)
// Giúp hệ thống chạy thử nghiệm ngay lập tức mà không bắt buộc phải cài đặt MongoDB
const memoryStudents = [
  {
    studentId: '21020001',
    fullName: 'Nguyễn Văn An',
    email: '21020001@vnu.edu.vn',
    faculty: 'Công nghệ Thông tin',
    academicStatus: 'ACTIVE',
    program: 'Chuẩn',
    creditsCompleted: 75
  },
  {
    studentId: '21020002',
    fullName: 'Trần Thị Bình',
    email: '21020002@vnu.edu.vn',
    faculty: 'Điện tử Viễn thông',
    academicStatus: 'SUSPENDED',
    program: 'Chất lượng cao',
    creditsCompleted: 42
  },
  {
    studentId: '21020003',
    fullName: 'Lê Hoàng Cường',
    email: '21020003@vnu.edu.vn',
    faculty: 'Cơ kỹ thuật và Tự động hóa',
    academicStatus: 'GRADUATED',
    program: 'Chuẩn',
    creditsCompleted: 135
  }
];

// ============================================================================
// 0. HEALTH CHECK ENDPOINT (Kiểm tra sức khỏe dịch vụ - Infrastructure Ping)
// ============================================================================
app.get('/healthz', (req, res) => {
  return res.status(200).json({
    status: 'UP',
    service: 'vnu-uet-student-registry-gateway',
    version: '1.0.0',
    database: isMongoConnected ? 'CONNECTED' : 'IN_MEMORY_FALLBACK',
    timestamp: new Date().toISOString(),
    uptimeSeconds: Math.floor(process.uptime())
  });
});

// ============================================================================
// 1. REGISTRY ECHO / HANDSHAKE: POST /api/v1/registry/echo
// ============================================================================
/**
 * Mô tả: Endpoint để các Service Consumer (Thư viện, KTX, Học phí) gửi tín hiệu bắt tay,
 *        kiểm tra khả năng tương thích và đo đạc độ trễ mạng giữa các dịch vụ.
 * 
 * Request Body mẫu:
 * {
 *   "consumerName": "LIBRARY_SYSTEM",
 *   "clientTimestamp": "2026-09-06T16:00:00.000Z",
 *   "payload": { "action": "HANDSHAKE" }
 * }
 */
app.post('/api/v1/registry/echo', (req, res) => {
  // ============================================================================
  // TODO 1 [HỌC VIÊN CÀI ĐẶT HẠT NHÂN]: Bắt tay & Kiểm tra tính tương thích dịch vụ
  // ----------------------------------------------------------------------------
  // Hướng dẫn nghiệp vụ:
  // 1. Kiểm tra Request Body:
  //    - Trường `consumerName` và `clientTimestamp` có được truyền lên không?
  //    - Nếu thiếu: Trả về HTTP 400 Bad Request với cấu trúc:
  //      { error: 'Bad Request', message: 'consumerName và clientTimestamp là bắt buộc.' }
  // 2. Tính toán độ trễ (latencyMs):
  //    - Lấy thời gian server hiện tại: const now = new Date();
  //    - Độ trễ xấp xỉ = now.getTime() - new Date(clientTimestamp).getTime();
  //    - Nếu clientTimestamp không hợp lệ (NaN), trả về HTTP 400.
  // 3. Trả về HTTP 200 OK với thông điệp bắt tay thành công:
  //    {
  //      status: 'ACKNOWLEDGED',
  //      consumer: consumerName,
  //      echoPayload: req.body.payload || null,
  //      serverTimestamp: now.toISOString(),
  //      latencyMs: Math.max(0, latencyMs),
  //      handshakeId: 'hs_' + Date.now()
  //    }
  // ============================================================================

  return res.status(501).json({
    error: 'Not Implemented',
    message: 'Chức năng echo đang chờ học viên cài đặt tại TODO 1.'
  });
});

// ============================================================================
// 2. STUDENT VERIFICATION: POST /api/v1/students/verify
// ============================================================================
/**
 * Mô tả: Cung cấp dịch vụ xác minh trạng thái học tập của sinh viên cho các hệ thống
 *        tiêu thụ dịch vụ (Service Consumer).
 * 
 * Request Body mẫu:
 * {
 *   "studentId": "21020001",
 *   "consumerSystem": "LIBRARY_SYSTEM"
 * }
 */
app.post('/api/v1/students/verify', async (req, res) => {
  // ============================================================================
  // TODO 2 [HỌC VIÊN CÀI ĐẶT HẠT NHÂN]: Xác thực trạng thái học tập sinh viên
  // ----------------------------------------------------------------------------
  // Hướng dẫn nghiệp vụ:
  // 1. Kiểm tra tính hợp lệ của dữ liệu đầu vào:
  //    - Trường `studentId` và `consumerSystem` có tồn tại không?
  //    - Nếu thiếu: Trả về HTTP 400 Bad Request với cấu trúc:
  //      { error: 'Bad Request', message: 'studentId và consumerSystem là bắt buộc.' }
  //
  // 2. Tìm kiếm sinh viên theo studentId:
  //    - Nếu isMongoConnected: Dùng await Student.findOne({ studentId: req.body.studentId.trim().toUpperCase() })
  //    - Nếu không: Tìm trong memoryStudents:
  //      memoryStudents.find(s => s.studentId === req.body.studentId.trim().toUpperCase())
  //
  // 3. Xử lý trường hợp không tìm thấy:
  //    - Nếu không tìm thấy sinh viên: Trả về HTTP 404 Not Found:
  //      { error: 'Not Found', message: `Không tìm thấy sinh viên có mã ${req.body.studentId}` }
  //
  // 4. Xử lý kết quả nghiệp vụ (Thành công):
  //    - Sinh viên được xem là đủ điều kiện sử dụng dịch vụ (`eligibleForServices: true`)
  //      KHI VÀ CHỈ KHI `academicStatus === 'ACTIVE'`.
  //    - Các trạng thái khác (SUSPENDED, GRADUATED, WITHDRAWN) -> `eligibleForServices: false`.
  //    - Trả về HTTP 200 OK kèm payload xác nhận tối giản (nguyên lý Information Hiding):
  //      {
  //        studentId: student.studentId,
  //        fullName: student.fullName,
  //        academicStatus: student.academicStatus,
  //        eligibleForServices: student.academicStatus === 'ACTIVE',
  //        verifiedBy: 'VNU-UET Student Registry Gateway',
  //        requestedBy: consumerSystem,
  //        verifiedAt: new Date().toISOString()
  //      }
  // ============================================================================

  return res.status(501).json({
    error: 'Not Implemented',
    message: 'Chức năng xác thực sinh viên đang chờ học viên cài đặt tại TODO 2.'
  });
});

// ----------------------------------------------------------------------------
// KHỞI ĐỘNG MÁY CHỦ
// ----------------------------------------------------------------------------
async function startServer() {
  try {
    // Thử kết nối MongoDB (Timeout sau 2 giây nếu không có DB chạy)
    await mongoose.connect(MONGODB_URI, { serverSelectionTimeoutMS: 2000 });
    isMongoConnected = true;
    console.log('[DATABASE] Kết nối MongoDB thành công.');
  } catch (err) {
    isMongoConnected = false;
    console.warn('[DATABASE] Không kết nối được MongoDB. Tự động chuyển sang chế độ In-Memory Mock Fallback.');
  }

  app.listen(PORT, () => {
    console.log(`========================================================`);
    console.log(`[SERVER] VNU-UET Student Registry Gateway đang chạy tại:`);
    console.log(`         http://localhost:${PORT}`);
    console.log(`[HEALTH] Kiểm tra trạng thái: http://localhost:${PORT}/healthz`);
    console.log(`========================================================`);
  });
}

// Khởi chạy server nếu file được chạy trực tiếp
if (require.main === module) {
  startServer();
}

module.exports = app;
