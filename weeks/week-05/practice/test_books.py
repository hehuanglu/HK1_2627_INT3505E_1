import unittest
from flask import Flask
from models import Book, Category, db
from routes.books import bp

BASE = "/api/v1/books"


class PaginationTest(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        db.init_app(app)
        app.register_blueprint(bp, url_prefix=BASE)
        self.context = app.app_context()
        self.context.push()
        db.create_all()
        tech = Category(id=1, name="Tech", slug="tech")
        novel = Category(id=2, name="Novel", slug="novel")
        db.session.add_all([
            Book(id=1, title="B", price_vnd=100, category=tech),
            Book(id=2, title="A", price_vnd=100, category=tech),
            Book(id=3, title="A", price_vnd=200, category=tech),
            Book(id=4, title="A", price_vnd=200, category=tech),
            Book(id=5, title="Novel", price_vnd=150, category=novel),
        ])
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def test_offset_genre_and_multikey(self):
        params = {"strategy": "offset", "genre": "tech", "sort": "-price,title", "limit": 2}
        first = self.client.get(BASE, query_string=params).json
        self.assertEqual([b["id"] for b in first["data"]], [3, 4])
        self.assertEqual(first["pagination"], {"offset": 0, "limit": 2, "total": 4, "has_next": True})
        params["offset"] = 2
        second = self.client.get(BASE, query_string=params).json
        self.assertEqual([b["id"] for b in second["data"]], [2, 1])
        self.assertFalse(second["pagination"]["has_next"])

    def test_cursor_multikey_with_ties(self):
        for sort, expected in [("-price,title", [3, 4, 2, 1]), ("price,-title", [1, 2, 4, 3]),
                               ("price,title", [2, 1, 3, 4]), ("-price,-title", [4, 3, 1, 2]),
                               ("id", [1, 2, 3, 4]), ("-id", [4, 3, 2, 1])]:
            with self.subTest(sort=sort):
                params = {"strategy": "cursor", "genre": "tech", "sort": sort, "limit": 1}
                ids = []
                for _ in range(5):
                    response = self.client.get(BASE, query_string=params)
                    self.assertEqual(response.status_code, 200)
                    page = response.json
                    ids.extend(b["id"] for b in page["data"])
                    if not page["page"]["more"]:
                        self.assertIsNone(page["page"]["next"])
                        break
                    params["cursor"] = page["page"]["next"]
                self.assertEqual(ids, expected)

    def test_filter_and_empty(self):
        for strategy in ("offset", "cursor"):
            params = {"strategy": strategy, "genre": "novel"}
            page = self.client.get(BASE, query_string=params).json
            self.assertEqual([b["id"] for b in page["data"]], [5])
            params["genre"] = "unknown"
            page = self.client.get(BASE, query_string=params).json
            self.assertEqual(page["data"], [])
            if strategy == "offset":
                self.assertEqual(page["pagination"]["total"], 0)
            else:
                self.assertEqual(page["page"], {"next": None, "more": False})

    def test_cursor_context(self):
        params = {"genre": "tech", "sort": "-price,title", "limit": 1}
        params["cursor"] = self.client.get(BASE, query_string=params).json["page"]["next"]
        for changes in ({"sort": "price,title"}, {"genre": "novel"}, {"category": 2}):
            response = self.client.get(BASE, query_string={**params, **changes})
            self.assertEqual(response.status_code, 400)

    def test_invalid_query(self):
        for query in ("strategy=foo", "strategy=offset&offset=-1", "strategy=offset&offset=x",
                      "limit=0", "limit=x", "sort=foo", "sort=price,", "sort=--id",
                      "category=x", "cursor=broken"):
            with self.subTest(query=query):
                self.assertEqual(self.client.get(BASE + "?" + query).status_code, 400)

    def test_default_and_max_limit(self):
        db.session.add_all([Book(title="Extra", price_vnd=100) for _ in range(101)])
        db.session.commit()
        self.assertEqual(len(self.client.get(BASE).json["data"]), 20)
        for strategy in ("offset", "cursor"):
            page = self.client.get(BASE, query_string={"strategy": strategy, "limit": 999}).json
            self.assertEqual(len(page["data"]), 100)


if __name__ == "__main__":
    unittest.main()
