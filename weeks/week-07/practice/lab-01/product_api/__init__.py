from flask import Flask
from werkzeug.exceptions import HTTPException

from .api.products import products_bp
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

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return {
            "error": error.code,
            "detail": error.message,
        }, error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return {
            "error": error.name.lower().replace(" ", "_"),
            "detail": error.description,
        }, error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        db.session.rollback()
        app.logger.exception("Unhandled API error")
        return {
            "error": "internal_error",
            "detail": "Đã xảy ra lỗi nội bộ.",
        }, 500

    return app
