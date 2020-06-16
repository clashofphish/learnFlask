from flask import current_app as app
from flask import Blueprint, Response
import json
# from threading import Thread
# import time

import lrnflsk.utility_functions.sqs_utilities as sqs_ut
from lrnflsk.long_process.long_tasks import celery_long_task
# import lrnflsk.long_tasks as lt


sqs = Blueprint('sqs', __name__)


@sqs.route('/', methods=['GET'])
def index():
    if app.sqs is None:
        app.sqs, message = sqs_ut.sqs_queue_check_get_url(app.config['SQS_NAME'])
    else:
        message = 'Queue already initialized in app'
    response_message = json.dumps({
        'message': message,
        'url': app.sqs
    })

    return Response(response_message, status=200, mimetype='application/json')


@sqs.route('/thread/duration/queue/<int:duration>', methods=['GET'])
def add_queue_message(duration):
    response = sqs_ut.sqs_clt_send_simple_message(
        queue_url=app.sqs,
        message_body=str(duration)
    )
    if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
        flsk_message = 'Message added to queue for duration: {}'.format(
            duration
        )
        print('Message added for {}'.format(duration))
    else:
        flsk_message = 'Message did not make it to queue for duration: {}'.format(duration)

    response_message = json.dumps({
        'queue_message': flsk_message
    })
    return Response(response_message, status=200, mimetype='application/json')


@sqs.route('/celery/<int:duration>', methods=['GET'])
def add_celery_task(duration):
    celery_long_task.delay(duration)
