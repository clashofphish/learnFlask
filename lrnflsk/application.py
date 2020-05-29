from flask import current_app as app
from flask import Blueprint, url_for
import os

bye = Blueprint('bye', __name__)


@bye.route('/')
def index():    # app.logger.debug('Log location {}'.format(app.config['LOG_LOC']))
    app.logger.error('Bye: Log level: {}'.format(app.config['LOG_LEVEL']))
    app.logger.info('Bye: Log info')
    app.logger.error('Bye: Log error')
    print(url_for('bye.index'))
    return 'Bye Index Page ' + str(app.config['LOG_LEVEL'])


@bye.route('/bye')
def goodbye_world():
    app.logger.debug('Bye world visited')
    return 'Bye World!'


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