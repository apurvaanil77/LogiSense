from flask import Blueprint, jsonify
from common.db import SessionLocal
from common.models.event import Event
from sqlalchemy import func

bp = Blueprint("analytics", __name__)


@bp.route("/analytics/deployments/count", methods=["GET"])
def deployment_count():
    session = SessionLocal()
    try:
        count = (
            session.query(func.count(Event.id))
            .filter(Event.event_type == "deployment_created")
            .scalar()
        )
        return jsonify({"deployment_count": count})
    finally:
        session.close()


@bp.route("/analytics/errors/recent", methods=["GET"])
def recent_errors():
    session = SessionLocal()
    try:
        events = (
            session.query(Event)
            .filter(Event.event_type == "error_occurred")
            .order_by(Event.created_at.desc())
            .limit(20)
            .all()
        )
        return jsonify(
            [
                {
                    "id": e.id,
                    "message": e.message,
                    "component_name": e.component_name,
                    "created_at": e.created_at.isoformat(),
                }
                for e in events
            ]
        )
    finally:
        session.close()


@bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200
