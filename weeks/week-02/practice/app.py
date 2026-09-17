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

if __name__ == "__main__":
    run = app.run(host="127.0.0.1", port=5002, debug=True)