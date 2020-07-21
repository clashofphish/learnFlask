from flask import Flask
import os
import logging
from healthcheck import HealthCheck, EnvironmentDump

from lrnflsk.blueprints.bye import bye
from lrnflsk.blueprints.hello import hello
from lrnflsk.blueprints.queue_tasks import sqs


def create_app() -> Flask:
    app = Flask(__name__)

    # Always use dev config
    app.config.from_object('config_dev')

    # *Should* load prod config when deployed into Docker container
    if os.getenv('LEARN_FLASK_CONFIG') is not None:
        app.config.from_envvar('LEARN_FLASK_CONFIG')

    # Set logging
    log_file = app.config['LOG_LOC'] + app.config['LOG_FILE']
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=('%(levelname)s %(asctime)s %(name)s '
                'LrnFlsk %(threadName)s: %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_file
    )

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





