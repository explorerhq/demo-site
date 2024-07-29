web: gunicorn explorer_demo.wsgi
worker: celery --app explorer_demo.celery_config.app worker

release: ./manage.py migrate --no-input && ./manage.py collectstatic --no-input
