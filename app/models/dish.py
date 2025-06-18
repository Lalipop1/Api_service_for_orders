from sqlalchemy import Column, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from app.models.base import Base

order_dish_asssociation = Table (
    'order_dish_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('dish_id', Integer, ForeignKey('dishes.id'))
)

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)

    orders = relationship("Order", secondary=order_dish_asssociation, back_populates="dishes")