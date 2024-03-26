import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from environs import Env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

env = Env()
env.read_env()

app = Celery('src',
             broker=f"amqp://{env.str('RABBITMQ_DEFAULT_USER')}:{env.str('RABBITMQ_DEFAULT_PASS')}@{env.str('RABBITMQ_HOST')}:{env.str('RABBITMQ_PORT')}/")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-location': {
        'task': 'api.tasks.run_task',
        'schedule': crontab(minute='*/3'),
    },
}
app.conf.timezone = 'UTC'
