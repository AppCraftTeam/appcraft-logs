# Generated by Django 3.2.10 on 2022-03-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogProxyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('start_at', models.DateTimeField()),
                ('time', models.FloatField()),
                ('user_id', models.IntegerField(null=True)),
                ('url', models.CharField(max_length=255, null=True)),
                ('headers', models.TextField(null=True)),
                ('method', models.CharField(max_length=255, null=True)),
                ('query_params', models.TextField(null=True)),
                ('request_body', models.TextField(null=True)),
                ('response_body', models.TextField(null=True)),
                ('error_reason', models.CharField(max_length=255, null=True)),
                ('status_code', models.IntegerField(null=True)),
                ('traceback', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
                'db_table': '_logs_proxy',
            },
        ),
    ]