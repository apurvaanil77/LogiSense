from services.worker.tasks import celery_app

if __name__ == "__main__":
    celery_app.worker_main(["worker", "--loglevel=INFO", "-Q", "events", "-P", "solo"])
