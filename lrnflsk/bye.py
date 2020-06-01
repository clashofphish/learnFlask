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


@bye.route('/config')
def set_dev_config():
    return {
        's3': str(app.config['S3_REGION']),
        'log': str(app.config['LOG_LEVEL']),
        'table': str(app.config['DB_TABLE'])
    }
#
#
# @app.route('/json/test')
# def json_api():
#     metal = 'essential'
#     thrash = [1, 3, 2, 4]
#     doom = 666
#     return {
#         "music": metal,
#         "tempo": thrash,
#         "genre": doom
#     }
#
#
# @app.route('/devconfig')
# def config_dev():
#     return {
#         's3': str(app.config['S3_REGION']),
#         'log': str(app.config['LOG_LEVEL']),
#         'table': str(app.config['DB_TABLE'])
#     }
