"""This is the file called when initializing the worker"""
from lrnflsk.factories.flask_instance import create_app
from lrnflsk.factories.celery_instance import configure_celery

# Imported for type hinting
from flask import Flask
from celery import Celery

app: Flask = create_app()
celery: Celery = configure_celery(app)
