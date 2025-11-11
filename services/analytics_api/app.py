from flask import Flask
from services.analytics_api.routes.analytics import bp as analytics_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(analytics_bp, url_prefix="/api")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8001)
