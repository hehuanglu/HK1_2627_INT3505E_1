from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

app.json.sort_keys = False
app.json.ensure_ascii = False

_next = 2
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin", "year": 2008}
]

def find(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None

# LIST - GET /books
@app.route("/books", methods = ["GET"])
def list_books():
    q = request.args.get("q", "").strip().lower()
    sort_by = request.args.get("sort", "").strip().lower()
    
    result = BOOKS.copy()
    
    # (a) Tìm kiếm theo title
    if q:
        result = [b for b in result if q in b.get("title", "").lower()]
        
    # (b) Sắp xếp theo title
    if sort_by == "title":
        result = sorted(result, key=lambda b: b.get("title", "").lower())
        
    return jsonify(result), 200

# DETAIL - GET /books/<int:book_id>
@app.route("/books/<int:book_id>", methods = ["GET"])
def get_book(book_id):
    book = find(book_id)
    if book is None:
        return {"error": "Not found"}, 404
    return jsonify(book), 200

# CREATE - POST /books (kèm mở rộng: validate year >= 1900)
@app.route("/books", methods = ["POST"])
def create_book():
    global _next
    data = request.get_json(silent = True) or {}
    title = data.get("title")
    author = data.get("author")
    year = data.get("year")
    
    if not title or not author:
        return {"error": "Missing title or author"}, 400
        
    # (c) Bắt buộc field year là số >= 1900
    if year is None or not isinstance(year, int) or year < 1900:
        return {"error": "Field 'year' must be an integer >= 1900"}, 400
        
    book = {"id": _next, "title": title, "author": author, "year": year}
    BOOKS.append(book)
    _next += 1
    return jsonify(book), 201, {"Location" : f"/books/{book['id']}"}

# UPDATE - PUT, DELETE - DELETE /books/<int:book_id>
@app.route("/books/<int:book_id>", methods = ["PUT", "DELETE"])
def modify_book(book_id):
    book = find(book_id)
    if book is None:
        return {"error": "Not found"}, 404
        
    if request.method == "PUT":
        data = request.get_json(silent = True) or {}
        
        if "year" in data:
            year = data["year"]
            if not isinstance(year, int) or year < 1900:
                return {"error": "Field 'year' must be an integer >= 1900"}, 400
                
        book.update(data)
        return jsonify(book), 200
    else:
        BOOKS.remove(book)
        return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)