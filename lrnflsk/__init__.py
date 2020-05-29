from flask import Flask, url_for
import os
import logging

import config_dev
# from lrnflsk.bye import bye
# from lrnflsk.hello import hello
from lrnflsk.application import hello, bye

def create_app(environment):
    app = Flask(__name__)

    # If dev use dev config
    # else if prod set env variable to use prod config
    if environment == 'prod':
        os.environ['LEARN_FLASK_CONFIG'] = ('/Users/zachary.smith/GitRepositories'
                                            '/nonWork/learnFlask/config_prod.py')
    else:
        app.config.from_object('config_dev')

    # Set env variable for prod config
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