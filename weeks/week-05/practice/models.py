from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BookAuthor(db.Model):
    __tablename__ = "book_authors"
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), primary_key=True)
    role = db.Column(db.String(10), default="co")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    books = db.relationship("Book", secondary="book_authors", back_populates="authors")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    display_name = db.Column(db.String(100))
    reviews = db.relationship("Review", back_populates="user")


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book = db.relationship("Book", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    price_vnd = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category")
    authors = db.relationship("Author", secondary="book_authors", back_populates="books")
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "price": {"amount": self.price_vnd, "currency": "VND"},
            "stock": self.stock,
            "category_id": self.category_id,
        }
