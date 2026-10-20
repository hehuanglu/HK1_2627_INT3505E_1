from app import app
from models import Book, Category, db

with app.app_context():
    db.create_all()
    if db.session.query(Book).first() is None:
        tech = Category(name="Công nghệ", slug="tech")
        novel = Category(name="Tiểu thuyết", slug="novel")
        db.session.add_all([
            Book(title="Python", price_vnd=100000, category=tech),
            Book(title="REST API", price_vnd=100000, category=tech),
            Book(title="SQL", price_vnd=200000, category=tech),
            Book(title="Truyện ngắn", price_vnd=80000, category=novel),
        ])
        db.session.commit()
        print("Đã thêm 4 sách mẫu.")
