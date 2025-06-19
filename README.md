# 🍽️ Restaurant API (FastAPI + Async SQLAlchemy)

**REST API для управления меню и заказами в ресторане** с асинхронной работой с базой данных.

## 📦 Структура проекта

```
restaurant_api/
├── alembic/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа FastAPI
│   ├── db.py                # Асинхронная конфигурация DB
│   ├── models/              # SQLAlchemy модели
│   │   ├── dish.py
│   │   ├── order.py
│   │   └── order_dish.py
│   ├── schemas/             # Pydantic схемы
│   ├── routers/             # API эндпоинты
│   └── services/            # Бизнес-логика
├── .env
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🚀 Быстрый старт

### 1. Запуск через Docker (рекомендуется)

```bash
# Собрать и запустить контейнеры
docker-compose up --build

# Остановить
docker-compose down
```

### 2. Взоможны проблемы с миграциями(воть решение)

```bash
# 1. Создаем пустую миграцию
docker-compose exec web alembic revision -m "create_tables"

# 2. Ручками пишем в файле миграций лежит тут alembic/versions/
def upgrade():
    # Создаём таблицу dishes
    op.create_table(
        'dishes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
    )

    # Создаём таблицу orders
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('customer_name', sa.String(), nullable=False),
        sa.Column('order_time', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('status', sa.String(), server_default='в обработке'),
    )

    # Создаём ассоциативную таблицу order_dish
    op.create_table(
        'order_dish',
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.id')),
        sa.Column('dish_id', sa.Integer(), sa.ForeignKey('dishes.id')),
    )

def downgrade():
    # В обратном порядке - сначала удаляем ассоциативную таблицу
    op.drop_table('order_dish')
    # Затем основные таблицы
    op.drop_table('dishes')
    op.drop_table('orders')

# 3. Применяем миграции
docker-compose exec web alembic upgrade head

# 4. Проверка наличия таблиц в бд
docker-compose exec db psql -U postgres -d restaurant -c "\dt"
```

## 🌐 API Endpoints

| Метод | Путь | Описание |
|-------|------|-----------|
| `GET` | `/dishes` | Получить все блюда |
| `POST` | `/dishes` | Добавить новое блюдо |
| `DELETE` | `/dishes/{id}` | Удалить блюдо |
| `GET` | `/orders` | Получить все заказы |
| `POST` | `/orders` | Создать новый заказ |
| `PATCH` | `/orders/{id}/status` | Обновить статус заказа |


## 🛠 Технологии

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 14 + asyncpg
- **ORM**: SQLAlchemy 2.0 (асинхронный режим)
- **Миграции**: Alembic с async поддержкой
- **Контейнеризация**: Docker + docker-compose
