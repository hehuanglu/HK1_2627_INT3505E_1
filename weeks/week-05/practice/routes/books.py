import base64
import json
from pathlib import Path

from flask import Blueprint, jsonify, request
from jsonschema import ValidationError, validate
from sqlalchemy import select, tuple_
from sqlalchemy.exc import IntegrityError

from models import Book, db

bp = Blueprint("books", __name__)
SCHEMA = json.loads((Path(__file__).parents[1] / "schemas/book.json").read_text())
SORT = {"id": Book.id, "price": Book.price_vnd}


@bp.errorhandler(ValidationError)
def validation_error(error):
    return {"error": "validation_failed", "field": list(error.path),
            "message": error.message}, 400


@bp.errorhandler(IntegrityError)
def duplicate_isbn(error):
    db.session.rollback()
    return {"error": "isbn_exists"}, 400


def parse_sort(raw):
    desc = raw.startswith("-")
    key = raw[1:] if desc else raw
    if key not in SORT:
        raise ValueError("sort chỉ nhận id, -id, price, -price.")
    p = SORT[key]
    cols = [p.desc(), Book.id.desc()] if desc else [p.asc(), Book.id.asc()]
    return p, cols, desc


def apply_cursor(q, raw, sort, p, desc):
    if not raw:
        return q
    try:
        c = json.loads(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)))
        if c["s"] != sort:
            raise ValueError
        value, book_id = int(c["v"]), int(c["i"])
    except (ValueError, KeyError, TypeError):
        raise ValueError("Cursor không hợp lệ hoặc khác sort.")
    pair = tuple_(p, Book.id)
    return q.where(pair < (value, book_id) if desc else pair > (value, book_id))


def build_response(items, sort, p, more):
    nxt = None
    if items and more:
        last = items[-1]
        state = {"s": sort, "v": getattr(last, p.key), "i": last.id}
        nxt = base64.urlsafe_b64encode(json.dumps(state).encode()).decode().rstrip("=")
    return jsonify(data=[book.to_dict() for book in items], page={"next": nxt, "more": more})


@bp.get("")
def list_books():
    try:
        limit = min(int(request.args.get("limit", "20")), 100)
        category = request.args.get("category")
        category = int(category) if category is not None else None
        if limit < 1:
            raise ValueError("limit phải lớn hơn 0.")
        sort = request.args.get("sort", "-id")
        p, cols, desc = parse_sort(sort)
        q = select(Book).order_by(*cols)
        if category is not None:
            q = q.where(Book.category_id == category)
        q = apply_cursor(q, request.args.get("cursor"), sort, p, desc)
    except ValueError as error:
        return {"error": str(error)}, 400
    rows = db.session.scalars(q.limit(limit + 1)).all()
    return build_response(rows[:limit], sort, p, len(rows) > limit)


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
