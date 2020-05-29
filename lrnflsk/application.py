from flask import Flask
import os
import logging

app = Flask(__name__)
app.config.from_object('config_dev')

log_file = app.config['LOG_LOC'] + '/lrnflsk.log'
logging.basicConfig(
    level=app.config['LOG_LEVEL'],
    format=('%(levelname)s %(asctime)s %(name)s '
            'LrnFlsk %(threadName)s: %(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=log_file
)


@app.route('/')
def index():    # app.logger.debug('Log location {}'.format(app.config['LOG_LOC']))
    app.logger.error('Log level: {}'.format(app.config['LOG_LEVEL']))
    app.logger.info('Log info')
    app.logger.error('Log error')
    return 'Index Page ' + str(app.config['LOG_LEVEL'])


@app.route('/hello')
def hello_world():
    app.logger.debug('Hello world visited')
    return 'Hello World!'


@app.route('/devconfig')
def set_dev_config():
    app.config.from_object('config_dev')
    return {
        's3': str(app.config['S3_REGION']),
        'log': str(app.config['LOG_LEVEL']),
        'table': str(app.config['DB_TABLE'])
    }


@app.route('/json/test')
def json_api():
    metal = 'essential'
    thrash = [1, 3, 2, 4]
    doom = 666
    return {
        "music": metal,
        "tempo": thrash,
        "genre": doom
    }


@app.route('/devconfig')
def config_dev():
    return {
        's3': str(app.config['S3_REGION']),
        'log': str(app.config['LOG_LEVEL']),
        'table': str(app.config['DB_TABLE'])
    }


def set_prod_config():
    os.environ['LEARN_FLASK_CONFIG'] = '/Users/zachary.smith/GitRepositories/nonWork/learnFlask/config_prod.py'


@app.route('/prodconfig/<int:toset>')
def config_prod(toset):
    if toset == 1:
        set_prod_config()
    if os.getenv('LEARN_FLASK_CONFIG') is not None:
        app.config.from_envvar('LEARN_FLASK_CONFIG')
        return {
            's3': str(app.config['S3_REGION']),
            'log': str(app.config['LOG_LEVEL']),
            'table': str(app.config['DB_TABLE'])
        }
    else:
        return 'No prod config'
