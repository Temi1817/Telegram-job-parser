# IT Jobs Bot

Telegram-бот, который агрегирует IT-вакансии из нескольких источников и отправляет только те, что подходят именно вам.

## Источники вакансий

- 🟡 **HH.kz / HeadHunter** — официальный API
- 💙 **Habr Career**
- 🌍 **RemoteOK**
- 🦎 **Djinni**
- 🚀 **Remotive**

## Возможности

- Парсинг вакансий каждые 30 минут в фоне
- Фильтрация по ключевым словам, зарплате, городу, опыту
- Выбор источников вакансий
- Дедупликация — одна вакансия придёт только один раз
- Настройка фильтров через инлайн-кнопки
- Интерфейс на русском / казахском / английском

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Запуск и выбор языка |
| `/filters` | Настроить фильтры |
| `/jobs` | Найти вакансии прямо сейчас |
| `/pause` | Приостановить уведомления |
| `/resume` | Возобновить уведомления |
| `/help` | Список команд |

---

## 1. Получение токена

### Telegram Bot Token

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Придумайте имя и username для бота
4. Скопируйте токен вида `1234567890:AAF...`

---

## 2. Локальный запуск

### Требования
- Python 3.11+

### Установка

```bash
# Клонировать / скачать проект
cd телегабот

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate
# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### Настройка

```bash
# Скопировать шаблон окружения
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
```

Открыть `.env` и заполнить:

```env
BOT_TOKEN=1234567890:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_PATH=jobs.db
UPDATE_INTERVAL_MINUTES=30
```

### Запуск

```bash
python main.py
```

---

## 3. Деплой бесплатно

### Railway (рекомендуется)

1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Создайте новый проект → **Deploy from GitHub repo**
3. Или через CLI:
   ```bash
   npm install -g @railway/cli
   railway login
   railway init
   railway up
   ```
4. Добавьте переменные окружения в Railway Dashboard → **Variables**:
   - `BOT_TOKEN`
5. В **Settings → Start Command** укажите: `python main.py`

> Бесплатный план Railway даёт $5/месяц кредитов — бота хватит на месяц.

### Render

1. Зарегистрируйтесь на [render.com](https://render.com)
2. **New → Web Service** → подключите GitHub репо
3. Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Instance Type:** Free
4. Добавьте переменные в **Environment**

> На бесплатном плане Render сервис засыпает через 15 мин неактивности. Для бота это нормально — он работает по polling, а не webhook.

### Fly.io

```bash
fly auth login
fly launch
fly secrets set BOT_TOKEN=xxx
fly deploy
```

---

## Структура проекта

```
телегабот/
├── main.py                  # Точка входа
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── bot/
│   ├── config.py            # Настройки из .env
│   ├── database.py          # SQLite (пользователи, фильтры, история)
│   ├── locales.py           # RU / KZ / EN переводы
│   ├── keyboards.py         # Инлайн-клавиатуры
│   ├── job_service.py       # Оркестратор: парсинг + фильтрация + отправка
│   ├── scheduler.py         # APScheduler (фоновый запуск каждые N минут)
│   ├── handlers/
│   │   ├── start.py         # /start, выбор языка, /pause, /resume
│   │   ├── filters.py       # /filters, настройка через FSM
│   │   └── jobs.py          # /jobs, кнопка "найти сейчас"
│   └── parsers/
│       ├── hh.py            # HeadHunter API
│       ├── habr.py          # Habr Career
│       ├── remoteok.py      # RemoteOK
│       ├── djinni.py        # Djinni
│       └── remotive.py      # Remotive
```
