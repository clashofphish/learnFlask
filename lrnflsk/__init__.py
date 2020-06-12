from flask import Flask
import os
import logging
from healthcheck import HealthCheck, EnvironmentDump
from threading import Thread
# from multiprocessing import Process

from lrnflsk.bye import bye
from lrnflsk.hello import hello
from lrnflsk.queue_tasks import sqs
from lrnflsk.utility_functions.sqs_utilities import sqs_queue_on_name
from lrnflsk.long_tasks import simple_long_task


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

    # Log which config using
    if os.getenv('LEARN_FLASK_CONFIG') is None:
        app.logger.debug('Using development config')
    elif os.getenv('LEARN_FLASK_CONFIG') is not None:
        app.logger.debug('Using prod config, but this message should not show up')

    # Register blueprints
    app.register_blueprint(bye, url_prefix='/bye')
    app.register_blueprint(hello, url_prefix='/hello')
    app.register_blueprint(sqs, url_prefix='/sqs')

    # Setup system check endpoints
    health = HealthCheck()
    envdump = EnvironmentDump()

    app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())
    app.add_url_rule('/environment', 'environment', view_func=lambda: envdump.run())

    # Setup SQS app object
    app.sqs, message = sqs_queue_on_name(app.config['SQS_NAME'])
    app.logger.debug(message)

    @app.before_first_request
    def start_background_threads():
        thread = Thread(
            target=simple_long_task,
            kwargs={'queue_resource': app.sqs}
        )
        thread.start()

    # @app.before_first_request
    # def start_background_threads():
    #     process = Process(
    #         target=simple_long_task,
    #         args=(app.sqs, )
    #     )
    #     process.daemon = True
    #     process.start()

    return app





