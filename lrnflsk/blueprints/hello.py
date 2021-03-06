from flask import current_app as app
from flask import Blueprint, url_for
import os

hello = Blueprint('hello', __name__)


@hello.route('/')
def index():    # app.logger.debug('Log location {}'.format(app.config['LOG_LOC']))
    app.logger.error('Hello: Log level: {}'.format(app.config['LOG_LEVEL']))
    app.logger.info('Hello: Log info')
    app.logger.error('Hello: Log error')
    print(url_for('hello.index'))
    return 'Hello Index Page ' + str(app.config['LOG_LEVEL'])


@hello.route('/hello')
def hello_world():
    app.logger.debug('Hello world visited')
    return 'Hello World!'