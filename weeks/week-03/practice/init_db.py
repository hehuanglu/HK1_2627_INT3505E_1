"""Chạy python init_db.py để tạo bảng và thêm dữ liệu mẫu nếu bảng đang rỗng."""

from app import app
from data import Post, db


with app.app_context():
    db.create_all()

    # Chạy lại script không xóa dữ liệu và không thêm trùng bộ dữ liệu mẫu.
    if Post.query.count() == 0:
        for number in range(1, 13):
            db.session.add(Post(
                title=f"Bài viết {number}",
                content=f"Nội dung mẫu của bài viết {number}.",
                status="published" if number % 2 == 0 else "draft",
                author_id=(number - 1) % 3 + 1,
            ))
        db.session.commit()

    print(f"Database: {db.engine.url.database}")
    print(f"Số bài viết: {Post.query.count()}")
