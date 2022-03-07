from django.apps import AppConfig
from django.conf import settings
from django.utils.functional import classproperty
from infi.clickhouse_orm import Database


class AppcraftLoggingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appcraft_logging'
    verbose_name = 'Логи запросов'

    def ready(self):
        db = self.db

        try:
            from .clickhouse.models import LogModel
            db.create_table(LogModel)
        except Exception as ex:
            raise NotImplementedError(f'Error during creation of clickhouse model:\n{ex}')

        settings.MIDDLEWARE.append(f'{self.name}.middleware.LogsMiddleware')

    @classproperty
    def db(self):
        try:
            config = settings.APPCRAFT_LOGGING_CONFIG
        except AttributeError as ex:
            raise NotImplementedError(
                f'APPCRAFT_LOGGING_CONFIG variable not found in settings.py.\n{ex}'
            )

        try:
            return Database(
                db_name=config['db_name'],
                username=config['username'],
                password=config['password'],
                db_url=f'http://localhost:{config["port"]}'
            )
        except KeyError as ex:
            raise NotImplementedError(
                'One of required keys for `APPCRAFT_LOGGING_CONFIG` '
                f'variable weren\'t provided: {ex}'
            )
