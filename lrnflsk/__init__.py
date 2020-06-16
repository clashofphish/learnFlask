from flask import Flask
from celery import Celery
import os
import logging
from healthcheck import HealthCheck, EnvironmentDump

from lrnflsk.hello_bye.bye import bye
from lrnflsk.hello_bye.hello import hello
from lrnflsk.long_process.queue_tasks import sqs

import config_dev as config


celery = Celery(__name__, broker=config.CELERY_BROKER_URL)


def create_app():
    app = Flask(__name__)

    # Always use dev config
    app.config.from_object('config_dev')

    # *Should* load prod config when deployed into Docker container
    if os.getenv('LEARN_FLASK_CONFIG') is not None:
        app.config.from_envvar('LEARN_FLASK_CONFIG')

    # Set logging
    log_file = app.config['LOG_LOC'] + '/lrnflsk.log'
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=('%(levelname)s %(asctime)s %(name)s '
                'LrnFlsk %(threadName)s: %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_file
    )

    # Push config to Celery
    celery.conf.update(app.config)

    # Register blueprints
    app.register_blueprint(bye, url_prefix='/bye')
    app.register_blueprint(hello, url_prefix='/hello')
    app.register_blueprint(sqs, url_prefix='/sqs')

    # Setup system check endpoints
    health = HealthCheck()
    envdump = EnvironmentDump()

    app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())
    app.add_url_rule('/environment', 'environment', view_func=lambda: envdump.run())

    return app





