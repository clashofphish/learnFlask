"""This file holds the celery tasks"""
import time
from lrnflsk.celery_holder import celery


@celery.task
def celery_long_task(duration):
    for i in range(duration):
        print("Working... {}/{}".format(i + 1, duration))
        time.sleep(2)
        if i == duration - 1:
            print('Completed work on {}'.format(duration))


