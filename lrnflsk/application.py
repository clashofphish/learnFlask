from lrnflsk.factories.flask_instance import create_app
from lrnflsk.factories.celery_instance import configure_celery

# Imported for type hinting
from flask import Flask
from celery import Celery


def create_full_app() -> Flask:
    app: Flask = create_app()
    cel_app: Celery = configure_celery(app)
    return app
