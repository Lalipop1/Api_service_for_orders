from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.models.order_dish import order_dish
from app.db import Base

class Dish(Base):
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    
    orders = relationship("Order", secondary="order_dish", back_populates="dishes")