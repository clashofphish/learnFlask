from lrnflsk import extensions


def configure_celery(app):
    """Configure celery instance using config from Flask app"""
    TaskBase = extensions.celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    extensions.celery.conf.update(app.config)
    extensions.celery.Task = ContextTask
    return extensions.celery
