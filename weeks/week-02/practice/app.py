from flask import Flask, jsonify, request, make_response, Response

app = Flask(__name__)

BOOKS = []
_next = 1

# GET /books 
@app.get("/books") 
def list_books():
    return jsonify (
        {
            "data" : BOOKS,
            "total" : len(BOOKS)
        }
    ), 200

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

if __name__ == "__main__":
    run = app.run(host="127.0.0.1", port=5002, debug=True)