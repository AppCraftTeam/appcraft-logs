from infi.clickhouse_orm import Log, Model, NullableField, fields


class LogModel(Model):
    uuid = fields.UUIDField()

    start_at = fields.DateTime64Field()
    time = fields.Float64Field()
    user_id = NullableField(fields.Int64Field())
    url = NullableField(fields.StringField())
    headers = NullableField(fields.StringField())
    method = NullableField(fields.StringField())
    query_params = NullableField(fields.StringField())
    request_body = NullableField(fields.StringField())
    response_body = NullableField(fields.StringField())
    error_reason = NullableField(fields.StringField())
    status_code = NullableField(fields.Int64Field())
    traceback = NullableField(fields.StringField())

    engine = Log()

    @classmethod
    def table_name(cls):
        return 'logs'
