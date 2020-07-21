"""This is the file used when celery needs to be imported for decorators"""
from celery import Celery

celery = Celery(__name__, include=['lrnflsk.tasks.long_tasks'])
