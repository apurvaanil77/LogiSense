from celery import Celery
from common.config import settings

celery_app = Celery(
    "logisense_ingestion",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.task_routes = {
    "worker.tasks.process_event": {"queue": "events"},
}
