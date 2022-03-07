# appcraft-logging

---

## Quick start

1. `pip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple appcraft-logging`
2. Add `appcarft-logging` to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...,
    'appcraft_logging',
    ...
]
```
3. Provide data of existing ClickHouse database via `APPCRAFT_LOGGING_CONFIG` variable in settings.py:
```python
...
# example
APPCRAFT_LOGGING_CONFIG = {
    'db_name': os.getenv('CLICKHOUSE_DB_NAME', 'db'),
    'username': os.getenv('CLICKHOUSE_USERNAME', 'root'),
    'password': os.getenv('CLICKHOUSE_PASSWORD', 'root'),
    'port': os.getenv('CLICKHOUSE_PORT', '8123')
}
...
```
4. `python manage.py migrate`. This package contains Django model for sampling admin site. Run migration to make it viable.

---

## Make class/function based view not loggable or loggable only with specified methods

> Please, note that `appcraft-logging` logs requests which url's starts with `api`. For example: `/api/users/me`, but not `/admin/...`.

Pillar of `appcraft-logging` package is `loggable_http_methods` property. Its description:
1. Should be a list(`[]`). If it isn't a list or not specified at all - view will be loggable.
2. Can contain multiple **UPPER CASE** HTTP method names (exmaple bellow).
3. It can be assigned to any class/function based view:
```python
# CBV

class MyView(APIView):
    # manually specify methods that should be logged.
    # will work the same way, if `loggable_http_methods` would be removed.
    loggable_http_methods = ['GET', 'POST']

    def get(self, request):
        ...

    def post(self, request):
        ...
```
```python
# FBV

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def my_fbv(request):
    return Response()
my_fbv.loggable_http_methods = ['GET', 'POST']  # same as with CBV.
```
4. To ignore specific view for logging: specify empty list for `loggable_http_methods`:
```python
# CBV

class MyView(APIView):
    loggable_http_methods = []  # none of get or post will be logged.

    def get(self, request):
        ...

    def post(self, request):
        ...
```
```python
# FBV

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def my_fbv(request):
    return Response()
my_fbv.loggable_http_methods = []  # same as with CBV.
```