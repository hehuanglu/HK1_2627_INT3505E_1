import base64
import json
from pathlib import Path

from flask import Blueprint, jsonify, request
from jsonschema import ValidationError, validate
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import IntegrityError

from models import Book, Category, db

bp = Blueprint("books", __name__)
SCHEMA = json.loads((Path(__file__).parents[1] / "schemas/book.json").read_text())
SORT = {"id": Book.id, "price": Book.price_vnd, "title": Book.title}


@bp.errorhandler(ValidationError)
def validation_error(error):
    return {"error": "validation_failed", "field": list(error.path),
            "message": error.message}, 400


@bp.errorhandler(IntegrityError)
def duplicate_isbn(error):
    db.session.rollback()
    return {"error": "isbn_exists"}, 400


def parse_sort(raw):
    keys = raw.split(",")
    if any(key.lstrip("-") not in SORT or key.startswith("--") for key in keys):
        raise ValueError("sort chỉ nhận id, price, title và dấu -.")
    if not any(key.lstrip("-") == "id" for key in keys):
        keys.append("-id" if keys[-1].startswith("-") else "id")
    return [(SORT[key.lstrip("-")], key.startswith("-")) for key in keys]


def apply_cursor(q, raw, sort, columns, filters):
    if not raw:
        return q
    try:
        c = json.loads(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)))
        values = c["v"]
        if c["s"] != sort or c["f"] != filters or len(values) != len(columns):
            raise ValueError
        if any(not isinstance(value, str if col.key == "title" else int)
               for (col, desc), value in zip(columns, values)):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        raise ValueError("Cursor không hợp lệ hoặc khác sort/filter.")
    conditions = []
    prefix = []
    for (col, desc), value in zip(columns, values):
        conditions.append(and_(*prefix, col < value if desc else col > value))
        prefix.append(col == value)
    return q.where(or_(*conditions))


def build_response(items, sort, columns, more, filters):
    nxt = None
    if items and more:
        last = items[-1]
        state = {"s": sort, "v": [getattr(last, col.key) for col, desc in columns],
                 "f": filters}
        nxt = base64.urlsafe_b64encode(json.dumps(state).encode()).decode().rstrip("=")
    return jsonify(data=[book.to_dict() for book in items], page={"next": nxt, "more": more})


@bp.get("")
def list_books():
    try:
        limit = min(int(request.args.get("limit", "20")), 100)
        category = request.args.get("category")
        category = int(category) if category is not None else None
        genre = request.args.get("genre")
        strategy = request.args.get("strategy", "cursor")
        if limit < 1:
            raise ValueError("limit phải lớn hơn 0.")
        if strategy not in ("offset", "cursor"):
            raise ValueError("strategy chỉ nhận offset hoặc cursor.")
        sort = request.args.get("sort", "-id")
        columns = parse_sort(sort)
        q = select(Book)
        if category is not None:
            q = q.where(Book.category_id == category)
        if genre is not None:
            q = q.join(Category).where(Category.slug == genre)
        filters = {"category": category, "genre": genre}
        if strategy == "offset":
            offset = int(request.args.get("offset", "0"))
            if offset < 0:
                raise ValueError("offset phải lớn hơn hoặc bằng 0.")
        else:
            q = apply_cursor(q, request.args.get("cursor"), sort, columns, filters)
    except ValueError as error:
        return {"error": str(error)}, 400
    q = q.order_by(*[col.desc() if desc else col.asc() for col, desc in columns])
    if strategy == "offset":
        total = db.session.scalar(select(func.count()).select_from(q.subquery()))
        rows = db.session.scalars(q.offset(offset).limit(limit)).all()
        return jsonify(data=[book.to_dict() for book in rows], pagination={
            "offset": offset, "limit": limit, "total": total,
            "has_next": offset + limit < total,
        })
    rows = db.session.scalars(q.limit(limit + 1)).all()
    return build_response(rows[:limit], sort, columns, len(rows) > limit, filters)


def read_payload():
    payload = request.get_json(silent=True)
    validate(payload, SCHEMA)
    return {
        "title": payload["title"], "isbn": payload.get("isbn"),
        "price_vnd": payload["price"]["amount"], "stock": payload.get("stock", 0),
        "category_id": payload.get("category_id"),
    }


@bp.post("")
def create_book():
    book = Book(**read_payload())
    db.session.add(book)
    db.session.commit()
    return book.to_dict(), 201


@bp.get("/<int:book_id>")
def get_book(book_id):
    return db.get_or_404(Book, book_id).to_dict()


@bp.put("/<int:book_id>")
def update_book(book_id):
    book = db.get_or_404(Book, book_id)
    for key, value in read_payload().items():
        setattr(book, key, value)
    db.session.commit()
    return book.to_dict()


@bp.delete("/<int:book_id>")
def delete_book(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return "", 204
