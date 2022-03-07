# Запуск БД Clickhouse в Docker контейнере через docker-compose

1. Добавить переменные окружения:
    1. `CLICKHOUSE_DB`
    2. `CLICKHOUSE_PORT`
    3. `CLICKHOUSE_USER`
    4. `CLICKHOUSE_PASSWORD`
2.
```yml
version: '3.5'

networks:
  server_develop:

services:
  ...

  clickhouse_server:
    image: yandex/clickhouse-server
    ports:
      - "${CLICKHOUSE_PORT}:8123"
    environment:
      CLICKHOUSE_DB: ${CLICKHOUSE_DB}
      CLICKHOUSE_USER: "${CLICKHOUSE_USER}"
      CLICKHOUSE_PASSWORD: "${CLICKHOUSE_PASSWORD}"
    volumes:
      - ./data/clickhouse:/var/lib/postgresql/data
```

# Запуск clickhouse-client

`clickhouse-client` - CLI для взаимодействия с БД прямо из терминала.

1. Перейдите в директорию нужного docker-compose'а
2. `docker-compose exec clickhouse_server bash`
3. `clickhouse-client --password <пароль>`