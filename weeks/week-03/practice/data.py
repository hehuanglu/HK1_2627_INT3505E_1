from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Hai cột dùng để lọc bài viết. Default giúp POST hiện tại vẫn tạo được bài.
    status = db.Column(db.String(20), nullable=False, default="draft")
    author_id = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "author_id": self.author_id,
        }
