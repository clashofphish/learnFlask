from flask import current_app as app
from flask import Blueprint, Response
import botocore.errorfactory as botoexcept
from threading import Thread
import json

import lrnflsk.utility_functions.sqs_utilities as sqs_ut
import lrnflsk.utility_functions.long_tasks as lt

sqs = Blueprint('sqs', __name__)


@sqs.route('/', methods=['GET'])
def index():
    if app.sqs is None:
        app.sqs, message = sqs_ut.sqs_queue_on_name(app.config['SQS_NAME'])
    else:
        message = 'Queue already initialized in app'
    response_message = json.dumps({'message': message})

    return Response(response_message, status=200, mimetype='application/json')
    # try:
    #     app.sqs = sqs_ut.sqs_get_queue_resource(app.config['SQS_NAME'])
    #     return 'Queue exists with name = {}'.format(app.config['SQS_NAME'])
    # except botoexcept.QueueDoesNotExist:
    #     app.sqs = sqs_ut.sqs_create_queue(app.config['SQS_NAME'])
    #     return 'Queue created with name = {}'.format(app.config['SQS_NAME'])


def thread_simple_long_task(queue_resource):
    messages = sqs_ut.sqs_pull_messages(queue_resource, max_messages=5)
    thrd_message = []
    for message in messages:
        thread = Thread(
            target=lt.simple_long_task,
            kwargs={
                'duration': message.body,
                'message': message
            }
        )
        thread.start()
        thrd_message.append(
            'Thread started for duration: {}'.format(message.body)
        )
    return thrd_message


@sqs.route('/thread/duration/act/<int:duration>', methods=['GET'])
def add_queue_message(duration):
    response = sqs_ut.sqs_send_simple_message(
        queue_resource=app.sqs,
        message_body=str(duration)
    )
    if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
        flsk_message = 'Message added to queue for duration: {}'.format(
            duration
        )
        print('Message added for {}'.format(duration))
    else:
        flsk_message = 'Message did not make it to queue for duration: {}'.format(duration)

    # Pull messages and do work
    thrd_message = thread_simple_long_task(app.sqs)

    response_message = json.dumps({
        'queue_message': flsk_message,
        'thread_message': thrd_message
    })
    return Response(response_message, status=200, mimetype='application/json')


@sqs.route('/thread/duration/queue/<int:duration>', methods=['GET'])
def add_queue_message(duration):
    response = sqs_ut.sqs_send_simple_message(
        queue_resource=app.sqs,
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