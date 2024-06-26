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

- [X] Установка FastAPI
- [X] Запуск приложения
- [X] Создание простого API
- [X] Создали CRUD API - Create, Read, Update, Delete
- [X] Добавили валидацию данных
- [X] Добавили схему данных  Pydantic
- [X] Добавили исключения
- [X] Добавили Dependency для работы с данными перед запросом
- [ ] Создали модель SQLAlchemy
- [ ] Подключили базу данных SQLite асинхронно

# 3-й урок

0. Depends
1. Экшин при запуски приложения
2. Экшин при закрытии приложения
3. Мидлвары
4. Создание страницы
5. Отдаем шаблон
6. Подключение статики
7. изменяем авторизацию
8. Работа с Хедерами, куками, формами
9. реализуем логику, регистрация, авторизация, выход
10. Оторажение главной страницы, для авторизованных и не авторизованных пользователей
11. Изучаем шаблонизаторы



# 5-й Урок:

1. .env, .gitignore, config.py
2. requirements.txt
3. Запуск на сервере
