from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models.dish import Dish
from app.schemas.dish import DishCreate, DishResponse
from typing import List

router = APIRouter(prefix="/dishes", tags=["dishes"])

@router.get("/", response_model=List[DishResponse])
async def get_dishes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dish))
    return result.scalars().all()

@router.post("/", response_model=DishResponse)
async def create_dish(dish: DishCreate, db: AsyncSession = Depends(get_db)):
    db_dish = Dish(**dish.dict())
    db.add(db_dish)
    await db.commit()
    await db.refresh(db_dish)
    return db_dish

@router.delete("/{dish_id}")
async def delete_dish(dish_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dish).where(Dish.id == dish_id))
    dish = result.scalar_one_or_none()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    await db.delete(dish)
    await db.commit()
    return {"message": "Dish deleted"}
