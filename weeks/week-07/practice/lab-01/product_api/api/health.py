from flask import Blueprint
from sqlalchemy import text

from ..extensions import db


health_bp = Blueprint("health", __name__)


@health_bp.get("/healthz")
def liveness():
    return {"status": "ok"}, 200


@health_bp.get("/ready")
def readiness():
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        db.session.rollback()
        return {"status": "degraded", "checks": {"db": "err"}}, 503
    return {"status": "ok", "checks": {"db": "ok"}}, 200
