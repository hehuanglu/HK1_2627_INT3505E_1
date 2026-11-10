from pathlib import Path

import connexion

from extensions import db
from models import Product  # noqa: F401 — register model before create_all


HERE = Path(__file__).resolve().parent
app = connexion.FlaskApp(
    __name__, specification_dir=str(HERE / "openapi")
)
app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products-design-first.db"
app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app.app)
app.add_api("products.yaml", validate_responses=True)

with app.app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(port=5002)
