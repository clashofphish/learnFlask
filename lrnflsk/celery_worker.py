"""This is the file called when initializing the worker"""
from lrnflsk.factories.flask_app import create_app
from lrnflsk.factories.celery_app import configure_celery

celery = configure_celery(create_app())
