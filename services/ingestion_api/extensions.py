from flask import Flask
from common.db import init_db


def init_extensions(app: Flask):
    with app.app_context():
        init_db()
