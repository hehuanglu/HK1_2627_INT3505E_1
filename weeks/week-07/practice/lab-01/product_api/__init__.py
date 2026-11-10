from flask import Flask
from werkzeug.exceptions import HTTPException

from .api.products import products_bp
from .api.orders import orders_bp
from .api.health import health_bp
from .config import Config
from .errors import ApiError
from .extensions import db


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(health_bp)

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return {
            "code": error.code,
            "message": error.message,
        }, error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return {
            "code": error.name.lower().replace(" ", "_"),
            "message": error.description,
        }, error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        db.session.rollback()
        app.logger.exception("Unhandled API error")
        return {
            "code": "internal_error",
            "message": "Đã xảy ra lỗi nội bộ.",
        }, 500

    @app.cli.command("init-db")
    def init_db_command():
        """Create tables for a new local/demo database."""
        db.create_all()
        print("Database tables are ready.")

    return app
