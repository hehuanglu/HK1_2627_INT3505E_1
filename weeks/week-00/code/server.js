/**
 * SOA Week 00: Course Service Demo
 * Mục đích: Minh họa nguyên lý Resource Naming (JJ Geewax) & Service Contract
 * Framework: Express.js + Mongoose (hỗ trợ InMemory fallback khi chưa bật MongoDB)
 */

const express = require('express');
const mongoose = require('mongoose');
const Course = require('./models/Course');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/soa_week_00';

// Middleware phân tích body JSON
app.use(express.json());

// Biến cờ theo dõi trạng thái kết nối Database
let isMongoConnected = false;

// Bộ nhớ đệm tạm thời (In-Memory Fallback) giúp demo chạy ngay cả khi chưa bật MongoDB
let memoryCourses = [
  {
    _id: '65e5f1a0b123456789abcdef',
    code: 'INT3111',
    title: 'Service-Oriented Architecture',
    credits: 3,
    department: 'Bộ môn Công nghệ Phần mềm',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    _id: '65e5f1a0b123456789abcdeg',
    code: 'INT3105',
    title: 'Software Engineering',
    credits: 3,
    department: 'Bộ môn Công nghệ Phần mềm',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

// -------------------------------------------------------------
// 0. HEALTH CHECK ENDPOINT (Kiểm tra sức khỏe dịch vụ)
// -------------------------------------------------------------
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'UP',
    database: isMongoConnected ? 'MongoDB Connected' : 'In-Memory Mock Fallback',
    timestamp: new Date().toISOString()
  });
});

// -------------------------------------------------------------
// 1. LIST COURSES: GET /api/v1/courses
// Pattern: Collection Resource Query
// -------------------------------------------------------------
app.get('/api/v1/courses', async (req, res) => {
  try {
    if (isMongoConnected) {
      const courses = await Course.find();
      return res.status(200).json({ courses, total: courses.length });
    }
    return res.status(200).json({ courses: memoryCourses, total: memoryCourses.length });
  } catch (error) {
    return res.status(500).json({ error: 'Lỗi máy chủ nội bộ', details: error.message });
  }
});

// -------------------------------------------------------------
// 2. CREATE COURSE: POST /api/v1/courses
// Pattern: Standard Create Method (Trả về mã 201 Created)
// -------------------------------------------------------------
app.post('/api/v1/courses', async (req, res) => {
  try {
    const { code, title, credits, department } = req.body;

    // Ràng buộc nghiệp vụ: Bắt buộc truyền mã và tên học phần
    if (!code || !title || !credits) {
      return res.status(400).json({
        error: 'Dữ liệu không hợp lệ',
        message: 'Trường code, title và credits là bắt buộc.'
      });
    }

    if (isMongoConnected) {
      const existing = await Course.findOne({ code: code.toUpperCase() });
      if (existing) {
        return res.status(409).json({ error: 'Xung đột', message: 'Mã học phần đã tồn tại.' });
      }
      const newCourse = await Course.create({ code, title, credits, department });
      return res.status(201).location(`/api/v1/courses/${newCourse._id}`).json(newCourse);
    }

    // Xử lý bằng In-Memory
    const existingMem = memoryCourses.find((c) => c.code === code.toUpperCase());
    if (existingMem) {
      return res.status(409).json({ error: 'Xung đột', message: 'Mã học phần đã tồn tại trong bộ nhớ.' });
    }

    const newCourseMem = {
      _id: new mongoose.Types.ObjectId().toString(),
      code: code.toUpperCase(),
      title,
      credits: Number(credits),
      department: department || 'Khoa Công nghệ Thông tin',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    memoryCourses.push(newCourseMem);

    return res.status(201).location(`/api/v1/courses/${newCourseMem._id}`).json(newCourseMem);
  } catch (error) {
    return res.status(400).json({ error: 'Yêu cầu không hợp lệ', details: error.message });
  }
});

// -------------------------------------------------------------
// 3. GET COURSE BY ID: GET /api/v1/courses/:id
// Pattern: Individual Resource Access
// -------------------------------------------------------------
app.get('/api/v1/courses/:id', async (req, res) => {
  try {
    const { id } = req.params;

    if (isMongoConnected) {
      if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(400).json({ error: 'Định dạng ID không hợp lệ' });
      }
      const course = await Course.findById(id);
      if (!course) {
        return res.status(404).json({ error: 'Không tìm thấy', message: 'Học phần không tồn tại.' });
      }
      return res.status(200).json(course);
    }

    // In-memory
    const courseMem = memoryCourses.find((c) => c._id === id);
    if (!courseMem) {
      return res.status(404).json({ error: 'Không tìm thấy', message: 'Học phần không tồn tại.' });
    }
    return res.status(200).json(courseMem);
  } catch (error) {
    return res.status(500).json({ error: 'Lỗi máy chủ nội bộ', details: error.message });
  }
});

// -------------------------------------------------------------
// 4. DELETE COURSE: DELETE /api/v1/courses/:id
// Pattern: Standard Delete (Trả về 204 No Content khi thành công)
// -------------------------------------------------------------
app.delete('/api/v1/courses/:id', async (req, res) => {
  try {
    const { id } = req.params;

    if (isMongoConnected) {
      if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(400).json({ error: 'Định dạng ID không hợp lệ' });
      }
      const deleted = await Course.findByIdAndDelete(id);
      if (!deleted) {
        return res.status(404).json({ error: 'Không tìm thấy học phần để xóa' });
      }
      return res.status(204).send();
    }

    const index = memoryCourses.findIndex((c) => c._id === id);
    if (index === -1) {
      return res.status(404).json({ error: 'Không tìm thấy học phần để xóa' });
    }
    memoryCourses.splice(index, 1);
    return res.status(204).send();
  } catch (error) {
    return res.status(500).json({ error: 'Lỗi máy chủ', details: error.message });
  }
});

// -------------------------------------------------------------
// KHỞI ĐỘNG DỊCH VỤ VÀ THIẾT LẬP KẾT NỐI
// -------------------------------------------------------------
mongoose
  .connect(MONGODB_URI, { serverSelectionTimeoutMS: 2000 })
  .then(() => {
    isMongoConnected = true;
    console.log('✅ Đã kết nối thành công tới MongoDB:', MONGODB_URI);
  })
  .catch((err) => {
    console.warn('⚠️ Không thể kết nối MongoDB cục bộ (Đang chạy chế độ In-Memory Mock):', err.message);
  })
  .finally(() => {
    app.listen(PORT, () => {
      console.log(`🚀 Course Service (Week 00) đang lắng nghe tại: http://localhost:${PORT}`);
      console.log(`   - Endpoint List:   GET    http://localhost:${PORT}/api/v1/courses`);
      console.log(`   - Endpoint Create: POST   http://localhost:${PORT}/api/v1/courses`);
      console.log(`   - Health Check:    GET    http://localhost:${PORT}/health`);
    });
  });

module.exports = app;
