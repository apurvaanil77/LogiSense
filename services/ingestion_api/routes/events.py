from flask import Blueprint, request, jsonify
from services.ingestion_api.schemas import EventSchema
from services.ingestion_api.celery_app import celery_app
from common.config import settings

bp = Blueprint("events", __name__)
event_schema = EventSchema()


def require_api_key():
    key = request.headers.get("x-api-key")
    if key != settings.API_KEY:
        return False
    return True


@bp.route("/event", methods=["POST"])
def ingest_event():
    if not require_api_key():
        return jsonify({"error": "Forbidden"}), 403

    json_data = request.get_json() or {}
    errors = event_schema.validate(json_data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Send to Celery/Redis for processing
    celery_app.send_task("worker.tasks.process_event", args=[json_data])
    return jsonify({"status": "queued"}), 202


@bp.route("/events", methods=["POST"])
def ingest_events_bulk():
    if not require_api_key():
        return jsonify({"error": "Forbidden"}), 403

    json_data = request.get_json()

    if not isinstance(json_data, list):
        return jsonify({"error": "Expected an array of events"}), 400

    validation_errors = {}
    queued_count = 0

    for idx, event in enumerate(json_data):
        errors = event_schema.validate(event)
        if errors:
            validation_errors[idx] = errors
            continue

        # queue valid events
        celery_app.send_task("worker.tasks.process_event", args=[event])
        queued_count += 1

    return jsonify(
        {
            "queued": queued_count,
            "failed": len(validation_errors),
            "errors": validation_errors,
        }
    ), (207 if validation_errors else 202)


@bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200
