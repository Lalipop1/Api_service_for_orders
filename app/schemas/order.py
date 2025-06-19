from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.dish import DishResponse

class OrderCreate(BaseModel):
    customer_name: str
    dish_ids: List[int]

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    order_time: datetime
    status: str
    dishes: List[DishResponse]

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: str
