from sqlalchemy import Table, Integer, Column, ForeignKey
from app.db import Base

order_dish = Table(
    "order_dish",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("dish_id", Integer, ForeignKey("dishes.id"))
)