# AI-Lecture-Notes-Generator (Курсовая работа, в процессе)

## Описание
**AI-Lecture-Notes-Generator** — это веб-приложение для загрузки и генерации конспектов лекций с использованием искусственного интеллекта.

Приложение поддерживает загрузку видеофайлов и презентаций, обработку контента и предоставление удобного интерфейса чата.

## Функционал
- **Регистрация и аутентификация пользователей**
- **Создание чатов** для хранения заметок и файлов
- **Загрузка видеофайлов и презентаций**
- **Просмотр загруженных файлов** с возможностью скачивания
- **Чат** для заметок, сделанные пользователем по лекции
- **Обработка загруженных материалов - TODO**

## Технологии
### Frontend:
- **React**
- **CSS**

### Backend:
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy + Alembic**
- **Auth JWT**

## Установка и запуск
### 1. Клонирование репозитория
```bash
  git clone https://github.com/EugeneGorbulya/AI-Lecture-Notes-Generator.git
  cd AI-Lecture-Notes-Generator
```

### 2. Настройка backend
#### Установка зависимостей
```bash
cd backend-notes-generator
python3 -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Запуск backend-сервера
```bash
uvicorn app.main:app --reload
```

### 3. Настройка frontend
#### Установка зависимостей
```bash
cd ../frontend-notes-generator
npm install
```

#### Запуск frontend-сервера
```bash
npm start
```

## API Endpoints
### Аутентификация
- `POST /api/users/register` — регистрация пользователя
- `POST /api/users/login` — аутентификация пользователя
- `GET /api/users/me` — информация о текущем пользователе

### Работа с чатами
- `POST /api/chats/` — создание нового чата
- `GET /api/chats/` — получение списка чатов
- `GET /api/message/{chat_id}/` — получение сообщений в чате
- `POST /api/message/{chat_id}/` — отправка текстового сообщения
- `POST /api/message/{chat_id}/file` — загрузка файла
- `GET /api/message/static/{file_name}` — скачивание файла

## TODO
- [ ] Добавить обработку видео-лекций и презентаций
- [ ] Добавить Docker и интегрировать CI/CD
- [ ] Использовать ML для обработки файлов

## Контакты
Автор: [Eugene Gorbulya](https://github.com/EugeneGorbulya)

