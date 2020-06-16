"""This file holds the celery tasks"""
import time
from lrnflsk.extensions import celery


@celery.task
def celery_long_task(duration):
    for i in range(duration):
        print("Working... {}/{}".format(i + 1, duration))
        time.sleep(2)
        if i == duration - 1:
            print('Completed work on {}'.format(duration))


