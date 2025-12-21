# Генератор и проверка паролей

Небольшое Flask‑приложение и CLI для генерации и оценки надёжности паролей. Есть веб‑UI, API и утилита командной строки.

## Быстрый старт
```bash
git clone https://github.com/ShurupovNikita/password_generator.git
cd password_generator
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py  # или flask --app app run --host 0.0.0.0 --port 8080
```
После запуска UI доступен на http://localhost:8080/.

## Требования
- Python 3.11+
- pip
- (опционально) Docker / Docker Compose для контейнерного запуска

## Варианты запуска
### 1) Из готового Docker-образа
```bash
# публичный образ на Docker Hub
docker pull shurupovnikita/password_generator:latest
docker run --rm -p 8080:8080 shurupovnikita/password_generator:latest
```
После старта UI доступен на http://localhost:8080/.

### 2) Docker Compose
```bash
docker compose up --build
```
Пробрасывается порт `8080`. Образ собирается локально из `Dockerfile`. Если хотите использовать опубликованный образ, можно заменить секцию `build` на `image: shurupovnikita/password_generator:latest`.

### 3) Запуск в локальном окружении
1) Установите зависимости: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
2) Запустите: `python app.py` (или `FLASK_APP=app.py flask run --host 0.0.0.0 --port 8080`).
3) Откройте `http://localhost:8080`.

## CLI-проверка паролей
```bash
python main.py "мойПароль123!"
# или интерактивно:
python main.py
```
CLI выводит длину, энтропию, балл (0–100), уровень и рекомендации.

## API методы
- `POST /api/check`
  - Тело: `{ "password": "строка" }`
  - Ответ: `{ length, entropy, score, level, recommendations }`
  - Ошибки: 400 при некорректном JSON.

- `POST /api/generate`
  - Тело (все поля опциональны): `{ "length": 16, "lower": true, "upper": true, "digits": true, "symbols": true }`
  - Ответ: `{ "password": "..." }`
  - Ошибки: 400 если все флаги отключены.

- `GET /health`
  - Ответ: `{ "status": "ok" }`

## Переменные окружения
- `FLASK_APP` — файл приложения (по умолчанию `app.py`). Нужен для `flask run`.
- `FLASK_RUN_PORT` — порт для `flask run` (по умолчанию 5000; в примерах используем 8080).
- `PYTHONUNBUFFERED=1` — отключает буферизацию stdout (используется в Docker).

## Структура
- `app.py` — Flask API + веб-страница.
- `checker.py` — логика оценки и генерации паролей.
- `main.py` — CLI для проверки паролей.
- `templates/index.html` — простой UI.
- `Dockerfile`, `docker-compose.yml` — контейнеризация.

## Ссылки
- Docker Hub: https://hub.docker.com/repository/docker/shurupovnikita/password_generator/general
- GitHub: https://github.com/ShurupovNikita/password_generator

## Полезно знать
- Минимальная длина генерируемого пароля — 4, максимальная — 128.
- Общие пароли из списка в `checker.py` сильно штрафуются.
