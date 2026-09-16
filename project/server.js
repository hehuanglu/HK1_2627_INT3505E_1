require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

// ============================================================
// Database Connection
// ============================================================
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/soa-project';

mongoose
  .connect(MONGO_URI)
  .then(() => console.log('✅ MongoDB connected:', MONGO_URI))
  .catch((err) => {
    console.error('❌ MongoDB connection error:', err.message);
    process.exit(1);
  });

// ============================================================
// Routes
// Mỗi tuần học thêm 1 route module ở đây (qua Gate C)
// ============================================================
const usersRouter = require('./routes/users');
app.use('/users', usersRouter);

// ============================================================
// Health Check
// (Tuần 10 sẽ mở rộng endpoint này thành /healthz chi tiết hơn)
// ============================================================
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ============================================================
// 404 — Resource Not Found
// ============================================================
app.use((_req, res) => {
  res.status(404).json({
    type: 'https://httpstatuses.com/404',
    title: 'Not Found',
    status: 404,
    detail: 'The requested resource does not exist.',
  });
});

// ============================================================
// Global Error Handler
// ============================================================
// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({
    type: 'https://httpstatuses.com/500',
    title: 'Internal Server Error',
    status: 500,
    detail: err.message || 'An unexpected error occurred.',
  });
});

// ============================================================
// Start Server
// ============================================================
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
