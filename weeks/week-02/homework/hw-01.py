import json
import os
import sqlite3
import uuid
from flask import Flask, jsonify, request, make_response, Response, g

app = Flask(__name__)

# Đường dẫn database SQLite dùng chung trong homework
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")

# Tham số phân trang mặc định
DEFAULT_SIZE, MAX_SIZE = 20, 100


# ─── Quản lý kết nối SQLite với Flask context (g) ───
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Cho phép truy cập cột theo tên: row["title"]
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Tự động khởi tạo cấu trúc bảng nếu chưa tồn tại"""
    with app.app_context():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT,
                price REAL,
                etag TEXT
            );

            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL DEFAULT 'pending',
                total REAL NOT NULL,
                items TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.commit()


def serialize_book(row):
    """Chuẩn hóa dữ liệu trả về của sách (loại bỏ trường kỹ thuật nội bộ)"""
    return {
        "id": row["id"],
        "title": row["title"],
        "author": row["author"],
        "isbn": row["isbn"],
        "price": row["price"]
    }


# ─── ENDPOINTS /books ───

# POST /books ── Tạo sách mới
@app.post("/books")
def create_book():
    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    data = request.get_json(silent=True) or {}
    t = (data.get("title") or "").strip()
    a = (data.get("author") or "").strip()
    isbn = (data.get("isbn") or "").strip()
    price = data.get("price")

    if not t or not a:
        return jsonify(error="Thiếu title hoặc author"), 422

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, isbn, price) VALUES (?, ?, ?, ?)",
        (t, a, isbn, price)
    )
    db.commit()
    book_id = cursor.lastrowid

    book = {
        "id": book_id,
        "title": t,
        "author": a,
        "isbn": isbn,
        "price": price
    }

    resp = make_response(jsonify(book), 201)
    resp.headers["Location"] = f"/books/{book_id}"
    return resp


# GET /books/<id> ── Lấy chi tiết sách + Cache 60s
@app.get("/books/<int:id>")
def fetch_book(id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if row is None:
        return jsonify(error="Not found"), 404

    resp = make_response(jsonify(serialize_book(row)), 200)
    resp.headers["Cache-Control"] = "max-age=60"
    return resp


# PUT /books/<id> ── Thay toàn bộ, author + title là bắt buộc
@app.put("/books/<int:id>")
def update_book(id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if row is None:
        return jsonify(error="Not found"), 404

    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    data = request.get_json(silent=True) or {}
    t = (data.get("title") or "").strip()
    a = (data.get("author") or "").strip()
    isbn = (data.get("isbn") or "").strip()
    price = data.get("price")

    if not t or not a:
        return jsonify(error="Thiếu title hoặc author"), 422

    db.execute(
        "UPDATE books SET title = ?, author = ?, isbn = ?, price = ? WHERE id = ?",
        (t, a, isbn, price, id)
    )
    db.commit()

    updated = {
        "id": id,
        "title": t,
        "author": a,
        "isbn": isbn,
        "price": price
    }
    return jsonify(updated), 200


# PATCH /books/<id> ── Cập nhật từng phần (Whitelist, chống đổi id)
@app.patch("/books/<int:id>")
def patch_book(id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if row is None:
        return jsonify(error="Not found"), 404

    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    p = request.get_json(silent=True) or {}

    if p.get("price") is not None and p.get("price") < 0:
        return jsonify(error="price must be >= 0"), 422

    allowed_fields = ["title", "author", "isbn", "price"]
    updates = []
    values = []
    for field in allowed_fields:
        if field in p:
            updates.append(f"{field} = ?")
            values.append(p[field].strip() if isinstance(p[field], str) else p[field])

    if updates:
        values.append(id)
        sql = f"UPDATE books SET {', '.join(updates)} WHERE id = ?"
        db.execute(sql, values)
        db.commit()

    updated_row = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    return jsonify(serialize_book(updated_row)), 200


# DELETE /books/<id> ── Idempotent xóa, trả 204
@app.delete("/books/<int:id>")
def delete_book(id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if row is None:
        return jsonify(error="Not found"), 404

    db.execute("DELETE FROM books WHERE id = ?", (id,))
    db.commit()
    return Response(status=204)


# GET /books ── Lọc, phân trang bằng SQL, HATEOAS links, Cache
@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be integers"), 400

    page = max(page, 1)
    size = min(max(size, 1), MAX_SIZE)

    conditions = []
    params = []

    author = request.args.get("author")
    if author:
        conditions.append("LOWER(author) = LOWER(?)")
        params.append(author.strip())

    q = (request.args.get("q") or "").strip()
    if q:
        conditions.append("LOWER(title) LIKE LOWER(?)")
        params.append(f"%{q}%")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    db = get_db()
    count_sql = f"SELECT COUNT(*) as cnt FROM books {where_clause}"
    total = db.execute(count_sql, params).fetchone()["cnt"]

    offset = (page - 1) * size
    query_sql = f"SELECT * FROM books {where_clause} LIMIT ? OFFSET ?"
    query_params = params + [size, offset]
    rows = db.execute(query_sql, query_params).fetchall()
    data = [serialize_book(r) for r in rows]

    last_page = max((total + size - 1) // size, 1)

    def u(p):
        return f"/books?page={p}&size={size}"

    links = {
        "self": {"href": u(page)},
        "first": {"href": u(1)},
        "last": {"href": u(last_page)}
    }

    if page > 1:
        links["prev"] = {"href": u(page - 1)}

    if page < last_page:
        links["next"] = {"href": u(page + 1)}

    body = {
        "data": data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": last_page
        },
        "_links": links
    }

    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp


# ─── ENDPOINTS /orders (Theo Slide 12 & 15) ───

# POST /orders ── Tạo đơn hàng
@app.post("/orders")
def create_order():
    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    total = data.get("total", 0.0)

    if not items or total <= 0:
        return jsonify(error="items list and positive total are required"), 422

    oid = f"o_{uuid.uuid4().hex[:8]}"
    db = get_db()
    db.execute(
        "INSERT INTO orders (id, status, total, items) VALUES (?, ?, ?, ?)",
        (oid, "pending", float(total), json.dumps(items))
    )
    db.commit()

    body = {
        "id": oid,
        "status": "pending",
        "total": float(total),
        "_links": {
            "self": {"href": f"/orders/{oid}"},
            "cancel": {"href": f"/orders/{oid}/cancel", "method": "POST"}
        }
    }
    resp = make_response(jsonify(body), 201)
    resp.headers["Location"] = f"/orders/{oid}"
    return resp


# GET /orders/<oid> ── Chi tiết đơn hàng kèm HATEOAS
@app.get("/orders/<oid>")
def get_order(oid):
    db = get_db()
    row = db.execute("SELECT * FROM orders WHERE id = ?", (oid,)).fetchone()
    if row is None:
        return jsonify(error="Order not found"), 404

    order = dict(row)
    links = {
        "self": {"href": f"/orders/{oid}"}
    }
    # Theo Slide 12: Đơn hàng pending có liên kết cancel
    if order["status"] == "pending":
        links["cancel"] = {"href": f"/orders/{oid}/cancel", "method": "POST"}

    items_data = []
    if order.get("items"):
        try:
            items_data = json.loads(order["items"])
        except json.JSONDecodeError:
            items_data = []

    body = {
        "id": order["id"],
        "status": order["status"],
        "total": order["total"],
        "items": items_data,
        "created_at": order["created_at"],
        "_links": links
    }
    return jsonify(body), 200


# POST /orders/<oid>/cancel ── Hủy đơn hàng (Hiện thực hóa action từ HATEOAS)
@app.post("/orders/<oid>/cancel")
def cancel_order(oid):
    db = get_db()
    row = db.execute("SELECT * FROM orders WHERE id = ?", (oid,)).fetchone()
    if row is None:
        return jsonify(error="Order not found"), 404

    if row["status"] != "pending":
        return jsonify(error=f"Cannot cancel order with status '{row['status']}'"), 400

    db.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (oid,))
    db.commit()

    return jsonify({
        "id": oid,
        "status": "cancelled",
        "message": "Order successfully cancelled"
    }), 200


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5002, debug=True)
