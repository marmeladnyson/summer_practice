# Notes API

REST API для управления заметками и пользователями на FastAPI, SQLAlchemy и PostgreSQL/SQLite.

## Возможности

- CRUD-операции с заметками;
- создание и просмотр пользователей;
- связь `users` -> `notes`;
- фильтрация заметок по статусу;
- пагинация через `skip` и `limit`;
- CORS для frontend-приложения через `CORS_ORIGINS`;
- единый JSON-формат прикладных ошибок;
- асинхронный учебный обработчик HTTP-ошибок в `app/log_parser.py`;
- автоматические тесты API через pytest.
- встроенный web-интерфейс для работы без Swagger.

Отчет по практике: [PRACTICE_REPORT.md](PRACTICE_REPORT.md).
Примеры SQL: [docs/SQL_EXAMPLES.md](docs/SQL_EXAMPLES.md).

## Локальный запуск

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py --port 8080
```

Без `DATABASE_URL` приложение использует SQLite-файл `notes.db`. Для PostgreSQL задайте переменную окружения:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/notes"
fastapi dev app/main.py --port 8080
```

Допустимые адреса frontend через запятую задаются переменной `CORS_ORIGINS`:

```powershell
$env:CORS_ORIGINS = "http://localhost:3000,http://localhost:5173"
```

Документация API доступна по адресу `http://127.0.0.1:8080/docs`.
Web-интерфейс доступен по адресу `http://127.0.0.1:8080/`.

### PostgreSQL через Docker Compose

Для практики с PostgreSQL и DBeaver:

```powershell
docker compose up --build
```

API будет доступен на `http://127.0.0.1:8080`, PostgreSQL на `localhost:5432`.
Параметры подключения DBeaver: host `localhost`, port `5432`, database `notes`, user `notes`, password `notes`.
Остановка с удалением данных:

```powershell
docker compose down -v
```

## Примеры запросов

Создать пользователя:

```powershell
curl.exe -X POST http://127.0.0.1:8080/users -H "Content-Type: application/json" -d '{"email":"user@example.com","phone":"+79990000000"}'
```

Создать заметку, подставив `id` пользователя:

```powershell
curl.exe -X POST http://127.0.0.1:8080/notes -H "Content-Type: application/json" -d '{"title":"Изучить SQL","user_id":"USER_ID"}'
```

Получить первую страницу заметок со статусом `false`:

```powershell
curl.exe "http://127.0.0.1:8080/notes?status_filter=false&skip=0&limit=20"
```

Обновить заметку:

```powershell
curl.exe -X PATCH http://127.0.0.1:8080/notes/NOTE_ID -H "Content-Type: application/json" -d '{"status":true}'
```

Ошибки приложения возвращаются в формате:

```json
{"code":"USER_NOT_FOUND","message":"Пользователь не найден","status":404}
```

## Тесты

```powershell
python -m pytest -q
```

Тесты используют отдельную SQLite-базу `test_notes.db`, которая исключена из Git.

## Структура

```text
app/
	database.py       # SQLAlchemy engine и сессии
	log_parser.py     # обработчик кодов ошибок в логах
	main.py           # FastAPI-приложение
	models.py         # ORM-модели
	schemas.py        # Pydantic-схемы
	routers/
		notes.py        # API заметок
		users.py        # API пользователей
tests/
	test_api.py       # интеграционные тесты CRUD
docs/
	SQL_EXAMPLES.md   # примеры SELECT, INSERT, UPDATE, DELETE, JOIN
```

## Текущий статус практики

Готовы REST API, SQLAlchemy-модели, связи таблиц, фильтрация, пагинация, тесты, Docker и локальный PostgreSQL.
Деплой на VPS и reverse proxy будут отдельным этапом.

### Render

В репозитории есть `render.yaml` для создания API и PostgreSQL через Blueprint:

1. отправить изменения в GitHub;
2. в Render выбрать **New -> Blueprint**;
3. выбрать репозиторий `marmeladnyson/summer_practice`;
4. подтвердить создание ресурсов из `render.yaml`;
5. после деплоя открыть адрес сервиса и проверить `/docs`.

Для бесплатного PostgreSQL Render может запросить подтверждение тарифа или недоступности базы в выбранном регионе. В этом случае базу можно создать отдельно и передать ее Internal Database URL в переменную `DATABASE_URL` Web Service.
