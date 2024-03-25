## Запуск приложения

Создание виртуального окружения
```bash
python -m venv .venv
```

Активация виртуального окружения
```bash
# source .venv/bin/activate # Linux
.\.venv\Scripts\activate # Windows
```

Установка зависимостей
```bash
pip install -r requirements.txt
```

Запуск приложения
```bash
uvicorn main:app --reload
```
- `main` - имя файла с приложением
- `app` - имя экземпляра FastAPI
- `--reload` - автоматическая перезагрузка приложения при изменении файлов
- `--port 8000` - порт для запуска приложения



Открыть в браузере  [OpenAPI](http://127.0.0.1:8000/docs) `http://127.0.0.1:8000/docs` для тестирования приложения


## 1 Урок
- [x] Установка FastAPI
- [x] Запуск приложения
- [x] Создание простого API
- [x] Создали CRUD API - Create, Read, Update, Delete
- [x] Добавили валидацию данных
- [x] Добавили схему данных  Pydantic
- [x] Добавили исключения
- [x] Добавили Dependency для работы с данными перед запросом
- [ ] Создали модель SQLAlchemy
- [ ] Подключили базу данных SQLite асинхронно