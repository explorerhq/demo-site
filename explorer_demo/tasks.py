from celery import shared_task
from django.core.management import call_command
from django.conf import settings
import json
import subprocess
from explorer.models import QueryLog, Query, QueryFavorite, DatabaseConnection
import os
import logging

logger = logging.getLogger(__name__)


@shared_task
def reset_env():
    try:
        # Deleting all entries from the models
        QueryLog.objects.all().delete()
        Query.objects.all().delete()
        QueryFavorite.objects.all().delete()
        DatabaseConnection.objects.all().delete()

        # Define the absolute path to the JSON file
        file_path = os.path.join(settings.BASE_DIR, 'model_data.json')

        with open(file_path, 'r') as f:
            call_command('loaddata', file_path)

        logger.info('Database has been successfully reset with data from model_data.json.')
    except Exception as e:
        logger.error(f'An error occurred while resetting the database: {e}')
        raise


@shared_task
def dump_demo_env():

    models_order = [
        'explorer.DatabaseConnection',
        'explorer.Query',
        'explorer.QueryLog',
    ]

    def dump_model_data(m):
        output = subprocess.check_output(['python', 'manage.py', 'dumpdata', m, '--format=json', '--indent=4'])
        return json.loads(output)

    output_file = os.path.join(settings.BASE_DIR, 'model_data.json')
    all_data = []

    for model in models_order:
        logger.info(f'Dumping {model} models...')
        model_data = dump_model_data(model)
        all_data.extend(model_data)
        logger.info(f'Done dumping {model} models...')

    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=4)
        logger.info(f'Done writing {output_file}')

