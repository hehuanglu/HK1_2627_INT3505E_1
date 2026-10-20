from flask import Flask
from models import db
from routes.books import bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookstore.db"
db.init_app(app)
app.register_blueprint(bp, url_prefix="/api/v1/books")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000)
