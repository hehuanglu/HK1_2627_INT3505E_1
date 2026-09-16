const express = require('express');
const router = express.Router();
const User = require('../models/User');

// ============================================================
// GET /users — List all users
// ============================================================
router.get('/', async (_req, res, next) => {
  try {
    // ========================================================
    // TODO [HỌC VIÊN IMPLEMENT — Tuần 02/03]:
    // Trả về danh sách tất cả User.
    // Gợi ý: User.find({})
    // Status code đúng: 200 OK
    // ========================================================
    return next(new Error('Not implemented yet'));
  } catch (err) {
    next(err);
  }
});

// ============================================================
// GET /users/:id — Get one user
// ============================================================
router.get('/:id', async (req, res, next) => {
  try {
    // ========================================================
    // TODO [HỌC VIÊN IMPLEMENT — Tuần 02/03]:
    // Tìm User theo req.params.id.
    // Nếu không tìm thấy → 404 Not Found.
    // Nếu tìm thấy → 200 OK + user object.
    // ========================================================
    return next(new Error('Not implemented yet'));
  } catch (err) {
    next(err);
  }
});

// ============================================================
// POST /users — Create a user
// ============================================================
router.post('/', async (req, res, next) => {
  try {
    // ========================================================
    // TODO [HỌC VIÊN IMPLEMENT — Tuần 02/03]:
    // Tạo User mới từ req.body.
    // Status code đúng: 201 Created + Location header.
    // Xử lý: email trùng → 409 Conflict (hoặc 422).
    // ========================================================
    return next(new Error('Not implemented yet'));
  } catch (err) {
    next(err);
  }
});

// ============================================================
// PATCH /users/:id — Partial update
// ============================================================
router.patch('/:id', async (req, res, next) => {
  try {
    // ========================================================
    // TODO [HỌC VIÊN IMPLEMENT — Tuần 02/03]:
    // Cập nhật một phần User (PATCH ≠ PUT).
    // Chỉ cập nhật field nào có trong req.body.
    // Nếu không tìm thấy → 404 Not Found.
    // ========================================================
    return next(new Error('Not implemented yet'));
  } catch (err) {
    next(err);
  }
});

// ============================================================
// DELETE /users/:id — Delete a user
// ============================================================
router.delete('/:id', async (req, res, next) => {
  try {
    // ========================================================
    // TODO [HỌC VIÊN IMPLEMENT — Tuần 02/03]:
    // Xoá User theo req.params.id.
    // Nếu không tìm thấy → 404 Not Found.
    // Nếu xoá thành công → 204 No Content (không có body).
    // ========================================================
    return next(new Error('Not implemented yet'));
  } catch (err) {
    next(err);
  }
});

module.exports = router;
