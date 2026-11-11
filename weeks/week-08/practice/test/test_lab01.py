import pytest
from jsonschema import ValidationError, validate

from tools import get_book_schema


def test_list_books_returns_empty_array(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_missing_book_returns_not_found(client):
    response = client.get("/books/9999")

    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"


def test_create_book_requires_title(client):
    response = client.post("/books", json={"author": "J.J. Geewax"})

    assert response.status_code == 400
    assert any(error["field"] == "title" for error in response.get_json()["errors"])


def test_get_deleted_book_returns_not_found(client):
    created = client.post(
        "/books", json={"title": "API Design Patterns", "author": "J.J. Geewax"}
    )
    assert created.status_code == 201
    book_url = f"/books/{created.get_json()['id']}"

    deleted = client.delete(book_url)
    assert deleted.status_code == 204
    assert deleted.data == b""

    fetched = client.get(book_url)
    assert fetched.status_code == 404
    assert fetched.get_json()["code"] == "NOT_FOUND"


def test_response_extra_field_blocked(client, book_with_private_field):
    response = client.get(f"/books/{book_with_private_field}")
    assert response.status_code == 200
    book = response.get_json()
    assert "password_hash" not in book

    schema = get_book_schema()
    # Correct the intentional Lab 2 year mismatch and express nullable types in JSON Schema.
    properties = schema["properties"]
    properties["year"] = {"type": ["integer", "null"]}
    properties["isbn"].pop("nullable")
    properties["isbn"]["type"] = ["string", "null"]
    validate(book, schema)

    with pytest.raises(ValidationError, match="password_hash") as rejected:
        validate({**book, "password_hash": "fixture-only"}, schema)
    assert rejected.value.validator == "additionalProperties"
