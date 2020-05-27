from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config_dev')


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/user/<username>')
def show_user_profile(username):
    return 'User is {}'.format(username)


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
