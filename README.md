# Rate Bot

Telegram bot that publishes current USDT to RUB exchange rate from Coinex.kg.

### Stack Overview

Main Libraries:
- [aiogram](https://github.com/aiogram/aiogram) - Asynchronous Telegram Bot API framework
- [taskiq](https://github.com/taskiq-python/taskiq-aio-pika) - Background task queue
- [taskiq-aiogram](https://github.com/taskiq-python/taskiq-aiogram) - Taskiq integration for aiogram
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) - ORM
- [alembic](https://github.com/sqlalchemy/alembic) - Database migrations

Infrastructure:
- Redis as in-memory storage
- PostgreSQL as database
- RabbitMQ as message-broker