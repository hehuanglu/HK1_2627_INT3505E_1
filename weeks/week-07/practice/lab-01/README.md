# Lab 1 — Product API

Triển khai tối thiểu Product API theo phần **Thực hành 01** của slide tuần 7. Ứng dụng dùng Flask application factory, một blueprint, Marshmallow schema, SQLAlchemy 2.x và SQLite mặc định.

## Chạy ứng dụng

Từ thư mục `weeks/week-07/practice/lab-01/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Lần chạy đầu, ứng dụng tạo bảng `products` trong database SQLite dưới thư mục `instance/`. Có thể thay database bằng biến môi trường `DATABASE_URL`; mặc định là `sqlite:///lab-01.sqlite`.

## API

Base path: `/api/v1/products`

| Method | Path | Mô tả |
| --- | --- | --- |
| `GET` | `/api/v1/products?page=1&size=20` | Liệt kê sản phẩm chưa archive, phân trang |
| `GET` | `/api/v1/products/{id}` | Lấy một sản phẩm chưa archive |
| `POST` | `/api/v1/products` | Tạo sản phẩm |
| `POST` | `/api/v1/products/{id}/reserve` | Đặt trước số lượng trong kho |
| `PATCH` | `/api/v1/products/{id}` | Cập nhật `name` và/hoặc `price_cents` |
| `DELETE` | `/api/v1/products/{id}` | Archive sản phẩm (soft-delete) |

### Tạo sản phẩm

```bash
curl -X POST http://127.0.0.1:5000/api/v1/products \
  -H 'Content-Type: application/json' \
  -d '{"sku":"PEN-001","name":"Bút chì","price_cents":5000,"qty_in_stock":10}'
```

`sku` dài 3–32 ký tự, `name` dài 1–255 ký tự, `price_cents` không âm và `qty_in_stock` mặc định bằng 0. `description` là trường tùy chọn.

Danh sách trả về `items`, `page`, `size`, `total`; kích thước trang từ 1 đến 100. List và get ẩn sản phẩm đã archive. Reserve nhận `{"qty": 1}`, yêu cầu số lượng dương và không cho tồn kho giảm dưới 0. PATCH chỉ thay đổi trường có mặt trong request body. DELETE trả `204 No Content`.

### Lỗi

Lỗi API dùng JSON nhất quán theo yêu cầu lab:

```json
{
  "error": "conflict",
  "detail": "sku đã tồn tại."
}
```

Validation trả `422`, không tìm thấy trả `404`, SKU trùng hoặc tồn kho không đủ trả `409`. Lỗi HTTP khác cũng được chuyển về JSON cùng cấu trúc.

## Phạm vi

Thư mục này chỉ hoàn thiện sáu endpoint của Lab 1. Các phần OrderItem, Docker Compose, health checks và pytest được nêu riêng ở mục bài tập thêm cuối slide, không thuộc lab này.
