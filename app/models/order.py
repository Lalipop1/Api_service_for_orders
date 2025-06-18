from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import func
from datetime import datetime
from app.models.base import Base



class Dish(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    order_time = Column(DateTime, server_default=func.now())
    status = Column(String, default="в обработке")

    dishes = relationship("Dish", secondary=order_dish_asssociation, back_populates="orders")