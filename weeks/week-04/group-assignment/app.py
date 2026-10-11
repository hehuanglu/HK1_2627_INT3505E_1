"""Books API cơ bản: lưu trong bộ nhớ và xác thực JWT cho các route ghi."""
import json
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from functools import wraps
from http import HTTPStatus
from math import isfinite

import jwt
import yaml
from flask import Flask, jsonify, request, send_from_directory
from swagger_ui_bundle import swagger_ui_path
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.json.ensure_ascii = False
app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET", "soa-week05-local-demo-secret-change-before-deployment")
OPENAPI_FILE = Path(__file__).with_name("openapi.yaml")

# Dữ liệu mất khi khởi động lại ứng dụng.
books = {}
next_id = 1


def error(status, detail):
    response = jsonify(
        type="about:blank", title=HTTPStatus(status).phrase,
        status=status, detail=detail, instance=request.path,
    )
    response.status_code = status
    response.content_type = "application/problem+json"
    if status == 401:
        response.headers["WWW-Authenticate"] = "Bearer"
    return response


def demo_token():
    """Tạo token dùng thử, có hiệu lực một giờ, cho bài thực hành local."""
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": "soa-student", "iat": now, "exp": now + timedelta(hours=1)},
        app.config["JWT_SECRET"], algorithm="HS256",
    )


def require_token(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        parts = request.headers.get("Authorization", "").split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return error(401, "Thiếu hoặc sai bearer token.")
        try:
            jwt.decode(parts[1], app.config["JWT_SECRET"], algorithms=["HS256"],
                       options={"require": ["sub", "exp"]})
        except jwt.InvalidTokenError:
            return error(401, "Bearer token không hợp lệ hoặc đã hết hạn.")
        return handler(*args, **kwargs)
    return wrapper


@app.errorhandler(HTTPException)
def http_error(exception):
    return error(exception.code, exception.description)


def read_book_input(required=False):
    if not request.is_json:
        return None, error(400, "Cần gửi nội dung JSON.")
    try:
        data = json.loads(request.get_data(), parse_constant=reject_json_constant)
    except (ValueError, UnicodeDecodeError):
        return None, error(400, "Nội dung JSON không hợp lệ.")
    if not isinstance(data, dict) or not data:
        return None, error(422, "Cần gửi một đối tượng có ít nhất một trường.")
    if set(data) - {"title", "author", "isbn", "price"}:
        return None, error(422, "Chỉ nhận title, author, isbn và price.")
    if required and not {"title", "author"} <= set(data):
        return None, error(422, "title và author là bắt buộc.")
    for field in ("title", "author", "isbn"):
        if field in data:
            if not isinstance(data[field], str):
                return None, error(422, f"{field} phải là chuỗi.")
            if field != "isbn" and len(data[field]) < 1:
                return None, error(422, f"{field} không được rỗng.")
    if "price" in data:
        price = data["price"]
        if (isinstance(price, bool) or not isinstance(price, (int, float))
                or price < 0 or (isinstance(price, float) and not isfinite(price))):
            return None, error(422, "price phải là số hữu hạn lớn hơn hoặc bằng 0.")
    return data, None


def reject_json_constant(value):
    raise ValueError(f"Giá trị không hợp lệ trong JSON: {value}")


def find_book(book_id):
    try:
        key = int(book_id)
        if key < 1:
            raise ValueError
    except ValueError:
        return None, error(400, "bookId phải là số nguyên lớn hơn hoặc bằng 1.")
    if key not in books:
        return None, error(404, "Không tìm thấy sách.")
    return books[key], None


@app.get("/")
def index():
    return {"message": "Ứng dụng Flask đang chạy."}


@app.get("/openapi.json")
def openapi_document():
    """Phục vụ OpenAPI dưới dạng JSON cho Swagger UI và công cụ client."""
    try:
        with OPENAPI_FILE.open(encoding="utf-8") as spec_file:
            spec = yaml.safe_load(spec_file)
    except (OSError, yaml.YAMLError):
        app.logger.exception("Không thể đọc openapi.yaml")
        return error(500, "Không thể tải tài liệu OpenAPI.")
    return jsonify(spec)


@app.get("/docs")
def swagger_docs():
    """Hiển thị Swagger UI dùng tài liệu OpenAPI của ứng dụng."""
    return """<!doctype html>
<html lang="vi">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Books API — Swagger UI</title>
    <link rel="stylesheet" href="/docs/swagger-ui.css">
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="/docs/swagger-ui-bundle.js"></script>
    <script>
      window.onload = () => SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",
        deepLinking: true,
        presets: [SwaggerUIBundle.presets.apis],
        layout: "BaseLayout"
      });
    </script>
  </body>
</html>"""


@app.get("/docs/<path:asset>")
def swagger_asset(asset):
    return send_from_directory(swagger_ui_path, asset)


@app.get("/v1/books")
def list_books():
    try:
        limit = int(request.args.get("limit", "20"))
        if not 1 <= limit <= 100:
            raise ValueError
    except ValueError:
        return error(400, "limit phải là số nguyên từ 1 đến 100.")
    query = request.args.get("q", "").casefold()
    results = [book for book in books.values() if query in book["title"].casefold()]
    return jsonify(results[:limit])


@app.post("/v1/books")
@require_token
def create_book():
    global next_id
    data, problem = read_book_input(required=True)
    if problem is not None:
        return problem
    book = {"id": next_id, **data}
    books[next_id] = book
    next_id += 1
    return jsonify(book), 201, {"Location": f"/v1/books/{book['id']}"}


@app.get("/v1/books/<book_id>")
def get_book_by_id(book_id):
    book, problem = find_book(book_id)
    if problem is not None:
        return problem
    return jsonify(book)


@app.patch("/v1/books/<book_id>")
@require_token
def patch_book(book_id):
    book, problem = find_book(book_id)
    if problem is not None:
        return problem
    data, problem = read_book_input()
    if problem is not None:
        return problem
    book.update(data)
    return jsonify(book)


@app.delete("/v1/books/<book_id>")
@require_token
def delete_book(book_id):
    book, problem = find_book(book_id)
    if problem is not None:
        return problem
    del books[book["id"]]
    return "", 204


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="127.0.0.1", port=port)
