# Веб приложение Доска-задач

## Описание проекта

Приложение предназначено для управления задачами в формате Kanban-доски. Пользователь может создавать, редактировать, удалять и просматривать задачи, распределяя их по статусам.

## Функциональные возможности

- Создание задачи
- Редактирование задачи
- Удаление задачи
- Отображение задач по колонкам:
  - К выполнению
  - В работе
  - Готово
- Хранение данных в SQLite
- Наличие автоматических тестов на основные CRUD-сценарии

## Технологический стек

- Python 3
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Pytest
- Docker

## Структура проекта

```text
task-board-web/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── routes.py
│   ├── templates/
│   │   ├── index.html
│   │   └── edit_task.html
│   └── static/
│       ├── style.css
│       └── script.js
│
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
│
├── schema.sql
├── run.py
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── .gitignore
```

## Установка и запуск без Docker


1. Клонировать репозиторий:
```bash
git clone https://github.com/RiGGeRXVI/task-board-web.git
cd task-board-web
```

2. Создать и активировать виртуальное окружение:
```bash
python -m venv .venv
source .venv/Scripts/activate
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Инициализировать базу данных:
```bash
flask --app run.py init-db
```

5. Запустить приложение:
```bash
flask --app run.py run
```

После запуска приложение будет доступно по адресу:
```
http://127.0.0.1:5000
```

## Запуск через Docker

1. Клонировать репозиторий:
```bash
git clone https://github.com/RiGGeRXVI/task-board-web.git
cd task-board-web
```

2. Собрать образ:
```bash
docker compose build
```

3. Инициализировать базу данных:
```bash
docker compose run --rm web flask --app run.py init-db
```

4. Запустить приложение:
```bash
docker compose up
```

После запуска приложение будет доступно по адресу:
```text
http://localhost:5000
```

## Запуск тестов

### Локально

```bash
python -m pytest
```

### Через Docker

```bash
docker compose run --rm web python -m pytest
```