# Dauren Qurylyss — Telegram Bot

Enterprise-grade Telegram бот для строительной компании.

## Стек
- Python 3.11+
- Aiogram 3.7
- SQLAlchemy 2.0 + asyncpg
- PostgreSQL (Neon.tech)
- Redis (опционально)
- APScheduler

## Возможности
- 🌐 Мультиязычность (kz / ru / en)
- 📈 AI Смета с историей расчётов
- 📅 Онлайн-запись на консультацию
- 🔔 Уведомления администратору
- 📊 Еженедельные отчёты
- 💰 Управление ценами через /admin
- 📸 Портфолио с фото
- ⚡ Redis кэш цен

## Запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

## .env

```
BOT_TOKEN=
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://localhost:6379/0
ADMIN_IDS=
ADMIN_CONTACT=@username
THROTTLE_RATE=1.0
PRICE_CACHE_TTL=300
```

## Структура

```
app/
├── core/          config, logger, constants
├── database/      models, engine, dao
├── services/      estimation, admin, analytics, booking,
│                  lead, notification, cache, scheduler
├── middlewares/   logging, throttling, db_session, error
├── handlers/      common, user, admin, fallback
├── keyboards/     user, admin
├── locales/       translations (kz/ru/en)
└── utils/         validators
```

## Команды бота

| Команда | Описание |
|---------|----------|
| /start  | Главное меню |
| /admin  | Админ панель (только ADMIN_IDS) |
