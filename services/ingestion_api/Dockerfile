FROM python:3.11-slim

WORKDIR /app
COPY ../.. /app

RUN pip install --no-cache-dir -r services/ingestion_api/requirements.txt

CMD ["python", "services/ingestion_api/app.py"]
