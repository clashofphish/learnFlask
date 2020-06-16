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


# Functions that use boto3 resource
def sqs_get_queue_resource(name: str):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=name)
    return queue


def sqs_queue_check_get_rsc(queue_name: str):
    try:
        queue = sqs_get_queue_resource(queue_name)
        return queue, 'Queue exists with name = {}'.format(queue_name)
    except botoexcept.QueueDoesNotExist:
        queue = sqs_create_queue(queue_name)
        return queue, 'Queue created with name = {}'.format(queue_name)


def sqs_rsc_send_simple_message(queue_resource, message_body: str):
    response = queue_resource.send_message(MessageBody=message_body)
    return response


def sqs_rsc_send_json_message(queue_resource, message_json: dict):
    response = queue_resource.send_message(MessageBody=json.dumps(message_json))
    return response


def sqs_rsc_pull_messages(queue_resource, max_messages=10, wait_time=5):
    message_bunch = queue_resource.receive_messages(
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time  # this wait time will override wait time configured in queue setup
    )
    print('Total messages pulled: {}'.format(len(message_bunch)))
    return message_bunch


# Functions that use boto3 client
def sqs_get_queue_url(name: str):
    sqs_clt = boto3.client('sqs')
    queue_url = sqs_clt.get_queue_url(QueueName=name)
    return queue_url


def sqs_queue_check_get_url(queue_name: str):
    try:
        queue = sqs_get_queue_url(queue_name)
        return queue['QueueUrl'], 'Queue exists with name = {}'.format(queue_name)
        # use client to get url need queue['QueueUrl']
    except botoexcept.QueueDoesNotExist:
        queue = sqs_create_queue(queue_name)
        return queue.url, 'Queue created with name = {}'.format(queue_name)
        # use resource to get url need queue.url


def sqs_clt_send_simple_message(queue_url: str, message_body: str):
    sqs_clt = boto3.client('sqs')
    response = sqs_clt.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response


def sqs_clt_send_json_message(queue_url: str, message_body: dict):
    sqs_clt = boto3.client('sqs')
    response = sqs_clt.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body)
    )
    return response


def sqs_clt_pull_messages(queue_url: str, max_messages=10, wait_time=5):
    sqs_clt = boto3.client('sqs')
    message_meta = sqs_clt.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time
    )
    if 'Messages' in message_meta:
        message_bunch = message_meta['Messages']
    else:
        message_bunch = []
    print('Total messages pulled: {}'.format(len(message_bunch)))
    return message_bunch
# message_bunch here is more rudimentary than with boto3 resource
#  get to messages: message_list = message_bunch['Messages']
#  within single message: for message in message_list:
#    get to message body: body = message['Body']
#    get to receipt handle: receipt_handle = message['ReceiptHandle']


def sqs_clt_delete_message(queue_url: str, receipt_handle: str):
    sqs_clt = boto3.client('sqs')
    response = sqs_clt.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return response
