web: gunicorn explorer_demo.wsgi
worker: celery --app explorer_demo.celery_config.app worker --beat --concurrency 2 -l INFO

release: ./manage.py migrate --no-input && ./manage.py collectstatic --no-input
