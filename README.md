





# Driver service

Перед запуском сервиса указать переменные окружения в файле ```docker_compose.yml``` для подключения базы данных:
```
      - POSTGRES_DB=
      - POSTGRES_USER=
      - POSTGRES_PASSWORD=
      - POSTGRES_HOST=
      - POSTGRES_PORT=
```

Для запуска сервиса воспользоваться командой:

```docker compose -f docker_compose.yml up --build -d```


Swagger UI доступен по адресу:

```
http://127.0.0.1:8000/docs
```

Получение списка по всем водителям:

```
http://127.0.0.1:8000/drivers
```

Получение данных по конкретному водителю:


```
http://127.0.0.1:8000/drivers/${id}
```
 - id - идентификатор водителя (формат - число)

