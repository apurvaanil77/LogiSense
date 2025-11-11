from flask import Flask
from flask_cors import CORS
from services.ingestion_api.extensions import init_extensions
from services.ingestion_api.routes.events import bp as events_bp


def create_app():
    app = Flask(__name__)
    init_extensions(app)
    app.register_blueprint(events_bp, url_prefix="/api")

    # ---- CORS FIX HERE ----
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                ]
            }
        },
        supports_credentials=True,
    )
    # -----------------------

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
