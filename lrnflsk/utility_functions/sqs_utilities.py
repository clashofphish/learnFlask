import boto3
import botocore.errorfactory as botoexcept
import json


def sqs_create_queue(name, wait_time: str = '2'):
    sqs = boto3.resource('sqs')
    queue = sqs.create_queue(
        QueueName=name,
        Attributes={
            'ReceiveMessageWaitTimeSeconds': wait_time
        }
    )
    return queue


def sqs_get_queue_resource(name):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=name)
    return queue


def sqs_send_simple_message(queue_resource, message_body):
    response = queue_resource.send_message(MessageBody=message_body)
    return response


def sqs_send_json_message(queue_resource, message_json):
    response = queue_resource.send_message(MessageBody=json.dumps(message_json))
    return response


def sqs_pull_messages(queue_resource, max_messages=10, wait_time=5):
    message_bunch = queue_resource.receive_messages(
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time
    )
    print('Total messages pulled: {}'.format(len(message_bunch)))
    return message_bunch


def sqs_queue_on_name(queue_name):
    try:
        queue = sqs_get_queue_resource(queue_name)
        return queue, 'Queue exists with name = {}'.format(queue_name)
    except botoexcept.QueueDoesNotExist:
        queue = sqs_create_queue(queue_name)
        return queue, 'Queue created with name = {}'.format(queue_name)
