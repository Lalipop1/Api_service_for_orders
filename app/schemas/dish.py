from pydantic import BaseModel

class DishCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

class DishResponse(DishCreate):
    id: int

    class Config:
        orm_mode = True
