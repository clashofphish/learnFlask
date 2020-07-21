from flask import Blueprint

from lrnflsk.long_process.long_tasks import celery_long_task


sqs = Blueprint('sqs', __name__)


@sqs.route('/celery/<int:duration>', methods=['GET'])
def add_celery_task(duration):
    celery_long_task.delay(duration)
    return 'Task queued'
