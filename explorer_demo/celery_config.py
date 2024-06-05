import os

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "explorer_demo.settings")

app = Celery("explorer_demo")

# Using a string here means the worker doesn"t have to serialize
# the configuration object to child processes.
# - namespace="CELERY" means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "explorer_demo.tasks.reset_env": {
        "task": "explorer_demo.tasks.reset_env",
        "schedule": crontab(hour="1", minute="0")
    },
    "explorer.tasks.remove_unused_sqlite_dbs": {
        "task": "explorer.tasks.remove_unused_sqlite_dbs",
        "schedule": crontab(hour="1", minute="20")
    }
}
