# Lab 1 + bài tập về nhà — Product and Order API

Triển khai Product API từ Lab 1, rồi mở rộng theo bài tập tuần 7. Ứng dụng dùng Flask application factory, blueprint riêng cho từng resource, Marshmallow ở biên HTTP, service cho nghiệp vụ đơn hàng, SQLAlchemy 2.x và SQLite.

## Chạy local

Từ thư mục `weeks/week-07/practice/lab-01/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db
python app.py
```

Database mặc định được tạo dưới `instance/lab-01.sqlite`. Có thể cấu hình đường dẫn bằng `DATABASE_URL`. CLI `init-db` dùng `create_all()` để khởi tạo bài thực hành mới; thay đổi schema trên dữ liệu đang dùng cần migration.

## API

### Products — `/api/v1/products`

| Method | Path | Mô tả |
| --- | --- | --- |
| `GET` | `/api/v1/products?page=1&size=20` | Liệt kê sản phẩm chưa archive, có phân trang |
| `GET` | `/api/v1/products/{id}` | Lấy một sản phẩm chưa archive |
| `POST` | `/api/v1/products` | Tạo sản phẩm |
| `POST` | `/api/v1/products/{id}/reserve` | Giảm số lượng kho khi đặt trước |
| `PATCH` | `/api/v1/products/{id}` | Cập nhật `name` và/hoặc `price_cents` |
| `DELETE` | `/api/v1/products/{id}` | Archive sản phẩm (soft-delete) |

Tạo sản phẩm:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/products \
  -H 'Content-Type: application/json' \
  -d '{"sku":"PEN-001","name":"Bút chì","price_cents":5000,"qty_in_stock":10}'
```

`sku` dài 3–32 ký tự, `name` dài 1–255 ký tự, `price_cents` không âm và `qty_in_stock` mặc định bằng 0. `description` là trường tùy chọn. Pagination giới hạn `size` từ 1 đến 100. List/get ẩn sản phẩm đã archive. Reserve nhận `{"qty": 1}`, yêu cầu số lượng dương và không cho tồn kho giảm dưới 0. PATCH chỉ thay đổi trường có trong body; DELETE trả `204 No Content`.

### Orders — `/api/v1/orders`

Blueprint orders riêng cung cấp `POST /api/v1/orders`, `GET /api/v1/orders` và `GET /api/v1/orders/{id}`.

```bash
curl -X POST http://127.0.0.1:5000/api/v1/orders \
  -H 'Content-Type: application/json' \
  -d '{"customer_name":"Nguyễn An","items":[{"product_id":1,"quantity":2}]}'
```

`OrderItem` là entity liên kết `Order` và `Product`; một sản phẩm có thể xuất hiện trong nhiều đơn hàng. Mỗi dòng lưu số lượng và `unit_price_cents` tại thời điểm đặt để lịch sử đơn hàng không đổi khi giá sản phẩm được cập nhật. Một đơn không nhận lặp cùng `product_id`. Luồng này ghi nhận đơn hàng, chưa trừ kho; thao tác reserve hiện có vẫn là endpoint riêng.

GET orders dùng `selectinload(Order.items)` kết hợp `joinedload(OrderItem.product)`: lấy danh sách orders và các dòng hàng liên quan theo số lượng truy vấn cố định, tránh N+1 khi serialize sản phẩm.

### Health checks

- `GET /healthz`: liveness, chỉ xác nhận process còn chạy, không truy cập database.
- `GET /ready`: readiness, chạy `SELECT 1`; trả `503` nếu database chưa sẵn sàng.

Lỗi API có cấu trúc JSON nhất quán `{"code":"...","message":"..."}`. Validation trả `422`, tài nguyên không có trả `404`, xung đột trả `409`; lỗi nội bộ được log phía server và không lộ stack trace qua response.

## Docker Compose

Cần cài Docker có Compose plugin. Từ thư mục này chạy:

```bash
docker compose up --build
```

API sẵn sàng tại `http://localhost:8080`. Compose tạo named volume `product_data` để giữ SQLite database qua lần khởi động lại. Image chạy Gunicorn với user không phải root; healthcheck của container theo dõi `/ready`. Dừng bằng `docker compose down`; dữ liệu volume được giữ lại. Xóa cả dữ liệu bằng `docker compose down -v`.

## Pytest

Cài dependency phát triển và chạy từ thư mục này:

```bash
pip install -r requirements-dev.txt
pytest
```

Các kiểm tra gồm POST tạo đơn và GET orders có eager loading; GET kiểm tra số SELECT không tăng theo số đơn/dòng hàng.
