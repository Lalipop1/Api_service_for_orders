from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.dish import Dish
from app.schemas.dish import DishCreate

async def get_dishes(db: AsyncSession):
    result = await db.execute(select(Dish))
    return result.scalars().all()

async def get_dish(db: AsyncSession, dish_id: int):
    result = await db.execute(select(Dish).where(Dish.id == dish_id))
    return result.scalar_one_or_none()

async def create_dish(db: AsyncSession, dish: DishCreate):
    db_dish = Dish(**dish.model_dump())
    db.add(db_dish)
    await db.commit()
    await db.refresh(db_dish)
    return db_dish

async def delete_dish(db: AsyncSession, dish_id: int):
    dish = await get_dish(db, dish_id)
    if dish:
        await db.delete(dish)
        await db.commit()
        return True
    return False