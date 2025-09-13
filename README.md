# Запуск проекта

## 1. Через терминал
1. Установить окружение `python -m venv env`
2. Установить в окружение `poetry`
3. Прописать `poetry install`
### 1.1 Запуски основных сервисов
1. FastAPI сервер `uvicorn run_server:app |--reload| -> для дебага`
2. Celery `celery -A celery_run worker --pool=solo --loglevel=info`
3. Очистить базу данных `python run_db.py`
4. Запустить тесты `pytest`

## 2. Через docker
1. Установите docker и docker compose
2. Выполните: `docker-compose up --build`
3. Откройте: http://localhost:8000