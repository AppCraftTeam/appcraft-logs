from django.db import connection
from django.core.management.base import BaseCommand

from seeds.user_seeder import UserSeeder


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fix_database_ids()

        UserSeeder().create()

        print('[DONE]')

    def fix_database_ids(self):
        tables = connection.introspection.table_names()
        seen_models = connection.introspection.installed_models(tables)
        cursor = connection.cursor()
        for model in seen_models:
            self.recovery_key(cursor, model)
        print()

    def recovery_key(self, cursor, model):
        table_name = model._meta.db_table
        table_id_seq = f'{table_name}_id_seq'
        try:
            raw = f"SELECT setval('{table_id_seq}', (SELECT MAX(id) FROM {table_name})+1)"
            cursor.execute(raw)
        except Exception:
            print(f'{table_name} not column ID')
