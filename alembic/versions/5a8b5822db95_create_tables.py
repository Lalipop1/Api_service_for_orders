"""create_tables

Revision ID: 5a8b5822db95
Revises: 
Create Date: 2025-06-19 16:02:41.832328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a8b5822db95'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
