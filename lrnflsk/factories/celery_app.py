from lrnflsk import extensions


def configure_celery(app):
    """Configure celery instance using config from Flask app"""
    TaskBase = extensions.celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    # extensions.celery.conf.update(
    #     broker_url=app.config['CELERY_BROKER_URL'],
    #     broker_transport_options=app.config['CELERY_BROKER_TRANSPORT_OPTIONS'],
    #     task_default_queue=app.config['CELERY_DEFAULT_QUEUE'],
    #     worker_enable_remote_control=app.config['CELERY_ENABLE_REMOTE_CONTROL'],
    #     worker_send_task_events=app.config['CELERY_SEND_EVENTS']
    # )
    extensions.celery.conf.update(app.config)
    extensions.celery.Task = ContextTask
    return extensions.celery
