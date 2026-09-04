const mongoose = require('mongoose');

// Định nghĩa Mongoose Schema cho thực thể Học phần (Course)
// Tuân thủ quy tắc Resource Model: thuộc tính camelCase, ràng buộc kiểu dữ liệu rõ ràng
const courseSchema = new mongoose.Schema(
  {
    code: {
      type: String,
      required: [true, 'Mã học phần là bắt buộc'],
      unique: true,
      trim: true,
      uppercase: true
    },
    title: {
      type: String,
      required: [true, 'Tên học phần là bắt buộc'],
      trim: true
    },
    credits: {
      type: Number,
      required: [true, 'Số tín chỉ là bắt buộc'],
      min: [1, 'Số tín chỉ tối thiểu là 1'],
      max: [10, 'Số tín chỉ tối đa là 10']
    },
    department: {
      type: String,
      default: 'Khoa Công nghệ Thông tin',
      trim: true
    }
  },
  {
    timestamps: true, // Tự động quản lý createdAt và updatedAt
    versionKey: false // Ẩn trường __v để giữ payload JSON sạch sẽ
  }
);

module.exports = mongoose.model('Course', courseSchema);
