import json
from pathlib import Path

from flask import Blueprint, jsonify, request
from jsonschema import ValidationError, validate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models import Book, db

bp = Blueprint("books", __name__)
SCHEMA = json.loads((Path(__file__).parents[1] / "schemas/book.json").read_text())


@bp.errorhandler(ValidationError)
def validation_error(error):
    return {"error": "validation_failed", "field": list(error.path),
            "message": error.message}, 400


@bp.errorhandler(IntegrityError)
def duplicate_isbn(error):
    db.session.rollback()
    return {"error": "isbn_exists"}, 400


@bp.get("")
def list_books():
    rows = db.session.scalars(select(Book).order_by(Book.id)).all()
    return jsonify([book.to_dict() for book in rows])


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
