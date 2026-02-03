# LogiSense – Ingestion API

The **Ingestion API** is the entry point for **LogiSense** , a cloud-native logging and analytics platform.

This service receives structured events from applications, validates them, authenticates the sender, and asynchronously forwards them to the processing pipeline via **Redis + Celery** .

---

## 🚀 Responsibilities

- Accept structured logging events over HTTP
- Validate incoming payloads
- Authenticate producers using API keys
- Push events to a distributed queue
- Provide health checks for orchestration systems
- Auto-initialize database schema (MVP)

---

## 🧱 Architecture Role

```
Client / App
     │
     ▼
Flask Ingestion API
     │
     ▼
Redis (Celery Broker)
     │
     ▼
Celery Worker → PostgreSQL

```

This service **does not** write directly to the database.

All writes are handled asynchronously by worker services.

---

## 🛠 Tech Stack

- **Python 3.11**
- **Flask** – HTTP API
- **Marshmallow** – Request validation
- **Celery** – Async task dispatch
- **Redis** – Message broker
- **PostgreSQL** – Persistent storage (via worker)
- **Docker** – Containerization

---

## 📂 Folder Structure

```
services/ingestion_api/
├── app.py                # Flask app entrypoint
├── config.py             # Service-level config wrapper
├── schemas.py            # Marshmallow schemas
├── extensions.py         # DB & app initialization
├── celery_app.py         # Celery configuration
├── routes/
│   └── events.py         # Event ingestion endpoints
├── requirements.txt
└── Dockerfile
```

---

## 🔐 Authentication

All requests (except `/health`) require an API key.

**Header**

```
x-api-key: <LOGISENSE_API_KEY>
```

API keys are configured via environment variables.

---

## 📡 API Endpoints

### `POST /api/event`

Submit an event to LogiSense.

**Headers**

```
Content-Type: application/json
x-api-key: <your-api-key>
```

**Payload**

```
{
  "event_type": "deployment_created",
  "deployment_id": "dep-123",
  "component_name": "backend",
  "status": "success",
  "message": "Deployment completed",
  "payload": {
    "version": "1.0.0",
    "region": "us-east-1"
  }
}
```

**Response**

```
{
  "status": "queued"
}
```

**Status Codes**

- `202` – Event accepted
- `400` – Validation error
- `403` – Invalid API key

---

### `GET /api/health`

Health check endpoint for Docker / Kubernetes.

**Response**

```
{
  "status": "ok"
}
```

---

## 🧪 Validation Rules

- `event_type` → required, non-empty string
- All other fields are optional
- Payload must be valid JSON

Validation is handled via **Marshmallow schemas** .

---

## ⚙️ Environment Variables

| Variable            | Description                          |
| ------------------- | ------------------------------------ |
| `POSTGRES_DSN`      | PostgreSQL connection string         |
| `REDIS_URL`         | Redis broker URL                     |
| `LOGISENSE_API_KEY` | API key for authentication           |
| `ENV`               | Environment (`dev`,`staging`,`prod`) |

Example:

```
POSTGRES_DSN=postgresql+psycopg2://logisense:logisense@postgres:5432/logisense
REDIS_URL=redis://redis:6379/0
LOGISENSE_API_KEY=dev-key
ENV=dev
```

---

## 🐳 Running Locally (Docker)

This service is intended to be run via **Docker Compose** with Redis and PostgreSQL.

```
docker compose up ingestion-api
```

Once running:

```
http://localhost:5000/api/health
```

---

## 📈 Design Notes

- Event ingestion is **non-blocking**
- No synchronous database writes
- Failures in downstream processing do **not** affect ingestion availability
- Designed for high-throughput event pipelines
- Easy to extend with new event types
