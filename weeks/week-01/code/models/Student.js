const mongoose = require('mongoose');

const studentSchema = new mongoose.Schema(
  {
    studentId: {
      type: String,
      required: true,
      unique: true,
      trim: true,
      uppercase: true
    },
    fullName: {
      type: String,
      required: true,
      trim: true
    },
    email: {
      type: String,
      required: true,
      trim: true,
      lowercase: true
    },
    faculty: {
      type: String,
      required: true,
      default: 'Công nghệ Thông tin'
    },
    academicStatus: {
      type: String,
      enum: ['ACTIVE', 'SUSPENDED', 'GRADUATED', 'WITHDRAWN'],
      default: 'ACTIVE'
    },
    program: {
      type: String,
      default: 'Chuẩn'
    },
    creditsCompleted: {
      type: Number,
      default: 0
    }
  },
  {
    timestamps: true
  }
);

module.exports = mongoose.model('Student', studentSchema);
