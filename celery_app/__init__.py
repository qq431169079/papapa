
from celery import Celery

celery = Celery('celery_app',
broker='redis://127.0.0.1:6379/1',
backend='redis://127.0.0.1:6379/1',
# include=['celery_app.tasks','app.main.tasks', 'app.scheduled.tasks'],
)