import pytest

from app import create_app
from models import Book, db


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "books.db"
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )
    yield application
    with application.app_context():
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def book_with_private_field(app, monkeypatch):
    # Rows loaded by the API will also have this simulated private attribute.
    monkeypatch.setattr(Book, "password_hash", "fixture-only", raising=False)
    with app.app_context():
        book = Book(title="API Design Patterns", author="J.J. Geewax", year=2021)
        db.session.add(book)
        db.session.commit()
        return book.id
