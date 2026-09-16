const mongoose = require('mongoose');

/**
 * User Schema — Resource cốt lõi của dự án xuyên suốt.
 *
 * Các tuần sau sẽ mở rộng schema này qua Gate C:
 * - Tuần 06: thêm `passwordHash`, `role` (RBAC)
 * - Tuần 09: thêm `apiVersion` metadata
 * - Tuần 11: thêm `deletedAt` (Soft Delete pattern)
 */
const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'name là bắt buộc'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'email là bắt buộc'],
      unique: true,
      lowercase: true,
      trim: true,
      match: [/^\S+@\S+\.\S+$/, 'email không hợp lệ'],
    },
  },
  {
    timestamps: true, // tự động thêm createdAt, updatedAt
    versionKey: false,
  }
);

module.exports = mongoose.model('User', userSchema);
