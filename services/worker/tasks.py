from celery import Celery
from common.config import settings
from common.db import SessionLocal
from common.models.event import Event

celery_app = Celery(
    "logisense_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

@celery_app.task(name="worker.tasks.process_event", max_retries=3)
def process_event(event_data: dict):
    session = SessionLocal()
    try:
        event = Event(
            event_type=event_data["event_type"],
            deployment_id=event_data.get("deployment_id"),
            component_name=event_data.get("component_name"),
            status=event_data.get("status"),
            message=event_data.get("message"),
            payload=event_data.get("payload"),
        )
        session.add(event)
        session.commit()
    except Exception as e:
        session.rollback()
        raise process_event.retry(exc=e, countdown=5)
    finally:
        session.close()
