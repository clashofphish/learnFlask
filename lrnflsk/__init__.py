from flask import Flask
import os
import logging


from lrnflsk.bye import bye
from lrnflsk.hello import hello


def create_app(environment):
    app = Flask(__name__)

    # Always use dev config
    app.config.from_object('config_dev')

    # If prod then overwrite dev config
    if environment == 'prod':
        os.environ['LEARN_FLASK_CONFIG'] = ('/Users/zachary.smith/GitRepositories'
                                            '/nonWork/learnFlask/config_prod.py')
    if os.getenv('LEARN_FLASK_CONFIG') is not None:
        app.config.from_envvar('LEARN_FLASK_CONFIG')

    log_file = app.config['LOG_LOC'] + '/lrnflsk.log'
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=('%(levelname)s %(asctime)s %(name)s '
                'LrnFlsk %(threadName)s: %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_file
    )

    if os.getenv('LEARN_FLASK_CONFIG') is None:
        app.logger.debug('Using development config')
    elif os.getenv('LEARN_FLASK_CONFIG') is not None:
        app.logger.debug('Using prod config, but this message should not show up')

    app.register_blueprint(bye, url_prefix='/bye')
    app.register_blueprint(hello, url_prefix='/hello')

    return app