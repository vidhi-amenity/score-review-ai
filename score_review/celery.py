from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'score_review.settings')

app = Celery('score_review')

# Using a string here eliminates the need to serialize
# the configuration object to child processes by the Celery worker.

# - namespace='CELERY' means all celery-related configuration keys
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django applications.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

