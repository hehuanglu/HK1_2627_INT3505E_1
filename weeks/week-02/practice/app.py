from flask import Flask, jsonify, request, make_response, Response

app = Flask(__name__)

# -- tham số phân trang 
DEFAULT_SZIE, MAX_SIZE = 20, 100

BOOKS = []
_next = 1

# POST /books
@app.post("/books")
def create_book():
    global _next
    if not request.is_json:
        return jsonify(error = "expected JSON"), 415
    
    data = request.get_json(silent = True) or {}
    t = (data.get("title") or "").strip()
    a = (data.get("author") or "").strip()

    if not t or not a:
        return jsonify(error = "Thiếu title hoặc author"), 422
    
    book = {"id" : _next, "title" : t, "author" : a}
    _next += 1
    BOOKS.append(book)

    resp = make_response(jsonify(book), 201)
    resp.headers["Location"] = f"/books/{book['id']}"
    return resp

# GET /books/<id> -- cache 60s
@app.get("/books/<int:id>")
def fetch(id):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == id), None)
    if i is None:
        return jsonify(error = "Not found"), 404

    resp = make_response(jsonify(BOOKS[i]), 200)
    resp.headers["Cache-Control"] = "max-age=60"
    return resp

# PUT /books/<id> -- thay toàn bộ, author + title là bắt buộc
@app.put("/books/<int:id>")
def update(id):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == id), None)

    if i is None:
        return jsonify(error = "Not found"), 404

    p = request.get_json(silent = True) or {}

    if not request.is_json:
        return jsonify(error = "expected JSON"), 415

    t, a = p.get("title", "").strip(), p.get("author", "").strip()

    if not t or not a:
        return jsonify(error = "Thiếu title hoặc author"), 422

    BOOKS[i] = {
        "id": id, "title": t, "author": a,
        "isbn": p.get("isbn", "").strip(), 
        "price": p.get("price")
    }

    return jsonify(BOOKS[i]), 200

#PATCH -- chỉ cập nhật field có trong body
@app.patch("/books/<int:id>")
def patch(id):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == id), None)

    if i is None:
        return jsonify(error = "Not found"), 404

    p = request.get_json(silent = True) or {}

    if not request.is_json:
        return jsonify(error = "expected JSON"), 415

    if p.get("price") < 0:
            return jsonify(error = "price must be >= 0"), 422

    BOOKS[i].update(p)
    return jsonify(BOOKS[i]), 200

# DELETE /books/<id>
@app.delete("/books/<int:id>")
def delete(id):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == id), None)

    if i is None:
        return jsonify(error = "Not found"), 404

    BOOKS.pop(i)
    return Response(status=204)

# list + filter + paginate + links
@app.get("/books")
def query():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SZIE))
    except ValueError:
        return jsonify(error = "page and size must be integers"), 422

    page = max(page, 1)
    size = min(max(size, 1), MAX_SIZE)

    # author chính xác, q tìm trong title
    flt = BOOKS

    a = request.args.get("author")
    if a:
        flt = [b for b in flt if b.get("author").lower() == a.lower()]

    q = (request.args.get("q") or "").strip()
    if q:
        flt = [b for b in flt if q.lower() in b.get("title", "").lower()]

    # paginate
    total = len(flt)
    start = (page - 1) * size
    end = start + size
    data = flt[start:end]
    last_page = (total + size - 1) // size 

    # HATEOAS links 
    def u(p):
        return f"/books?page={p}&size={size}"

    links = {
        "self": {"href": u(page)},
        "first": {"href": u(1)},
        "last": {"href": u(max(last_page, 1))}
    }

    if page > 1:
        links["prev"] = {"href": u(page - 1)}

    if end < total:
        links["next"] = {"href": u(page + 1)}

    body = {
        "data": data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": last_page
        },
        "links": links
    }

    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp



if __name__ == "__main__":
    run = app.run(host="127.0.0.1", port=5002, debug=True)
    