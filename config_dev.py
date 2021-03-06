import logging

S3_REGION = 'us-east-1'
DB_TABLE = 'dev-table'
SQS_NAME = 'ZS-test'

LOG_LEVEL = logging.INFO
LOG_LOC = '/Users/zachary.smith/GitRepositories/nonWork/learnFlask/logs/'
LOG_FILE = 'lrnflsk.log'

# Celery configuration
BROKER_URL = 'sqs://'  # https://queue.amazonaws.com/318689803902/ZS-test
BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-east-1',
    #'polling_interval': 5,  # number of sec to sleep between polls
    'wait_time_seconds': 5
}
CELERY_DEFAULT_QUEUE = SQS_NAME
CELERY_ENABLE_REMOTE_CONTROL = False
CELERY_SEND_EVENTS = False
