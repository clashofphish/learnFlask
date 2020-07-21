from lrnflsk import celery_holder

# Imported for type hinting
from flask import Flask
from celery import Celery


def configure_celery(app: Flask) -> Celery:
    """Configure celery instance using config from Flask app
    :returns Celery app
    """
    TaskBase = celery_holder.celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_holder.celery.conf.update(app.config)
    celery_holder.celery.Task = ContextTask
    return celery_holder.celery
