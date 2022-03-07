from django.db import models


class LogProxyModel(models.Model):
    uuid = models.UUIDField()
    start_at = models.DateTimeField()
    time = models.FloatField()
    user_id = models.IntegerField(null=True)
    url = models.CharField(max_length=255, null=True)
    headers = models.TextField(null=True)
    method = models.CharField(max_length=255, null=True)
    query_params = models.TextField(null=True)
    request_body = models.TextField(null=True)
    response_body = models.TextField(null=True)
    error_reason = models.CharField(max_length=255, null=True)
    status_code = models.IntegerField(null=True)
    traceback = models.TextField(null=True)

    def __str__(self):
        return f'Дата: {self.start_at}. Запрос: {self.url}'

    @classmethod
    def from_clickhouse_model(cls, instance):
        return cls(
            uuid=instance.uuid,
            start_at=instance.start_at,
            time=instance.time,
            user_id=instance.user_id,
            url=instance.url,
            headers=instance.headers,
            method=instance.method,
            query_params=instance.query_params,
            request_body=instance.request_body,
            response_body=instance.response_body,
            error_reason=instance.error_reason,
            status_code=instance.status_code,
            traceback=instance.traceback
        )

    class Meta:
        db_table = '_logs_proxy'
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
