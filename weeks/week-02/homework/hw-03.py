import hashlib
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


# ─── Hàm tiện ích ETag (Slide 21 & Slide 26) ───
def compute_book_etag(title, author, isbn, price):
    """
    Tạo ETag bằng cách hash nội dung theo gợi ý Slide 26:
    'Gợi ý: hash theo nội dung, lưu cùng record.'
    """
    content = f"{title}|{author}|{isbn}|{price}"
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def is_etag_matched(if_none_match_header, current_etag):
    """
    Kiểm tra khớp ETag giữa header If-None-Match và ETag hiện tại của record.
    Hỗ trợ cả dạng quoted ('\"hash\"'), unquoted, và wildcard (*).
    """
    if not if_none_match_header:
        return False
    # Xử lý client gửi nhiều ETag ngăn cách bởi dấu phẩy hoặc có prefix W/
    tags = [
        t.strip().lstrip("W/").strip('"')
        for t in if_none_match_header.split(",")
    ]
    return "*" in tags or current_etag in tags


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
    """Tự động khởi tạo cấu trúc bảng với cột etag lưu cùng record"""
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


# ─── ENDPOINTS /books ───

# POST /books ── Tạo sách mới (Tính ETag và lưu cùng record)
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

    # Tính ETag dựa trên nội dung
    etag = compute_book_etag(t, a, isbn, price)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, isbn, price, etag) VALUES (?, ?, ?, ?, ?)",
        (t, a, isbn, price, etag)
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
    resp.headers["ETag"] = f'"{etag}"'
    return resp


# GET /books/<id> ── Hỗ trợ ETag & Conditional Request If-None-Match (Bài tập 3)
@app.get("/books/<int:id>")
def fetch_book(id):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    if row is None:
        return jsonify(error="Not found"), 404

    book = dict(row)
    etag = book.get("etag")
    calculated_etag = compute_book_etag(book["title"], book["author"], book["isbn"], book["price"])

    # Tự động đồng bộ ETag nếu chưa có (do hw-01 tạo) hoặc nội dung đã bị thay đổi
    if etag != calculated_etag:
        etag = calculated_etag
        db.execute("UPDATE books SET etag = ? WHERE id = ?", (etag, id))
        db.commit()

    # Kiểm tra Conditional Request qua header If-None-Match
    if_none_match = request.headers.get("If-None-Match")
    if if_none_match and is_etag_matched(if_none_match, etag):
        # Theo RFC 9110: 304 Not Modified KHÔNG được có body, nhưng phải có ETag & Cache-Control
        resp = Response(status=304)
        resp.headers["ETag"] = f'"{etag}"'
        resp.headers["Cache-Control"] = "max-age=60"
        return resp

    # Trả về dữ liệu nếu ETag không khớp hoặc client không gửi If-None-Match
    resp = make_response(jsonify({
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "isbn": book["isbn"],
        "price": book["price"]
    }), 200)
    resp.headers["ETag"] = f'"{etag}"'
    resp.headers["Cache-Control"] = "max-age=60"
    return resp


# PUT /books/<id> ── Thay toàn bộ, tính lại ETag mới
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

    new_etag = compute_book_etag(t, a, isbn, price)

    db.execute(
        "UPDATE books SET title = ?, author = ?, isbn = ?, price = ?, etag = ? WHERE id = ?",
        (t, a, isbn, price, new_etag, id)
    )
    db.commit()

    updated = {
        "id": id,
        "title": t,
        "author": a,
        "isbn": isbn,
        "price": price
    }
    resp = make_response(jsonify(updated), 200)
    resp.headers["ETag"] = f'"{new_etag}"'
    return resp


# PATCH /books/<id> ── Cập nhật từng phần, tính lại ETag mới
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
    
    current_book = dict(row)
    for field in allowed_fields:
        if field in p:
            val = p[field].strip() if isinstance(p[field], str) else p[field]
            updates.append(f"{field} = ?")
            values.append(val)
            current_book[field] = val

    if updates:
        new_etag = compute_book_etag(
            current_book["title"],
            current_book["author"],
            current_book["isbn"],
            current_book["price"]
        )
        updates.append("etag = ?")
        values.append(new_etag)

        values.append(id)
        sql = f"UPDATE books SET {', '.join(updates)} WHERE id = ?"
        db.execute(sql, values)
        db.commit()
    else:
        new_etag = current_book.get("etag")

    updated_row = db.execute("SELECT id, title, author, isbn, price FROM books WHERE id = ?", (id,)).fetchone()
    resp = make_response(jsonify(dict(updated_row)), 200)
    if new_etag:
        resp.headers["ETag"] = f'"{new_etag}"'
    return resp


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


# GET /books ── Lọc, phân trang, HATEOAS links, Cache
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
    query_sql = f"SELECT id, title, author, isbn, price FROM books {where_clause} LIMIT ? OFFSET ?"
    query_params = params + [size, offset]
    rows = db.execute(query_sql, query_params).fetchall()
    data = [dict(r) for r in rows]

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


# POST /orders/<oid>/cancel ── Hủy đơn hàng
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
    app.run(host="127.0.0.1", port=5003, debug=True)
