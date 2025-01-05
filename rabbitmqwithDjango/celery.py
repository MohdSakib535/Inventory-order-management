from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rabbitmqwithDjango.settings')

app = Celery('rabbitmqwithDjango')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

#  celery beat setting
app.conf.beat_schedule={
    'send-mail-everyday':{
    'task':'orders.tasks.send_daily_sales_report',
    'schedule': crontab(minute='*/1'),
    # 'args':()

    
    }
}



app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
