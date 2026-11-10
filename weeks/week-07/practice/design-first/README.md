# Product API — Design-First

Bản tối thiểu song song với `../code-first`: cùng resource Product, cùng hai thao tác liệt kê và tạo mới. Khác biệt chính là hợp đồng OpenAPI được viết trước; Connexion ánh xạ `operationId` trong YAML tới các hàm Python và validate request/response theo spec.

## Công cụ trong slide tuần 7

- **OpenAPI 3.0 YAML** trong `openapi/products.yaml` là hợp đồng API.
- **Connexion** nạp hợp đồng và nối operation với handler qua `operationId`.
- **Flask-SQLAlchemy** lưu Product vào SQLite, tương tự ví dụ Code-First.

## Chạy thử

Từ thư mục này:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

API chạy tại `http://localhost:5002`; giao diện Swagger UI ở `/ui/`.

```bash
curl http://localhost:5002/products
curl -X POST http://localhost:5002/products \
  -H 'Content-Type: application/json' \
  -d '{"name":"Bút chì","price":5000,"description":"HB"}'
```

Thử gửi `name` rỗng hoặc `price` âm để thấy Connexion từ chối request theo OpenAPI schema trước khi gọi handler. Database SQLite được tạo trong instance folder của Flask.
